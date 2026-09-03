import os
import subprocess
from pathlib import Path


API_SERVER_NAME = "digital-growth-charts-server"
API_SERVER_VERSION = "5.0.0"  # this is set by bump version


def _resolve_commit() -> str:
    if github_sha := os.getenv("GITHUB_SHA"):
        return github_sha

    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).parent,
            check=True,
            capture_output=True,
            text=True,
            timeout=2,
        ).stdout.strip() or "unknown"
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return "unknown"


API_SERVER_COMMIT = _resolve_commit()
