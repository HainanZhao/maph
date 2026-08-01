#!/usr/bin/env python3
"""Run the read-only G0 replay chain, v2, including the sealed adjudication.

V1 is preserved as its original 13-check recovery record.  This successor
adds the bounded literature audit, hostile gate audit, and authoritative G0
reconciliation after they were separately sealed.  The runner itself is only
an OBSERVED operational replay; it does not make a new gate decision.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from typing import Final


ROOT: Final = Path(__file__).resolve().parents[1]

# The inventory is finite and ordered.  No glob, directory scan, writer, or
# host-timing artifact is permitted to become a replay input implicitly.
CHECKS: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    ("source-manifest-v3", ("proof/build_source_manifest_v3.py", "--check")),
    ("stream-a-frozen-source-ledger", ("proof/check_cycle_2_stream_a_sources.py",)),
    ("cycle-1-exact-two-route-reconciliation-v3", ("proof/audit_cycle1_routes.py", "--check", "artifacts/cycle-1-route-reconciliation-v3.json")),
    ("stream-b-route-a-v3", ("proof/audit_cycle2_stream_b_route_a_v3.py", "--check", "artifacts/cycle-2-stream-b-route-a-v3.json")),
    ("stream-b-route-b-v1", ("proof/replay_cycle2_stream_b_route_b.py", "--check", "artifacts/cycle-2-stream-b-route-b-v1.json")),
    ("stream-b-two-route-reconciliation-v2", ("proof/reconcile_cycle2_stream_b_routes_v2.py", "--check", "artifacts/cycle-2-stream-b-route-reconciliation-v2.json")),
    ("stream-c-official-formula-source-closure-v4", ("proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py",)),
    ("stream-c-independent-official-sword-audit-v1", ("proof/audit_mit_sword_official_bitstream_v1.py", "--check")),
    ("stream-c-route-a-v5", ("proof/replay_cycle2_stream_c_route_a_v5.py", "--check", "artifacts/cycle-2-stream-c-route-a-v5.json")),
    ("stream-c-route-b-v5", ("proof/replay_short_intervals_stream_c_route_b_v5.py", "--check")),
    ("stream-c-two-route-reconciliation-v2", ("proof/reconcile_cycle2_stream_c_two_routes_v2.py", "--check")),
    ("cycle-2-per-route-resource-configuration-v1", ("proof/run_cycle2_g0_resource_gate_v1.py", "--check-config", "artifacts/cycle-2-g0-per-route-resource-gate-config-v1.json")),
    ("g0-dependency-evidence-correction-v3", ("proof/audit_g0_dependency_evidence_v3.py", "--check")),
    ("g0-literature-source-gate-audit-v1", ("proof/audit_g0_literature_source_gates_v1.py", "--check")),
    ("g0-hostile-final-gate-audit-v1", ("proof/audit_g0_final_gate_v1.py", "--check")),
    ("g0-authoritative-full-reconstruction-v1", ("proof/reconcile_g0_full_v1.py", "--check")),
)

# These raw records include host-dependent timing observations.  The runner
# checks the immutable configuration only; the sealed G0 certificate retains
# its separately scoped OBSERVED resource evidence.
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
)


def validate_static_configuration() -> None:
    """Reject accidental writers, mutable inputs, or unregistered legacy rows."""
    identifiers = [identifier for identifier, _ in CHECKS]
    if not CHECKS or len(identifiers) != len(set(identifiers)):
        raise RuntimeError("empty or duplicate G0 replay-check inventory")
    flattened = tuple(argument for _, command in CHECKS for argument in command)
    if any(argument == "--write" or argument.startswith("--write-") for argument in flattened):
        raise RuntimeError("G0 replay configuration contains a writer")
    if any(mutable in flattened for mutable in TIMING_MUTABLE_RAW_ARTIFACTS):
        raise RuntimeError("G0 replay configuration reads a timing-mutable artifact")
    allowed_v1 = {
        "stream-b-route-b-v1", "stream-c-independent-official-sword-audit-v1",
        "cycle-2-per-route-resource-configuration-v1", "g0-literature-source-gate-audit-v1",
        "g0-hostile-final-gate-audit-v1", "g0-authoritative-full-reconstruction-v1",
    }
    unexpected = [identifier for identifier, command in CHECKS if identifier not in allowed_v1 and any("-v1.py" in argument for argument in command)]
    if unexpected:
        raise RuntimeError(f"unregistered legacy checker in G0 replay: {unexpected}")


def run() -> dict[str, object]:
    """Run all fixed checkers, stopping fail-closed at the first failure."""
    validate_static_configuration()
    results: list[dict[str, object]] = []
    for identifier, command in CHECKS:
        if not (ROOT / command[0]).is_file():
            raise RuntimeError(f"missing registered checker: {command[0]}")
        completed = subprocess.run((sys.executable, *command), cwd=ROOT, capture_output=True, text=True)
        if completed.returncode:
            failure = {"failed_check": identifier, "command": [sys.executable, *command], "stdout": completed.stdout, "stderr": completed.stderr}
            raise RuntimeError(json.dumps(failure, sort_keys=True))
        results.append({"id": identifier, "command": list(command), "epistemic_status": "OBSERVED"})
    return {
        "artifact_id": "g0-read-only-replay-harness-v2",
        "supersedes": "g0-read-only-replay-harness-v1; v1 is retained as its original 13-check snapshot",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "OBSERVED operational replay result only: listed read-only checks exited zero. The sealed full reconstruction's own claim boundary, not this runner, adjudicates G0.",
        "status": "PASS",
        "checks": results,
        "excluded_timing_mutable_raw_artifacts": list(TIMING_MUTABLE_RAW_ARTIFACTS),
        "non_promotion": "The runner adds no theorem or G0 conclusion. It replays the separately sealed authoritative reconciliation, which remains an exact reconstruction of published consequences only.",
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
