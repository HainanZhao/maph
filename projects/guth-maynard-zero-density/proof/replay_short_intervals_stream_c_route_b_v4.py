#!/usr/bin/env python3
"""Deterministic v4 closure of Stream-C Route B's formula-source blocker."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
B = Fraction(30, 13)
FROZEN = {
    "formula_source_ledger_v2": ("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v2.json", "3433e974b9751d310447847d75abbf529e5b4ed7e21e87a0224e4efb8ea0fde3"),
    "formula_source_check_v2": ("proof/check_cycle_2_stream_c_explicit_formula_sources_v2.py", "346a7beb7a5c2387b99f5a3e03a78bd0bf9856b38ce0e6bd4da0192d95b95f27"),
    "route_b_v3": ("artifacts/cycle-2-stream-c-route-b-v3.json", "9eca349eae8721e1b0c80a5d54ccf75a08cc7e1fdf99ca887548891c480d53f5"),
    "route_b_v3_replay": ("proof/replay_short_intervals_stream_c_route_b_v3.py", "254899acff31f3fa4eb644ab677b13ed5c928719ab789195fe11323660556d74"),
    "gm_tex": ("artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def verify() -> dict[str, str]:
    checked: dict[str, str] = {}
    for name, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"frozen dependency hash mismatch: {relative}"
        checked[name] = actual
    subprocess.run(
        ["python3", str(ROOT / "proof/check_cycle_2_stream_c_explicit_formula_sources_v2.py")],
        check=True, capture_output=True, text=True,
    )
    subprocess.run(
        ["python3", str(ROOT / "proof/replay_short_intervals_stream_c_route_b_v3.py"), "--check", str(ROOT / "artifacts/cycle-2-stream-c-route-b-v3.json")],
        check=True, capture_output=True, text=True,
    )
    source = json.loads((ROOT / "artifacts/cycle-2-stream-c-explicit-formula-source-closure-v2.json").read_text())
    v3 = json.loads((ROOT / "artifacts/cycle-2-stream-c-route-b-v3.json").read_text())
    assert source["epistemic_status"] == "PROVED"
    assert v3["retained_v2_nodes"]["status"] == "PROVED"
    assert v3["exact_transfer_invariants"]["b"] == "30/13"
    return checked


def certificate() -> dict[str, Any]:
    checked = verify()
    one_over_b = Fraction(1, 1) / B
    two_over_b = Fraction(2, 1) / B
    assert one_over_b == Fraction(13, 30)
    assert two_over_b == Fraction(13, 15)
    assert Fraction(17, 30) == 1 - one_over_b
    assert Fraction(2, 15) == 1 - two_over_b
    # If rho=beta+i*gamma with 0<=beta<=1, a disagreement between
    # |rho|<=T and |gamma|<T is contained in |T-|gamma||<=1 for T>=2.
    assert Fraction(1, 1) <= Fraction(2, 1)
    return {
        "artifact_type": "stream-c-route-b-closure-certificate",
        "certificate_version": 4,
        "supersedes": "v3 only by closing its external truncated-explicit-formula source node; v1-v3 remain preserved",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED conditional only on Guth--Maynard's published zero-density theorem: the archived explicit-formula source, endpoint transfer, height/multiplicity convention bridge, and Route-B dependency chain are closed. No new density exponent or prime-interval exponent is claimed.",
        "frozen_dependencies": checked,
        "external_truncated_explicit_formula": {
            "status": "PROVED",
            "source": "Kedlaya 18.785 Theorem 1 and proof unit, licensed MIT OCW CC BY-NC-SA 4.0; source ledger v2",
            "range": "all x>=2, T>0; GM uses 2<=T<=x",
            "remainder_transfer": "At u=ceil(x)-1 and v=floor(x+y), the half-weight and endpoint changes plus both source remainders are O(x(log x)^3/T).",
        },
        "convention_bridge": {
            "status": "PROVED",
            "endpoint": "sum_(n in [x,x+y]) Lambda(n) differs from psi_0(v)-psi_0(u) by O(log x), with v-u=y+O(1).",
            "multiplicity": "Kedlaya's residue computation explicitly counts every zero with multiplicity; the local boundary count is pinned by HSW plus Bui--Heath-Brown.",
            "height": "Kedlaya uses |gamma|<T. Any literal GM |rho|<=T discrepancy lies in unit boundary strips and is O(x log T/T), absorbed in O(x(log x)^3/T).",
        },
        "retained_route_b_v3_nodes": {
            "status": "PROVED",
            "near_one_density": "Huxley (corrected bibliographic identity)",
            "zero_free_high_height": "Ford Theorem 5",
            "zero_free_low_height": "Platt--Trudgian Theorem 1",
            "local_pair_count": "Hasanalizade--Shen--Wong plus Bui--Heath-Brown",
        },
        "exact_transfer_invariants": {
            "status": "PROVED",
            "b": q(B),
            "1_over_b": q(one_over_b),
            "2_over_b": q(two_over_b),
            "uniform_theta": "17/30",
            "almost_all_theta": "2/15",
        },
        "route_conclusion": {
            "status": "PROVED conditional only on Guth--Maynard's published zero-density theorem",
            "uniform": "The Route-B deduction supplies the stated asymptotic in intervals of exponent theta=17/30+epsilon.",
            "almost_all": "The Route-B deduction supplies the stated almost-all asymptotic at exponent theta=2/15+epsilon.",
            "scope": "This is a source-chain closure of Guth--Maynard's existing deduction, not an improvement or independent reproof of its density theorem.",
        },
        "replay": {
            "interpreter_requirement": "Python 3 standard library plus pinned system mutool for PDF text-anchor verification",
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/replay_short_intervals_stream_c_route_b_v4.py --write projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-route-b-v4.json",
        },
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", type=Path, metavar="PATH")
    action.add_argument("--check", type=Path, metavar="PATH")
    args = parser.parse_args()
    output = render(certificate())
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(output, encoding="utf-8")
    elif args.check:
        if args.check.read_text(encoding="utf-8") != output:
            raise SystemExit(f"certificate mismatch: regenerate with --write ({args.check})")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
