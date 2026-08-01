#!/usr/bin/env python3
"""Execute/check the sealed 160-row corrected CRR finite-analogue probe v2.

This runner is intentionally a discovery program.  It records OBSERVED finite
rows and RECOGNIZED complex diagnostics; it makes no continuous claim.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import resource
import sys
import time
from typing import Any

import mpmath as mp
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
PREREG = ROOT / "artifacts/cycle-4-p1r-crr-finite-probe-preregistration-v2.json"
OUTPUT = ROOT / "discovery/cycle-4-p1r-crr-finite-probe-v2.json"
PREREG_BUILDER = ROOT / "discovery/build_cycle_4_p1r_crr_finite_probe_preregistration_v2.py"
CONVENTIONS = ROOT / "conventions/crr_finite_analogue_probe_v2.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def current_rss_bytes() -> int:
    for line in Path("/proc/self/status").read_text(encoding="utf-8").splitlines():
        if line.startswith("VmRSS:"):
            return int(line.split()[1]) * 1024
    raise RuntimeError("VmRSS unavailable")


def runtime_metadata() -> dict[str, Any]:
    return {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "mpmath": mp.__version__,
        "numpy": np.__version__,
        "optimization_level": sys.flags.optimize,
    }


def validate_prereg() -> tuple[dict[str, Any], Any]:
    builder = load_module(PREREG_BUILDER, "crr_probe_v2_prereg_builder")
    expected = builder.render(builder.seal())
    require(PREREG.is_file() and PREREG.read_bytes() == expected, "sealed v2 preregistration byte replay failed")
    artifact = json.loads(expected)
    require(artifact["status"] == "SEALED_DISCOVERY_PREREGISTRATION_EXECUTABLE", "v2 preregistration is not executable")
    conventions = load_module(CONVENTIONS, "crr_probe_v2_conventions")
    require(runtime_metadata() == artifact["runtime"], "runtime does not match sealed v2 preregistration")
    require(sha256(CONVENTIONS) == artifact["frozen_hashes"]["v2_conventions"]["sha256"], "v2 convention hash mismatch")
    return artifact, conventions


def farey_nodes(q: int, order: int) -> tuple[np.ndarray, np.ndarray]:
    fractions = {(0, 1), (1, 1)}
    for den in range(1, q + 1):
        for num in range(1, den):
            if math.gcd(num, den) == 1:
                fractions.add((num, den))
    ordered = sorted(fractions, key=lambda x: x[0] / x[1])
    roots, weights = np.polynomial.legendre.leggauss(order)
    all_nodes: list[np.ndarray] = []
    all_weights: list[np.ndarray] = []
    for index, (num, den) in enumerate(ordered):
        centre = num / den
        left = 0.0 if index == 0 else (centre + ordered[index - 1][0] / ordered[index - 1][1]) / 2.0
        right = 1.0 if index + 1 == len(ordered) else (centre + ordered[index + 1][0] / ordered[index + 1][1]) / 2.0
        all_nodes.append((left + right) / 2.0 + (right - left) * roots / 2.0)
        all_weights.append((right - left) * weights / 2.0)
    return np.concatenate(all_nodes), np.concatenate(all_weights)


def insert_repaired(values: set[int], start: int, h: int) -> int | None:
    for offset in range(h):
        point = (start + offset) % h
        if point not in values:
            values.add(point)
            return point
    return None


def initialize_w(row: dict[str, Any], c: Any) -> tuple[set[int] | None, int]:
    scale = c.scales(row["N"])
    h, r = scale["H"], scale["R"]
    family, variant = row["family"], row["variant"]
    stream = c.SplitMix64(int(row["row_seed"], 16))
    values: set[int] = set()
    words = 0

    def next_word() -> int:
        nonlocal words
        words += 1
        return stream.next_u64()

    if family == "F1-phase-rounded-frame":
        radius = h // (8 * r)
        for j in range(r):
            word = next_word()
            if insert_repaired(values, (j * h) // r + (word % (2 * radius + 1)) - radius, h) is None:
                return None, words
    elif family == "F2-macrocell-resonant-layers":
        cells = variant["macrocells"]
        for j in range(r):
            cell, local = j % cells, j // cells
            count = (r + cells - 1 - cell) // cells
            left, right = (cell * h) // cells, ((cell + 1) * h) // cells
            width, radius = right - left, (right - left) // (8 * count)
            word = next_word()
            start = left + (local * width) // count + (word % (2 * radius + 1)) - radius
            if insert_repaired(values, start, h) is None:
                return None, words
    elif family == "F3-near-product-rational-packet":
        denominator = variant["packet_denominator"]
        radius = h // (16 * r)
        for j in range(r):
            lane, local = j % denominator, j // denominator
            count = (r + denominator - 1 - lane) // denominator
            word = next_word()
            start = (local * h) // count + (lane * h) // denominator + (word % (2 * radius + 1)) - radius
            if insert_repaired(values, start, h) is None:
                return None, words
    elif family == "F4-quadratic-modular-chirp":
        for _ in range(r):
            if insert_repaired(values, next_word() % h, h) is None:
                return None, words
    elif family == "F5-symmetric-positive-trace-spectral":
        half, rank = (h - 1) // 2, variant["spectral_rank"]
        for _ in range(r // 2):
            a = 1 + ((next_word() % half) * rank % half)
            if insert_repaired(values, a, h) is None or insert_repaired(values, h - a, h) is None:
                return None, words
        if r % 2 and insert_repaired(values, 0, h) is None:
            return None, words
    else:
        raise RuntimeError(f"unknown family {family}")
    return values, words


def phase_labels_and_d(w: np.ndarray, n: int, h: int, family: str, variant: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
    if family == "F4-quadratic-modular-chirp":
        p = variant["prime_modulus"]
        indices = np.arange(n, dtype=np.float64)
        coeff = np.exp(2j * np.pi * ((indices * indices + indices) % p) / p)
        padded = np.zeros(h, dtype=np.complex128)
        padded[:n] = coeff
        return np.full(n, -1, dtype=np.int16), h * np.fft.ifft(padded)[w], coeff
    indicator = np.zeros(h, dtype=np.float64)
    indicator[w] = 1.0
    sums = np.fft.fft(indicator)[:n]
    phases = variant["phase_denominator"]
    candidates = np.exp(2j * np.pi * np.arange(phases) / phases)
    labels = np.empty(n, dtype=np.int16)
    for index, value in enumerate(sums):
        if value == 0.0:
            labels[index] = 0
        else:
            labels[index] = int(np.argmin(np.abs(value / abs(value) - candidates)))
    coeff = candidates[labels]
    padded = np.zeros(h, dtype=np.complex128)
    padded[:n] = coeff
    return labels, h * np.fft.ifft(padded)[w], None


def energy_counts(w: np.ndarray, h: int) -> tuple[np.ndarray, int]:
    sums = (w[:, None] + w[None, :]) % h
    counts = np.bincount(sums.ravel(), minlength=h).astype(np.int64)
    return counts, int(np.dot(counts, counts))


def swap_energy(counts: np.ndarray, energy: int, w: np.ndarray, old: int, new: int, h: int) -> tuple[dict[int, int], int]:
    other = w[w != old]
    changes: dict[int, int] = {}
    def change(place: int, amount: int) -> None:
        key = place % h
        changes[key] = changes.get(key, 0) + amount
    change(2 * old, -1)
    for z in other:
        change(old + int(z), -2)
    change(2 * new, 1)
    for z in other:
        change(new + int(z), 2)
    next_energy = energy
    for place, amount in changes.items():
        before = int(counts[place])
        next_energy += 2 * before * amount + amount * amount
    return changes, next_energy


def apply_changes(counts: np.ndarray, changes: dict[int, int]) -> None:
    for place, amount in changes.items():
        counts[place] += amount


def cubic_binary(w: np.ndarray, n: int, h: int, mode: int) -> float:
    modes = np.concatenate((np.arange(-mode, 0), np.arange(1, mode + 1)))
    u = np.exp(2j * np.pi * np.outer(w, modes) / h)
    gram = u.conj().T @ u
    weights = 1.0 - np.abs(modes) / (mode + 1.0)
    a = weights[:, None] * gram
    trace_a = np.trace(a)
    trace_a2 = np.trace(a @ a)
    trace_a3 = np.trace(a @ a @ a)
    trace_b3 = trace_a3 - 3.0 * mode * trace_a2 + 3.0 * mode * mode * trace_a - len(w) * mode**3
    return float((n**3 * trace_b3).real)


def rational_binary(w: np.ndarray, nodes: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, float]:
    values = np.empty(len(nodes), dtype=np.complex128)
    for start in range(0, len(nodes), 256):
        stop = min(start + 256, len(nodes))
        values[start:stop] = np.exp(2j * np.pi * np.outer(nodes[start:stop], w)).sum(axis=1)
    return values, float(weights[np.abs(values) >= 0.0].sum())


def rational_measure(values: np.ndarray, weights: np.ndarray, threshold: float) -> float:
    return float(weights[np.abs(values) >= threshold].sum())


def proxy_score(d_values: np.ndarray, energy: int, rational_values: np.ndarray, rational_weights: np.ndarray, cubic: float, n: int) -> float:
    margin = 1.05
    lv_cut = margin * 0.75 * n**0.7
    e_low, e_high = margin * 0.25 * n * n, 4.0 * n * n / margin
    mu_cut = margin * 0.2 * n**(-0.4)
    cubic_cut = margin * 0.05 * n**3.6
    if not all(math.isfinite(x) for x in (float(np.min(np.abs(d_values))), float(cubic))) or cubic <= 0.0:
        return float("-inf")
    mu = rational_measure(rational_values, rational_weights, margin * 0.75 * n**0.6)
    return min(float(np.min(np.abs(d_values))) / lv_cut, min(energy / e_low, e_high / energy), mu / mu_cut, cubic / cubic_cut)


def cubic_mp(w: list[int], n: int, h: int, mode: int, bits: int) -> mp.mpf:
    old = mp.mp.prec
    mp.mp.prec = bits
    try:
        modes = list(range(-mode, 0)) + list(range(1, mode + 1))
        sums: dict[int, mp.mpc] = {}
        for difference in range(-2 * mode, 2 * mode + 1):
            sums[difference] = mp.fsum(mp.expj(2 * mp.pi * difference * point / h) for point in w)
        length = 2 * mode
        a = mp.matrix(length)
        for i, left in enumerate(modes):
            weight = mp.mpf(1) - abs(left) / mp.mpf(mode + 1)
            for j, right in enumerate(modes):
                a[i, j] = weight * sums[right - left]
        a2, a3 = a * a, a * a * a
        trace_a = mp.fsum(a[i, i] for i in range(length))
        trace_a2 = mp.fsum(a2[i, i] for i in range(length))
        trace_a3 = mp.fsum(a3[i, i] for i in range(length))
        value = n**3 * (trace_a3 - 3 * mode * trace_a2 + 3 * mode * mode * trace_a - len(w) * mode**3)
        return mp.re(value)
    finally:
        mp.mp.prec = old


def confirm_cubic_failure(w: list[int], n: int, h: int, c8: float, c12: float) -> tuple[bool, dict[str, Any]]:
    cut = mp.mpf(21) / 20 * mp.mpf(1) / 20 * mp.power(n, mp.mpf(18) / 5)
    observed: dict[str, Any] = {"binary_C8": repr(c8), "binary_C12": repr(c12), "dual_precision": {}}
    statuses: list[bool] = []
    for bits in (256, 384):
        a, b = cubic_mp(w, n, h, 8, bits), cubic_mp(w, n, h, 12, bits)
        disagreement = abs(a - b) <= mp.mpf(1) / 20 * max(abs(b), mp.mpf(1) / 20 * mp.power(n, mp.mpf(18) / 5))
        fails = a <= 0 or b <= 0 or b < cut or not disagreement
        observed["dual_precision"][str(bits)] = {"C8": mp.nstr(a, 30), "C12": mp.nstr(b, 30), "fails": bool(fails)}
        statuses.append(bool(fails))
    return all(statuses), observed


def run_row(row: dict[str, Any], c: Any, started: float, cap_seconds: int, cap_rss: int) -> dict[str, Any]:
    n, scale = row["N"], c.scales(row["N"])
    h, r, q = scale["H"], scale["R"], scale["Q"]
    if time.monotonic() - started >= cap_seconds or current_rss_bytes() >= cap_rss:
        return {"id": row["id"], "row_number": row["row_number"], "status": "RESOURCE_CAP", "epistemic_status": "OBSERVED", "reason": "cap before initialization"}
    values, init_words = initialize_w(row, c)
    if values is None:
        return {"id": row["id"], "row_number": row["row_number"], "status": "INIT_INVALID", "epistemic_status": "OBSERVED", "rng_words_initialization": init_words}
    if len(values) != r:
        return {"id": row["id"], "row_number": row["row_number"], "status": "SET_CARDINALITY", "epistemic_status": "OBSERVED", "rng_words_initialization": init_words}
    if any(point < 0 or point >= h for point in values):
        return {"id": row["id"], "row_number": row["row_number"], "status": "SET_DOMAIN", "epistemic_status": "OBSERVED"}
    w = np.array(sorted(values), dtype=np.int64)
    counts, energy = energy_counts(w, h)
    nodes16, weights16 = farey_nodes(q, 16)
    rational_values16, _ = rational_binary(w, nodes16, weights16)
    labels, d_values, chirp_coefficients = phase_labels_and_d(w, n, h, row["family"], row["variant"])
    cubic8 = cubic_binary(w, n, h, 8)
    current = proxy_score(d_values, energy, rational_values16, weights16, cubic8, n)
    stream = c.SplitMix64(int(row["row_seed"], 16))
    for _ in range(init_words):
        stream.next_u64()
    accepted = 0
    for proposal in range(c.MUTATIONS_PER_ROW):
        if time.monotonic() - started >= cap_seconds or current_rss_bytes() >= cap_rss:
            return {"id": row["id"], "row_number": row["row_number"], "status": "RESOURCE_CAP", "epistemic_status": "OBSERVED", "reason": "cap during proposal", "proposals_completed": proposal, "accepted": accepted}
        old = int(w[stream.next_u64() % r])
        remaining = set(map(int, w))
        remaining.remove(old)
        new = insert_repaired(remaining, stream.next_u64() % h, h)
        if new is None:
            return {"id": row["id"], "row_number": row["row_number"], "status": "INIT_INVALID", "epistemic_status": "OBSERVED", "reason": "mutation scan exhausted", "proposals_completed": proposal, "accepted": accepted}
        candidate_w = np.array(sorted(remaining), dtype=np.int64)
        changes, candidate_energy = swap_energy(counts, energy, w, old, new, h)
        candidate_labels, candidate_d, candidate_chirp = phase_labels_and_d(candidate_w, n, h, row["family"], row["variant"])
        candidate_rational, _ = rational_binary(candidate_w, nodes16, weights16)
        candidate_cubic = cubic_binary(candidate_w, n, h, 8)
        candidate_score = proxy_score(candidate_d, candidate_energy, candidate_rational, weights16, candidate_cubic, n)
        if candidate_score - current >= float(c.PROXY_INCREMENT):
            w, labels, d_values, rational_values16, cubic8 = candidate_w, candidate_labels, candidate_d, candidate_rational, candidate_cubic
            chirp_coefficients = candidate_chirp
            apply_changes(counts, changes)
            energy, current, accepted = candidate_energy, candidate_score, accepted + 1
    nodes32, weights32 = farey_nodes(q, 32)
    rational_values32, _ = rational_binary(w, nodes32, weights32)
    mu16 = rational_measure(rational_values16, weights16, 1.05 * 0.75 * n**0.6)
    mu32 = rational_measure(rational_values32, weights32, 1.05 * 0.75 * n**0.6)
    cubic12 = cubic_binary(w, n, h, 12)
    lv = float(np.min(np.abs(d_values)))
    result: dict[str, Any] = {
        "id": row["id"], "row_number": row["row_number"], "status": "NO_RETAINED_HIT",
        "epistemic_status": "OBSERVED", "family": row["family"], "variant": row["variant"], "N": n,
        "rng_words_initialization": init_words, "rng_words_total": init_words + 2 * c.MUTATIONS_PER_ROW,
        "proposals_completed": c.MUTATIONS_PER_ROW, "accepted": accepted, "final_W": [int(x) for x in w],
        "final_W_sha256": sha256_bytes(",".join(map(str, w)).encode("ascii")),
        "binary64": {"min_abs_D": repr(lv), "energy_exact": energy, "mu16": repr(mu16), "mu32": repr(mu32), "C8": repr(cubic8), "C12": repr(cubic12), "proxy_score": repr(current)},
    }
    cubic_fails, recognition = confirm_cubic_failure([int(x) for x in w], n, h, cubic8, cubic12)
    result["recognized_cubic"] = recognition
    if cubic_fails:
        result["outcome_diagnostic"] = "cubic"
        return result
    result["status"] = "RECOGNITION_RADIUS"
    result["outcome_diagnostic"] = "cubic did not supply a dual-precision failure; remaining high-precision diagnostics are not yet evaluated"
    return result


def make_global_cap_row(row: dict[str, Any]) -> dict[str, Any]:
    return {"id": row["id"], "row_number": row["row_number"], "status": "GLOBAL_CAP_UNREACHED", "epistemic_status": "OBSERVED", "reason": "aggregate resource cap fired on an earlier row"}


def render(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def execute() -> dict[str, Any]:
    prereg, c = validate_prereg()
    started = time.monotonic()
    rows: list[dict[str, Any]] = []
    schedule = prereg["schedule"]["rows"]
    cap = False
    for index, row in enumerate(schedule):
        if cap:
            rows.append(make_global_cap_row(row))
            continue
        outcome = run_row(row, c, started, prereg["resources"]["aggregate_wall_seconds"], prereg["resources"]["max_rss_bytes"])
        rows.append(outcome)
        if outcome["status"] == "RESOURCE_CAP":
            cap = True
            for later in schedule[index + 1:]:
                rows.append(make_global_cap_row(later))
            break
    require(len(rows) == 160 and len({row["id"] for row in rows}) == 160, "row retention invariant failed")
    statuses: dict[str, int] = {}
    for row in rows:
        statuses[row["status"]] = statuses.get(row["status"], 0) + 1
    return {
        "artifact_id": "cycle-4-p1r-crr-finite-probe-v2",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Finite surrogate results only. No row proves CRR compatibility/incompatibility, a saturation theorem, a density improvement, or a short-interval consequence. A miss is not a universal negative.",
        "predecessor": {"artifact": str(PREREG.relative_to(ROOT)), "sha256": sha256(PREREG), "status": prereg["status"]},
        "runner": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF), "runtime": runtime_metadata(), "resource_clock": "time.monotonic", "rss_source": "/proc/self/status:VmRSS"},
        "resources": {"wall_seconds": time.monotonic() - started, "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024, "cap_seconds": prereg["resources"]["aggregate_wall_seconds"], "cap_rss_bytes": prereg["resources"]["max_rss_bytes"]},
        "research_stage_review_policy": {"hostile_audit": "NOT_INITIATED; DEFERRED_TO_PAPER_STAGE", "complex_values": "RECOGNIZED", "finite_rows": "OBSERVED"},
        "status_counts": statuses,
        "rows": rows,
        "replay": {"check_command": "python3 discovery/run_cycle_4_p1r_crr_finite_probe_v2.py --check", "execution_command": "python3 discovery/run_cycle_4_p1r_crr_finite_probe_v2.py --write", "no_resume": True},
    }


def check() -> None:
    prereg, _ = validate_prereg()
    require(OUTPUT.is_file(), "finite probe result artifact is absent")
    payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
    require(payload["predecessor"]["sha256"] == sha256(PREREG), "result preregistration hash mismatch")
    require(payload["runner"]["sha256"] == sha256(SELF), "result runner hash mismatch")
    require(payload["runner"]["runtime"] == runtime_metadata(), "result runtime mismatch")
    rows = payload["rows"]
    scheduled = prereg["schedule"]["rows"]
    require(len(rows) == len(scheduled) == 160, "result row count mismatch")
    require([row["id"] for row in rows] == [row["id"] for row in scheduled], "result order/schedule mismatch")
    allowed = set(prereg["failure_codes"]) | {"RETAINED_HIT"}
    require(all(row["status"] in allowed for row in rows), "unknown result status")
    require(sum(payload["status_counts"].values()) == 160, "result status count mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite executed finite-probe artifact")
        payload = execute()
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
        print(json.dumps({"artifact": OUTPUT.name, "status_counts": payload["status_counts"]}, sort_keys=True))
    else:
        check()
        print(json.dumps({"artifact": OUTPUT.name, "check": "ok"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
