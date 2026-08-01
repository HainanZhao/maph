#!/usr/bin/env python3
"""Seal the P7 detector-side local-occupancy obstruction and conditional route."""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from conventions import p7_detector_local_occupancy_v1 as C
from conventions.proof_runtime_v2 import require_pinned_runtime


OUT = ROOT / "artifacts/p7-detector-local-occupancy-v1.json"
SELF = Path(__file__)
FILES = {
    "conventions": ROOT / "conventions/p7_detector_local_occupancy_v1.py",
    "document": ROOT / "docs/p7-detector-local-occupancy-v1.md",
    "tests": ROOT / "tests/test_p7_detector_local_occupancy_v1.py",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_occupancy(times: tuple[Fraction, ...], radius: Fraction) -> int:
    """Maximum number of distinct times in a closed radius-radius interval."""
    require(radius > 0, "local occupancy radius must be positive")
    require(len(times) == len(set(times)), "time projection must be a set")
    ordered = tuple(sorted(times))
    return max(
        sum(left <= right <= left + 2 * radius for right in ordered)
        for left in ordered
    )


def local_difference_multiplicity(times: tuple[Fraction, ...], radius: Fraction) -> int:
    """Exact maximum count in a closed difference window of radius radius."""
    require(radius > 0, "difference sampling radius must be positive")
    differences = tuple(first - second for first in times for second in times)
    ordered = tuple(sorted(differences))
    return max(
        sum(left <= right <= left + 2 * radius for right in ordered)
        for left in ordered
    )


def local_zero_geometry_check() -> dict[str, object]:
    """Check the exact disk geometry used with the pinned zero-circle lemma."""
    epsilon = C.LOCAL_ZERO_CENTER_REAL_PART - 1
    radius = C.LOCAL_ZERO_CIRCLE_RADIUS
    half = Fraction(1, 2)
    horizontal = 1 + epsilon - half
    max_distance_squared = horizontal * horizontal + half * half
    radius_squared = radius * radius
    require(epsilon == Fraction(1, 20), "frozen local-zero horizontal shift changed")
    require(radius == Fraction(3, 4), "frozen local-zero circle radius changed")
    require(max_distance_squared == Fraction(221, 400), "local-zero geometry numerator changed")
    require(radius_squared == Fraction(225, 400), "local-zero circle radius square changed")
    require(radius_squared - max_distance_squared == Fraction(1, 100), "local-zero disk margin vanished")
    return {
        "right_half_zero_region": "beta>=1/2 and |gamma-u|<=1/2",
        "circle_center": "21/20+i*u",
        "circle_radius": str(radius),
        "maximum_distance_squared": str(max_distance_squared),
        "circle_radius_squared": str(radius_squared),
        "strict_margin": str(radius_squared - max_distance_squared),
        "functional_equation_transport": "A nontrivial zero beta+i*gamma of chi with beta<1/2 maps to 1-beta-i*gamma of bar(chi), so its ordinate lies in the reflected unit window centered at -u.",
        "per_half_bound": "L_circ(q,u)=(3/4)(4 log 4+2 log q+4 log(|u|+3)+12)+8=3 log 4+(3/2)log q+3 log(|u|+3)+17.",
        "unit_window_bound": "Z_chi(u)<=L_0(q,u):=3 log q+6 log(|u|+3)+6 log 4+34.",
        "derivation_scope": "The source circle lemma is applied to the exact primitive conductor f_chi, with q=N(f_chi), D_K=4, n_K=2, and delta(chi)<=1. It bounds the zero multiset and hence also distinct zero ordinates.",
    }


def detector_geometry_obstruction_check() -> dict[str, object]:
    """Exact coloured-block model saturating D<=m times local occupancy."""
    colours = C.EXACT_CHECKS["colours"]
    blocks = C.EXACT_CHECKS["blocks"]
    require(isinstance(colours, int) and colours >= 1, "frozen colour count is invalid")
    require(isinstance(blocks, int) and blocks >= 1, "frozen block count is invalid")
    radius = C.SAMPLING_RADIUS
    by_colour = {
        colour: tuple(
            Fraction(3 * block) + Fraction(colour, 8 * colours)
            for block in range(blocks)
        )
        for colour in range(colours)
    }
    times = tuple(sorted(value for fibre in by_colour.values() for value in fibre))
    sample_size = len(times)
    occupancy = local_occupancy(times, radius)
    multiplicity = local_difference_multiplicity(times, radius)
    same_colour_gaps = [
        fibre[index + 1] - fibre[index]
        for fibre in by_colour.values()
        for index in range(len(fibre) - 1)
    ]
    require(all(gap >= 1 for gap in same_colour_gaps), "fibrewise one-separation failed")
    require(sample_size == colours * blocks, "block model size changed")
    require(occupancy == colours, "local cross-character occupancy is not sharp in frozen model")
    require(multiplicity == sample_size * occupancy, "D<=m*M is not sharp in frozen model")
    require(multiplicity >= sample_size, "diagonal difference floor was lost")
    return {
        "radius_Delta": str(radius),
        "colours_P": colours,
        "blocks_J": blocks,
        "time_projection_size_m": sample_size,
        "times_by_colour": {str(colour): [str(value) for value in fibre] for colour, fibre in by_colour.items()},
        "minimum_same_colour_gap": str(min(same_colour_gaps)),
        "per_colour_unit_window_count": 1,
        "uncoloured_local_occupancy_M_Delta": occupancy,
        "local_difference_multiplicity_D_Delta": multiplicity,
        "sharp_upper_bound_m_times_M": sample_size * occupancy,
        "model_status": "COMBINATORIAL_ONLY: this is not an assertion about actual zeros or a constructed P7 detector.",
        "conclusion": "Even per-character unit-window count one and 1-separation allow D_Delta=mP. Therefore individual local zero counts and primitive-family cardinality alone cannot remove the cross-character factor P.",
    }


def joint_sampling_algebra_check() -> dict[str, object]:
    """Exact bookkeeping for the conditional common-detector local sampler."""
    threshold_squared = C.EXACT_CHECKS["joint_threshold_squared"]
    mass = C.EXACT_CHECKS["joint_mass"]
    require(isinstance(threshold_squared, int) and threshold_squared > 0, "joint threshold is invalid")
    require(isinstance(mass, int) and mass > 0, "joint mass is invalid")
    selected_times = mass // threshold_squared
    require(mass % threshold_squared == 0 and selected_times == 3, "joint sampling exact model changed")
    require(C.SAMPLING_RADIUS + C.SOBLEV_RADIUS == Fraction(1, 2), "local Sobolev support changed")
    return {
        "finite_threshold_squared_V2": threshold_squared,
        "finite_continuous_mass_bound": mass,
        "deduced_selected_time_count": selected_times,
        "exact_counting_step": "If every selected representative has |D_chi(t)|^2>=V^2 and the joint sampled L2 mass is at most L||c||_2^2, then M_Delta V^2<=L||c||_2^2.",
        "translation": "For a local center u, replace c(a) by c_u(a)=c(a)(Na)^(-iu). Its l2 norm and support are unchanged, and chi(a)=0 off (a,f)=1 remains exactly the frozen zero extension.",
        "local_source_window": "With Delta=r=1/4, Sobolev intervals for a 1-separated character fibre are disjoint and lie in [-1/2,1/2] after translation; enlarge to the source interval [-2,2].",
        "source_scale": "L_loc(N,Q)=(4+(1/2)log^2(2N))(2N+16Q^2)(log(4Q))^A, from Thorner Theorem 2.1 with source cutoff 2N, conductor cutoff 2Q, height 2, and m=0.",
    }


def source_integrity() -> dict[str, object]:
    rows: dict[str, object] = {}
    for label, row in C.SOURCES.items():
        path = ROOT / row["path"]
        require(path.is_file() and digest(path) == row["sha256"], f"pinned source mismatch: {label}")
        rows[label] = dict(row)

    preregistration = json.loads((ROOT / C.SOURCES["p7_preregistration_v2"]["path"]).read_text(encoding="utf-8"))
    gate = next(item for item in preregistration["gates"] if item["id"] == C.GATE_ID)
    require(gate["state"] == "UNEXECUTED", "immutable P7-3 gate state changed")

    colour = json.loads((ROOT / C.SOURCES["p7_fixed_ray_colour_v1"]["path"]).read_text(encoding="utf-8"))
    shell = colour["dyadic_shell"]
    require(shell["fixed_group_bound"] == "|X(f)|<=N(f)<=2Q.", "fixed ray-class cardinality boundary changed")
    require(shell["complete_character_bound"] == "sum_{Q<Nf<=2Q}|X(f)|<12Q^2.", "dyadic family cardinality boundary changed")

    transfer = json.loads((ROOT / C.SOURCES["p7_fixed_ray_discrepancy_transfer_v1"]["path"]).read_text(encoding="utf-8"))
    require(transfer["gate_outcome"] == "ADVANCED_COMPLETE_TO_PRIMITIVE_L2_TRANSFER_DIFFERENCE_SAMPLING_OPEN", "P7 difference-sampling predecessor changed")
    require("D_Delta(T)=sup_v" in transfer["difference_sampling"]["definition"], "P7 D_Delta convention unavailable")
    require("H z_B^2" in transfer["selected_cubic_budget"]["thorner_difference_gate"], "P7 cubic target unavailable")

    selected = json.loads((ROOT / C.SOURCES["p7_selected_gram_excess_v1"]["path"]).read_text(encoding="utf-8"))
    parseval = selected["fixed_ray_class_average_compression"]["complete_character_parseval"]
    require("delta_2^2=H^-1" in parseval and "eta in X" in parseval, "selected fixed-ray parseval identity changed")

    ray = json.loads((ROOT / C.SOURCES["p7_ray_orthogonality_v1"]["path"]).read_text(encoding="utf-8"))
    specialization = ray["large_sieve"]["checked_specialization"]
    require("m=0" in specialization and "chi primitive" in ray["large_sieve"]["shell_conclusion"], "primitive m=0 L2 specialization unavailable")

    thorner = (ROOT / C.SOURCES["thorner_2019_rendered"]["path"]).read_text(encoding="utf-8")
    for marker in (
        "Theorem 2.1. Let c(a) be a function on the ideals of",
        "where ∗ denotes summing over primitive characters",
        "(N + Q2T nK)(log QT)A",
    ):
        require(marker in thorner, f"pinned Thorner locator unavailable: {marker}")

    lfzd = (ROOT / C.SOURCES["thorner_zaman_lfzd_tex"]["path"]).read_text(encoding="utf-8")
    for marker in (
        r"\xi(s, \chi) = w(\chi) \xi(1-s, \bar{\chi})",
        r"N_{\chi}(r; s) :=",
        r"then, for $0 < r \leq 1$",
        r"4\log D_K + 2 \log \N \kf_{\chi}",
        r"2n_K\log(|t|+3)",
    ):
        require(marker in lfzd, f"pinned Thorner--Zaman locator unavailable: {marker}")
    return rows


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    sources = source_integrity()
    identities = {label: {"path": str(path.relative_to(ROOT)), "sha256": digest(path)} for label, path in FILES.items()}
    identities["builder"] = {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)}
    local_zero = local_zero_geometry_check()
    obstruction = detector_geometry_obstruction_check()
    joint = joint_sampling_algebra_check()
    return {
        "artifact_id": "p7-detector-local-occupancy-v1",
        "epistemic_status": "PROVED",
        "gate": C.GATE_ID,
        "gate_outcome": "CONTAINED_DETECTOR_SIDE_OCCUPANCY_OBSTRUCTION_GATE_REMAINS_OPEN",
        "claim_boundary": "Exact local-zero/counting consequences, a sharp combinatorial detector-geometry obstruction, and a conditional common-detector joint-sampling reduction only. No P7 detector or source-scale D_Delta bound is established.",
        "review_policy": "LIGHTWEIGHT_SOURCE_ALGEBRA_REPLAY; no hostile audit initiated.",
        "exact_conductor_and_extension": {
            "status": "PROVED",
            "selected_rows": "W is a set of (f,chi,t) with Q<N(f)<=2Q and chi primitive of exact finite conductor f; no row is replaced by an imprimitive character at another modulus.",
            "zero_extension": "Every polynomial retains chi(a)=0 when (a,f)!=1. The local phase c_u(a)=c(a)(Na)^(-iu) changes neither the support nor this extension.",
            "source_indexing": "Thorner's star sum is primitive, so each exact conductor is indexed once in the shell restriction.",
        },
        "individual_local_zero_count": {
            "status": "PROVED",
            "definition": "Z_chi(u) is the number of nontrivial zeros in the zero multiset of L(s,chi) with |Im(rho)-u|<=1/2.",
            "bound": "For q=N(f_chi), Z_chi(u)<=L_0(q,u)=3 log q+6 log(|u|+3)+6 log 4+34.",
            "method": "Apply the pinned circle-zero lemma at 21/20+i*u with radius 3/4 to beta>=1/2, then use xi(s,chi)=w(chi)xi(1-s,bar(chi)) for beta<1/2.",
            "finite_exact_geometry_check": local_zero,
            "detector_thinning_consequence": "If each selected time is assigned to a zero of the same exact primitive L(s,chi) within alpha, at most b selected times are assigned to one zero, and alpha+Delta<=1/2, then a single fibre contributes at most bL_0(q,u) times to a radius-Delta window about u.",
        },
        "what_zero_counts_and_cardinality_give": {
            "status": "PROVED",
            "uncoloured_projection": "Let T=pi_t(W), m=|T|, and M_Delta(T)=sup_u # (T intersect [u-Delta,u+Delta]). Then D_Delta(T)<=m M_Delta(T), while D_Delta(T)>=m from the diagonal pairs.",
            "with_one_separated_fibres": "For Delta<1/2, one-separated exact-character fibres already give M_Delta(T)<=P, where P is the number of characters that occur. The local-zero bound cannot improve the factor 1 per fibre.",
            "fixed_modulus": "At one f, P<=|X(f)|<=N(f)<=2Q, so D_Delta(T)<=2mQ.",
            "whole_shell": "Across the selected shell, P<=F_prim(Q)<=sum_{Q<Nf<=2Q}|X(f)|<12Q^2, so D_Delta(T)<12mQ^2.",
            "without_a_separated_thinning": "The zero-assignment hypothesis alone gives M_Delta(T)<=bP L_0(2Q,T+alpha), which is weaker than P when the standard one-separated thinning is available.",
            "subpower_assessment": "If Q=T^vartheta with fixed vartheta>0, the fixed-modulus factor is T^vartheta and the shell factor is T^(2vartheta), up to logarithms. They are subpower only after the additional restriction Q=T^o(1), which is not frozen P7 data.",
        },
        "sharp_detector_geometry_obstruction": {
            "status": "PROVED",
            "statement": "Fibrewise one-separation, per-character unit-window count one, and primitive-family cardinality P permit D_Delta(T)=mP. Therefore those data do not imply any o(mP) local difference bound.",
            "finite_exact_check": obstruction,
            "scope": "The finite construction proves a logical obstruction for the stated counting/separation hypotheses only. It does not manufacture zeros of Hecke L-functions or a detector sample.",
        },
        "existing_joint_l2": {
            "status": "PROVED",
            "unconditional_constant_polynomial_consequence": "Taking c to be supported on the unit ideal gives D_chi(t)=1 for every exact primitive row. The localized P7-2 sampling argument consequently gives only M_Delta(T)<<_K(1+16Q^2)(log(4Q))^A (after choosing one row per distinct time), which is cardinality scale rather than subpower when Q is a fixed power of T.",
            "why_it_does_not_close_the_gate": "The existing joint L2 theorem bounds values of a chosen common polynomial; by itself it supplies no detector threshold that is strong enough to beat the Q or Q^2 family factor.",
        },
        "conditional_common_detector_sampling": {
            "status": "PROVED",
            "hypotheses": [
                "Every exact-character fibre W_chi is 1-separated.",
                "One common ideal coefficient function c(a), supported on N<Na<=2N and retaining the frozen zero extension, satisfies |D_chi(t)|>=V for every detector row, where D_chi(t)=sum c(a)chi(a)(Na)^(-it).",
                "The local source specialization is taken with conductor cutoff 2Q, height 2, and m=0 after translating by the local center u.",
            ],
            "localized_joint_bound": "M_Delta(T)V^2 <<_K L_loc(N,Q)||c||_2^2, where L_loc=(4+(1/2)log^2(2N))(2N+16Q^2)(log(4Q))^A for Delta=1/4.",
            "difference_consequence": "D_Delta(T)<<_K m L_loc(N,Q)||c||_2^2/V^2.",
            "exact_required_detector_strength": "To meet any prescribed difference target D_target, it is sufficient that one common detector has L_loc(N,Q)||c||_2^2/V^2 <<_K D_target/m. For the fixed-ray Thorner cubic budget, D_target is the prior H z_B^2/(Gamma_Th||u_f||_2^2) scale.",
            "finite_exact_bookkeeping_check": joint,
            "current_status": "P7 has no source-checked detector furnishing this common c, uniform V, and range. Hence this is a conditional reduction, not an achieved source-scale D_Delta estimate.",
        },
        "weakest_cross_character_occupancy_input": {
            "status": "PROVED",
            "direct_pairwise_minimum": "The logically weakest input for the present L2-to-discrete route is the target statement D_Delta(T)<=D_target itself (or a different localized theorem that bypasses this route).",
            "weakest_one_point_form": "Among uncoloured one-point height hypotheses, impose OCC_Delta(M): M_Delta(T)=sup_u #(T intersect [u-Delta,u+Delta])<=M. It gives D_Delta(T)<=mM, sharply.",
            "target_form": "For a given D_target, the required occupancy hypothesis is OCC_Delta(D_target/m). The diagonal floor D_Delta>=m shows that no such route can have D_target<m.",
            "labelled_detector_variant": "The stronger labelled condition sup_u #{(f,chi,t) in W: |t-u|<=Delta}<=M also suffices, but unlabelled OCC is weaker because repeated character labels at one height are irrelevant to T.",
            "sharpness": "The finite P-colour/J-block model realizes equality D_Delta=mM, so a universal improvement to this occupancy-to-difference implication is false.",
        },
        "gate_assessment": {
            "status": "OBSERVED",
            "analytic_effect": "This result materially sharpens the diagnosis and records the exact detector-side missing hypothesis, but it does not supply an unconditional source-scale local occupancy bound.",
            "gate_effect": "P7-3 remains open. Even a successful D_Delta input would still require the separate common averaged-block A_0 cubic estimate recorded by the predecessor.",
        },
        "source_integrity": sources,
        "artifact_identity": identities,
        "non_promotion": list(C.NON_PROMOTION),
        "resource_contract": C.RESOURCE_LIMITS,
        "replay": {
            "script": str(SELF.relative_to(ROOT)),
            "script_sha256": digest(SELF),
            "runtime": runtime,
            "write_command": "python3 proof/build_p7_detector_local_occupancy_v1.py --write",
            "check_command": "python3 proof/build_p7_detector_local_occupancy_v1.py --check",
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
    started = time.monotonic_ns()
    data = render(report())
    elapsed = time.monotonic_ns() - started
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "P7 detector occupancy replay exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "P7 detector occupancy replay exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7 detector occupancy artifact")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "P7 detector occupancy artifact mismatch; issue a versioned correction rather than overwrite")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
