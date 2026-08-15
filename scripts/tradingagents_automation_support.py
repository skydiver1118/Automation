from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def tradingagents_runner_env(tradingagents_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    site_packages = tradingagents_root / ".venv" / "Lib" / "site-packages"
    scripts_dir = tradingagents_root / ".venv" / "Scripts"

    pythonpath_parts = [str(tradingagents_root)]
    if site_packages.exists():
        pythonpath_parts.append(str(site_packages))
    existing_pythonpath = env.get("PYTHONPATH")
    if existing_pythonpath:
        pythonpath_parts.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

    env["VIRTUAL_ENV"] = str(tradingagents_root / ".venv")
    env["PATH"] = os.pathsep.join([str(scripts_dir), env.get("PATH", "")])
    return env


def can_execute_python(python_executable: Path, cwd: Path) -> tuple[bool, str | None]:
    try:
        completed = subprocess.run(
            [str(python_executable), "--version"],
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except OSError as exc:
        return False, f"{type(exc).__name__}: {exc}"
    if completed.returncode != 0:
        output = (completed.stdout or "").strip()
        return False, output or f"exit code {completed.returncode}"
    return True, None


def python_command_for_tradingagents(python_executable: Path, tradingagents_root: Path) -> tuple[list[str], dict[str, str], str]:
    runnable, detail = can_execute_python(python_executable, tradingagents_root)
    if runnable:
        return [str(python_executable)], os.environ.copy(), str(python_executable)

    env = tradingagents_runner_env(tradingagents_root)
    fallback = f"{sys.executable} (fallback with TradingAgents PYTHONPATH)"
    reason = detail or "unknown launch failure"
    print(f"TradingAgents venv launcher unavailable ({reason}); using {fallback}.")
    return [sys.executable], env, fallback


def git_base_command(repo: Path) -> list[str]:
    return ["git", "-c", f"safe.directory={repo.resolve()}"]
