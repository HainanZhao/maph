#!/usr/bin/env python3
"""Independent integer-arithmetic verifier for the printed W2 table."""

from __future__ import annotations

import math
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROW = re.compile(
    r"SHINTANI_DIVISOR_(?P<exponent>\d+)_IDEAL=.* "
    r"RAY_ORDER=(?P<ray>\d+) W=(?P<w>\d+) "
    r"N_INDEX=(?P<n>\d+) CLEARING_EXPONENT=(?P<m>\d+)"
)


def main() -> None:
    completed = subprocess.run(
        ["gp", "-q", "scripts/q7_p7_w2_divisors.gp"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode or "user error" in completed.stderr:
        raise SystemExit(completed.stdout + completed.stderr)
    rows = []
    for line in completed.stdout.splitlines():
        match = ROW.fullmatch(line)
        if match:
            rows.append({key: int(value) for key, value in match.groupdict().items()})
    if len(rows) != 2:
        raise SystemExit(f"expected two divisor rows, got {rows}")
    full_ray_order = 12
    expected_f = {0: 1, 1: 7}
    expected_h = 1
    for row in rows:
        expected_n = row["w"] * full_ray_order // row["ray"]
        if row["n"] != expected_n:
            raise SystemExit(f"bad distribution index: {row}")
        base = expected_h if row["exponent"] == 0 else expected_f[row["exponent"]]
        if row["m"] != 12 * base * row["n"]:
            raise SystemExit(f"bad clearing exponent: {row}")
    safe = math.lcm(*(row["m"] for row in rows))
    if safe != 4032:
        raise SystemExit(f"unexpected safe exponent {safe}")
    required = [
        "SHINTANI_W_VALUES=[4, 1]",
        "REAL_DISTRIBUTION_DENOMINATORS_CLEARED=1",
        "Q7_P7_W2_DIVISOR_TABLE_CERTIFIED=1",
    ]
    missing = [marker for marker in required if marker not in completed.stdout]
    if missing:
        raise SystemExit(f"missing markers: {missing}")
    output = ROOT / "artifacts" / "q7-p7-w2-divisor-table-v1.txt"
    output.write_text(completed.stdout)
    print("INDEPENDENT_DIVISOR_ROW_COUNT=2")
    print("INDEPENDENT_SAFE_EXPONENT=4032")
    print("Q7_P7_W2_DIVISOR_TABLE_INDEPENDENTLY_VERIFIED=1")


if __name__ == "__main__":
    main()
