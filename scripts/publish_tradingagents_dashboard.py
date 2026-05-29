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
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

from tradingagents_automation_support import git_base_command


WORKSPACE = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = WORKSPACE / "tradingagents_dashboard"
PUBLISH_REPO = WORKSPACE / "github_pages_repo"
REFRESH_SCRIPT = WORKSPACE / "scripts" / "refresh_tradingagents_dashboard.py"
REPO_CLONE_URL = "https://github.com/skydiver1118/my_yolo_test.git"
REPO_WEB_URL = "https://github.com/skydiver1118/my_yolo_test"
PAGES_URL = "https://skydiver1118.github.io/my_yolo_test/"

ROOT_FILES = ["app.js", "styles.css", "README.md", "_headers"]

PAGES_WORKFLOW = """name: Deploy dashboard to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Configure Pages
        uses: actions/configure-pages@v5
        with:
          enablement: true
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: .
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""


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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def copy_dashboard_files() -> None:
    if not (DASHBOARD_DIR / "index.html").exists():
        raise FileNotFoundError(f"Dashboard source is missing: {DASHBOARD_DIR}")

    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    index = (DASHBOARD_DIR / "index.html").read_text(encoding="utf-8")
    index = re.sub(r"styles\.css(\?v=[^\"']+)?", f"styles.css?v={stamp}", index)
    index = re.sub(r"app\.js(\?v=[^\"']+)?", f"app.js?v={stamp}", index)
    index = re.sub(r"data/dashboard-data\.js\?v=[^\"']+", f"data/dashboard-data.js?v={stamp}", index)
    write_text(PUBLISH_REPO / "index.html", index)

    for filename in ROOT_FILES:
        source = DASHBOARD_DIR / filename
        if source.exists():
            shutil.copy2(source, PUBLISH_REPO / filename)

    data_dir = PUBLISH_REPO / "data"
    data_dir.mkdir(exist_ok=True)
    shutil.copy2(DASHBOARD_DIR / "data" / "dashboard-data.js", data_dir / "dashboard-data.js")
    write_text(PUBLISH_REPO / ".nojekyll", "")
    write_text(PUBLISH_REPO / ".github" / "workflows" / "pages.yml", PAGES_WORKFLOW)


def parse_dashboard_data() -> dict:
    data_path = DASHBOARD_DIR / "data" / "dashboard-data.js"
    raw = data_path.read_text(encoding="utf-8")
    match = re.search(r"window\.TRADING_AGENTS_DASHBOARD_DATA\s*=\s*(\{.*\});?\s*$", raw, re.S)
    if not match:
        raise ValueError(f"Could not parse generated dashboard data: {data_path}")
    return json.loads(match.group(1))


def refresh_dashboard(report_mode: str, report_date: str | None) -> int:
    cmd = [sys.executable, str(REFRESH_SCRIPT), "--reports", report_mode]
    if report_date:
        cmd.extend(["--date", report_date])
    completed = run(cmd, WORKSPACE, check=False)
    return completed.returncode


def commit_and_push() -> tuple[bool, str]:
    git_run(["add", "."], PUBLISH_REPO)
    status = git_run(["status", "--porcelain"], PUBLISH_REPO).stdout.strip()
    if not status:
        sha = git_run(["rev-parse", "--short", "HEAD"], PUBLISH_REPO).stdout.strip()
        return False, sha

    message = f"Refresh TradingAgents dashboard {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    git_run(["commit", "-m", message], PUBLISH_REPO)
    git_run(["push", "origin", "main"], PUBLISH_REPO)
    sha = git_run(["rev-parse", "--short", "HEAD"], PUBLISH_REPO).stdout.strip()
    return True, sha


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


def build_email_body(data: dict, refresh_code: int, pushed: bool, sha: str) -> str:
    portfolio = data.get("portfolio", {})
    stocks = data.get("stocks", [])
    coverage = sum(1 for stock in stocks if stock.get("fullReport", {}).get("available"))
    symbols = ", ".join(stock.get("symbol", "") for stock in stocks[:12])
    status = "complete" if refresh_code == 0 else f"completed with refresh exit code {refresh_code}"
    deploy_action = "New GitHub Pages commit pushed" if pushed else "No GitHub content changes; existing page remains current"
    return "\n".join(
        [
            "TradingAgents dashboard refresh finished.",
            "",
            f"Status: {status}",
            f"Dashboard: {PAGES_URL}",
            f"Repository: {REPO_WEB_URL}",
            f"Deploy: {deploy_action}",
            f"Commit: {sha}",
            "",
            f"Watchlist symbols: {len(stocks)}",
            f"Full-report coverage: {coverage}/{len(stocks)}",
            f"Portfolio rating: {portfolio.get('rating', '--')}",
            f"First symbols: {symbols}",
            "",
            "The dashboard is static-hosted on GitHub Pages and updates after the Pages workflow completes.",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh, publish, and email the TradingAgents dashboard.")
    parser.add_argument("--reports", choices=["missing", "all", "none"], default="missing")
    parser.add_argument("--date", default=None, help="Optional TradingAgents report date.")
    parser.add_argument("--email-to", default=None, help="Completion email recipient.")
    parser.add_argument("--skip-email", action="store_true", help="Publish without sending a completion email.")
    args = parser.parse_args()

    refresh_code = refresh_dashboard(args.reports, args.date)
    ensure_publish_repo()
    copy_dashboard_files()
    data = parse_dashboard_data()
    pushed, sha = commit_and_push()

    if not args.skip_email:
        recipient = normalize_recipient(args.email_to)
        body = build_email_body(data, refresh_code, pushed, sha)
        send_completion_email(recipient, "[TradingAgents Dashboard] Refresh complete", body)
        print(f"Completion email sent to {recipient}.")

    print(f"Dashboard URL: {PAGES_URL}")
    if refresh_code != 0:
        return refresh_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
