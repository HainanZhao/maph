#!/usr/bin/env python3
"""Exact group-layer screen for the conductor-one AFK subfamily.

This intentionally does not claim an AFK packet or a TCC result.  AFK's
order-ray indexing agrees with the maximal-order ray group only when f=1;
even there this script records solely the character support of 1-R before
the imprimitive-monoid and Engine-A checks.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import json
from math import gcd, lcm
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SKELETON = ROOT / "discovery" / "tcc-sweep-afk-tuple-skeleton-d1024-v1.json"
OUTPUT = ROOT / "discovery" / "tcc-sweep-conductor-one-group-layer-d1024-v1.json"


def pari_polynomial(discriminant: int) -> str:
    if discriminant % 4 == 1:
        return f"x^2-x+{(1-discriminant)//4}"
    return f"x^2-{discriminant//4}"


def run_pari(rows: list[dict[str, object]]) -> dict[tuple[int, int], tuple[list[int], list[int]]]:
    lines = ["default(parisizemax,4G);"]
    for row in rows:
        d, r, delta = int(row["d"]), int(row["r"]), int(row["fundamental_discriminant"])
        lines.extend(
            [
                f"K=bnfinit({pari_polynomial(delta)},1);",
                f"R=bnrinit(K,[{d},[1,0]],1);",
                f"print(\"ROW|{d}|{r}|\",Vec(R.cyc),\"|\",Vec(bnrisprincipal(R,idealhnf(K,{d-1}),0)[1]));",
            ]
        )
    completed = subprocess.run(
        ["gp", "-q"], input="\n".join(lines), text=True, capture_output=True,
        cwd=ROOT, check=True,
    )
    result: dict[tuple[int, int], tuple[list[int], list[int]]] = {}
    for line in completed.stdout.splitlines():
        if not line.startswith("ROW|"):
            continue
        _, d, r, cyc, sign_log = line.split("|")
        result[(int(d), int(r))] = (
            [int(x) for x in cyc.strip()[1:-1].split(",") if x],
            [int(x) for x in sign_log.strip()[1:-1].split(",") if x],
        )
    if len(result) != len(rows):
        raise RuntimeError((len(result), len(rows), completed.stderr))
    return result


def character_order(cyc: list[int], coordinate: tuple[int, ...]) -> int:
    return lcm(*(1 if a == 0 else n // gcd(n, a) for n, a in zip(cyc, coordinate)))


def support_orders(cyc: list[int], sign_log: list[int]) -> list[int]:
    orders = []
    for coordinate in itertools.product(*(range(n) for n in cyc)):
        pairing = sum(Fraction(a * b, n) for a, b, n in zip(coordinate, sign_log, cyc))
        if pairing.denominator != 1:
            orders.append(character_order(cyc, coordinate))
    return sorted(orders)


def main() -> None:
    skeleton = json.loads(SKELETON.read_text())
    # Canonical r=1 rows are covered by the existing all-d>=5 order-ray
    # no-go theorem.  This discovery run spends PARI time only on the
    # genuinely noncanonical, conductor-one rows left outside that theorem.
    input_rows = [
        row for row in skeleton["records"]
        if row["r"] != 1 and 1 in row["allowed_form_conductors"]
    ]
    pari = run_pari(input_rows)
    rows = []
    for input_row in input_rows:
        key = (int(input_row["d"]), int(input_row["r"]))
        cyc, sign_log = pari[key]
        orders = support_orders(cyc, sign_log)
        rows.append(
            {
                **input_row,
                "ray_invariant_factors": cyc,
                "sign_class_log_of_(d-1)": sign_log,
                "support_character_orders": orders,
                "full_quadratic_group_layer": bool(orders) and max(orders) <= 2,
                "nonquadratic_support_count": sum(order > 2 for order in orders),
            }
        )
    hits = [row for row in rows if row["d"] > 8 and row["full_quadratic_group_layer"]]
    result = {
        "schema": "tcc-sweep-conductor-one-group-layer-v1",
        "claim_tag": "OBSERVED",
        "scope": "noncanonical maximal-order f=1 group layer only; not an AFK monoid, Euler, packet, or TCC certificate",
        "dimension_limit": 1024,
        "input_row_count": len(rows),
        "full_quadratic_group_layer_count": sum(row["full_quadratic_group_layer"] for row in rows),
        "full_quadratic_group_layer_hits_above_8": hits,
        "records": rows,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("TCC_SWEEP_CONDUCTOR_ONE_GROUP_LAYER=PASS")


if __name__ == "__main__":
    main()
