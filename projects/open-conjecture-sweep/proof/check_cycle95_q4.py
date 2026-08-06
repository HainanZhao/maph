from __future__ import annotations
import csv, json, sys
from pathlib import Path

def d2(a: int, b: int) -> int:
    return (a ^ b).bit_count() ** 2

def main(out: str) -> None:
    path = Path(out)
    rows = list(csv.DictReader(path.open(), delimiter="\t"))
    assert len(rows) == 65519
    seen = set()
    max_cost = 0
    for row in rows:
        subset = int(row["subset"]); cost = int(row["cost"])
        cyc = [int(x) for x in row["cycle"].split(",")]
        assert subset.bit_count() >= 2
        assert len(cyc) == subset.bit_count() and len(set(cyc)) == len(cyc)
        assert set(cyc) == {i for i in range(16) if subset & (1 << i)}
        assert cyc[0] == min(cyc)
        direct = sum(d2(cyc[i], cyc[(i + 1) % len(cyc)]) for i in range(len(cyc)))
        assert direct == cost and cost <= 32
        assert subset not in seen
        seen.add(subset); max_cost = max(max_cost, cost)
    assert len(seen) == 65519 and max_cost == 32
    summary = json.loads((path.parent / (path.name + ".summary.json")).read_text())
    assert summary == {"status": "PASS", "subsets": 65519, "max_cost": 32, "over_threshold": 0}
    print(json.dumps({"status": "PASS", "subsets": len(seen), "max_cost": max_cost}, sort_keys=True))

if __name__ == "__main__":
    main(sys.argv[1])
