#!/usr/bin/env python3
"""Seal the exact P7-3 coloured ideal Gram/energy bridge and its boundary."""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from conventions import p7_common_ideal_cubic_v1 as C
from conventions.proof_runtime_v2 import require_pinned_runtime


OUT = ROOT / "artifacts/p7-common-ideal-cubic-v1.json"
SELF = Path(__file__)
FILES = {
    "conventions": ROOT / "conventions/p7_common_ideal_cubic_v1.py",
    "document": ROOT / "docs/p7-common-ideal-cubic-v1.md",
    "tests": ROOT / "tests/test_p7_common_ideal_cubic_v1.py",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_product(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [[sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))] for i in range(len(left))]


def finite_gram_identity() -> dict[str, object]:
    """An exact Z/2 test of the labelled ideal cubic expansion.

    Ideals 0 and 1 have the same norm but opposite nontrivial-character
    value.  All times are zero, so the calculation is over integers.
    """
    ideal_classes = (0, 1, 0)
    norms = (5, 5, 7)
    labels = (0, 1, 1)
    # K_xy=sum_a (-1)^((label_x-label_y)*class(a)); norms are retained for
    # the record even though t_x=t_y=0 in this exact test.
    sign = lambda left, right, ideal: -1 if ((left - right) * ideal_classes[ideal]) % 2 else 1
    kernel = [[sum(sign(labels[x], labels[y], a) for a in range(3)) for y in range(3)] for x in range(3)]
    cube = matrix_product(matrix_product(kernel, kernel), kernel)
    direct_trace = sum(cube[i][i] for i in range(3))
    expanded_trace = 0
    for x in range(3):
        for y in range(3):
            for z in range(3):
                for a in range(3):
                    for b in range(3):
                        for c in range(3):
                            expanded_trace += sign(labels[x], labels[y], a) * sign(labels[y], labels[z], b) * sign(labels[z], labels[x], c)
    require(direct_trace == expanded_trace, "labelled Gram cubic expansion failed")
    return {
        "field_model": "formal Z/2 character group; integer-valued exact check",
        "ideal_norms": list(norms),
        "equal_norm_distinct_ideals": [0, 1],
        "character_labels": list(labels),
        "kernel": kernel,
        "direct_trace_K_cubed": direct_trace,
        "expanded_labelled_ideal_trace": expanded_trace,
    }


