#!/usr/bin/env python3
"""Versioned exact v3 correction for the Stream-C Route-B source closure.

V3 preserves the v2 mathematics but corrects its Huxley bibliographic identity
and withdraws its whole-route PASS pending an independently checked
truncated-explicit-formula source ledger.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
B = Fraction(30, 13)
S0 = Fraction(4, 5)
ONE_OVER_B = Fraction(13, 30)
TWO_OVER_B = Fraction(13, 15)

FROZEN_FILES = {
    "huxley_volume": (
        "artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf",
        "5946d8579810f0754e972d42a09ed2a703604b8fb4e6377f14caaa5dc48f9797",
    ),
    "guth_maynard_tex": (
        "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
        "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    ),
}


def q(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_frozen_files() -> dict[str, str]:
    checked: dict[str, str] = {}
    for key, (relative, expected) in FROZEN_FILES.items():
        observed = sha256(ROOT / relative)
        assert observed == expected, f"frozen source hash mismatch: {relative}"
        checked[key] = observed
    return checked


def certificate() -> dict[str, Any]:
    """Construct and exactly check the correction's rational invariants."""
    source_hashes = verify_frozen_files()
    h_s0 = Fraction(3, 1) / (3 * S0 - 1)
    margin = B - h_s0
    assert h_s0 == Fraction(15, 7)
    assert margin == Fraction(15, 91)
    assert ONE_OVER_B == 1 / B
    assert TWO_OVER_B == 2 / B
    assert Fraction(17, 30) == 1 - ONE_OVER_B
    assert Fraction(2, 15) == 1 - TWO_OVER_B

    return {
        "artifact_type": "versioned-stream-c-route-b-correction-certificate",
        "certificate_version": 3,
        "supersedes": "v2 only for the two explicitly listed corrections; v2 remains preserved",
        "epistemic_status": "OBSERVED",
        "claim_boundary": (
            "OBSERVED for the full route: its external truncated-explicit-formula source has not been "
            "independently checked. PROVED within the artifact: the Huxley bibliographic correction, "
            "the unchanged rational density arithmetic, and the status containment of the other v2 nodes."
        ),
        "source_hashes_checked": source_hashes,
        "correction_1_huxley_bibliography": {
            "status": "PROVED",
            "v2_incorrect_citation": "M. N. Huxley, The distribution of zeros of the Riemann zeta-function, Invent. Math. 15 (1972), 141-163.",
            "correct_citation": "M. N. Huxley, On the difference between consecutive primes, Invent. Math. 15 (1972), 164-170.",
            "frozen_locator": "(1.9), printed p. 164 / PDF p. 173",
            "cause": "citation identity was copied incorrectly; the frozen source and Guth--Maynard bibliography identify the correct article.",
            "affected_claims": "bibliographic metadata only; the theorem statement, two-sided height convention, log^44 factor, and exponent calculations are unchanged.",
        },
        "unchanged_huxley_math": {
            "status": "PROVED",
            "statement": "N(s,T) << T^(3(1-s)/(3s-1))(log T)^44 uniformly for 3/4<=s<=1 and -T<=gamma<=T.",
            "near_one_coefficient": {
                "h(4/5)": q(h_s0),
                "b": q(B),
                "b_minus_h(4/5)": q(margin),
                "identity": "b-3/(3s-1)=3(30s-23)/(13(3s-1)) >= 15/91 on [4/5,1]",
            },
        },
        "correction_2_explicit_formula_status": {
            "status": "PROVED",
            "observed_display": "GM TeX lines 2407-2417 displays the formula and cites Davenport Chapter 17.",
            "external_dependency_status": "OBSERVED",
            "unverified_items": [
                "external theorem statement and its precise hypotheses",
                "endpoint and zero-sum conventions",
                "multiplicity and truncation convention",
                "uniformity of O(x(log x)^3/T) in the employed range",
            ],
            "consequence": "No full Stream-C Route-B PASS or G0 PASS is licensed in v3.",
        },
        "retained_v2_nodes": {
            "status": "PROVED",
            "near_one_density": "Huxley (corrected citation) remains checked.",
            "zero_free_high_height": "Ford Theorem 5 remains checked.",
            "zero_free_low_height": "Platt--Trudgian Theorem 1 remains checked.",
            "local_pair_count": "Hasanalizade--Shen--Wong RvM with Bui--Heath-Brown multiplicity convention remains checked.",
            "scope": "These are partial dependency closures, not a route-level PASS.",
        },
        "exact_transfer_invariants": {
            "b": q(B),
            "1_over_b": q(ONE_OVER_B),
            "2_over_b": q(TWO_OVER_B),
            "uniform_theta": "17/30",
            "almost_all_theta": "2/15",
            "status": "PROVED exact rational arithmetic only; downstream use remains contingent on the OBSERVED formula node.",
        },
        "next_authorized_dependency_action": "Incorporate and independently check the literature agent's formula ledger before changing external_truncated_explicit_formula from OBSERVED.",
        "replay": {
            "interpreter_requirement": "Python 3 standard library only",
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/replay_short_intervals_stream_c_route_b_v3.py --write projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-route-b-v3.json",
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
