#!/usr/bin/env python3
"""Read-only G0 replay successor v3 with a non-bypassable runtime boundary.

V3 retains every v2 operational check, adds the two Cycle-1 read-only route
wrappers, published-source v5, the six-route resource configuration, and the
bounded v2 hostile audit.  It ends at the corrected authoritative v2
reconstruction.  This harness is an OBSERVED replay only; it does not decide
G0 or prove a new theorem.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any, Final


ROOT: Final = Path(__file__).resolve().parents[1]
RUNTIME_RELATIVE: Final = "conventions/proof_runtime_v1.py"
RUNTIME_SHA256: Final = "83e486ad6252435745d8465f143a25d0a16e78bd82076ad5965368065deb645b"
PINNED_IMPLEMENTATION: Final = "CPython"
PINNED_VERSION: Final = (3, 12, 3)

# The inventory is fixed and ordered.  It deliberately does not contain a
# discovery script, directory scan, writer, or raw timing artifact path.
CHECKS: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    ("source-manifest-v3", ("proof/build_source_manifest_v3.py", "--check")),
    ("stream-a-frozen-source-ledger", ("proof/check_cycle_2_stream_a_sources.py",)),
    ("cycle-1-exact-two-route-reconciliation-v3", ("proof/audit_cycle1_routes.py", "--check", "artifacts/cycle-1-route-reconciliation-v3.json")),
    ("cycle1-route-a-readonly-v1", ("proof/replay_cycle1_route_a_readonly_v1.py",)),
    ("cycle1-route-b-readonly-v1", ("proof/replay_cycle1_route_b_readonly_v1.py",)),
    ("stream-b-route-a-v3", ("proof/audit_cycle2_stream_b_route_a_v3.py", "--check", "artifacts/cycle-2-stream-b-route-a-v3.json")),
    ("stream-b-route-b-v1", ("proof/replay_cycle2_stream_b_route_b.py", "--check", "artifacts/cycle-2-stream-b-route-b-v1.json")),
    ("stream-b-two-route-reconciliation-v2", ("proof/reconcile_cycle2_stream_b_routes_v2.py", "--check", "artifacts/cycle-2-stream-b-route-reconciliation-v2.json")),
    ("stream-c-official-formula-source-closure-v4", ("proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py",)),
    ("stream-c-independent-official-sword-audit-v1", ("proof/audit_mit_sword_official_bitstream_v1.py", "--check")),
    ("stream-c-published-formula-source-v5", ("proof/check_explicit_formula_published_source_v5.py", "--check")),
    ("stream-c-route-a-v5", ("proof/replay_cycle2_stream_c_route_a_v5.py", "--check", "artifacts/cycle-2-stream-c-route-a-v5.json")),
    ("stream-c-route-b-v5", ("proof/replay_short_intervals_stream_c_route_b_v5.py", "--check")),
    ("stream-c-two-route-reconciliation-v2", ("proof/reconcile_cycle2_stream_c_two_routes_v2.py", "--check")),
    ("cycle-2-per-route-resource-configuration-v1", ("proof/run_cycle2_g0_resource_gate_v1.py", "--check-config", "artifacts/cycle-2-g0-per-route-resource-gate-config-v1.json")),
    ("g0-six-route-resource-configuration-v2", ("proof/run_g0_resource_gate_v2.py", "--check-config", "artifacts/g0-six-route-resource-gate-config-v2.json")),
    ("g0-dependency-evidence-correction-v3", ("proof/audit_g0_dependency_evidence_v3.py", "--check")),
    ("g0-literature-source-gate-audit-v1", ("proof/audit_g0_literature_source_gates_v1.py", "--check")),
    ("g0-historical-final-gate-audit-v1", ("proof/audit_g0_final_gate_v1.py", "--check")),
    ("g0-v2-bounded-hostile-audit-v1", ("proof/audit_g0_v2_hostile_v1.py", "--check")),
    ("g0-authoritative-full-reconstruction-v1", ("proof/reconcile_g0_full_v1.py", "--check")),
    ("g0-authoritative-full-reconstruction-v2", ("proof/reconcile_g0_full_v2.py", "--check")),
)

# These are host-dependent measurements.  They must not be direct check
# inputs.  The final authoritative reconciliation reads its own frozen v2
# record to validate that sealed evidence; the harness never regenerates it.
TIMING_MUTABLE_RAW_ARTIFACTS: Final[tuple[str, ...]] = (
    "artifacts/baseline-route-a-v1.json",
    "artifacts/baseline-route-a-v2.json",
    "artifacts/baseline-route-a-v3.json",
    "artifacts/cycle-1-replay-performance-v1.json",
    "artifacts/cycle-1-replay-performance-v2.json",
    "artifacts/cycle-2-stream-b-route-a-v1.json",
    "artifacts/cycle-2-stream-b-route-a-v2.json",
    "artifacts/cycle-2-stream-c-route-a-v1.json",
    "artifacts/cycle-2-stream-c-route-a-v2.json",
    "artifacts/cycle-2-stream-c-route-a-v3-performance.json",
    "artifacts/cycle-2-stream-c-route-a-v4-performance.json",
    "artifacts/cycle-2-stream-c-route-a-v5-performance.json",
    "artifacts/cycle-2-stream-c-route-b-v5-performance.json",
    "artifacts/cycle-2-g0-per-route-resource-gate-performance-v1.json",
    "artifacts/g0-six-route-resource-gate-performance-v2.json",
)


def fail(message: str) -> None:
    """Raise explicitly: this preflight must remain effective under ``-O``."""
    raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runtime_preflight() -> dict[str, object]:
    """Enforce the exact, non-optimized interpreter before any replay work."""
    if sys.flags.optimize != 0:
        fail("G0 replay v3 rejects optimized Python: sys.flags.optimize must equal 0")
    actual = (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    if platform.python_implementation() != PINNED_IMPLEMENTATION:
        fail(f"G0 replay v3 requires {PINNED_IMPLEMENTATION}, got {platform.python_implementation()}")
    if actual != PINNED_VERSION:
        fail(f"G0 replay v3 requires CPython {PINNED_VERSION}, got {actual}")
    runtime_path = ROOT / RUNTIME_RELATIVE
    if sha256(runtime_path) != RUNTIME_SHA256:
        fail("G0 replay v3 runtime convention hash mismatch")
    spec = importlib.util.spec_from_file_location("g0_runtime_v1", runtime_path)
    if spec is None or spec.loader is None:
        fail("cannot load pinned G0 runtime convention")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    declared = (module.IMPLEMENTATION, tuple(module.VERSION))
    if declared != (PINNED_IMPLEMENTATION, PINNED_VERSION):
        fail("runtime convention declaration differs from v3 preflight")
    # Calling the legacy checker after explicit checks confirms agreement, but
    # no safety depends on its assert statements.
    returned = module.assert_pinned_runtime()
    if returned["implementation"] != PINNED_IMPLEMENTATION or returned["version"] != ".".join(map(str, PINNED_VERSION)):
        fail("legacy runtime convention return differs from v3 preflight")
    return {
        "implementation": PINNED_IMPLEMENTATION,
        "version": ".".join(map(str, PINNED_VERSION)),
        "optimization": sys.flags.optimize,
        "runtime_convention_sha256": RUNTIME_SHA256,
        "epistemic_status": "OBSERVED",
    }


def validate_static_configuration() -> None:
    identifiers = [identifier for identifier, _ in CHECKS]
    if not CHECKS or len(identifiers) != len(set(identifiers)):
        fail("empty or duplicate G0 v3 replay-check inventory")
    required = {
        "cycle1-route-a-readonly-v1", "cycle1-route-b-readonly-v1",
        "stream-c-published-formula-source-v5", "g0-six-route-resource-configuration-v2",
        "g0-v2-bounded-hostile-audit-v1", "g0-authoritative-full-reconstruction-v2",
    }
    if not required.issubset(identifiers):
        fail("v3 inventory omits a corrected-v2 coverage check")
    if identifiers[-1] != "g0-authoritative-full-reconstruction-v2":
        fail("v3 must end at the corrected authoritative G0 v2 reconstruction")
    flattened = tuple(argument for _, command in CHECKS for argument in command)
    if any(argument == "--write" or argument.startswith("--write-") for argument in flattened):
        fail("G0 v3 replay configuration contains a writer")
    if any(mutable in flattened for mutable in TIMING_MUTABLE_RAW_ARTIFACTS):
        fail("G0 v3 replay configuration names a timing-mutable artifact")
    for _, command in CHECKS:
        if not (ROOT / command[0]).is_file():
            fail(f"missing registered checker: {command[0]}")


def run() -> dict[str, Any]:
    runtime = runtime_preflight()
    validate_static_configuration()
    results: list[dict[str, object]] = []
    for identifier, command in CHECKS:
        completed = subprocess.run((sys.executable, *command), cwd=ROOT,
                                   capture_output=True, text=True)
        if completed.returncode != 0:
            fail(json.dumps({"failed_check": identifier, "command": [sys.executable, *command], "stdout": completed.stdout, "stderr": completed.stderr}, sort_keys=True))
        results.append({"id": identifier, "command": list(command), "epistemic_status": "OBSERVED"})
    return {
        "artifact_id": "g0-read-only-replay-harness-v3",
        "supersedes": "g0-read-only-replay-harness-v2 operationally; v1 and v2 remain immutable historical runners",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "OBSERVED operational replay only: under explicitly checked normal CPython 3.12.3, all listed read-only checkers exited zero. The sealed v2 reconstruction's conditional claim boundary, not this runner, adjudicates G0. The runner proves no new zero-density or prime-interval theorem.",
        "status": "PASS",
        "runtime_preflight": runtime,
        "checks": results,
        "bounded_v2_containment": "The included hostile audit records that g0-full-v2's standalone runtime pin is bypassable under -O. This v3 runner rejects optimized mode before invoking it; the contained v2 defect is not silently promoted or erased.",
        "excluded_timing_mutable_raw_artifacts": list(TIMING_MUTABLE_RAW_ARTIFACTS),
        "non_promotion": "The runner makes no theorem, no new G0 decision, and no claim that host-specific resource measurements are mathematical proof.",
    }


def main() -> int:
    try:
        result = run()
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
