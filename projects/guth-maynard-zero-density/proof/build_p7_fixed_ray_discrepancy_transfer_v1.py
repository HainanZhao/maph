#!/usr/bin/env python3
"""Seal the P7 fixed-ray discrepancy transfer and sampling reduction."""
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
from conventions import p7_fixed_ray_discrepancy_transfer_v1 as C
from conventions.proof_runtime_v2 import require_pinned_runtime


OUT = ROOT / "artifacts/p7-fixed-ray-discrepancy-transfer-v1.json"
SELF = Path(__file__)
FILES = {
    "conventions": ROOT / "conventions/p7_fixed_ray_discrepancy_transfer_v1.py",
    "document": ROOT / "docs/p7-fixed-ray-discrepancy-transfer-v1.md",
    "tests": ROOT / "tests/test_p7_fixed_ray_discrepancy_transfer_v1.py",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_difference_multiplicity(times: tuple[Fraction, ...], radius: Fraction) -> int:
    """Exact maximum count in a closed difference window of radius radius."""
    require(radius > 0, "sampling radius must be positive")
    differences = sorted(first - second for first in times for second in times)
    result = 0
    for left in differences:
        result = max(result, sum(left <= right <= left + 2 * radius for right in differences))
    return result


def local_difference_energy(times: tuple[Fraction, ...], tolerance: Fraction) -> int:
    """Exact four-fold local difference energy at the given tolerance."""
    require(tolerance >= 0, "difference-energy tolerance must be nonnegative")
    differences = tuple(first - second for first in times for second in times)
    return sum(abs(first - second) <= tolerance for first in differences for second in differences)


def zero_extension_transfer_check() -> dict[str, object]:
    """A finite check of the delicate equality F_eta=F_eta_star(u_f)."""
    weights = tuple(Fraction(value) for value in C.EXACT_CHECKS["formal_transfer_weights"])
    require(weights == (Fraction(2), Fraction(3)), "frozen formal transfer weights changed")
    # a_0 is coprime to f=pq. a_1 is coprime to the primitive ancestor's
    # conductor d=p, but not to f. The coefficient restriction u_f must
    # remove a_1; merely substituting eta_star into the old polynomial fails.
    primitive_values = (Fraction(1), Fraction(-1))
    complete_zero_extended_values = (Fraction(1), Fraction(0))
    restricted_coefficients = (weights[0], Fraction(0))
    complete_value = sum(weight * value for weight, value in zip(weights, complete_zero_extended_values, strict=True))
    reindexed_value = sum(weight * value for weight, value in zip(restricted_coefficients, primitive_values, strict=True))
    incorrect_value = sum(weight * value for weight, value in zip(weights, primitive_values, strict=True))
    require(complete_value == reindexed_value == 2, "zero-extension reindexing failed")
    require(incorrect_value == -1, "formal model did not expose coefficient restriction")
    return {
        "formal_modulus": "f=pq with primitive ancestor d=p dividing f",
        "ideal_rows": [
            {
                "label": "a_0",
                "coprime_to_f": True,
                "u": str(weights[0]),
                "eta_mod_f": str(complete_zero_extended_values[0]),
                "eta_star_mod_d": str(primitive_values[0]),
                "u_f": str(restricted_coefficients[0]),
            },
            {
                "label": "a_1",
                "coprime_to_d_but_not_f": True,
                "u": str(weights[1]),
                "eta_mod_f": str(complete_zero_extended_values[1]),
                "eta_star_mod_d": str(primitive_values[1]),
                "u_f": str(restricted_coefficients[1]),
            },
        ],
        "complete_zero_extended_F_eta_at_v_zero": str(complete_value),
        "primitive_reindexed_F_eta_star_with_u_f_at_v_zero": str(reindexed_value),
        "incorrect_unrestricted_primitive_expression_at_v_zero": str(incorrect_value),
        "conclusion": "The exact reindexing requires u_f=u*1_(a,f)=1; retaining u would change the polynomial.",
    }


def progression_energy_check() -> dict[str, object]:
    """Exact separated progression showing energy is not a sharp sampler."""
    length = C.EXACT_CHECKS["progression_length"]
    require(isinstance(length, int) and length >= 2, "frozen progression length is invalid")
    radius = Fraction(1, 4)
    times = tuple(Fraction(index) for index in range(length))
    multiplicity = local_difference_multiplicity(times, radius)
    energy = local_difference_energy(times, 2 * radius)
    expected_energy = (2 * length**3 + length) // 3
    require(multiplicity == length, "separated progression local multiplicity changed")
    require(energy == expected_energy, "separated progression local difference energy changed")
    require(multiplicity * multiplicity <= energy, "local multiplicity is not bounded by difference energy")
    return {
        "radius": str(radius),
        "times": [str(value) for value in times],
        "local_difference_multiplicity": multiplicity,
        "local_difference_energy_at_2Delta": energy,
        "exact_formula": "(2m^3+m)/3",
        "formula_value": expected_energy,
        "energy_square_root_over_exact_multiplicity_squared": f"{energy}/{multiplicity * multiplicity}",
        "asymptotic_sampling_loss": "E_diff^(1/2)/D_Delta is asymptotic to a constant times m^(1/2).",
    }


def fibrewise_sharpness_check() -> dict[str, object]:
    """Exact sharpness of D_Delta<=|T|P from fibrewise separation alone."""
    colours = C.EXACT_CHECKS["fibre_colours"]
    blocks = C.EXACT_CHECKS["fibre_blocks"]
    require(isinstance(colours, int) and colours >= 1, "frozen colour count is invalid")
    require(isinstance(blocks, int) and blocks >= 1, "frozen block count is invalid")
    radius = Fraction(1, 4)
    by_colour = {
        colour: tuple(Fraction(3 * block) + Fraction(colour, 8 * colours) for block in range(blocks))
        for colour in range(colours)
    }
    times = tuple(sorted(value for fibre in by_colour.values() for value in fibre))
    sample_size = len(times)
    multiplicity = local_difference_multiplicity(times, radius)
    require(all(fibre[index + 1] - fibre[index] >= 1 for fibre in by_colour.values() for index in range(len(fibre) - 1)), "fibrewise separation failed")
    require(sample_size == blocks * colours, "fibre construction size changed")
    require(multiplicity == sample_size * colours, "fibrewise separation upper bound is not sharp in the frozen model")
    return {
        "radius": str(radius),
        "colours_P": colours,
        "blocks_J": blocks,
        "time_projection_size_m": sample_size,
        "times_by_colour": {str(colour): [str(value) for value in fibre] for colour, fibre in by_colour.items()},
        "minimum_same_colour_gap": 3,
        "local_difference_multiplicity": multiplicity,
        "fibrewise_upper_bound_mP": sample_size * colours,
        "sharpness": "All within-block differences lie in the radius-1/4 window about zero; no better bound follows from fibrewise separation alone.",
    }


def exponent_and_budget_check() -> dict[str, object]:
    """Exact algebra for D-to-delta-to-cubic bookkeeping."""
    ratio = C.EXACT_CHECKS["exponent_loss_ratio"]
    require(isinstance(ratio, int) and ratio > 0, "frozen exponent ratio is invalid")
    root = 1
    while root * root < ratio:
        root += 1
    require(root * root == ratio, "frozen exponent ratio must be a square")
    group_order = C.EXACT_CHECKS["budget_group_order"]
    a3 = C.EXACT_CHECKS["budget_a3"]
    delta = C.EXACT_CHECKS["budget_delta"]
    require(all(isinstance(value, int) and value > 0 for value in (group_order, a3, delta)), "frozen cubic budget parameters are invalid")
    budget = 3 * group_order**3 * delta * (a3 + delta) ** 2
    require(budget == 864, "frozen cubic budget formula changed")
    require(ratio == 16 and root == 4 and root**3 == 64, "D exponent bookkeeping changed")
    return {
        "representative_class_average_parameters": {"H": group_order, "a_3": a3, "delta": delta},
        "exact_budget_3H_cubed_delta_a3_plus_delta_squared": budget,
        "definition": "z_B is the positive root of 3H^3 z(a_3+z)^2=B.",
        "difference_multiplier_ratio": ratio,
        "delta_squared_multiplier": ratio,
        "delta_multiplier": root,
        "perturbative_cubic_multiplier": root,
        "delta_dominant_cubic_multiplier": root**3,
        "exponent_rule": "If D_Delta gains T^kappa, then delta gains T^(kappa/2); the cubic perturbation gains T^(kappa/2) when delta<=a_3 and T^(3kappa/2) when delta>=a_3.",
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
    ray = json.loads((ROOT / C.SOURCES["p7_ray_orthogonality_v1"]["path"]).read_text(encoding="utf-8"))
    require(ray["gate_outcome"] == "PASS_EXACT_PROJECTOR_AND_SCOPED_L2_LARGE_SIEVE", "P7-2 large sieve prerequisite unavailable")
    selected = json.loads((ROOT / C.SOURCES["p7_selected_gram_excess_v1"]["path"]).read_text(encoding="utf-8"))
    parseval = selected["fixed_ray_class_average_compression"]["complete_character_parseval"]
    require("delta_2^2=H^-1" in parseval and "eta in X" in parseval, "predecessor discrepancy identity changed")
    fixed = json.loads((ROOT / C.SOURCES["p7_fixed_ray_colour_v1"]["path"]).read_text(encoding="utf-8"))
    require("delta-separated character fibres" in fixed["coloured_energy"]["fibre_spacing_bound"], "fixed-ray fibre boundary changed")
    norm = json.loads((ROOT / C.SOURCES["p7_norm_status_v3"]["path"]).read_text(encoding="utf-8"))
    require(norm["corrected_claim"]["epistemic_status"] == "PROVED", "P7 norm aggregation status unavailable")
    thorner = (ROOT / C.SOURCES["thorner_2019_rendered"]["path"]).read_text(encoding="utf-8")
    for marker in (
        "Theorem 2.1. Let c(a) be a function on the ideals of",
        "Nq≤Q",
        "where ∗ denotes summing over primitive characters",
        "(N + Q2T nK)(log QT)A",
    ):
        require(marker in thorner, f"pinned Thorner locator unavailable: {marker}")
    zaman = (ROOT / C.SOURCES["zaman_tex"]["path"]).read_text(encoding="utf-8")
    for marker in (
        "extend it to all of $I(\\cO)$ by zero",
        "divides $\\kq$",
        "push-forward of a Hecke character modulo",
    ):
        require(marker in zaman, f"pinned Zaman conductor/extension locator unavailable: {marker}")
    gm = (ROOT / C.SOURCES["guth_maynard_tex"]["path"]).read_text(encoding="utf-8")
    for marker in (
        "Bound for singular values in terms of traces",
        "S_{3} \\lessapprox_\\epsilon T^2 |W|^{3/2}+TN|W|^{1/2}E(W)^{1/2}",
    ):
        require(marker in gm, f"pinned Guth--Maynard locator unavailable: {marker}")
    return rows


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    sources = source_integrity()
    identities = {label: {"path": str(path.relative_to(ROOT)), "sha256": digest(path)} for label, path in FILES.items()}
    identities["builder"] = {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)}
    transfer = zero_extension_transfer_check()
    progression = progression_energy_check()
    fibre = fibrewise_sharpness_check()
    budget = exponent_and_budget_check()
    return {
        "artifact_id": "p7-fixed-ray-discrepancy-transfer-v1",
        "epistemic_status": "PROVED",
        "gate": C.GATE_ID,
        "gate_outcome": "ADVANCED_COMPLETE_TO_PRIMITIVE_L2_TRANSFER_DIFFERENCE_SAMPLING_OPEN",
        "claim_boundary": "Exact fixed-ray complete-to-primitive L2 transfer, local difference sampling reduction, elementary norm-collapsed companion, and sharp fibrewise/difference-energy containment only. No selected primitive Guth--Maynard-shaped cubic estimate, Hecke large-value theorem, density theorem, detector, or prime-ideal theorem is proved.",
        "review_policy": "LIGHTWEIGHT_SOURCE_ALGEBRA_REPLAY; no hostile audit initiated.",
        "complete_to_primitive_transfer": {
            "status": "PROVED",
            "setup": "Fix f, X=Cl(f)^, H=|X|, q=Nf, and u_f(a)=u(a)1_(a,f)=1. Every eta in X has one primitive exact conductor d_eta|f and primitive ancestor eta_star modulo d_eta.",
            "exact_identity": "F_eta(v)=sum_a u(a)eta(a)(Na)^(iv)=sum_a u_f(a)eta_star(a)(Na)^(iv).",
            "zero_extension_reason": "On (a,f)=1 the two character values agree. On the complement u_f vanishes, which exactly reproduces eta modulo f without inflating eta_star.",
            "thorner_reindexing": "The map eta -> (d_eta,eta_star) is injective into Thorner's primitive m=0 family with Nd_eta<=q. Enlarge this nonnegative subcollection to all primitive conductors <=q before applying Theorem 2.1 with ideal cutoff 2N and height B.",
            "continuous_L2": "sum_{eta in X} integral_-B^B |F_eta(v)|^2 dv <<_K (2N+q^2B^2)(log(qB))^A ||u_f||_2^2.",
            "derivative": "The same bound for F_eta' has an additional log^2(2N), since the common coefficient is u_f(a)log Na.",
            "loss_accounting": "No tau(f), 2^omega(f), completion factor, signed primitive-projector triangle inequality, or altered zero extension enters this fixed-modulus L2 transfer.",
            "finite_zero_extension_check": transfer,
        },
        "difference_sampling": {
            "status": "PROVED",
            "definition": "D_Delta(T)=sup_v #{(t,s) in T^2: |t-s-v|<=Delta}, with 0<Delta<1/2 and T=pi_t W subset [0,T_height].",
            "local_sobolev": "|F(x)|^2<=Delta^-1 integral_(x-Delta)^(x+Delta)|F|^2+2Delta integral_(x-Delta)^(x+Delta)|F'|^2.",
            "exact_reduction": "Summing local Sobolev over t-s and using D_Delta yields delta_2^2 <= H^-1 D_Delta times the complete-character continuous L2-plus-derivative mass.",
            "thorner_bound": "delta_2^2 <<_K H^-1 D_Delta Gamma_Th(N,q,B,Delta)||u_f||_2^2, B=T_height+Delta, Gamma_Th=(Delta^-1+2Delta log^2(2N))(2N+q^2B^2)(log(qB))^A.",
            "scope": "This is a completion-free raw L2 discrepancy estimate, not the source-shaped selected cubic estimate.",
        },
        "norm_collapsed_companion": {
            "status": "PROVED",
            "norm_coefficients": "b_eta(n)=sum_{Na=n}u_f(a)eta(a), so F_eta(v)=sum_{N<n<=2N}b_eta(n)n^(iv).",
            "elementary_mean_value": "integral_-B^B |sum b(n)n^(iv)|^2 dv << (B+N(1+log(2N)))sum|b(n)|^2, by expansion plus the harmonic-series Schur bound.",
            "complete_character_norm_bound": "sum_eta sum_n|b_eta(n)|^2 <= H Delta_K(N)||u_f||_2^2, Delta_K(N)=max_{N<n<=2N}a_Q(i)(n)<=max tau(n).",
            "discrepancy_bound": "delta_2^2 << D_Delta Gamma_MV(N,B,Delta)||u_f||_2^2, Gamma_MV=(Delta^-1+2Delta log^2(2N))(B+N(1+log(2N)))Delta_K(N).",
            "cancellation": "The H from complete-character norm aggregation cancels the H^-1 in the exact discrepancy identity.",
            "normalization_scope": "If N<=T_height^C for fixed C, then Delta_K(N)=T_height^o(1) by the already pinned P7-1 divisor normalization.",
            "non_promotion": "This companion remains a raw L2/difference-sampling bound; it supplies neither a selected primitive cubic estimate nor an L-infinity large-value theorem.",
        },
        "per_character_separation": {
            "status": "PROVED",
            "bound": "If each exact-primitive-character fibre is 1-separated and P_f colours can occur, then D_Delta(T)<=|T|P_f for Delta<1/2; in particular D_Delta<=|T|H.",
            "reason": "A length-2Delta interval contains at most one time from each fibre. For fixed t the admissible s values lie in one such interval.",
            "sharpness": "The exact P-colour/J-block construction t_(j,c)=3j+c/(8P) realizes D_(1/4)=|T|P while every fibre is 3-separated.",
            "finite_exact_check": fibre,
            "implication": "Per-character separation permits a fixed-power cross-character clustering loss and cannot by itself make D_Delta subpower.",
        },
        "difference_energy_boundary": {
            "status": "PROVED",
            "definition": "E_diff_(2Delta)(T)=#{(t1,t2,t3,t4): |(t1-t2)-(t3-t4)|<=2Delta}.",
            "universal_relation": "D_Delta(T)^2<=E_diff_(2Delta)(T).",
            "sharp_sampling_message": "The L2-to-discrete transfer weights local continuous mass by an L-infinity difference multiplicity. Energy gives only its square-root upper bound unless a higher-moment/local-distribution input is added.",
            "progression_countercost": "For T={0,...,m-1}, Delta=1/4, D_Delta=m but E_diff_(2Delta)=(2m^3+m)/3. Replacing D by E_diff^(1/2) costs m^(1/2) in delta_2^2 and m^(1/4) in the perturbative cubic error.",
            "coloured_energy_boundary": "The preceding P7 coloured energy has a character-product equation and does not bound this uncoloured difference statistic under the frozen hypotheses.",
            "finite_exact_check": progression,
        },
        "selected_cubic_budget": {
            "status": "PROVED",
            "predecessor_inequality": "G(K_W)<=H^3(G(A_0)+3delta_2(a_3+delta_2)^2), a_3=||A_0||_S3.",
            "budget_root": "For target discrepancy budget B>0, define z_B(a_3,H)>0 by 3H^3 z_B(a_3+z_B)^2=B.",
            "thorner_difference_gate": "The Thorner route meets B if D_Delta is at most a K-constant times H z_B^2/(Gamma_Th||u_f||_2^2).",
            "mean_value_difference_gate": "The norm-collapsed route meets B if D_Delta is at most a constant times z_B^2/(Gamma_MV||u_f||_2^2).",
            "additional_open_input": "A source-shaped bound for the averaged block A_0 is separately required; the displayed D_Delta condition controls only the discrepancy perturbation.",
            "exponent_cost": "If D_Delta=T^kappa relative to a subpower benchmark, delta_2 gains T^(kappa/2). The perturbative cubic term gains T^(kappa/2), while the delta-dominant cubic term gains T^(3kappa/2).",
            "finite_exact_check": budget,
        },
        "scoped_no_go": {
            "status": "PROVED",
            "statement": "Complete-to-primitive reindexing, Thorner L2, the elementary norm-collapsed L2 bound, per-character separation, and an unlocalized difference energy do not imply a Guth--Maynard-shaped selected cubic excess bound under the frozen P7 hypotheses.",
            "reason": "Their strongest deterministic combination is the displayed D_Delta bounds. Fibrewise separation permits the sharp |T|P_f scale, and energy alone can lose an extra square-root multiplicity.",
            "minimal_missing_statistic": "A source-scale local uncoloured difference-sampling bound D_Delta(T)<=D_target, with D_target set by the displayed cubic-budget gate, or a localized higher-moment/ray-class distribution theorem that bypasses this L2 sampling step.",
            "non_overclaim": "This does not rule out additional detector arithmetic, an ideal-class Poisson theorem, or a new higher-moment method. The finite sharpness constructions are not P7 detector or zero examples.",
        },
        "source_integrity": sources,
        "artifact_identity": identities,
        "non_promotion": list(C.NON_PROMOTION),
        "resource_contract": C.RESOURCE_LIMITS,
        "replay": {
            "script": str(SELF.relative_to(ROOT)),
            "script_sha256": digest(SELF),
            "runtime": runtime,
            "write_command": "python3 proof/build_p7_fixed_ray_discrepancy_transfer_v1.py --write",
            "check_command": "python3 proof/build_p7_fixed_ray_discrepancy_transfer_v1.py --check",
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
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "P7 discrepancy replay exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "P7 discrepancy replay exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7 discrepancy artifact")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "P7 discrepancy artifact mismatch; issue a versioned correction rather than overwrite")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
