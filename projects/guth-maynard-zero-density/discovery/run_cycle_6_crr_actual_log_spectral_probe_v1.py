#!/usr/bin/env python3
"""Execute/check the frozen bounded actual-log CRR spectral probe."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import resource
import sys
import time
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
PREREG = ROOT / "artifacts/cycle-6-crr-actual-log-spectral-probe-preregistration-v2.json"
PREREG_BUILDER = ROOT / "discovery/build_cycle_6_crr_actual_log_spectral_probe_preregistration_v2.py"
CONVENTIONS = ROOT / "conventions/crr_actual_log_spectral_probe_v1.py"
OUTPUT = ROOT / "discovery/cycle-6-crr-actual-log-spectral-probe-v1.json"
EXPECTED_RUNTIME = {
    "implementation": "CPython",
    "python": "3.12.3",
    "numpy": "1.26.4",
    "optimization_level": 0,
}


class ResourceCapReached(RuntimeError):
    """Internal control flow for the pre-registered non-resumable cap rule."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_module(path: Path, label: str):
    spec = importlib.util.spec_from_file_location(label, path)
    require(spec is not None and spec.loader is not None, f"cannot load module: {label}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime_metadata() -> dict[str, Any]:
    result = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "optimization_level": sys.flags.optimize,
    }
    require(result == EXPECTED_RUNTIME, "actual-log spectral runner requires non-optimized CPython 3.12.3 and NumPy 1.26.4")
    return result


def rss_bytes() -> int:
    # Linux ru_maxrss is KiB.  The repository's pinned runtime is Linux.
    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024


def load_prereg():
    builder = load_module(PREREG_BUILDER, "crr_actual_log_spectral_prereg_v2")
    expected = builder.render(builder.seal())
    require(PREREG.is_file() and PREREG.read_bytes() == expected, "sealed v2 actual-log preregistration byte replay failed")
    artifact = json.loads(expected)
    require(artifact["status"] == "SEALED_DISCOVERY_PREREGISTRATION_EXECUTABLE", "actual-log preregistration is not executable")
    require(runtime_metadata() == artifact["runtime"], "runner runtime does not match preregistration")
    require(sha256(CONVENTIONS) == artifact["frozen_hashes"]["conventions"]["sha256"], "conventions hash mismatch")
    require(sha256(SELF) == artifact["frozen_hashes"]["runner"]["sha256"], "runner hash mismatch")
    return artifact


def finite_float(value: float, label: str) -> float:
    result = float(value)
    require(np.isfinite(result), f"non-finite diagnostic: {label}")
    return result


def normalize_score(values: np.ndarray, label: str) -> np.ndarray:
    maximum = float(np.max(values))
    require(np.isfinite(maximum) and maximum > 0.0, f"degenerate score: {label}")
    return values / maximum


def leading_phase_metrics(matrix: np.ndarray, conventions, cap_checker=None) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    if cap_checker is not None and cap_checker():
        raise ResourceCapReached()
    gram = matrix @ matrix.conjugate().T
    eigenvalues, left_vectors = np.linalg.eigh(gram)
    lam = finite_float(float(np.real(eigenvalues[-1])), "leading lambda")
    require(lam > 0.0, "leading eigenvalue is not positive")
    u = left_vectors[:, -1]
    x = matrix.conjugate().T @ u / np.sqrt(lam)
    b = conventions.phase(x)
    values = matrix @ b
    norm_values = finite_float(float(np.linalg.norm(values)), "leading output norm")
    minimum = finite_float(float(np.min(np.abs(values))), "leading output minimum")
    n = matrix.shape[1]
    r = matrix.shape[0]
    rho = finite_float(float(np.sum(np.abs(x)) ** 2 / n), "rho")
    phi = finite_float(float(np.sqrt(r) * minimum / norm_values), "phi")
    certificate_square = finite_float(lam * n * rho * phi**2 / r, "leading certificate square")
    require(minimum**2 + 1e-8 >= certificate_square, "finite leading-phase certificate failed")
    return b, values, {
        "lambda_recognized": lam,
        "rho_recognized": rho,
        "phi_recognized": phi,
        "certificate_lower_root_recognized": finite_float(np.sqrt(max(0.0, certificate_square)), "leading certificate root"),
        "leading_minimum_abs_recognized": minimum,
        "leading_l2_norm_recognized": norm_values,
    }


