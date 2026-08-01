#!/usr/bin/env python3
"""Seal the fixed-ray coloured P7-3 reduction and its scoped barriers."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from conventions import p7_fixed_ray_colour_diagonalization_v1 as C
from conventions.proof_runtime_v2 import require_pinned_runtime


OUT = ROOT / "artifacts/p7-fixed-ray-colour-diagonalization-v1.json"
SELF = Path(__file__)
FILES = {
    "conventions": ROOT / "conventions/p7_fixed_ray_colour_diagonalization_v1.py",
    "document": ROOT / "docs/p7-fixed-ray-colour-diagonalization-v1.md",
    "tests": ROOT / "tests/test_p7_fixed_ray_colour_diagonalization_v1.py",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_product(left: list[list[object]], right: list[list[object]]) -> list[list[object]]:
    require(left and right and len(left[0]) == len(right), "invalid matrix dimensions")
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def transpose(matrix: list[list[object]]) -> list[list[object]]:
    require(matrix, "cannot transpose an empty matrix")
    return [[matrix[row][column] for row in range(len(matrix))] for column in range(len(matrix[0]))]


def trace(matrix: list[list[object]]) -> object:
    require(len(matrix) == len(matrix[0]), "trace requires a square matrix")
    return sum(matrix[index][index] for index in range(len(matrix)))


def cyclic_two_character(character: int, group_element: int) -> int:
    """The complete character group of Z/2, represented by signs."""
    return -1 if (character * group_element) % 2 else 1


def fourier_projector_check() -> dict[str, object]:
    """Exact complete-group transform and primitive-subset mixing check."""
    H = C.EXACT_CHECKS["fourier_projector_group_order"]
    require(H == 2, "the frozen exact Fourier check requires H=2")
    fourier = [[1, 1], [1, -1]]
    ideal_classes = (0, 1, 0)
    design = [
        [cyclic_two_character(character, ideal_class) for ideal_class in ideal_classes]
        for character in range(H)
    ]
    transformed = matrix_product(fourier, design)
    require(transformed == [[2, 0, 2], [0, 2, 0]], "complete Fourier transform did not isolate ray classes")
    gram = matrix_product(design, transpose(design))
    transformed_gram_numerator = matrix_product(matrix_product(fourier, gram), transpose(fourier))
    transformed_gram = [[Fraction(value, H) for value in row] for row in transformed_gram_numerator]
    require(transformed_gram == [[4, 0], [0, 2]], "unitary Gram diagonalization failed")
    projector_rows = []
    for selected in ((), (0,), (0, 1)):
        diagonal = [[1 if row == column and row in selected else 0 for column in range(H)] for row in range(H)]
        numerator = matrix_product(matrix_product(fourier, diagonal), transpose(fourier))
        projector = [[Fraction(value, H) for value in row] for row in numerator]
        require(matrix_product(projector, projector) == projector, "Fourier-conjugated selector is not a projection")
        off_diagonal_hs_squared = sum(
            projector[row][column] ** 2
            for row in range(H)
            for column in range(H)
            if row != column
        )
        cardinality = len(selected)
        expected_mixing = Fraction(cardinality * (H - cardinality), H)
        require(off_diagonal_hs_squared == expected_mixing, "projector mixing formula failed")
        projector_rows.append(
            {
                "selected_characters": list(selected),
                "selected_cardinality": cardinality,
                "projector": [[str(value) for value in row] for row in projector],
                "off_diagonal_hs_squared": str(off_diagonal_hs_squared),
                "expected_mixing": str(expected_mixing),
                "ray_class_diagonal": off_diagonal_hs_squared == 0,
            }
        )
    require(
        [row["ray_class_diagonal"] for row in projector_rows] == [True, False, True],
        "proper primitive subset did not exhibit the required Fourier mixing",
    )
    return {
        "ambient_group": "Z/2",
        "unnormalized_fourier_matrix": fourier,
        "ideal_classes": list(ideal_classes),
        "design_matrix": design,
        "unnormalized_transformed_design": transformed,
        "unitary_transformed_gram": [[str(value) for value in row] for row in transformed_gram],
        "projector_rows": projector_rows,
        "proper_subset_mixing": "For the one-character subset, the exact off-diagonal Hilbert--Schmidt square is 1/2.",
    }


def coloured_cubic_check() -> dict[str, object]:
    """Exact labelled-cubic regrouping on a formal Z/2 ray class group."""
    H = C.EXACT_CHECKS["coloured_cubic_group_order"]
    require(H == 2, "the frozen coloured cubic check requires H=2")
    ideal_classes = (0, 1, 0)
    sample = ((0, 0), (1, 0))
    kernel = [
        [
            sum(
                cyclic_two_character(sample[left][0], ideal_class)
                * cyclic_two_character(sample[right][0], ideal_class)
                for ideal_class in ideal_classes
            )
            for right in range(len(sample))
        ]
        for left in range(len(sample))
    ]
    direct_trace = trace(matrix_product(matrix_product(kernel, kernel), kernel))

    def coloured_sum(group_element: int) -> int:
        return sum(cyclic_two_character(character, group_element) for character, _time in sample)

    regrouped = 0
    for class_a in ideal_classes:
        for class_b in ideal_classes:
            for class_c in ideal_classes:
                regrouped += (
                    coloured_sum((class_a - class_c) % H)
                    * coloured_sum((class_b - class_a) % H)
                    * coloured_sum((class_c - class_b) % H)
                )
    require(direct_trace == regrouped == 72, "coloured cubic trace regrouping failed")
    return {
        "ambient_group": "Z/2",
        "ideal_classes": list(ideal_classes),
        "sample": [list(row) for row in sample],
        "kernel": kernel,
        "direct_trace": direct_trace,
        "regrouped_trace": regrouped,
        "identity_mode_explanation": "Only triples with all three ray classes equal survive the full-character coloured sums.",
    }


def exact_coloured_energy(group_order: int, times: tuple[int, ...]) -> int:
    points = tuple((character, time) for character in range(group_order) for time in times)
    result = 0
    for first in points:
        for second in points:
            for third in points:
                for fourth in points:
                    if first[1] + second[1] != third[1] + fourth[1]:
                        continue
                    if (first[0] + second[0] - third[0] - fourth[0]) % group_order == 0:
                        result += 1
    return result


def coloured_energy_check() -> dict[str, object]:
    """Exact Parseval/energy counts and sharp aligned examples."""
    H = C.EXACT_CHECKS["coloured_energy_group_order"]
    length = C.EXACT_CHECKS["coloured_energy_progression_length"]
    progression = tuple(range(1, length + 1))
    progression_energy = exact_coloured_energy(H, progression)
    expected_progression = H**3 * (2 * length**3 + length) // 3
    require(progression_energy == expected_progression, "coloured progression energy formula failed")
    one_height_H = C.EXACT_CHECKS["one_height_group_order"]
    one_height_energy = exact_coloured_energy(one_height_H, (0,))
    require(one_height_energy == one_height_H**3, "one-height coloured energy did not saturate cubic scale")
    return {
        "progression": {
            "group_order": H,
            "times": list(progression),
            "coloured_energy": progression_energy,
            "formula": "H^3(2r^3+r)/3",
            "formula_value": expected_progression,
        },
        "one_height": {
            "group_order": one_height_H,
            "times": [0],
            "coloured_energy": one_height_energy,
            "sample_cardinality": one_height_H,
            "maximal_cubic_scale": one_height_H**3,
        },
        "spacing_bound": "If every character fibre is delta-separated, fixing three points fixes the fourth colour and leaves at most floor(2Delta/delta)+1 fourth times.",
    }


def completion_check() -> dict[str, object]:
    """Exact sharp completion-size and diagonal-cancellation calculation."""
    H = C.EXACT_CHECKS["completion_group_order"]
    scale = C.EXACT_CHECKS["completion_diagonal_scale"]
    selected = tuple((character, 3 * character) for character in range(H))
    selected_count = len(selected)
    selected_times = {time for _character, time in selected}
    completed_count = H * len(selected_times)
    completion_factor = Fraction(completed_count, selected_count)
    require(completion_factor == H, "disjoint character-time support did not realize sharp completion factor")
    complete_sample = tuple((character, time) for character in range(H) for time in (0, 2))
    complete_factor = Fraction(H * len({time for _character, time in complete_sample}), len(complete_sample))
    require(complete_factor == 1, "colour-complete sample has incorrect completion factor")
    selected_trace = selected_count * scale
    selected_cubic_trace = selected_count * scale**3
    selected_excess = selected_cubic_trace - Fraction(selected_trace**3, selected_count**2)
    completed_first_trace = completed_count * scale**3
    completion_excess = completed_first_trace - Fraction(selected_trace**3, selected_count**2)
    expected_completion_excess = (completed_count - selected_count) * scale**3
    require(selected_excess == 0, "diagonal selected model must cancel exactly")
    require(completion_excess == expected_completion_excess, "completion trace loss formula failed")
    return {
        "sharp_disjoint_support": {
            "group_order": H,
            "selected_points": [list(row) for row in selected],
            "selected_count": selected_count,
            "distinct_time_count": len(selected_times),
            "completed_count": completed_count,
            "completion_factor": str(completion_factor),
        },
        "colour_complete_support": {
            "selected_count": len(complete_sample),
            "distinct_time_count": len({time for _character, time in complete_sample}),
            "completion_factor": str(complete_factor),
        },
        "diagonal_trace_model": {
            "scale": scale,
            "selected_cubic_excess": str(selected_excess),
            "completed_upper_trace_minus_selected_diagonal": str(completion_excess),
            "expected_uncancelled_diagonal": str(expected_completion_excess),
        },
    }


def gaussian_ideal_count_up_to(bound: int) -> int:
    """Count nonzero Gaussian-integer unit orbits in a finite disk exactly."""
    radius = math.isqrt(bound)
    generators = 0
    for real_part in range(-radius, radius + 1):
        for imaginary_part in range(-radius, radius + 1):
            if real_part == 0 and imaginary_part == 0:
                continue
            if real_part * real_part + imaginary_part * imaginary_part <= bound:
                generators += 1
    require(generators % 4 == 0, "nonzero Gaussian generators did not split into unit orbits")
    return generators // 4


def shell_and_fallback_check() -> dict[str, object]:
    """Exact elementary shell accounting and formal fibrewise normalization."""
    shell_rows = []
    for Q in C.EXACT_CHECKS["shell_Q_values"]:
        ideal_count = gaussian_ideal_count_up_to(2 * Q)
        require(ideal_count < 6 * Q, "Gaussian ideal lattice bound failed")
        complete_character_upper = 2 * Q * ideal_count
        require(complete_character_upper < 12 * Q * Q, "dyadic complete-character bound failed")
        shell_rows.append(
            {
                "Q": Q,
                "ideals_norm_at_most_2Q": ideal_count,
                "strict_6Q_bound": 6 * Q,
                "complete_character_upper": complete_character_upper,
                "strict_12Q_squared_bound": 12 * Q * Q,
            }
        )
    powers = list(C.EXACT_CHECKS["fallback_threshold_powers"])
    require(powers == [2, 4, 4], "frozen P7-1/Guth--Maynard threshold powers changed")
    # The following two homogeneous inequalities are checked without square
    # roots by squaring their nonnegative sides.
    R_values = (1, 4, 9)
    E_values = (4, 9, 16)
    sum_r_three_halves = sum(value * math.isqrt(value) for value in R_values)
    require(sum_r_three_halves**2 <= sum(R_values) ** 3, "shell cubic-cardinality inequality failed")
    sum_root_re = sum(math.isqrt(r_value * e_value) for r_value, e_value in zip(R_values, E_values, strict=True))
    require(sum_root_re**2 <= sum(R_values) * sum(E_values), "shell Cauchy--Schwarz inequality failed")
    return {
        "ideal_shell_rows": shell_rows,
        "fixed_modulus_bound": "|X(f)|<=N(f)<=2Q",
        "total_complete_character_bound": "sum_{Q<Nf<=2Q}|X(f)|<12Q^2",
        "fallback_normalization": {
            "threshold_powers": powers,
            "multipliers_after_V_to_V/Delta_N": ["Delta_N^2", "Delta_N^4", "Delta_N^4"],
            "absorption_hypothesis": "N<=T^C for fixed C",
            "family_multiplier": "F_prim(Q)<=sum_f|X(f)|<12Q^2",
        },
        "conditional_shell_summation_check": {
            "R_values": list(R_values),
            "E_values": list(E_values),
            "sum_R_three_halves": sum_r_three_halves,
            "R_total": sum(R_values),
            "sum_sqrt_RE": sum_root_re,
            "E_total": sum(E_values),
        },
    }


def source_integrity() -> dict[str, object]:
    rows: dict[str, object] = {}
    for label, row in C.SOURCES.items():
        path = ROOT / row["path"]
        require(path.is_file() and digest(path) == row["sha256"], f"pinned source mismatch: {label}")
        rows[label] = dict(row)
    prereg = json.loads((ROOT / C.SOURCES["p7_preregistration_v2"]["path"]).read_text(encoding="utf-8"))
    gate = next(item for item in prereg["gates"] if item["id"] == C.GATE_ID)
    require(gate["state"] == "UNEXECUTED", "frozen P7-3 preregistration state changed")
    p7_2 = json.loads((ROOT / C.SOURCES["p7_ray_orthogonality_v1"]["path"]).read_text(encoding="utf-8"))
    require(p7_2["gate_outcome"] == "PASS_EXACT_PROJECTOR_AND_SCOPED_L2_LARGE_SIEVE", "P7-2 prerequisite missing")
    p7_3 = json.loads((ROOT / C.SOURCES["p7_common_ideal_cubic_v1"]["path"]).read_text(encoding="utf-8"))
    require(p7_3["gate_outcome"] == "PASS_EXACT_IDEAL_IDENTITIES_CONTAINED_COMMON_SAMPLE_CUBIC_OPEN", "P7-3 predecessor boundary changed")
    norm = json.loads((ROOT / C.SOURCES["p7_norm_status_v3"]["path"]).read_text(encoding="utf-8"))
    require(norm["corrected_claim"]["epistemic_status"] == "PROVED", "P7-1 normalization status missing")
    require(norm["corrected_claim"]["hypothesis"] == "N<=T^C for a fixed C", "P7-1 normalization hypothesis changed")
    gm = (ROOT / C.SOURCES["guth_maynard_tex"]["path"]).read_text(encoding="utf-8")
    for marker in (
        "\\begin{lmm}[Large values of Dirichlet polynomials controlled by singular values]",
        "\\label{eq:EnergyDef}",
        "S_{3} \\lessapprox_\\epsilon T^2 |W|^{3/2}+TN|W|^{1/2}E(W)^{1/2}",
        "energy is essentially maximal",
        "N^{18/5}V^{-4}",
        "TN^{12/5}V^{-4}",
    ):
        require(marker in gm, f"pinned Guth--Maynard locator unavailable: {marker}")
    return rows


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    source_rows = source_integrity()
    identities = {label: {"path": str(path.relative_to(ROOT)), "sha256": digest(path)} for label, path in FILES.items()}
    identities["builder"] = {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)}
    fourier = fourier_projector_check()
    cubic = coloured_cubic_check()
    energy = coloured_energy_check()
    completion = completion_check()
    shell = shell_and_fallback_check()
    return {
        "artifact_id": "p7-fixed-ray-colour-diagonalization-v1",
        "epistemic_status": "PROVED",
        "gate": C.GATE_ID,
        "gate_outcome": "CONTAINED_FIXED_MODULUS_CHARACTER_AWARE_REDUCTION_AND_COMPLETION_LOSS",
        "claim_boundary": "Exact fixed-modulus coloured Fourier/Gram/cubic identities, sharp completion and fibre-spacing barriers, elementary dyadic-shell accounting, and a conditional character-by-character fallback only. No coloured primitive cubic estimate, Hecke large-value theorem, zero-density theorem, detector, or prime-ideal theorem is proved.",
        "review_policy": "LIGHTWEIGHT_SOURCE_ALGEBRA_REPLAY; no hostile audit initiated.",
        "fixed_modulus_coloured_cubic": {
            "status": "PROVED",
            "sample": "W is a finite subset of X(f) times R, with the selected P7 primitive sample embedded in the complete ambient X(f).",
            "coloured_sum": "R_W(g;v)=sum_{(chi,t) in W} chi(g)v^(it).",
            "exact_trace": "tr(K^3)=sum_{a,b,c}u(a)u(b)u(c) R_W([a][c]^-1;Na/Nc) R_W([b][a]^-1;Nb/Na) R_W([c][b]^-1;Nc/Nb).",
            "label_loss": "None in the exact regrouping: all character labels are summed into the three coloured Fourier sums.",
            "finite_exact_check": cubic,
        },
        "complete_group_diagonalization": {
            "status": "PROVED",
            "unitary_transform": "U_(g,chi)=H^(-1/2) conjugate(chi(g)); (UM)_((g,t),a)=H^(1/2)c(a)w(Na/N)(Na)^(it)1_[a]=g.",
            "full_gram": "U(MM*)U*=H direct_sum_{g in G} C_g.",
            "selected_projection": "B=UP_WU* has B_((g,t),(h,s))=1_(t=s)H^-1 sum_{chi in A_t}chi(hg^-1).",
            "selected_trace": "tr(K_W^3)=H^3 tr([B(direct_sum_g C_g)B]^3).",
            "positivity": "B is an orthogonal projection and B(direct_sum_g C_g)B is positive semidefinite.",
            "diagonalization_criterion": "B is ray-class diagonal exactly when every A_t is empty or all of X(f).",
            "complete_sample_no_loss": "For W=X(f)xS and equal ray-class mass N/H, the diagonal cubic scale is H^3*H*|S|*(N/H)^3=|W|N^3.",
            "finite_exact_check": fourier,
        },
        "coloured_energy": {
            "status": "PROVED",
            "exact_identity": "E_col^=(W)=H^-1 sum_{g in G} integral_0^1 |sum_{(chi,t) in W}chi(g)e(t theta)|^4 dtheta.",
            "fibre_spacing_bound": "E_col^Delta(W)<= (floor(2Delta/delta)+1)|W|^3 for delta-separated character fibres.",
            "sharpness": "W=X(f)x{0} has E_col^=|W|^3 although every fibre has one point.",
            "critical_scope": "A coloured-energy-only substitution into the pinned refined S3 bound has maximal term TN|W|^2 on this permitted scale; this is not a P7 density-exponent calculation.",
            "finite_exact_check": energy,
        },
        "completion_barrier": {
            "status": "PROVED",
            "completion_factor": "kappa_f(W)=|X(f)||pi_t W|/|W| in [1,|X(f)|].",
            "sharp_example": "One globally separated point at a distinct time for each of H characters has kappa_f(W)=H.",
            "trace_comparison": "For A=N I_m and a selected R-row compression with m=kappa R, the selected cubic excess is zero but replacing its cubic trace by tr(A^3) leaves (kappa-1)RN^3.",
            "implication": "Trace positivity/completion alone does not preserve the Guth--Maynard selected-side diagonal cancellation unless kappa_f(W)=T^o(1) or a new selected-side estimate is proved.",
            "finite_exact_check": completion,
        },
        "dyadic_shell": {
            "status": "PROVED",
            "fixed_group_bound": "|X(f)|<=N(f)<=2Q.",
            "ideal_count_bound": "For Q>=8, fewer than 6Q integral ideals of Z[i] have norm at most 2Q.",
            "complete_character_bound": "sum_{Q<Nf<=2Q}|X(f)|<12Q^2.",
            "completion_loss": "Fixed-modulus full-character completion can cost up to 2Q; a raw global uncoloured separation extraction can face O(Q^2) labelled fibres.",
            "cross_conductor_term": "X_cross(W;c)=tr(K^3)-sum_f tr(K_{W_f}^3) is generally signed and has no common ray-class Fourier group.",
            "finite_exact_check": shell["ideal_shell_rows"],
        },
        "fixed_character_fallback": {
            "status": "PROVED",
            "hypotheses": [
                "For every selected primitive chi, W_chi is 1-separated in [0,T] and |D_chi(t)|>=V.",
                "D_chi(t)=sum_{N<n<=2N}A_chi(n)n^(it), with the P7 zero extension and one common dyadic N.",
                "N<=T^C for a fixed C, so the P7-1 divisor normalization is T^o(1).",
            ],
            "normalization": "b_chi,n=A_chi(n)/Delta_N, Delta_N=max_{N<n<=2N}tau(n), has |b_chi,n|<=1 and changes V to V/Delta_N.",
            "per_character_bound": "T^o(1)(N^2V^-2+N^(18/5)V^-4+TN^(12/5)V^-4) after the stated N<=T^C absorption.",
            "summed_bound": "F_prim(Q)T^o(1)(N^2V^-2+N^(18/5)V^-4+TN^(12/5)V^-4), with F_prim(Q)<=sum_f|X(f)|<12Q^2.",
            "exact_loss_boundary": "F_prim(Q) is unavoidable in this direct nonnegative character-by-character summation. The 12Q^2 bound is not a lower bound for all joint methods.",
            "conductor_height_boundary": "If Q=T^vartheta, the crude uniform bound carries T^(2vartheta); it is subpower only under an additional Q=T^o(1) restriction.",
            "non_promotion": "This is an automatic P7-1 plus Guth--Maynard application, not a new Hecke theorem; P7 detector and density implications remain unproved.",
            "finite_exact_check": shell["fallback_normalization"],
        },
        "conditional_shell_reduction": {
            "epistemic_status": "PROVED",
            "hypotheses": [
                "A selected-side primitive coloured fixed-modulus S3 estimate of source shape.",
                "A same-scale control of the signed cross-conductor cubic contribution.",
            ],
            "conclusion": "For R=sum_f R_f and E=sum_f E_f, sum_f R_f^(3/2)<=R^(3/2) and sum_f R_f^(1/2)E_f^(1/2)<=R^(1/2)E^(1/2); no separate number-of-moduli factor is forced at this formal homogeneous S3 summation step.",
            "finite_exact_check": shell["conditional_shell_summation_check"],
        },
        "missing_analytic_statistic": {
            "epistemic_status": "CONJECTURED",
            "selected_side_excess": "G_f(W;c)=tr(K_{W_f}^3)-[tr(K_{W_f})]^3/|W_f|^2.",
            "cross_conductor_excess": "X_cross(W;c)=tr(K^3)-sum_f tr(K_{W_f}^3).",
            "required_bound": "A colour-aware affine/Poisson estimate must control both quantities from coloured energy, local cross-character height information, and the exact primitive projector without a kappa completion or signed-projector triangle loss.",
            "not_supplied_by_pinned_sources": "Neither the integer Guth--Maynard theorem nor the P7-2 common-ideal L2 Hecke large sieve supplies the required selected-side primitive cubic estimate.",
        },
        "source_integrity": source_rows,
        "artifact_identity": identities,
        "non_promotion": list(C.NON_PROMOTION),
        "resource_contract": C.RESOURCE_LIMITS,
        "replay": {
            "script": str(SELF.relative_to(ROOT)),
            "script_sha256": digest(SELF),
            "runtime": runtime,
            "write_command": "python3 proof/build_p7_fixed_ray_colour_diagonalization_v1.py --write",
            "check_command": "python3 proof/build_p7_fixed_ray_colour_diagonalization_v1.py --check",
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
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "P7 fixed-ray replay exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "P7 fixed-ray replay exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7 fixed-ray artifact")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "P7 fixed-ray artifact mismatch; issue a versioned correction rather than overwrite")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
