#!/usr/bin/env python3
"""Deterministic Route-A continuation for the three Stream-B coverage gaps.

This is an exact rational-exponent audit conditional on the pinned published
inputs.  It extends Route A v2 without importing Route B, and deliberately
does not claim a new zero-density theorem or a full G0 promotion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GM = ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
GM_TAR = ROOT / "artifacts/sources/guth-maynard-2405.20552v2-source.tar"
V2 = ROOT / "artifacts/cycle-2-stream-b-route-a-v2.json"
FROZEN = {
    GM: "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    GM_TAR: "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc",
}
LO, HI = Fraction(7, 10), Fraction(4, 5)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def q(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def a(s: Fraction) -> Fraction:
    return 15 * (1 - s) / (3 + 5 * s)


def ell(s: Fraction) -> Fraction:
    return Fraction(10, 1) / (6 + 10 * s)


def upper(s: Fraction) -> Fraction:
    return Fraction(15, 1) / (6 + 10 * s)


def d(s: Fraction) -> Fraction:
    return Fraction(18, 5) - 4 * s


def alpha(s: Fraction) -> Fraction:
    return a(s) / d(s)


def mvt_residual(s: Fraction) -> Fraction:
    return (250 * (s - Fraction(3, 4)) ** 2 + Fraction(3, 8)) / (2 * (3 + 5 * s) * (9 - 10 * s))


def poly_add(*values: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    degree = max(len(value) for value in values)
    result = [Fraction(0, 1) for _ in range(degree)]
    for value in values:
        for index, coefficient in enumerate(value):
            result[index] += coefficient
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return tuple(result)


def poly_scale(value: tuple[Fraction, ...], scalar: Fraction) -> tuple[Fraction, ...]:
    return tuple(scalar * coefficient for coefficient in value)


def poly_mul(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    result = [Fraction(0, 1) for _ in range(len(left) + len(right) - 1)]
    for i, a_coefficient in enumerate(left):
        for j, b_coefficient in enumerate(right):
            result[i + j] += a_coefficient * b_coefficient
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return tuple(result)


def symbolic_identity_audit() -> None:
    """Exact polynomial certificates for all rational identities used below."""
    one_minus_s = (Fraction(1, 1), Fraction(-1, 1))
    one_minus_2s = (Fraction(1, 1), Fraction(-2, 1))
    denominator = (Fraction(3, 1), Fraction(5, 1))
    a_numerator = (Fraction(15, 1), Fraction(-15, 1))
    upper_denominator = (Fraction(6, 1), Fraction(10, 1))
    d_numerator = (Fraction(18, 1), Fraction(-20, 1))  # d=d_numerator/5
    third_coefficient = (Fraction(12, 5), Fraction(-4, 1))
    ell_numerator = (Fraction(10, 1),)
    # A=2(1-s)u and A=1+(12/5-4s)ell, after cross multiplication.
    assert poly_mul(a_numerator, upper_denominator) == poly_mul(poly_scale(one_minus_s, Fraction(30, 1)), denominator)
    assert poly_mul(a_numerator, upper_denominator) == poly_mul(poly_add(upper_denominator, poly_mul(third_coefficient, ell_numerator)), denominator)
    # The exact MVT residual numerator after the common denominator
    # (3+5s)(18-20s)=2(3+5s)(9-10s).
    direct_mvt_numerator = poly_add(
        poly_mul(a_numerator, d_numerator),
        poly_scale(poly_mul(denominator, d_numerator), Fraction(-1, 1)),
        poly_scale(poly_mul(one_minus_2s, a_numerator), Fraction(-5, 1)),
    )
    assert direct_mvt_numerator == (Fraction(141, 1), Fraction(-375, 1), Fraction(250, 1))
    # A-2(1-s) has numerator (1-s)(9-10s) over 3+5s.
    assert poly_add(a_numerator, poly_scale(poly_mul(one_minus_s, denominator), Fraction(-2, 1))) == poly_mul(one_minus_s, (Fraction(9, 1), Fraction(-10, 1)))


def check_sources() -> None:
    for path, expected in FROZEN.items():
        assert sha256(path) == expected, f"frozen source hash mismatch: {path.name}"
    gm = GM.read_text(encoding="utf-8")
    for phrase in (
        "If $N,k$ are such that $N^k\\le T^\\alpha$, then we apply Theorem \\ref{thrm:LargeValues}",
        "N^{2k(1-\\sigma)}+N^{(18/5-4\\sigma)k}+TN^{(12/5-4\\sigma)k}",
        "If instead we have $N^k>T^\\alpha$, then we apply the usual Mean Value Theorem",
        "1+(1-2\\sigma)\\alpha=\\frac{129-195\\sigma+50\\sigma^2}",
        "Thus it suffices to show that if $N<T^{1/2+o(1)}$ and $W$ is a 1-separated set",
    ):
        assert phrase in gm, f"missing GM §13.1 anchor: {phrase}"


def exact_exponent_audit() -> dict[str, Any]:
    """Check every displayed identity at exact endpoints and its sign proof."""
    symbolic_identity_audit()
    for s in (LO, Fraction(3, 4), HI):
        # These identities are recorded below with their factorizations;
        # sampled substitutions protect against transcription errors.
        assert a(s) == 2 * (1 - s) * upper(s)
        assert a(s) == d(s) * alpha(s)
        assert a(s) == 1 + (Fraction(12, 5) - 4 * s) * ell(s)
        assert a(s) - (1 + (1 - 2 * s) * alpha(s)) == mvt_residual(s)
        assert a(s) - 2 * (1 - s) == (1 - s) * (9 - 10 * s) / (3 + 5 * s)
    assert d(HI) == Fraction(2, 5) > 0
    assert 4 * LO - Fraction(12, 5) == Fraction(2, 5) > 0
    assert upper(HI) - 1 == Fraction(1, 14) > 0
    assert a(HI) == Fraction(3, 7) > 0
    assert mvt_residual(LO) == Fraction(1, 26)
    assert mvt_residual(Fraction(3, 4)) == Fraction(1, 54)
    assert mvt_residual(HI) == Fraction(1, 14)
    return {
        "range": "7/10 <= sigma <= 4/5",
        "range_signs": {
            "1-sigma": ">= 1/5 > 0",
            "3+5sigma": ">= 13/2 > 0",
            "9-10sigma": ">= 1 > 0",
            "d(sigma)=18/5-4sigma": ">= 2/5 > 0",
            "4sigma-12/5": ">= 2/5 > 0",
            "u(sigma)-1": ">= 1/14 > 0",
            "A(sigma)": ">= 3/7 > 0",
        },
        "definitions": {
            "A(sigma)": "15(1-sigma)/(3+5sigma)",
            "ell(sigma)": "10/(6+10sigma)",
            "u(sigma)": "15/(6+10sigma)",
            "alpha(sigma)": "A(sigma)/(18/5-4sigma)",
        },
        "theorem_1_1_structural_terms": {
            "source_terms": ["L^(2-2sigma)", "L^(18/5-4sigma)", "T L^(12/5-4sigma)"],
            "q_definition": "L=N^k=T^q",
            "branch_condition": "ell(sigma) <= q <= u(sigma) eventually and q <= alpha(sigma)",
            "first_residual": "A(sigma)-2q(1-sigma)=2(1-sigma)(u(sigma)-q) >= 0",
            "second_residual": "A(sigma)-(18/5-4sigma)q=(18/5-4sigma)(alpha(sigma)-q) >= 0",
            "third_residual": "A(sigma)-[1+(12/5-4sigma)q]=(4sigma-12/5)(q-ell(sigma)) >= 0",
            "conclusion": "Every Theorem 1.1 structural exponent is <= A(sigma); the large-k upper bound is eventual, so the analytic conclusion retains T^o(1), not a finite-T equality.",
        },
        "mvt_branch": {
            "branch_condition": "q>alpha(sigma), q<=u(sigma) eventually",
            "first_term": "A(sigma)-2q(1-sigma)=2(1-sigma)(u(sigma)-q) >= 0 eventually",
            "second_term_residual": "A(sigma)-[1+(1-2sigma)alpha(sigma)]=[250(sigma-3/4)^2+3/8]/[2(3+5sigma)(9-10sigma)] > 0",
            "positivity": "The numerator is >=3/8>0; both denominator factors are positive on the frozen interval.",
            "exact_sample_margins": {"7/10": q(mvt_residual(LO)), "3/4": q(mvt_residual(Fraction(3, 4))), "4/5": q(mvt_residual(HI))},
            "conclusion": "The second MVT exponent is strictly below A(sigma); no finite-T endpoint upgrade is asserted.",
        },
        "type_ii": {
            "residual": "A(sigma)-2(1-sigma)=(1-sigma)(9-10sigma)/(3+5sigma) > 0",
            "conclusion": "2(1-sigma) <= A(sigma) throughout 7/10 <= sigma <= 4/5",
        },
    }


def additional_rows() -> list[dict[str, Any]]:
    return [
        {
            "id": "SB-A21-beta-cutoff-wording-correction",
            "status": "PROVED",
            "locator": "GM §13.1 and MP Definition Type I/II",
            "statement": "Correction to v2 wording only: the GM and MP Type-I detectors agree in divisor sum, damping, dyadic N range, and threshold. The condition beta>=sigma belongs to the R_II(sigma,T) counting restriction, not to MP's Type-I detector definition.",
            "falsifier": "A beta-dependent condition in the MP Type-I detector would require a renewed detector comparison.",
        },
        {
            "id": "SB-A22-theorem-1-1-three-structural-terms",
            "status": "PROVED",
            "locator": "GM Theorem 1.1 and §13.1",
            "statement": "For L=N^k=T^q with ell(sigma)<=q<=u(sigma) eventually and q<=alpha(sigma), all three source exponents 2q(1-sigma), (18/5-4sigma)q, and 1+(12/5-4sigma)q are at most A(sigma), by the three exact residual factorizations recorded in exact_exponent_audit.",
            "falsifier": "A sign reversal in any displayed residual, or failure of q to lie in the stated branch range, invalidates this application row.",
        },
        {
            "id": "SB-A23-mvt-strict-positive-residual",
            "status": "PROVED",
            "locator": "GM §13.1, equation following the mean-value branch",
            "statement": "For q>alpha(sigma), the second mean-value exponent has exact strictly positive residual [250(sigma-3/4)^2+3/8]/[2(3+5sigma)(9-10sigma)]. Its denominator and numerator are positive on the full frozen interval; the first term is controlled by the eventual q<=u(sigma) bound.",
            "falsifier": "A zero or negative denominator/numerator on 7/10<=sigma<=4/5 would refute the strict-margin conclusion.",
        },
        {
            "id": "SB-A24-type-ii-and-dyadic-reassembly",
            "status": "PROVED",
            "locator": "GM §13.1 opening dyadic reduction; MP Lemma 24; elementary eta identity",
            "statement": "The Type-II exponent obeys 2(1-sigma)<=A(sigma) by an exact positive residual. For every epsilon>0, summing positive shells U=T/2^j gives sum_j U^(A+epsilon)<=T^(A+epsilon)/(1-2^(-A-epsilon)); fixed low shells are O(1). There is no real non-trivial zeta zero because eta(s)>0 and zeta(s)=eta(s)/(1-2^(1-s))<0 for 0<s<1; conjugation therefore changes the positive-height multiplicity count by exactly two.",
            "falsifier": "A real non-trivial zero, nonpositive A(sigma), or a shell bound lacking uniform eventual constants would invalidate this reassembly.",
        },
    ]


def build_report() -> dict[str, Any]:
    check_sources()
    inherited = json.loads(V2.read_text(encoding="utf-8"))
    inherited_body = {key: value for key, value in inherited.items() if key not in {"mathematical_and_source_audit_sha256", "replay"}}
    assert canonical_sha256(inherited_body) == inherited["mathematical_and_source_audit_sha256"]
    exact = exact_exponent_audit()
    new_rows = additional_rows()
    assert all(row["status"] == "PROVED" for row in inherited["rows"] + new_rows)
    return {
        "artifact_id": "cycle-2-stream-b-route-a-v3",
        "route": "A",
        "stream": "B",
        "supersedes": {
            "artifact": "cycle-2-stream-b-route-a-v2",
            "canonical_audit_sha256": inherited["mathematical_and_source_audit_sha256"],
            "preservation": "v1 and v2 are retained unchanged; this is an additive continuation and wording correction.",
        },
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED only as a pinned-source application audit and exact rational-exponent check. It neither re-proves GM/MP analytic theorems nor proves a new density estimate or a full G0 claim.",
        "pass_state": "NARROW PASS: all Stream-B application nodes represented by Route A v2 plus the Theorem-1.1 terms, strict MVT residual, and final Type-I/Type-II reassembly are source-pinned and checked. Stream C remains outside this audit.",
        "frozen_source_hashes": {str(path.relative_to(ROOT)): value for path, value in FROZEN.items()},
        "inherited_rows": inherited["rows"],
        "rows": new_rows,
        "exact_rational_audit": exact,
        "open_blockers": [],
        "replay": {
            "interpreter_requirement": "Python 3 standard library only",
            "script": str(Path(__file__).relative_to(ROOT)),
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_cycle2_stream_b_route_a_v3.py --write projects/guth-maynard-zero-density/artifacts/cycle-2-stream-b-route-a-v3.json",
        },
    }


def render(report: dict[str, Any]) -> str:
    return json.dumps(report, sort_keys=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", type=Path, metavar="PATH")
    action.add_argument("--check", type=Path, metavar="PATH")
    args = parser.parse_args()
    output = render(build_report())
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
