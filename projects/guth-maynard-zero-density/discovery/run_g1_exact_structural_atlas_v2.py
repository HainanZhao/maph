#!/usr/bin/env python3
"""Corrected, source-pinned exact structural G1 atlas authority.

This version preserves v1 but fixes its replay boundary: it rejects optimized
Python, enforces the frozen CPython/mpmath runtime, verifies the frozen
preregistration document and primary-source bytes directly, and derives its
local grid from the frozen convention module.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import resource
import sys
import time
from typing import Any

import mpmath


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from conventions.g1_atlas_v1 import (
    BASE_SEED, COEFFICIENT_FAMILIES, COEFFICIENT_XOR, PRECISIONS_BITS,
    REGISTERED_PAIRS, SCREEN_SCALE, SET_FAMILIES, SET_XOR,
    VALIDATION_SCALES, local_n_grid, local_s_grid, local_v_grid,
    local_w_grid, primary_spine, q,
)
from discovery.run_g1_exact_structural_atlas_v1 import local_row, transfer_row


PREREG = ROOT / "artifacts/cycle-3-g1-atlas-preregistration-v1.json"
DOC = ROOT / "docs/cycle-3-g1-atlas-preregistration-v1.md"
TEX = ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
TAR = ROOT / "artifacts/sources/arxiv-2405.20552v2.tar"
CONVENTIONS = ROOT / "conventions/g1_atlas_v1.py"
V1_SCRIPT = ROOT / "discovery/run_g1_exact_structural_atlas_v1.py"
V1_ARTIFACT = ROOT / "artifacts/cycle-3-g1-exact-structural-atlas-v1.json"
OUTPUT = ROOT / "artifacts/cycle-3-g1-exact-structural-atlas-v2.json"
PERFORMANCE = ROOT / "artifacts/cycle-3-g1-exact-structural-atlas-v2-performance.json"

PINS = {
    "preregistration_artifact": (PREREG, "227ec1c66b2e109653354b6c3245b4e809fe52692c01514ac10064c23db2b6f8"),
    "preregistration_document": (DOC, "0510bb5ced5b3a5fd4377dea57216b226b58b49158ad6ddb6185775c967bfd72"),
    "guth_maynard_tex": (TEX, "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "guth_maynard_source_tar": (TAR, "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc"),
    "frozen_conventions": (CONVENTIONS, "642a61fc03e5de6c7f7df5338e88da552ef1c72a7b7d7897898fb23740106ca5"),
    "v1_formula_engine": (V1_SCRIPT, "24deb3435082349905d002c030fb8e9a022018c6bf34cdb63d9a516470d0aaea"),
    "v1_exact_rows": (V1_ARTIFACT, "16b46d32fbe0b2d24eceda1dceebf51d2591019e36acd92085fe749685fc4023"),
}
PRE_CORRECTION_CONVENTION_SHA256 = "3d3cef60c32dff2a2e4cbd3c10b229464d74aadbbaef53ba1fccc7158b78d726"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ceil_q(value: Any) -> int:
    return -(-value.numerator // value.denominator)


def direct_pins() -> tuple[dict[str, str], dict[str, Any]]:
    require(sys.flags.optimize == 0, "G1 exact atlas v2 forbids -O/-OO")
    require(platform.python_implementation() == "CPython", "G1 exact atlas v2 requires CPython")
    require(platform.python_version() == "3.12.3", "G1 exact atlas v2 requires CPython 3.12.3")
    require(mpmath.__version__ == "1.2.1", "G1 exact atlas v2 requires mpmath 1.2.1")
    hashes: dict[str, str] = {}
    for label, (path, expected) in PINS.items():
        observed = sha256(path)
        require(observed == expected, f"G1 exact atlas v2 frozen hash mismatch: {path}")
        hashes[label] = observed
    prereg = json.loads(PREREG.read_text())
    require(prereg["artifact_id"] == "cycle-3-g1-atlas-preregistration-v1", "wrong preregistration identity")
    require(prereg["frozen_before_discovery"] is True, "preregistration is not sealed")
    require(prereg["document"] == {"path": "docs/cycle-3-g1-atlas-preregistration-v1.md", "sha256": PINS["preregistration_document"][1]}, "preregistration document pin mismatch")
    require(prereg["sources"]["gm_tex"]["path"] == str(TEX.relative_to(ROOT)) and prereg["sources"]["gm_tex"]["sha256"] == PINS["guth_maynard_tex"][1], "preregistration TeX pin mismatch")
    require(prereg["sources"]["gm_tar"] == {"path": str(TAR.relative_to(ROOT)), "sha256": PINS["guth_maynard_source_tar"][1]}, "preregistration tar pin mismatch")
    require(prereg["runtime"] == {"implementation": "CPython", "python": "3.12.3", "mpmath": "1.2.1", "precisions_bits": [256, 384]}, "preregistration runtime pin mismatch")
    return hashes, prereg


def convention_rows(prereg: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    s_values, n_values, v_values, w_values = local_s_grid(), local_n_grid(), local_v_grid(), local_w_grid()
    require({"s": [q(value) for value in s_values], "n": [q(value) for value in n_values], "v": [q(value) for value in v_values], "w": [q(value) for value in w_values], "expected_rows": 7744} == prereg["local_grid"], "frozen convention grid disagrees with preregistration")
    local = [local_row(s, n, v, w) for s in s_values for n in n_values for v in v_values for w in w_values]
    require(len(local) == 7744 and len({row["id"] for row in local}) == 7744, "convention-derived local grid mismatch")
    transfer: list[dict[str, Any]] = []
    for s in s_values:
        ell = 10 / (6 + 10 * s)
        n0s = {type(s)(index, 100) for index in range(2, 51)} | {type(s)(5, 13), ell / 2}
        for n0 in sorted(n0s):
            transfer.append(transfer_row(s, n0))
    require(len(transfer) == 560 and len({row["id"] for row in transfer}) == 560, "convention-derived transfer grid mismatch")
    frozen_keys = ("s", "n0", "k", "q", "ell", "u", "alpha", "provenance", "branch")
    require([{key: row[key] for key in frozen_keys} for row in transfer] == [{key: row[key] for key in frozen_keys} for row in prereg["transfer_rows"]], "v2 transfer coordinates differ from frozen preregistration")
    return local, transfer


def convention_semantics(prereg: dict[str, Any]) -> dict[str, Any]:
    """Check every frozen finite convention against the sealed artifact."""
    spine = [{"s": q(s), "n": q(n), "v": q(v), "w": q(w)} for s, n, v, w in primary_spine()]
    require(spine == prereg["screen"]["spine"], "corrected convention primary spine differs from preregistration")
    require(list(COEFFICIENT_FAMILIES) == prereg["families"]["coefficients"], "coefficient convention differs from preregistration")
    require(list(SET_FAMILIES) == prereg["families"]["sets"], "set convention differs from preregistration")
    require([list(pair) for pair in REGISTERED_PAIRS] == prereg["screen"]["pairs"], "registered pairs differ from preregistration")
    require(SCREEN_SCALE == prereg["screen"]["scale_U"], "screen scale differs from preregistration")
    require(list(VALIDATION_SCALES) == prereg["retention"]["validation_scales_U"], "validation scales differ from preregistration")
    require(list(PRECISIONS_BITS) == prereg["runtime"]["precisions_bits"], "precision convention differs from preregistration")
    require({"seed": f"0x{BASE_SEED:016x}", "coefficient_xor": f"0x{COEFFICIENT_XOR:016x}", "set_xor": f"0x{SET_XOR:016x}"} == {key: prereg["rng"][key] for key in ("seed", "coefficient_xor", "set_xor")}, "RNG convention differs from preregistration")
    return {
        "epistemic_status": "PROVED",
        "claim": "The current convention module produces exactly the frozen grids, 42-coordinate spine, family ordering, registered pairs, scales, precisions, and RNG constants recorded in the sealed preregistration.",
        "old_sha256": PRE_CORRECTION_CONVENTION_SHA256,
        "new_sha256": PINS["frozen_conventions"][1],
        "old_to_new_event": "OBSERVED runtime hardening: primary_spine bare asserts were replaced by explicit RuntimeError failures; v1 outputs are preserved and no old byte is overwritten.",
        "checked": {"local_rows": 7744, "primary_spine_rows": len(spine), "registered_pairs": len(REGISTERED_PAIRS), "screen_scale_U": SCREEN_SCALE, "validation_scales_U": list(VALIDATION_SCALES), "precisions_bits": list(PRECISIONS_BITS)},
    }


def certificate() -> dict[str, Any]:
    hashes, prereg = direct_pins()
    semantics = convention_semantics(prereg)
    local, transfer = convention_rows(prereg)
    v1 = json.loads(V1_ARTIFACT.read_text())
    require(local == v1["local_rows"] and transfer == v1["transfer_rows"], "v2 exact rows disagree with retained independently-audited v1 rows")
    local_anchor = next(row for row in local if row["id"] == "L:s=7/10;n=5/6;v=7/10;w=2/3")
    transfer_anchor = next(row for row in transfer if row["id"] == "T:s=7/10;n0=5/13;k=2;q=10/13")
    require(local_anchor["energy"]["terms"] == {"E1": "5/3", "E2": "5/3", "E3": "5/3"}, "mandatory local energy tie fails")
    require(transfer_anchor["source_term_exponents"] == {"LV1": "6/13", "LV2": "8/13", "LV3": "9/13"}, "mandatory transfer anchor fails")
    return {
        "artifact_id": "cycle-3-g1-exact-structural-atlas-v2",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED exact rational evaluation of the finite formulas frozen by the sealed G1 preregistration, conditional on the directly hash-verified cited source formulas. It evaluates no finite complex Dirichlet polynomial and proves no new large-values, density, short-interval, extremizer, or saturation theorem.",
        "supersession": {"supersedes": "cycle-3-g1-exact-structural-atlas-v1", "reason": "v1 row data is retained, but v2 directly verifies source/document/runtime pins, rejects optimized mode, and derives the local grid from the frozen conventions module."},
        "scope": {"finite_complex_probes_evaluated": 0, "screen_rows_evaluated": 0, "local_rows": len(local), "transfer_rows": len(transfer)},
        "frozen_inputs": {"hashes": hashes, "runtime": {"implementation": platform.python_implementation(), "python": platform.python_version(), "mpmath": mpmath.__version__, "optimization": sys.flags.optimize}, "convention_derivation": {"module": "conventions/g1_atlas_v1.py", "functions": ["local_s_grid", "local_n_grid", "local_v_grid", "local_w_grid", "primary_spine", "q"], "status": "DIRECT_IMPORT_AND_PREREGISTRATION_CROSSCHECK"}, "convention_runtime_correction": semantics},
        "formula_conventions": {"fraction_serialization": "reduced numerator/denominator strings from conventions.g1_atlas_v1.q", "signed_residual": "left-minus-right", "transfer_residual": "B-minus-source-term", "energy_terms_present_only_when": "v=s"},
        "counts": {"local_total": len(local), "local_energy_eligible": sum(row["energy_eligible"] for row in local), "local_energy_ineligible": sum(not row["energy_eligible"] for row in local), "transfer_total": len(transfer), "transfer_exact_power_scale": sum(row["provenance"] == "EXACT_POWER_SCALE" for row in transfer), "transfer_asymptotic_endpoint_only": sum(row["provenance"] == "ASYMPTOTIC_ENDPOINT_ONLY" for row in transfer), "transfer_by_branch": dict(sorted(Counter(row["branch"] for row in transfer).items()))},
        "mandatory_anchors": {"local": local_anchor, "transfer": transfer_anchor},
        "local_rows": local,
        "transfer_rows": transfer,
        "replay": {"script_sha256": sha256(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/discovery/run_g1_exact_structural_atlas_v2.py --write", "check_command": "python3 projects/guth-maynard-zero-density/discovery/run_g1_exact_structural_atlas_v2.py --check", "performance_command": "python3 projects/guth-maynard-zero-density/discovery/run_g1_exact_structural_atlas_v2.py --write-performance"},
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def write_performance(start: float, finish: float, payload: dict[str, Any]) -> None:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    PERFORMANCE.write_text(render({"artifact_id": "cycle-3-g1-exact-structural-atlas-v2-performance", "epistemic_status": "OBSERVED", "claim_boundary": "OBSERVED single-host exact-atlas replay measurement only; it is not a mathematical or finite-probe resource-cap certificate.", "atlas_artifact": {"path": str(OUTPUT.relative_to(ROOT)), "sha256": sha256(OUTPUT)}, "workload": payload["scope"], "environment": {"implementation": platform.python_implementation(), "python": platform.python_version(), "mpmath": mpmath.__version__, "platform": platform.platform()}, "measurement": {"wall_seconds": finish - start, "ru_maxrss": usage.ru_maxrss, "ru_maxrss_unit": "KiB on Linux"}, "command": payload["replay"]["performance_command"]}))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write-performance", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()
    value = certificate()
    finished = time.perf_counter()
    payload = render(value)
    if args.write:
        OUTPUT.write_text(payload)
    elif args.check:
        require(OUTPUT.is_file() and OUTPUT.read_text() == payload, "G1 exact structural atlas v2 artifact mismatch")
        print(json.dumps({"artifact": OUTPUT.name, "verified": True}, sort_keys=True))
    else:
        require(OUTPUT.is_file() and OUTPUT.read_text() == payload, "write/check v2 atlas before recording performance")
        write_performance(started, finished, value)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