def minimum_value_refinement(matrix: np.ndarray, initial_b: np.ndarray, conventions, cap_checker=None) -> tuple[np.ndarray, list[dict[str, float]]]:
    b = initial_b.copy()
    records: list[dict[str, float]] = []
    for iteration in range(conventions.MINIMUM_VALUE_ITERATIONS):
        if cap_checker is not None and cap_checker():
            raise ResourceCapReached()
        before_values = matrix @ b
        z = conventions.phase(before_values)
        inverse = 1.0 / np.maximum(np.abs(before_values), conventions.EPSILON)
        p = inverse / np.sum(inverse)
        before_weighted_abs = finite_float(float(np.dot(p, np.abs(before_values))), "weighted before")
        c = matrix.conjugate().T @ (p * z)
        b_next = conventions.phase(c)
        after_values = matrix @ b_next
        after_linear = finite_float(float(np.real(np.vdot(p * z, after_values))), "weighted linear after")
        after_weighted_abs = finite_float(float(np.dot(p, np.abs(after_values))), "weighted abs after")
        require(after_linear + 1e-8 >= before_weighted_abs, "fixed-p phase update decreased its linear objective")
        require(after_weighted_abs + 1e-8 >= after_linear, "absolute row sum fell below phase functional")
        records.append(
            {
                "iteration": iteration + 1,
                "fixed_p_weighted_abs_before_recognized": before_weighted_abs,
                "fixed_p_linear_after_recognized": after_linear,
                "fixed_p_weighted_abs_after_recognized": after_weighted_abs,
                "minimum_abs_after_recognized": finite_float(float(np.min(np.abs(after_values))), "minimum after"),
            }
        )
        b = b_next
    return b, records


def farey_metrics(times: np.ndarray, feature: np.ndarray, labels, conventions) -> dict[str, Any]:
    aggregate = np.sum(feature[times], axis=0)
    score = finite_float(float(np.real(np.vdot(aggregate, aggregate))), "discrete Farey score")
    counts = np.asarray([label[3] for label in labels], dtype=np.float64)
    raw_values = aggregate / np.sqrt(counts)
    raw_abs = np.abs(raw_values)
    active = int(np.count_nonzero(raw_abs >= conventions.RAW_FAREY_AMPLITUDE))
    return {
        "discrete_ray_weighted_score_recognized": score,
        "label_count": int(len(labels)),
        "raw_amplitude_threshold": conventions.RAW_FAREY_AMPLITUDE,
        "active_label_count": active,
        "active_label_fraction_recognized": finite_float(active / len(labels), "active label fraction"),
        "raw_amplitude_minimum_recognized": finite_float(float(np.min(raw_abs)), "Farey amplitude minimum"),
        "raw_amplitude_maximum_recognized": finite_float(float(np.max(raw_abs)), "Farey amplitude maximum"),
    }


