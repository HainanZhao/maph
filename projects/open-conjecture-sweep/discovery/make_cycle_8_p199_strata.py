#!/usr/bin/env python3
"""Freeze the deterministic completed-orbit sample for Cycle 8."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "discovery/out/k13-p199.txt"
TARGET = ROOT / "discovery/out/cycle8-p199-strata.txt"
TOTAL = 4_748_938
PER_STRATUM = 10


def main() -> None:
    indices = [stratum * TOTAL // 10 + offset for stratum in range(10) for offset in range(PER_STRATUM)]
    if indices != sorted(indices) or len(indices) != 100 or len(set(indices)) != 100:
        raise AssertionError("invalid frozen index schedule")
    chosen: dict[int, str] = {}
    needed = set(indices)
    with SOURCE.open() as handle:
        for index, line in enumerate(handle):
            if index in needed:
                row = line.strip()
                if len(row.split()) != 13:
                    raise AssertionError(f"malformed source row {index}")
                chosen[index] = row
    if len(chosen) != len(indices):
        raise AssertionError(f"source row count/index mismatch: found {len(chosen)} expected {len(indices)}")
    TARGET.write_text("\n".join(chosen[index] for index in indices) + "\n")
    print(f"rows={len(indices)} first_index={indices[0]} last_index={indices[-1]}")


if __name__ == "__main__":
    main()
