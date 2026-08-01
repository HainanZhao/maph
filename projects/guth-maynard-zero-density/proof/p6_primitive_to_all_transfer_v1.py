#!/usr/bin/env python3
"""Replay the narrow primitive-to-all Dirichlet-character transfer lemma.

This script proves only the elementary conductor/Euler-factor transfer used by
P6 Z05/Z06.  It does not repair the CGL detector, its X/T tail, its external
inputs, its multiplicity convention, or its undefined T-smooth condition.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import sys
import tarfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUT = ROOT / "artifacts/p6-primitive-to-all-transfer-v1.json"
CGL_TAR = ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.tar"
PREREG = ROOT / "artifacts/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1.json"
RECONCILIATION = ROOT / "artifacts/p6-cgl-v2-reconciliation-v1.json"
CONVENTIONS = ROOT / "conventions/baseline.py"
CGL_TAR_SHA256 = "b982cd5afa5b5e8a9abff2c6306519ba558d321b19aadd3fdbe59b3750f8e9ae"
TEX_MEMBER = "Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_Zero_Density_of_Dirichlet___L_-Functions.tex"
WALL_CAP_NS = 60_000_000_000
RSS_CAP_KIB = 262_144


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cgl_lines() -> list[str]:
    require(digest(CGL_TAR) == CGL_TAR_SHA256, "pinned CGL v2 tar hash changed")
    with tarfile.open(CGL_TAR, "r") as archive:
        member = archive.getmember(TEX_MEMBER)
        extracted = archive.extractfile(member)
        require(extracted is not None, "pinned CGL TeX member is absent")
        return extracted.read().decode("utf-8").splitlines()


def source_checks() -> dict[str, object]:
    lines = cgl_lines()
    # Convert human TeX line numbers to zero-based Python positions only here.
    line_2109 = lines[2108]
    line_2137 = lines[2136]
    line_2150 = lines[2149]
    require("primitive characters modulo $q$" in line_2109, "CGL 2109 primitive scope changed")
    require("all factors of $q$ and summing" in line_2109, "CGL 2109 transfer announcement changed")
    require("\\prod_{p | q}" in line_2137, "CGL 2137 principal Euler product changed")
    require("\\sum_{\\chi \\bmod q}" in line_2150, "CGL 2150 all-character sum changed")
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    reconciliation = json.loads(RECONCILIATION.read_text(encoding="utf-8"))
    expected = ["Z05_PRIMITIVE_EULER_FACTORS", "Z06_CONDUCTOR_SUM_Q1"]
    prereg_rows = {row["id"]: row for row in prereg["row_registry"]}
    require(all(row in prereg_rows for row in ("Z05", "Z06")), "P6 Z05/Z06 registry changed")
    require(reconciliation["overall_disposition"] == "OPEN_ANALYTIC_INPUT", "P6 reconciliation disposition changed")
    require(
        all(item in reconciliation["open_analytic_obligations"]["shared_open_after_label_normalization"] for item in expected),
        "reconciliation no longer records the primitive-to-all obligations",
    )
    conventions = CONVENTIONS.read_text(encoding="utf-8")
    require('ZERO_ORDINATE_INTERVAL = "absolute_value_at_most_T"' in conventions, "height convention changed")
    require('ZERO_MULTIPLICITY = "included"' in conventions, "multiplicity convention changed")
    return {
        "cgl_v2_tar": {
            "path": str(CGL_TAR.relative_to(ROOT)),
            "sha256": CGL_TAR_SHA256,
            "tex_member": TEX_MEMBER,
            "locators": {
                "primitive_reduction_announcement": "TeX 2109",
                "principal_example_of_finite_euler_factor": "TeX 2136--2138",
                "all_character_zero_sum": "TeX 2148--2152",
            },
        },
        "p6_records": {
            "preregistration": {"path": str(PREREG.relative_to(ROOT)), "sha256": digest(PREREG)},
            "reconciliation": {"path": str(RECONCILIATION.relative_to(ROOT)), "sha256": digest(RECONCILIATION)},
        },
        "frozen_zero_count_conventions": {
            "path": str(CONVENTIONS.relative_to(ROOT)),
            "sha256": digest(CONVENTIONS),
            "height": "|Im rho| <= T",
            "multiplicity": "included",
            "transfer_note": "The divisor identity is valid both with and without multiplicity if one convention is used on both sides; it does not resolve P6 S03's source wording.",
        },
    }


def proof_payload() -> dict[str, object]:
    """Return a finite, replayable statement of the elementary proof.

    The universal parts are supplied as a self-contained finite-group and
    Euler-product derivation rather than inferred from a numerical search.
    """
    return {
        "epistemic_status": "PROVED",
        "definitions": {
            "character_mod_q": "A Dirichlet character modulo q is a group character of (Z/qZ)^* extended by 0 off integers coprime to q.",
            "primitive_count": "N^*(sigma,T;d)=sum_{psi primitive mod d} N(sigma,T,psi).",
            "zero_region": "sigma>0, |Im rho|<=T; the P6 application uses sigma>1/2.",
        },
        "primitive_inducer": {
            "statement": "Every Dirichlet character chi modulo q has one and only one primitive inducing character chi* of conductor d dividing q.",
            "self_contained_derivation": [
                "Write q=product_p p^(a_p) and use the Chinese-remainder identification (Z/qZ)^*=product_p (Z/p^(a_p)Z)^*.",
                "For each local group character, take the least b_p in {0,...,a_p} through which it factors under reduction to (Z/p^(b_p)Z)^*; b_p=0 denotes the trivial modulus-1 factor.",
                "Their product is a character chi* modulo d=product_p p^(b_p), and extending chi* by zero away from (n,q)=1 gives chi.",
                "If chi* were induced from a proper divisor of d, one local b_p would not be least. Hence chi* is primitive; least local exponents also prove uniqueness.",
            ],
            "scope": "This uses only finite-group factorization and covers p=2 as well as odd primes; no primitive-root parametrization is needed.",
        },
        "euler_factor_zero_transfer": {
            "identity": "L(s,chi)=L(s,chi*) product_{p|q, p not|d}(1-chi*(p)p^(-s)).",
            "derivation": [
                "For Re(s)>1, divide the two absolutely convergent Euler products: the omitted Euler factors are exactly the primes p|q with p not|d.",
                "Meromorphic continuation gives the same identity globally. For each such p, |chi*(p)|=1.",
                "If 1-chi*(p)p^(-s)=0, taking absolute values gives p^(-Re(s))=1, hence Re(s)=0.",
                "Thus the finite factor is holomorphic and nonvanishing in Re(s)>0, so L(s,chi) and L(s,chi*) have identical zero multisets there, including multiplicities.",
            ],
            "principal_case": "The principal character has d=1 and the same argument applies; poles are also unchanged in Re(s)>0, while the assertion concerns zero multisets.",
        },
        "exact_partition": {
            "identity": "sum_{chi mod q} N(sigma,T,chi)=sum_{d|q} N^*(sigma,T;d), for sigma>0.",
            "derivation": [
                "The unique-conductor map partitions all characters modulo q by d|q.",
                "Within each conductor class, replace chi by its unique primitive inducer using the preceding zero-multiset equality.",
            ],
        },
        "conditional_envelope_transfer": {
            "uniform_input": "Fix sigma0>0 and A>=0. Suppose that for every delta>0 there are C_delta,K_delta such that N^*(sigma,T;d)<=C_delta(dT)^(A(1-sigma)+delta) whenever sigma0<=sigma<1, d,T>=1, and dT>=K_delta.",
            "large_dT_sum": "sum_{d|q, dT>=K_delta} N^*(sigma,T;d) <= C_delta tau(q)(qT)^(A(1-sigma)+delta).",
            "divisor_loss": "For every delta>0, tau(q)<<_delta q^delta<= (qT)^delta for q,T>=1. Choosing delta=epsilon/2 gives exponent A(1-sigma)+epsilon.",
            "small_dT": "For dT<K_delta, necessarily d<=K_delta and T<=K_delta. The finite constant B_{K_delta,sigma0}=sum_{d<=K_delta} sum_{psi primitive mod d} N(sigma0,K_delta,psi) bounds all such terms. It is absorbed because qT>=1. Thus no asymptotic estimate is applied outside its dT range.",
            "conclusion": "sum_{chi mod q} N(sigma,T,chi) <<_{epsilon,sigma0} (qT)^(A(1-sigma)+epsilon), uniformly for q,T>=1 and sigma0<=sigma<1.",
        },
        "cgl_final_envelope_specialization": {
            "conditional_primitive_input": "N^*(sigma,T;d) <<_epsilon (dT)^epsilon[(d^(7/3)T^2)^(1-sigma)+(dT)^((30/13)(1-sigma))], uniformly in the stated primitive range, with the same small-dT convention above.",
            "transferred_all_character_envelope": "sum_{chi mod q}N(sigma,T,chi) <<_epsilon (qT)^epsilon[(q^(7/3)T^2)^(1-sigma)+(qT)^((30/13)(1-sigma))].",
            "uniform_consequence": "Since T>=1 and 30/13<7/3, this implies the monotone uniform 7/3 envelope (qT)^((7/3)(1-sigma)+epsilon).",
            "why_monotone": "Both displayed primitive bases are nondecreasing in d, so replacing d by q before the divisor sum is valid.",
        },
        "limits": [
            "This transfer does not justify an arbitrary q1-sensitive intermediate formula: after induction the relevant conductor is d, and a chosen q1 need not divide d or retain its source range.",
            "It closes the mathematical content of Z05/Z06 only for a separately established primitive envelope that is monotone in the conductor, not for the CGL preprint as a whole.",
            "Z03_TAIL_X_RANGE, S06_EXTERNAL_INPUTS, F08_T_SMOOTH_UNDEFINED, and S03_MULTIPLICITY_NOT_STATED remain open.",
        ],
    }


def payload() -> dict[str, object]:
    sources = source_checks()
    proof = proof_payload()
    return {
        "artifact_id": "p6-primitive-to-all-transfer-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "A narrow self-contained conductor/Euler-factor transfer lemma. It "
            "proves the primitive-to-all reduction for a monotone, uniformly "
            "available primitive zero-density envelope; it neither validates nor "
            "repairs Chen--Gupta--Li v2, and proves no new zero-density or "
            "short-interval theorem. No hostile audit is initiated."
        ),
        "source_checks": sources,
        "lemma": proof,
        "p6_effect": {
            "Z05": "PROVED_FOR_ZERO_COUNTS_IN_Re_s_GREATER_THAN_0",
            "Z06": "PROVED_FOR_MONOTONE_PRIMITIVE_ENVELOPES_WITH_UNIFORMITY_AND_SMALL_dT_HANDLED",
            "not_promoted": [
                "CGL-v2 zero-density theorem",
                "q1-sensitive intermediate formulae",
                "Z03_TAIL_X_RANGE",
                "S06_EXTERNAL_INPUTS",
                "F08_T_SMOOTH_UNDEFINED",
                "S03_MULTIPLICITY_NOT_STATED",
            ],
        },
        "replay": {
            "command": "python3 proof/p6_primitive_to_all_transfer_v1.py --check",
            "python_implementation": sys.implementation.name,
            "python_version": ".".join(map(str, sys.version_info[:3])),
            "optimized": sys.flags.optimize,
            "wall_cap_ns": WALL_CAP_NS,
            "rss_cap_kib": RSS_CAP_KIB,
        },
    }


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.write != args.check, "choose exactly one of --write or --check")
    require(sys.flags.optimize == 0, "transfer replay rejects optimized Python")
    require(sys.version_info[:3] == (3, 12, 3) and sys.platform.startswith("linux"), "transfer replay requires CPython 3.12.3 on linux")
    started = time.monotonic_ns()
    value = payload()
    elapsed = time.monotonic_ns() - started
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    require(elapsed < WALL_CAP_NS, "transfer replay exceeded 60-second wall cap")
    require(rss < RSS_CAP_KIB, "transfer replay exceeded 256-MiB RSS cap")
    encoded = render(value)
    if args.write:
        require(not OUT.exists(), "refusing to overwrite transfer artifact")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file(), "transfer artifact is absent")
        require(OUT.read_bytes() == encoded, "transfer artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as err:
        print(err, file=sys.stderr)
        raise SystemExit(1)
