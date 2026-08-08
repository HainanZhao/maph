#!/usr/bin/env python3
"""Build the post-review Lane B manuscript and proof-release files."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof import build_lane_b_release_archive_v2 as base  # noqa: E402


base.PREFIX = "lane-b-separator-compression-2026-08-correction-v3"


if __name__ == "__main__":
    raise SystemExit(base.main())