def row_payload(row_id: str, times: np.ndarray, final_b: np.ndarray, matrix: np.ndarray, feature: np.ndarray, labels, leading: dict[str, float], minimum_history: list[dict[str, float]], conventions) -> dict[str, Any]:
    values = matrix @ final_b
    max_coefficient = finite_float(float(np.max(np.abs(final_b))), "coefficient cap")
    min_value = finite_float(float(np.min(np.abs(values))), "final minimum value")
    energy = conventions.tolerance_one_energy(times)
    farey = farey_metrics(times, feature, labels, conventions)
    spacing = int(np.min(np.diff(times)))
    require(times.size == conventions.R and spacing >= conventions.MINIMUM_SEPARATION, "final common W violates frozen shape")
    require(max_coefficient <= 1.0 + 2.0**-40, "capped-phase coefficient bound failed")
    center_energy = conventions.R**4 // conventions.H
    gates = {
        "coefficient_cap": max_coefficient <= 1.0 + 2.0**-40,
        "central_minimum_value": min_value >= conventions.CENTRAL_VALUE,
        "central_energy_band": center_energy / 4.0 <= energy <= 4.0 * center_energy,
        "discrete_farey_activity": farey["active_label_fraction_recognized"] >= 0.125,
        "leading_certificate": leading["certificate_lower_root_recognized"] >= conventions.CENTRAL_VALUE,
    }
    status = "OBSERVED_JOINT_PROXY_HIT" if all(gates.values()) else "NO_RETAINED_HIT"
    return {
        "id": row_id,
        "status": status,
        "epistemic_status": "OBSERVED",
        "claim_boundary": "One bounded actual-log row only; no continuous CRR or AFARI/FARI conclusion follows.",
        "common_pair": {
            "W": [int(value) for value in times],
            "W_cardinality": int(times.size),
            "W_minimum_spacing": spacing,
            "coefficient_complex128_sha256": sha256_bytes(np.ascontiguousarray(final_b).tobytes()),
            "coefficient_maximum_abs_recognized": max_coefficient,
        },
        "base_proxy": {
            "central_value_threshold": conventions.CENTRAL_VALUE,
            "final_minimum_abs_recognized": min_value,
            "final_minimum_ratio_recognized": finite_float(min_value / conventions.CENTRAL_VALUE, "minimum ratio"),
        },
        "energy": {
            "epistemic_status": "PROVED",
            "definition": "ordered E_1(W)=#{(t1,t2,t3,t4):|t1+t2-t3-t4|<=1}",
            "exact_value": energy,
            "central_R4_over_H": center_energy,
            "central_ratio_recognized": finite_float(energy / center_energy, "energy ratio"),
        },
        "actual_farey_discrete": farey,
        "leading_phase_diagnostic": leading,
        "minimum_value_iteration": {
            "epistemic_status": "RECOGNIZED",
            "records": minimum_history,
            "fixed_p_checks": "Each recorded update passed weighted_linear_after>=weighted_abs_before and weighted_abs_after>=weighted_linear_after up to 1e-8.",
            "scope": "Changing p between iterations removes any asserted global monotonicity.",
        },
        "retention_gates": gates,
    }


def initial_farey_set(feature: np.ndarray, conventions) -> tuple[np.ndarray, np.ndarray]:
    right = conventions.normalized_power(lambda vector: feature.conjugate().T @ (feature @ vector), feature.shape[1], conventions.FAREY_POWER_ITERATIONS)
    score = np.abs(feature @ right)
    return conventions.select_stratified(score), score


