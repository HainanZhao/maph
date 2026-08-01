#!/usr/bin/env python3
"""Seal the status-only v2 correction of the P7 Q(i) preregistration."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import resource
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from conventions import p7_hecke_qi_v2 as C


def load_v1():
    path = ROOT / "proof/build_p7_hecke_qi_preregistration_v1.py"
    spec = importlib.util.spec_from_file_location("p7_hecke_qi_v1_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load P7 v1 builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V1 = load_v1()
OUT = ROOT / "artifacts/p7-hecke-qi-preregistration-v2.json"
V1_ARTIFACT = ROOT / "artifacts/p7-hecke-qi-preregistration-v1.json"
DOC = ROOT / "docs/p7-hecke-qi-preregistration-v2-correction.md"
CONVENTIONS = ROOT / "conventions/p7_hecke_qi_v2.py"
TESTS = ROOT / "tests/test_p7_hecke_qi_preregistration_v2.py"
WALL_CAP_NS = 60_000_000_000
RSS_CAP_KIB = 262_144


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload() -> dict[str, object]:
    require(V1_ARTIFACT.is_file(), "v1 P7 preregistration is absent")
    require(V1.render(V1.payload()) == V1_ARTIFACT.read_bytes(), "v1 P7 preregistration no longer replays")
    value = V1.payload()
    value["artifact_id"] = "p7-hecke-qi-preregistration-v2"
    value["status"] = "PREREGISTERED_UNEXECUTED_STATUS_CORRECTION"
    value["claim_boundary"] = (
        "Status-only correction of P7 v1. It labels the preselected repeated-norm "
        "witness CONJECTURED until P7-1 checks it. It changes no family, source, "
        "range, threshold, or gate; proves no Hecke density, Guth--Maynard transfer, "
        "or prime-ideal result; initiates neither hostile audit nor theorem search."
    )
    value["correction"] = {
        "predecessor": {"path": str(V1_ARTIFACT.relative_to(ROOT)), "sha256": digest(V1_ARTIFACT)},
        "defect": "v1 presented a preselected material algebraic witness without an explicit epistemic tag.",
        "repair": "The same frozen witness is now explicitly CONJECTURED and cannot close P7-1 until independently checked.",
        "unchanged": ["family", "source pins", "all gate identifiers and pass/fail rules", "resource caps", "no-search/no-hostile-audit boundary"],
    }
    value["selection"]["family"] = C.FAMILY_CONVENTION
    value["selection"]["field"] = C.FIELD
    value["selection"]["zero_count"] = C.ZERO_CONVENTION
    value["selection"]["L_function"] = C.L_FUNCTION_CONVENTION
    gate = next(item for item in value["gates"] if item["id"] == "P7-1-NORM-AGGREGATION")
    gate["preselected_witness"] = C.REPEATED_NORM_WITNESS
    value["non_promotion"] = list(C.NO_GO_OR_NON_PROMOTION)
    value["artifact_identity"] = {
        "conventions": {"path": str(CONVENTIONS.relative_to(ROOT)), "sha256": digest(CONVENTIONS)},
        "document": {"path": str(DOC.relative_to(ROOT)), "sha256": digest(DOC)},
        "builder": {"path": str(Path(__file__).relative_to(ROOT)), "sha256": digest(Path(__file__))},
        "tests": {"path": str(TESTS.relative_to(ROOT)), "sha256": digest(TESTS)},
    }
    value["replay"] = {
        "command": "python3 proof/build_p7_hecke_qi_preregistration_v2.py --check",
        "python_implementation": sys.implementation.name,
        "python_version": ".".join(map(str, sys.version_info[:3])),
        "optimized": sys.flags.optimize,
        "wall_cap_ns": WALL_CAP_NS,
        "rss_cap_kib": RSS_CAP_KIB,
    }
    return value


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.write != args.check, "choose exactly one of --write or --check")
    require(sys.flags.optimize == 0, "P7 v2 preregistration rejects optimized Python")
    require(sys.version_info[:3] == (3, 12, 3) and sys.platform.startswith("linux"), "P7 v2 requires CPython 3.12.3 on linux")
    started = time.monotonic_ns()
    encoded = render(payload())
    elapsed = time.monotonic_ns() - started
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    require(elapsed < WALL_CAP_NS, "P7 v2 preregistration exceeded wall cap")
    require(rss < RSS_CAP_KIB, "P7 v2 preregistration exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7 v2 preregistration")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file(), "sealed P7 v2 preregistration is absent")
        require(OUT.read_bytes() == encoded, "sealed P7 v2 preregistration mismatch")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as err:
        print(err, file=sys.stderr)
        raise SystemExit(1)
