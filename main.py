#!/usr/bin/env python3
"""Thin wrapper: run visualization script with default n=12."""
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent
    script = project_root / "scripts" / "run_visualization.py"
    rc = subprocess.call(
        [sys.executable, str(script), "--n", "12"],
        cwd=project_root,
    )
    sys.exit(rc)
