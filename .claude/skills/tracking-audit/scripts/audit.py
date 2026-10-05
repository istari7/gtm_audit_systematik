#!/usr/bin/env python3
"""Entry point for the tracking-audit skills. Run from the repo root; audits are written to outputs/<slug>/:

    python .claude/skills/tracking-audit/scripts/audit.py run bychari.com poler.com
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tracking_audit.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
