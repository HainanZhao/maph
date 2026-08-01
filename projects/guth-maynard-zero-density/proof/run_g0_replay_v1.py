#!/usr/bin/env python3
"""Run the read-only, deterministic Cycle-2 G0 replay chain.

This is an operational replay harness.  It deliberately has no G0 decision
logic: a PASS here means only that every listed immutable source, exact, and
reconciliation checker succeeded.  The separately versioned global
reconciliation is the only place permitted to decide the analytic gate.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from typing import Final


ROOT: Final = Path(__file__).resolve().parents[1]

# This list is deliberately finite and ordered.  New artifacts cannot enter a
# G0 replay merely by appearing in a directory.  Every checker is invoked in a
# read-only mode and must compare its recomputation to a pinned certificate or
# source bytes.  The Cycle-1 Route-A writers and raw performance artifacts are
# excluded because their records contain host-time observations.
CHECKS: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    (
        "source-manifest-v3",
        ("proof/build_source_manifest_v3.py", "--check"),
    ),
    (
        "stream-a-frozen-source-ledger",
        ("proof/check_cycle_2_stream_a_sources.py",),
    ),
    (
        "cycle-1-exact-two-route-reconciliation-v3",
        (
            "proof/audit_cycle1_routes.py",
            "--check",
            "artifacts/cycle-1-route-reconciliation-v3.json",
        ),
    ),
    (
        "stream-b-route-a-v3",
        (
            "proof/audit_cycle2_stream_b_route_a_v3.py",
            "--check",
            "artifacts/cycle-2-stream-b-route-a-v3.json",
        ),
    ),
    (
        "stream-b-route-b-v1",
        (
            "proof/replay_cycle2_stream_b_route_b.py",
            "--check",
            "artifacts/cycle-2-stream-b-route-b-v1.json",
        ),
    ),
    (
        "stream-b-two-route-reconciliation-v2",
        (
            "proof/reconcile_cycle2_stream_b_routes_v2.py",
            "--check",
            "artifacts/cycle-2-stream-b-route-reconciliation-v2.json",
        ),
    ),
    (
        "stream-c-official-formula-source-closure-v4",
        ("proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py",),
    ),
    (
        "stream-c-independent-official-sword-audit-v1",
        ("proof/audit_mit_sword_official_bitstream_v1.py", "--check"),
    ),
    (
        "stream-c-route-a-v5",
        (
            "proof/replay_cycle2_stream_c_route_a_v5.py",
            "--check",
            "artifacts/cycle-2-stream-c-route-a-v5.json",
        ),
    ),
    (
        "stream-c-route-b-v5",
        ("proof/replay_short_intervals_stream_c_route_b_v5.py", "--check"),
    ),
    (
        "stream-c-two-route-reconciliation-v2",
        ("proof/reconcile_cycle2_stream_c_two_routes_v2.py", "--check"),
    ),
    (
        "cycle-2-per-route-resource-configuration-v1",
        (
            "proof/run_cycle2_g0_resource_gate_v1.py",
            "--check-config",
            "artifacts/cycle-2-g0-per-route-resource-gate-config-v1.json",
        ),
    ),
    (
        "g0-dependency-evidence-correction-v3",
        ("proof/audit_g0_dependency_evidence_v3.py", "--check"),
    ),
)

# These artifacts contain host-specific observations.  They are evidence for
# the separately scoped resource gate, never fixed byte inputs to this replay.
TIMING_MUTABLE_RAW_ARTIFACTS: Final[tuple[str, ...]] = (
    "artifacts/cycle-2-stream-c-route-a-v3-performance.json",
    "artifacts/cycle-2-stream-c-route-a-v4-performance.json",
    "artifacts/cycle-2-stream-c-route-a-v5-performance.json",
    "artifacts/cycle-2-stream-c-route-b-v5-performance.json",
    "artifacts/cycle-2-g0-per-route-resource-gate-performance-v1.json",
)


def validate_static_configuration() -> None:
    """Reject accidental writers, mutable inputs, or dynamically added rows."""
    identifiers = [identifier for identifier, _ in CHECKS]
    if len(identifiers) != len(set(identifiers)):
        raise RuntimeError("duplicate G0 replay-check identifier")
    if not CHECKS:
        raise RuntimeError("empty G0 replay chain")
    flattened = tuple(argument for _, command in CHECKS for argument in command)
    if any(argument == "--write" or argument.startswith("--write-") for argument in flattened):
        raise RuntimeError("G0 replay configuration contains a writer")
    if any(mutable in flattened for mutable in TIMING_MUTABLE_RAW_ARTIFACTS):
        raise RuntimeError("G0 replay configuration reads a timing-mutable artifact")
    if any("-v1.py" in argument and "v1" in identifier for identifier, command in CHECKS for argument in command if "source-manifest" not in identifier):
        # This intentionally permits preserved Route-B v1 and SWORD-audit v1
        # only because each is a named current input of a later reconciliation.
        allowed_v1 = {
            "stream-b-route-b-v1",
            "stream-c-independent-official-sword-audit-v1",
        }
        unexpected = [identifier for identifier, command in CHECKS if identifier not in allowed_v1 and any("-v1.py" in argument for argument in command)]
        if unexpected:
            raise RuntimeError(f"unregistered legacy checker in G0 replay: {unexpected}")


def run() -> dict[str, object]:
    """Execute every fixed checker, stopping at the first nonzero exit."""
    validate_static_configuration()
    results: list[dict[str, object]] = []
    for identifier, command in CHECKS:
        script = ROOT / command[0]
        if not script.is_file():
            raise RuntimeError(f"missing registered checker: {command[0]}")
        completed = subprocess.run(
            (sys.executable, *command),
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            details = {
                "failed_check": identifier,
                "command": [sys.executable, *command],
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }
            raise RuntimeError(json.dumps(details, sort_keys=True))
        results.append({"id": identifier, "command": list(command), "epistemic_status": "OBSERVED"})
    return {
        "artifact_id": "g0-read-only-replay-harness-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "OBSERVED operational replay result only: listed read-only checks exited zero. This output neither proves a new theorem nor decides G0.",
        "status": "PASS",
        "checks": results,
        "excluded_timing_mutable_raw_artifacts": list(TIMING_MUTABLE_RAW_ARTIFACTS),
        "non_promotion": "A successful replay is not G0 PASS; only a separately versioned global analytic reconciliation may adjudicate that gate.",
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
