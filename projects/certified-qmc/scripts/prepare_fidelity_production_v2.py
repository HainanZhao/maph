#!/usr/bin/env python3
"""Version the fidelity freeze after the human-authorized VPS amendment."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
V1_SPEC = ROOT / "data" / "cycles-016-017-fidelity-spec.json"
V1_PREREG = (
    ROOT / "data" / "cycles-016-017-preregistration.json"
)
PAUSE = (
    ROOT / "certificates"
    / "cycles-016-017-throughput-pause-v1.json"
)
V2_SPEC = (
    ROOT / "data" / "cycles-016-017-fidelity-spec-v2.json"
)
V2_PREREG = (
    ROOT / "data" / "cycles-016-017-preregistration-v2.json"
)
MAXIMUM_NS_PER_UPDATE = "4.34480050068027950"
DRIFT_FRACTION = "0.75"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: object) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].endswith("Z"):
        raise SystemExit(
            "usage: prepare_fidelity_production_v2.py FROZEN_AT_UTC"
        )
    frozen_at = sys.argv[1]
    pause = json.loads(PAUSE.read_text())
    if (
        pause["preservation"]["resume_under_v1_forbidden"] is not True
        or pause["frozen_trigger"]["triggered"] is not True
    ):
        raise ValueError("v1 pause transcript is not admissible")

    spec = json.loads(V1_SPEC.read_text())
    spec["run_id"] = "cycles-016-017-fidelity-v2"
    spec["frozen_at_utc"] = frozen_at
    spec["preregistrations"] = [
        "data/cycles-016-017-preregistration-v2.json",
        "data/cycles-016-017-preregistration.json",
        "certificates/cycles-016-017-throughput-pause-v1.json",
        "data/workstream-b-production-freeze.json",
        "data/workstream-b-streaming-pilot-preregistration-v2.json",
    ]
    monitor = spec["throughput_monitor"]
    monitor["maximum_aggregate_ns_per_update"] = (
        MAXIMUM_NS_PER_UPDATE
    )
    monitor["drift_fraction"] = DRIFT_FRACTION
    monitor["amendment"] = (
        "Human-authorized VPS variance allowance; the seven-node-day "
        "hard budget and all certification gates are unchanged."
    )
    V2_SPEC.write_text(
        json.dumps(spec, indent=2, sort_keys=True) + "\n"
    )

    prereg = json.loads(V1_PREREG.read_text())
    prereg.pop("preregistration_sha256")
    prereg["schema"] = (
        "certified-qmc-cycles-016-017-production-"
        "preregistration-v2"
    )
    prereg["frozen_at_utc"] = frozen_at
    prereg["production_started"] = False
    prereg["predecessor"] = {
        "preregistration": {
            "path": str(V1_PREREG.relative_to(ROOT)),
            "sha256": digest(V1_PREREG),
        },
        "production_spec": {
            "path": str(V1_SPEC.relative_to(ROOT)),
            "sha256": digest(V1_SPEC),
        },
        "failed_partial_dataset": "artifacts/fidelity-v1",
        "pause_transcript": {
            "path": str(PAUSE.relative_to(ROOT)),
            "sha256": digest(PAUSE),
        },
        "disposition": "PRESERVED_DO_NOT_RESUME",
    }
    prereg["human_authorization"] = {
        "received_before_v2_measurement": True,
        "context": (
            "The production host is a VPS where performance "
            "fluctuation is expected."
        ),
        "authorized_change": (
            "Relax the throughput-drift rule while retaining an "
            "effective monitoring gate."
        ),
    }
    prereg["amendment"] = {
        "changed": {
            "throughput_drift_fraction": {
                "v1": "0.25",
                "v2": DRIFT_FRACTION,
            },
            "maximum_aggregate_ns_per_update": {
                "v1": "3.10342892905734250",
                "v2": MAXIMUM_NS_PER_UPDATE,
            },
            "output_dataset": {
                "v1": "artifacts/fidelity-v1",
                "v2": "artifacts/fidelity-v2",
            },
        },
        "unchanged": [
            "seven-node-day hard budget",
            "five-billion-update enforcement floor",
            "all input hashes and the 22-table grid",
            "plain __int128 kernel source and compiler flags",
            "work-prime schedule and two universal overflow primes",
            "manifest, selected-entry replay, and oracle gates",
            "post-run audit seed and selected oracle entries",
        ],
        "v2_alarm_boundary_projected_node_days": (
            "2.7037874722879594"
        ),
        "rationale": (
            "The v1 alarm fired at 3.653537 ns/update, while same-host "
            "single-process diagnostics remained below the original "
            "ceiling. A +75% VPS alarm admits observed orchestration "
            "variance yet preserves substantial margin below seven "
            "node-days."
        ),
    }
    prereg["production_spec"] = {
        "path": str(V2_SPEC.relative_to(ROOT)),
        "sha256": digest(V2_SPEC),
    }
    prereg["run_gate"]["maximum_aggregate_ns_per_update"] = (
        MAXIMUM_NS_PER_UPDATE
    )
    prereg["run_gate"]["throughput_drift_fraction"] = (
        DRIFT_FRACTION
    )
    prereg["preregistration_sha256"] = canonical_sha(prereg)
    V2_PREREG.write_text(
        json.dumps(prereg, indent=2, sort_keys=True) + "\n"
    )
    print(
        json.dumps(
            {
                "frozen_at_utc": frozen_at,
                "spec": str(V2_SPEC),
                "spec_sha256": digest(V2_SPEC),
                "preregistration": str(V2_PREREG),
                "preregistration_file_sha256": digest(V2_PREREG),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
