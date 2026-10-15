#!/usr/bin/env python3
"""Run the ETCP audit from the repository root.

Usage:
    python ETCP_File_9_run_audit.py

This runs etcp_audit.py and regenerates the audit outputs
defined by that script. It does not train models or reproduce
forecasting metrics.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "etcp_audit.py"
if not SCRIPT.is_file():
    raise SystemExit("Cannot find etcp_audit.py in the repository root.")
result = subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=False)
raise SystemExit(result.returncode)