def coloured_energy_identity() -> dict[str, object]:
    """Exact finite Z/2 coloured-energy/orthogonality check."""
    # (character label in Z/2, discrete time); two colours collide at t=0.
    points = ((0, 0), (1, 0), (1, 1), (0, 2))
    coloured = 0
    uncoloured = 0
    for p1 in points:
        for p2 in points:
            for p3 in points:
                for p4 in points:
                    time_relation = p1[1] + p2[1] == p3[1] + p4[1]
                    if time_relation:
                        uncoloured += 1
                    if time_relation and (p1[0] + p2[0] - p3[0] - p4[0]) % 2 == 0:
                        coloured += 1
    require(coloured <= uncoloured, "coloured energy cannot exceed uncoloured multiplicity energy")
    # This is the finite character-orthogonality expansion of the same count:
    # (1/2) sum_g chi_1(g)chi_2(g)conj(chi_3(g)chi_4(g)).
    orthogonality_count = 0
    for p1 in points:
        for p2 in points:
            for p3 in points:
                for p4 in points:
                    if p1[1] + p2[1] != p3[1] + p4[1]:
                        continue
                    char_sum = sum((-1) ** (g * (p1[0] + p2[0] - p3[0] - p4[0])) for g in (0, 1))
                    require(char_sum in (0, 2), "finite character orthogonality failed")
                    orthogonality_count += char_sum // 2
    require(orthogonality_count == coloured, "coloured Parseval count failed")
    return {
        "points": [list(point) for point in points],
        "colour_group": "Z/2",
        "coloured_energy": coloured,
        "uncoloured_time_energy_with_multiplicity": uncoloured,
        "orthogonality_parseval_count": orthogonality_count,
        "same_height_distinct_colours": [[0, 0], [1, 0]],
    }


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    source_rows = {}
    for label, row in C.SOURCES.items():
        path = ROOT / row["path"]
        require(path.is_file() and digest(path) == row["sha256"], f"pinned source mismatch: {label}")
        source_rows[label] = dict(row)
    prereg = json.loads((ROOT / C.SOURCES["p7_preregistration_v2"]["path"]).read_text())
    gate = next(item for item in prereg["gates"] if item["id"] == C.GATE_ID)
    require(gate["state"] == "UNEXECUTED", "the frozen P7-3 preregistration state changed")
    p7_2 = json.loads((ROOT / C.SOURCES["p7_ray_orthogonality_v1"]["path"]).read_text())
    require(p7_2["gate_outcome"] == "PASS_EXACT_PROJECTOR_AND_SCOPED_L2_LARGE_SIEVE", "P7-2 prerequisite missing")
    identities = {label: {"path": str(path.relative_to(ROOT)), "sha256": digest(path)} for label, path in FILES.items()}
    identities["builder"] = {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)}
    return {
        "artifact_id": "p7-common-ideal-cubic-v1",
        "epistemic_status": "PROVED",
        "gate": C.GATE_ID,
        "gate_outcome": "PASS_EXACT_IDEAL_IDENTITIES_CONTAINED_COMMON_SAMPLE_CUBIC_OPEN",
        "claim_boundary": "Exact labelled-ideal Gram and fixed-modulus coloured-energy identities, plus a scoped source-hypothesis/type boundary. No P7 cubic large-value inequality is proved.",
        "review_policy": "LIGHTWEIGHT_SOURCE_ALGEBRA_REPLAY; no hostile audit initiated.",
        "sample_convention": C.SAMPLE_CONVENTION,
        "exact_ideal_gram_bridge": {
            "polynomial": "D_x=Sum_a c(a) chi_x(a) w(Na/N) (Na)^(i t_x), with x=(f_x,chi_x,t_x), |c(a)|<=1 and chi_x(a)=0 if (a,f_x)!=1.",
            "gram_kernel": "K_xy=Sum_a |c(a)|^2 w(Na/N)^2 chi_x(a) conjugate(chi_y(a)) (Na)^(i(t_x-t_y)). K=M M^* is positive semidefinite.",
            "norm_fibre_formula": "K_xy=Sum_n n^(i(t_x-t_y)) B_xy(n), where B_xy(n)=Sum_{Na=n}|c(a)|^2w(n/N)^2chi_x(a)conjugate(chi_y(a)).",
            "single_character_l2_fibre_bound": "For b_chi(n)=Sum_{Na=n}c(a)chi(a), Cauchy gives |b_chi(n)|^2 <= a_Q(i)(n) Sum_{Na=n}|c(a)|^2 1_(a,f)=1. Since a_Q(i)(n)<=tau(n)=N^(o(1)) on n~N, norm collapse has only an N^(o(1)) L2 loss (and is T^(o(1)) in the already pinned N<=T^C regime).",
            "cubic_trace": "tr(K^3)=Sum_{x,y,z in W} Sum_{a,b,c} u(a)u(b)u(c) chi_x(a/c)chi_y(b/a)chi_z(c/b)(Na/Nc)^(i t_x)(Nb/Na)^(i t_y)(Nc/Nb)^(i t_z), with u(a)=|c(a)|^2w(Na/N)^2 and every quotient notation meaning the displayed product of character values, including zero extensions.",
            "repeated_norm_statement": "Na=Nb removes only the t-phase. Distinct ideals of equal norm remain separate in B_xy(n); repeated norms themselves have the recorded divisor-bounded L2 cost, while the unresolved obstruction is the surviving pair-label dependence and coloured sample geometry.",
            "finite_exact_check": finite_gram_identity(),
        },
        "fixed_modulus_coloured_energy": {
            "ambient_group": "For one modulus f, G_f=Cl(f) and its full character group Ghat_f are used as the ambient colour group; W may be a subset of primitive labels.",
            "definition": "E_col^=(W)=#{(x1,x2,x3,x4) in W^4: t1+t2=t3+t4 and chi1 chi2=chi3 chi4 in Ghat_f}.",
            "parseval_identity": "E_col^=(W)=|G_f|^(-1) Sum_{g in G_f} Integral_0^1 |Sum_{(chi,t) in W} chi(g)e(t theta)|^4 dtheta for integral t; a smooth real-height version replaces the exact time diagonal by the Fourier weight.",
            "comparison": "E_col^=(W) is at most the uncoloured exact additive energy of the time multiset, not of a de-duplicated time set.",
            "primitive_not_group": "Exact-conductor primitive characters need not be closed under multiplication. For f=(3), the unique nontrivial primitive order-two character squares to the conductor-one character. The Parseval identity therefore uses the complete ambient group, not a fictional primitive character group.",
            "finite_exact_check": coloured_energy_identity(),
        },
        "scoped_verbatim_import_failure": {
            "gm_hypothesis": "The pinned Guth--Maynard cubic trace is for one integer coefficient sequence and one globally separated uncoloured W subset of R; its Poisson step uses sums over all integers n in a common block.",
            "failure_1_pair_coefficients": "After norm grouping, the exact coefficient is B_xy(n), depending on the pair of character labels, rather than one common b_n. P7-1 already gives two unequal one-character norm aggregates in one conductor shell.",
            "failure_2_colour_collisions": "The density family naturally gives separation within each character fibre, while two distinct characters may contribute the same height. Such points are distinct elements of W but are not globally separated in the uncoloured t-coordinate, so the cited m=0 diagonal reduction cannot be invoked verbatim.",
            "failure_3_varying_moduli": "There is no single ray-class character group for varying exact conductors. Inflating every character to a common multiple F changes zero-extended values on ideals coprime to its own conductor but not to F, unless c is globally restricted to (a,F)=1; that restriction is an unproved new loss.",
            "positivity_boundary": "K is positive semidefinite, but the displayed labelled cubic summands and the primitive Moebius projector are signed/complex. Positivity of the whole trace is not a positive primitive projector or a replacement for the missing coloured affine estimate.",
            "scope": "This proves only that the cited integer argument's hypotheses are absent for the joint family. It does not rule out a new character-aware, coloured, or conductor-by-conductor argument.",
        },
        "missing_estimate_for_next_gate": {
            "required_object": "A family-uniform bound for the off-diagonal labelled cubic trace (or an equivalent large-value inequality) for common ideal c, with colour-local height separation, repeated norm fibres B_xy(n), and primitive exact-conductor indexing retained.",
            "must_control": ["same-height different-character collisions", "cross-conductor triple terms", "the signed primitive projector without termwise positivity", "the loss from any common-modulus inflation or conductor-by-conductor decomposition"],
            "not_supplied_by_sources": "Neither the checked Guth--Maynard integer cubic-trace result nor Thorner's cited L2 Hecke large sieve supplies this estimate.",
        },
        "source_integrity": source_rows,
        "artifact_identity": identities,
        "non_promotion": list(C.NON_PROMOTION),
        "resource_contract": C.RESOURCE_LIMITS,
        "replay": {"script": str(SELF.relative_to(ROOT)), "script_sha256": digest(SELF), "runtime": runtime, "write_command": "python3 proof/build_p7_common_ideal_cubic_v1.py --write", "check_command": "python3 proof/build_p7_common_ideal_cubic_v1.py --check"},
    }


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.write != args.check, "choose exactly one of --write or --check")
    started = time.monotonic_ns()
    data = render(report())
    elapsed = time.monotonic_ns() - started
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "P7-3 replay exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "P7-3 replay exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7-3 artifact")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "P7-3 artifact mismatch; issue a versioned correction rather than overwrite")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
