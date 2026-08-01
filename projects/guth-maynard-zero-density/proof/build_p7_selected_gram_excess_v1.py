#!/usr/bin/env python3
"""Seal P7 selected-Gram cubic-excess and conductor-pinching reductions."""
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
from conventions import p7_selected_gram_excess_v1 as C
from conventions.proof_runtime_v2 import require_pinned_runtime


OUT = ROOT / "artifacts/p7-selected-gram-excess-v1.json"
SELF = Path(__file__)
FILES = {
    "conventions": ROOT / "conventions/p7_selected_gram_excess_v1.py",
    "document": ROOT / "docs/p7-selected-gram-excess-v1.md",
    "tests": ROOT / "tests/test_p7_selected_gram_excess_v1.py",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def zero_matrix(rows: int, columns: int) -> list[list[Fraction]]:
    return [[Fraction(0) for _column in range(columns)] for _row in range(rows)]


def identity(size: int) -> list[list[Fraction]]:
    return [[Fraction(int(row == column)) for column in range(size)] for row in range(size)]


def diagonal(entries: tuple[int, ...]) -> list[list[Fraction]]:
    return [[Fraction(entries[row] if row == column else 0) for column in range(len(entries))] for row in range(len(entries))]


def all_ones(size: int) -> list[list[Fraction]]:
    return [[Fraction(1) for _column in range(size)] for _row in range(size)]


def matrix_add(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    require(len(left) == len(right) and len(left[0]) == len(right[0]), "matrix addition dimensions disagree")
    return [[left[row][column] + right[row][column] for column in range(len(left[0]))] for row in range(len(left))]


def matrix_subtract(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    require(len(left) == len(right) and len(left[0]) == len(right[0]), "matrix subtraction dimensions disagree")
    return [[left[row][column] - right[row][column] for column in range(len(left[0]))] for row in range(len(left))]


def matrix_scale(scalar: Fraction, matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[scalar * entry for entry in row] for row in matrix]


def matrix_product(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    require(left and right and len(left[0]) == len(right), "matrix product dimensions disagree")
    return [
        [sum(left[row][middle] * right[middle][column] for middle in range(len(right))) for column in range(len(right[0]))]
        for row in range(len(left))
    ]


def matrix_trace(matrix: list[list[Fraction]]) -> Fraction:
    require(matrix and len(matrix) == len(matrix[0]), "trace needs a nonempty square matrix")
    return sum(matrix[index][index] for index in range(len(matrix)))


def cube_trace(matrix: list[list[Fraction]]) -> Fraction:
    return matrix_trace(matrix_product(matrix_product(matrix, matrix), matrix))


def principal(matrix: list[list[Fraction]], indices: tuple[int, ...]) -> list[list[Fraction]]:
    return [[matrix[row][column] for column in indices] for row in indices]


def block_diagonal(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    require(len(left) == len(left[0]) and len(right) == len(right[0]), "block diagonal needs square blocks")
    left_size = len(left)
    right_size = len(right)
    result = zero_matrix(left_size + right_size, left_size + right_size)
    for row in range(left_size):
        for column in range(left_size):
            result[row][column] = left[row][column]
    for row in range(right_size):
        for column in range(right_size):
            result[left_size + row][left_size + column] = right[row][column]
    return result


def excess(matrix: list[list[Fraction]]) -> Fraction:
    size = len(matrix)
    require(size > 0 and size == len(matrix[0]), "excess needs a nonempty square matrix")
    total_trace = matrix_trace(matrix)
    return cube_trace(matrix) - total_trace**3 / (size**2)


def variance_two(matrix: list[list[Fraction]]) -> Fraction:
    size = len(matrix)
    total_trace = matrix_trace(matrix)
    return matrix_trace(matrix_product(matrix, matrix)) - total_trace**2 / size


def coloured_energy(points: tuple[tuple[int, int], ...], group_order: int) -> int:
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


def psd_excess_check() -> dict[str, object]:
    """Exact eigenvalue identity and its sharp universal factor-three family."""
    n = C.EXACT_CHECKS["excess_sharpness_n"]
    require(isinstance(n, int) and n >= 1, "frozen sharpness parameter is invalid")
    matrix = diagonal((n + 1, n - 1))
    mean = matrix_trace(matrix) / 2
    variance = variance_two(matrix)
    value = excess(matrix)
    operator_norm = Fraction(n + 1)
    exact_weighted = sum((eigenvalue - mean) ** 2 * (eigenvalue + 2 * mean) for eigenvalue in (n + 1, n - 1))
    upper = 3 * operator_norm * variance
    require(mean == n, "sharpness mean changed")
    require(variance == 2, "sharpness variance changed")
    require(value == exact_weighted == 6 * n, "centred cubic identity failed")
    require(value <= upper and value / upper == Fraction(n, n + 1), "factor-three sharpness ratio failed")
    return {
        "family": "K_n=diag(n+1,n-1), n>=1",
        "checked_n": n,
        "mean": str(mean),
        "variance_two": str(variance),
        "cubic_excess": str(value),
        "three_lambda_variance": str(upper),
        "ratio": str(value / upper),
        "asymptotic_sharpness": "ratio=n/(n+1), which tends to 1",
    }


def conductor_pinching_check() -> dict[str, object]:
    """Exact sharp upper example for aggregate exact-conductor pinching."""
    size = C.EXACT_CHECKS["pinching_rank_one_size"]
    require(isinstance(size, int) and size >= 2, "frozen pinching matrix size is invalid")
    matrix = all_ones(size)
    total_cubic = cube_trace(matrix)
    block_cubic_sum = Fraction(size)
    cross = total_cubic - block_cubic_sum
    global_excess = excess(matrix)
    variance = variance_two(matrix)
    operator_norm = Fraction(size)
    raw_l2_upper = operator_norm * matrix_trace(matrix) - matrix_trace(matrix) ** 2 / size
    require(total_cubic == size**3, "rank-one cubic trace changed")
    require(cross == size**3 - size, "cross-conductor difference changed")
    require(cross == global_excess, "pinching upper bound is not sharp on singleton blocks")
    require(variance == raw_l2_upper == size**2 - size, "rank-one raw L2 variance saturation failed")
    return {
        "matrix": "J_R with one selected row in each conductor block",
        "R": size,
        "trace_cubed": str(total_cubic),
        "sum_fixed_conductor_cubes": str(block_cubic_sum),
        "aggregate_cross_conductor_term": str(cross),
        "global_selected_excess": str(global_excess),
        "variance_two": str(variance),
        "raw_l2_variance_upper": str(raw_l2_upper),
        "sharpness": "X_cross=G(K)=R^3-R; the upper inequality is exact.",
    }


def hadamard_by_time() -> list[list[Fraction]]:
    """Unnormalised (Z/2 Fourier) tensor I_time in character-time order."""
    return [
        [Fraction(1), Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(-1), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(-1)],
    ]


def selected_projection(indices: tuple[int, ...]) -> list[list[Fraction]]:
    return [[Fraction(int(row == column and row in indices)) for column in range(4)] for row in range(4)]


def class_average_check() -> dict[str, object]:
    """Exact completion-free class-average selector compression check."""
    require(C.EXACT_CHECKS["class_average_group_order"] == 2, "frozen class-average group changed")
    indices = C.EXACT_CHECKS["class_average_selected_indices"]
    require(indices == (0, 3), "frozen class-average selector changed")
    c_zero = [[Fraction(5), Fraction(2)], [Fraction(2), Fraction(2)]]
    c_one = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(4)]]
    # Principal minors certify the two displayed real symmetric blocks are PSD.
    require(c_zero[0][0] >= 0 and c_zero[1][1] >= 0 and c_zero[0][0] * c_zero[1][1] - c_zero[0][1] ** 2 >= 0, "C_0 is not PSD")
    require(c_one[0][0] >= 0 and c_one[1][1] >= 0 and c_one[0][0] * c_one[1][1] - c_one[0][1] ** 2 >= 0, "C_1 is not PSD")
    c_bar = matrix_scale(Fraction(1, 2), matrix_add(c_zero, c_one))
    delta_zero = matrix_subtract(c_zero, c_bar)
    delta_one = matrix_subtract(c_one, c_bar)
    require(matrix_add(delta_zero, delta_one) == zero_matrix(2, 2), "ray-class discrepancies do not average to zero")
    complete_blocks = block_diagonal(c_zero, c_one)
    average_blocks = block_diagonal(c_bar, c_bar)
    hadamard = hadamard_by_time()
    transformed = matrix_scale(Fraction(1, 2), matrix_product(matrix_product(hadamard, complete_blocks), hadamard))
    selector = selected_projection(indices)
    selected_full = matrix_product(matrix_product(selector, transformed), selector)
    average_full = matrix_product(matrix_product(selector, average_blocks), selector)
    selected = principal(selected_full, indices)
    averaged = principal(average_full, indices)
    gram = matrix_scale(Fraction(2), selected)
    averaged_gram = matrix_scale(Fraction(2), averaged)
    trace_difference = matrix_trace(selected) - matrix_trace(averaged)
    cubic_difference = cube_trace(selected) - cube_trace(averaged)
    discrepancy_hs_squared = sum(entry * entry for row in delta_zero for entry in row) + sum(entry * entry for row in delta_one for entry in row)
    nontrivial_complete_fourier_block = matrix_subtract(c_zero, c_one)
    complete_fourier_hs_squared = sum(entry * entry for row in nontrivial_complete_fourier_block for entry in row)
    points = ((0, 0), (1, 1))
    energy = coloured_energy(points, 2)
    require(c_bar == [[Fraction(3), Fraction(1)], [Fraction(1), Fraction(3)]], "class average changed")
    require(selected == [[Fraction(3), Fraction(1)], [Fraction(1), Fraction(3)]], "selected exact Gram reduction changed")
    require(averaged == [[Fraction(3), Fraction(0)], [Fraction(0), Fraction(3)]], "averaged selector split changed")
    require(trace_difference == 0 and cubic_difference == 18, "trace-preserving class-average comparison failed")
    require(excess(gram) == 144 and excess(averaged_gram) == 0, "selected excess comparison failed")
    require(discrepancy_hs_squared == 14, "ray-class Hilbert--Schmidt discrepancy changed")
    require(Fraction(complete_fourier_hs_squared, 2) == discrepancy_hs_squared, "finite ray-class Parseval discrepancy identity failed")
    require(energy == 6 and energy == 2 * len(points) ** 2 - len(points), "minimal coloured-energy witness failed")
    # Here ||A-A_0||_S3 <= delta_2 < 4 and ||A_0||_S3 < 4, so the
    # exact perturbation bound has the purely rational coarse upper 768.
    perturbation_upper = 3 * 4 * (4 + 4) ** 2
    require(abs(cubic_difference) <= perturbation_upper, "coarse exact perturbation check failed")
    return {
        "ambient_group": "Z/2",
        "class_blocks": {
            "C_0": [[str(entry) for entry in row] for row in c_zero],
            "C_1": [[str(entry) for entry in row] for row in c_one],
            "C_bar": [[str(entry) for entry in row] for row in c_bar],
        },
        "selected_points": [[character, height] for character, height in points],
        "local_height_multiplicity": 1,
        "coloured_energy": energy,
        "minimal_energy_2R_squared_minus_R": 2 * len(points) ** 2 - len(points),
        "selected_A": [[str(entry) for entry in row] for row in selected],
        "averaged_A_0": [[str(entry) for entry in row] for row in averaged],
        "trace_A_equals_trace_A_0": str(matrix_trace(selected)),
        "trace_cubic_difference_A_minus_A_0": str(cubic_difference),
        "selected_gram_excess": str(excess(gram)),
        "averaged_gram_excess": str(excess(averaged_gram)),
        "ray_class_delta_2_squared": str(discrepancy_hs_squared),
        "complete_character_fourier_hs_squared": str(complete_fourier_hs_squared),
        "parseval_delta_2_squared": "H^-1 times the nontrivial complete-character Frobenius square = 28/2 = 14",
        "coarse_exact_perturbation_upper": perturbation_upper,
        "conclusion": "With no same-height collision and minimal coloured energy, nonzero ray-class discrepancy still creates selected cubic excess.",
    }


def source_integrity() -> dict[str, object]:
    rows: dict[str, object] = {}
    for label, row in C.SOURCES.items():
        path = ROOT / row["path"]
        require(path.is_file() and digest(path) == row["sha256"], f"pinned source mismatch: {label}")
        rows[label] = dict(row)
    preregistration = json.loads((ROOT / C.SOURCES["p7_preregistration_v2"]["path"]).read_text(encoding="utf-8"))
    gate = next(item for item in preregistration["gates"] if item["id"] == C.GATE_ID)
    require(gate["state"] == "UNEXECUTED", "immutable P7-3 preregistration state changed")
    ray = json.loads((ROOT / C.SOURCES["p7_ray_orthogonality_v1"]["path"]).read_text(encoding="utf-8"))
    require(ray["gate_outcome"] == "PASS_EXACT_PROJECTOR_AND_SCOPED_L2_LARGE_SIEVE", "P7-2 source gate is unavailable")
    fixed = json.loads((ROOT / C.SOURCES["p7_fixed_ray_colour_diagonalization_v1"]["path"]).read_text(encoding="utf-8"))
    require("generally signed" in fixed["dyadic_shell"]["cross_conductor_term"], "predecessor correction target changed")
    common = json.loads((ROOT / C.SOURCES["p7_common_ideal_cubic_v3"]["path"]).read_text(encoding="utf-8"))
    require(common["epistemic_status"] == "OBSERVED", "P7 common-ideal correction chain changed")
    guth_maynard = (ROOT / C.SOURCES["guth_maynard_tex"]["path"]).read_text(encoding="utf-8")
    for marker in (
        "Bound for singular values in terms of traces",
        "S_{3} \\lessapprox_\\epsilon T^2 |W|^{3/2}+TN|W|^{1/2}E(W)^{1/2}",
        "energy is essentially maximal",
    ):
        require(marker in guth_maynard, f"pinned Guth--Maynard locator unavailable: {marker}")
    thorner = (ROOT / C.SOURCES["thorner_2019_rendered"]["path"]).read_text(encoding="utf-8")
    for marker in (
        "Theorem 2.1. Let c(a) be a function on the ideals of",
        "(N + Q2T nK)(log QT)A",
    ):
        require(marker in thorner, f"pinned Thorner locator unavailable: {marker}")
    return rows


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    sources = source_integrity()
    identities = {label: {"path": str(path.relative_to(ROOT)), "sha256": digest(path)} for label, path in FILES.items()}
    identities["builder"] = {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)}
    psd = psd_excess_check()
    pinching = conductor_pinching_check()
    class_average = class_average_check()
    return {
        "artifact_id": "p7-selected-gram-excess-v1",
        "epistemic_status": "PROVED",
        "gate": C.GATE_ID,
        "gate_outcome": "ADVANCED_SELECTED_GRAM_REDUCTION_CROSS_CONDUCTOR_CONTAINED",
        "claim_boundary": "Exact PSD selected-excess and conductor-pinching inequalities, fixed-ray class-average compression, and a raw-L2 consequence only. No selected primitive Guth--Maynard-shaped cubic estimate, Hecke large-value theorem, density theorem, detector, or prime-ideal theorem is proved.",
        "review_policy": "LIGHTWEIGHT_SOURCE_ALGEBRA_REPLAY; no hostile audit initiated.",
        "correction": {
            "predecessor": {
                "path": C.SOURCES["p7_fixed_ray_colour_diagonalization_v1"]["path"],
                "sha256": C.SOURCES["p7_fixed_ray_colour_diagonalization_v1"]["sha256"],
            },
            "defect": "The predecessor described the aggregate X_cross=tr(K^3)-sum_f tr(K_f^3) as generally signed. Individual block-expansion summands can be signed, but the aggregate is nonnegative for every PSD K.",
            "cause": "The aggregate trace difference was not subjected to PSD block pinching before it was described.",
            "repair": "PSD pinching proves 0<=X_cross<=G(K); the upper bound retains the global selected diagonal subtraction.",
            "affected_claim": "Only the aggregate-sign wording and the need for a separately signed cross-conductor triangle estimate are corrected. The lack of a common ray group and the need for a quantitative global Gram bound remain.",
            "rerun": "The exact Fraction-only finite checks below and the focused builder/test replay verify the correction.",
        },
        "selected_psd_excess": {
            "status": "PROVED",
            "definition": "G(K)=tr(K^3)-tr(K)^3/R^2, mu=tr(K)/R, V2(K)=tr(K^2)-tr(K)^2/R, Lambda(K)=||K||_op.",
            "exact_identity": "G(K)=sum_j (lambda_j-mu)^2(lambda_j+2mu).",
            "bound": "0<=G(K)<=(Lambda(K)+2mu)V2(K)<=3Lambda(K)V2(K).",
            "meaning": "The tr(K)^3/R^2 term is the selected-side diagonal cancellation; no character completion is used.",
            "finite_sharpness_check": psd,
        },
        "cross_conductor_pinching": {
            "status": "PROVED",
            "definition": "X_cross(K)=tr(K^3)-sum_f tr(K_f^3), with K_f the exact-conductor principal blocks.",
            "lower_bound": "0<=X_cross by Schatten-3 contractivity of the block pinching E(K)=direct_sum_f K_f.",
            "upper_bound": "X_cross<=G(K), because X_cross=G(K)-sum_f G(K_f)+R[(sum_f p_f mu_f)^3-sum_f p_f mu_f^3] and Jensen makes the bracket nonpositive.",
            "individual_term_warning": "Individual expansion terms with several conductor labels can be signed; this does not make the aggregate X_cross signed.",
            "finite_sharpness_check": pinching,
        },
        "fixed_ray_class_average_compression": {
            "status": "PROVED",
            "setup": "At one modulus f, U(MM*)U*=H direct_sum_{g in Cl(f)} C_g. P_W is the exact primitive selected-row projector; no projector signs or zero extensions are altered.",
            "definitions": "C_bar=H^-1 sum_g C_g, Delta_g=C_g-C_bar, A=P_W U^*(direct_sum_g C_g)U P_W, A_0=P_W(I_X tensor C_bar)P_W, delta_3=(sum_g||Delta_g||_S3^3)^(1/3).",
            "trace_preservation": "tr(A)=tr(A_0), since the ray-class diagonal of U P_W U^* is |A_t|/H and sum_g Delta_g=0.",
            "selection_decomposition": "A_0=direct_sum_{chi in X} C_bar restricted to T_chi; it contains no completion factor kappa_f(W).",
            "perturbation": "|tr(A^3)-tr(A_0^3)|<=3delta_3(||A_0||_S3+delta_3)^2, hence G(K_W)<=H^3[G(A_0)+3delta_3(||A_0||_S3+delta_3)^2].",
            "checkable_stronger_discrepancy": "delta_3<=(sum_g||C_g-C_bar||_S2^2)^(1/2)=delta_2.",
            "complete_character_parseval": "delta_2^2=H^-1 sum_{eta in X, eta!=1} sum_{t,s in T}|sum_{(a,f)=1}u(a)eta(a)(Na)^(i(t-s))|^2.",
            "difference_multiset_boundary": "Current fibre separation/local height data do not control the uncoloured difference multiset T-T, and coloured energy has a different colour equation. Applying the P7-2 primitive L2 theorem to this complete-character identity would additionally require conductor-safe complete-to-primitive transfer and difference sampling.",
            "missing_input": "A source-scale ideal-class distribution/Poisson estimate for delta_3 or delta_2, plus a common averaged-block cubic estimate.",
            "finite_exact_check": class_average,
        },
        "sampled_l2_consequence": {
            "status": "PROVED",
            "hypotheses": [
                "W lies in [0,T] and each fixed primitive-character fibre is 1-separated.",
                "The P7-2 Thorner Theorem 2.1 specialization is used with ideal cutoff 2N, height T+1, K=Q(i), R=2Q, and m=0.",
                "The P7 zero extension is retained in every polynomial and no common modulus is introduced.",
            ],
            "sampling": "Unit-interval Sobolev sampling and disjoint intervals within each character fibre multiply the continuous source L2 bound by at most 1+log^2(2N).",
            "large_sieve_scale": "L_{N,Q,T}=(1+log^2(2N))(2N+4Q^2(T+1)^2)(log(2Q(T+1)))^A up to the checked K-dependent source constant.",
            "operator_and_variance": "Lambda(K)<<_K L_{N,Q,T}, tr(K^2)<<_K L_{N,Q,T}tr(K), and G(K)<<_K 3L_{N,Q,T}(L_{N,Q,T}tr(K)-tr(K)^2/R).",
            "scope": "For tr(K) asymptotic to RN and N<=T^C, this is T^o(1)RN(N+Q^2T^2)^2. It is a raw-L2 fallback, not the Guth--Maynard refined S3 shape.",
            "sharp_raw_l2_barrier": "The rank-one J_R check saturates tr(K^2)=Lambda(K)tr(K) and has G(K)=R^3-R; raw L2 data alone supplies no fixed R-saving.",
        },
        "contained_no_go": {
            "status": "PROVED",
            "statement": "Within the abstract selected Gram class, PSD positivity, a raw L2 operator bound, coloured energy, and local height multiplicity alone do not control the selected cubic excess.",
            "finite_witness": "The Z/2 class-average check has local height multiplicity one and minimum coloured energy six, but selected excess 144 while averaged-block excess is zero.",
            "weakest_route_specific_statistics": "For the PSD route: the centred Gram variance V2 together with Lambda. For the class-average route: delta_3, or the stronger checkable delta_2.",
            "non_overclaim": "These are finite algebraic countermodels, not P7 zero, detector, or large-value examples and do not exclude another character-aware method.",
        },
        "source_integrity": sources,
        "artifact_identity": identities,
        "non_promotion": list(C.NON_PROMOTION),
        "resource_contract": C.RESOURCE_LIMITS,
        "replay": {
            "script": str(SELF.relative_to(ROOT)),
            "script_sha256": digest(SELF),
            "runtime": runtime,
            "write_command": "python3 proof/build_p7_selected_gram_excess_v1.py --write",
            "check_command": "python3 proof/build_p7_selected_gram_excess_v1.py --check",
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
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "P7 selected-Gram replay exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "P7 selected-Gram replay exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7 selected-Gram artifact")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "P7 selected-Gram artifact mismatch; issue a versioned correction rather than overwrite")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
