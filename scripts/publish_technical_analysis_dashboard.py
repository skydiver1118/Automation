from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import smtplib
import ssl
import subprocess
import sys
from email.message import EmailMessage
from datetime import datetime
from pathlib import Path

from tradingagents_automation_support import git_base_command


WORKSPACE = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = WORKSPACE / "technical_analysis_dashboard"
PUBLISH_REPO = WORKSPACE / "github_pages_repo"
BUILD_SCRIPT = WORKSPACE / "scripts" / "build_technical_analysis_dashboard.py"
REPO_CLONE_URL = "https://github.com/skydiver1118/my_yolo_test.git"
PAGES_URL = "https://skydiver1118.github.io/my_yolo_test/technical-analysis/"


def run(cmd: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    print(f"+ {' '.join(cmd)}")
    completed = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if completed.stdout:
        print(completed.stdout.rstrip())
    if check and completed.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {completed.returncode}: {' '.join(cmd)}")
    return completed


def git_run(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run([*git_base_command(cwd), *args], cwd, check=check)


def ensure_publish_repo() -> None:
    if (PUBLISH_REPO / ".git").exists():
        git_run(["pull", "--ff-only"], PUBLISH_REPO)
        return
    run(["git", "clone", REPO_CLONE_URL, str(PUBLISH_REPO)], WORKSPACE)


def build_dashboard(date_text: str | None) -> None:
    cmd = [sys.executable, str(BUILD_SCRIPT)]
    if date_text:
        cmd.extend(["--date", date_text])
    run(cmd, WORKSPACE)


def copy_dashboard() -> None:
    if not (DASHBOARD_DIR / "index.html").exists():
        raise FileNotFoundError(f"Dashboard source is missing: {DASHBOARD_DIR}")
    if not (DASHBOARD_DIR / "data" / "dashboard-data.js").exists():
        raise FileNotFoundError("Run build_technical_analysis_dashboard.py before publishing.")

    target_dir = PUBLISH_REPO / "technical-analysis"
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True)

    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    index = (DASHBOARD_DIR / "index.html").read_text(encoding="utf-8")
    index = re.sub(r"styles\.css(\?v=[^\"']+)?", f"styles.css?v={stamp}", index)
    index = re.sub(r"app\.js(\?v=[^\"']+)?", f"app.js?v={stamp}", index)
    index = re.sub(r"data/dashboard-data\.js(\?v=[^\"']+)?", f"data/dashboard-data.js?v={stamp}", index)
    (target_dir / "index.html").write_text(index, encoding="utf-8")

    for filename in ["app.js", "styles.css", "README.md"]:
        shutil.copy2(DASHBOARD_DIR / filename, target_dir / filename)

    shutil.copytree(DASHBOARD_DIR / "data", target_dir / "data")
    shutil.copytree(DASHBOARD_DIR / "charts", target_dir / "charts")
    (PUBLISH_REPO / ".nojekyll").write_text("", encoding="utf-8")


def commit_and_push(push: bool) -> tuple[bool, str]:
    git_run(["add", "technical-analysis", ".nojekyll"], PUBLISH_REPO)
    status = git_run(["status", "--porcelain"], PUBLISH_REPO).stdout.strip()
    if not status:
        sha = git_run(["rev-parse", "--short", "HEAD"], PUBLISH_REPO).stdout.strip()
        return False, sha

    message = f"Publish technical analysis dashboard {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    git_run(["commit", "-m", message], PUBLISH_REPO)
    if push:
        git_run(["push", "origin", "main"], PUBLISH_REPO)
    sha = git_run(["rev-parse", "--short", "HEAD"], PUBLISH_REPO).stdout.strip()
    return True, sha


def parse_dashboard_data() -> dict[str, object]:
    data_path = DASHBOARD_DIR / "data" / "dashboard-data.js"
    text = data_path.read_text(encoding="utf-8")
    match = re.search(r"window\.TECHNICAL_ANALYSIS_DASHBOARD_DATA\s*=\s*(\{.*\});?\s*$", text, re.S)
    if not match:
        raise ValueError(f"Could not parse dashboard data: {data_path}")
    return json.loads(match.group(1))


def normalize_recipient(value: str | None) -> str:
    recipient = (value or os.environ.get("ALERT_EMAIL_TO") or "skydiver1118@gmail.com").strip()
    if recipient.lower() == "skydiver1118@gmail":
        return "skydiver1118@gmail.com"
    return recipient


def send_completion_email(recipient: str, subject: str, body: str) -> None:
    host = os.environ.get("ALERT_SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("ALERT_SMTP_PORT", "587"))
    username = os.environ.get("ALERT_SMTP_USER", "")
    password = os.environ.get("ALERT_SMTP_PASSWORD", "")
    sender = os.environ.get("ALERT_EMAIL_FROM", username)
    if not username or not password or not sender:
        raise RuntimeError("Email needs ALERT_SMTP_USER, ALERT_SMTP_PASSWORD, and ALERT_EMAIL_FROM.")

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.starttls(context=context)
        smtp.login(username, password)
        smtp.send_message(message)


def build_email_body(data: dict[str, object], changed: bool, pushed: bool, sha: str) -> str:
    summary = data.get("summary", {}) if isinstance(data.get("summary"), dict) else {}
    stocks = data.get("stocks", []) if isinstance(data.get("stocks"), list) else []
    top_symbols = summary.get("topSymbols", [])
    if isinstance(top_symbols, list):
        top_line = ", ".join(str(symbol) for symbol in top_symbols[:12])
    else:
        top_line = ""

    if changed and pushed:
        deploy_action = "New GitHub Pages commit pushed"
    elif changed:
        deploy_action = "Dashboard rebuilt and committed locally; push was skipped"
    else:
        deploy_action = "No GitHub content changes; existing page remains current"

    return "\n".join(
        [
            "Technical-analysis dashboard scanner finished.",
            "",
            f"Dashboard: {PAGES_URL}",
            f"Deploy: {deploy_action}",
            f"Commit: {sha}",
            f"Generated at: {data.get('generatedAt', '--')}",
            f"Latest market date: {summary.get('latestMarketDate', '--')}",
            "",
            f"Watchlist symbols: {summary.get('watchlistCount', len(stocks))}",
            f"Scored: {summary.get('scoredCount', '--')}",
            f"Failed: {summary.get('failedCount', '--')}",
            f"Average technical score: {summary.get('averageTradingScore', '--')}",
            f"Bullish / Neutral / Bearish: {summary.get('bullishCount', '--')} / {summary.get('neutralCount', '--')} / {summary.get('bearishCount', '--')}",
            f"Top symbols: {top_line or '--'}",
            "",
            "This scanner refreshes charts, reports, scores, and the published technical-analysis dashboard.",
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build and publish the technical-analysis dashboard.")
    parser.add_argument("--date", default=None, help="Optional snapshot date passed to the build script.")
    parser.add_argument("--skip-build", action="store_true", help="Copy the existing local dashboard without rebuilding data.")
    parser.add_argument("--no-push", action="store_true", help="Commit locally but do not push to GitHub Pages.")
    parser.add_argument("--email-to", default=None, help="Completion email recipient.")
    parser.add_argument("--skip-email", action="store_true", help="Publish without sending a completion email.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.skip_build:
        build_dashboard(args.date)
    ensure_publish_repo()
    copy_dashboard()
    changed, sha = commit_and_push(push=not args.no_push)
    if not args.skip_email:
        data = parse_dashboard_data()
        recipient = normalize_recipient(args.email_to)
        body = build_email_body(data, changed, pushed=not args.no_push, sha=sha)
        send_completion_email(recipient, "[Technical Analysis Dashboard] Scanner complete", body)
        print(f"Completion email sent to {recipient}.")
    print(f"Dashboard URL: {PAGES_URL}")
    print(f"Commit: {sha}")
    print("Published changes." if changed else "No publish changes detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