def execute_semantic(enforce_resources: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    prereg = load_prereg()
    conventions = load_module(CONVENTIONS, "crr_actual_log_spectral_probe_conventions")
    started = time.monotonic()

    def cap_reached() -> bool:
        return (time.monotonic() - started) > conventions.RESOURCE_WALL_SECONDS or rss_bytes() > conventions.RESOURCE_RSS_BYTES

    all_times = np.arange(conventions.H, dtype=np.int64)
    indices, weight = conventions.coefficient_indices_and_weight()
    feature, labels = conventions.farey_feature_matrix(all_times)
    initial_times, farey_power_score = initial_farey_set(feature, conventions)
    full_matrix = conventions.measurement_matrix(all_times, indices, weight)
    rows: list[dict[str, Any]] = []
    schedule = prereg["row_schedule"]
    for schedule_index, row in enumerate(schedule):
        if enforce_resources and cap_reached():
            rows.append({"id": row["id"], "status": "RESOURCE_CAP", "epistemic_status": "OBSERVED", "claim_boundary": "Resource outcome only; no mathematical conclusion."})
            for later in schedule[schedule_index + 1 :]:
                rows.append({"id": later["id"], "status": "GLOBAL_CAP_UNREACHED", "epistemic_status": "OBSERVED", "claim_boundary": "Resource outcome only; no mathematical conclusion."})
            break
        try:
            times = initial_times.copy()
            histories: list[dict[str, Any]] = []
            matrix = full_matrix[times]
            checker = cap_reached if enforce_resources else None
            leading_b, _, leading = leading_phase_metrics(matrix, conventions, checker)
            final_b = leading_b
            if row["id"] != "F0-farey-leading-phase":
                final_b, history = minimum_value_refinement(matrix, leading_b, conventions, checker)
                histories.extend({"stage": "initial", **record} for record in history)
            if row["id"] == "F2-joint-reselection-minimum":
                for outer in range(conventions.JOINT_OUTER_ITERATIONS):
                    if checker is not None and checker():
                        raise ResourceCapReached()
                    all_values = full_matrix @ final_b
                    joint_score = 0.5 * normalize_score(np.abs(farey_power_score), "Farey score") + 0.5 * normalize_score(np.abs(all_values), "Dirichlet score")
                    times = conventions.select_stratified(joint_score)
                    matrix = full_matrix[times]
                    leading_b, _, leading = leading_phase_metrics(matrix, conventions, checker)
                    final_b, history = minimum_value_refinement(matrix, leading_b, conventions, checker)
                    histories.extend({"stage": f"joint-{outer + 1}", **record} for record in history)
            rows.append(row_payload(row["id"], times, final_b, matrix, feature, labels, leading, histories, conventions))
        except ResourceCapReached:
            rows.append({"id": row["id"], "status": "RESOURCE_CAP", "epistemic_status": "OBSERVED", "claim_boundary": "Resource outcome only; no mathematical conclusion."})
            for later in schedule[schedule_index + 1 :]:
                rows.append({"id": later["id"], "status": "GLOBAL_CAP_UNREACHED", "epistemic_status": "OBSERVED", "claim_boundary": "Resource outcome only; no mathematical conclusion."})
            break
    semantic = {
        "artifact_id": "cycle-6-crr-actual-log-spectral-probe-v1",
        "epistemic_status": "OBSERVED",
        "status": "SEALED_BOUNDED_ACTUAL_LOG_DISCOVERY_RESULT",
        "claim_boundary": "Three pre-registered bounded actual-log rows only. No result proves or refutes continuous CRR compatibility/incompatibility, AFARI/FARI, a saturation theorem, a density theorem, or a short-interval theorem. A miss is not a universal negative.",
        "runtime": runtime_metadata(),
        "runner": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "preregistration": {
            "path": str(PREREG.relative_to(ROOT)),
            "sha256": sha256(PREREG),
            "artifact_id": prereg["artifact_id"],
        },
        "numerics": {
            "status": "RECOGNIZED",
            "scope": "NumPy binary64/complex128 diagnostics. Exact energy and ray labels are separately proved integer calculations; no floating value is certified numerical.",
        },
        "literal_structure": {
            "dirichlet": prereg["actual_labels"]["dirichlet"],
            "farey": prereg["actual_labels"]["farey"],
            "ray_score": prereg["actual_labels"]["ray_score"],
            "cross_gram": prereg["actual_labels"]["inherited_cross_gram"],
            "not_rationalmass": "The three theta nodes do not evaluate the continuous smoothing or measure predicate RationalMass(v).",
        },
        "rows": rows,
        "outcome_counts": {status: sum(row.get("status") == status for row in rows) for status in sorted({row.get("status") for row in rows})},
        "falsifier": "A semantic replay mismatch, coefficient-cap violation, spacing/cardinality violation, or exact-energy/ray-label failure invalidates the affected finite row.",
    }
    resources = {
        "wall_seconds_observed": time.monotonic() - started,
        "peak_rss_bytes_observed": rss_bytes(),
        "wall_seconds_cap": conventions.RESOURCE_WALL_SECONDS,
        "rss_bytes_cap": conventions.RESOURCE_RSS_BYTES,
    }
    return semantic, resources


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    semantic, resources = execute_semantic(enforce_resources=args.write)
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite actual-log spectral result")
        payload = {**semantic, "resources_observed": resources}
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "actual-log spectral result is absent")
        observed = json.loads(OUTPUT.read_text(encoding="utf-8"))
        observed_semantic = {key: value for key, value in observed.items() if key != "resources_observed"}
        require(render(observed_semantic) == render(semantic), "actual-log spectral semantic replay mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "outcomes": semantic["outcome_counts"], "status": semantic["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
