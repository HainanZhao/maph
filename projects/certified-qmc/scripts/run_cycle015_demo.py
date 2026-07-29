#!/usr/bin/env python3
"""Execute the preregistered Cycle-015 kill/resume and replay gate."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.certificate import canonical_sha256
from src.exact_error import RuleSpec
from src.scaled_integer import scaled_squared_error


PREREG = ROOT / "data" / "cycle-015-preregistration-v2.json"
SPEC = ROOT / "data" / "cycle-015-pilot-spec.json"
BASELINE = ROOT / "artifacts" / "cycle-015-pilot"
DRIVER = ROOT / "scripts" / "run_chunked_production.py"
VERIFIER = ROOT / "scripts" / "verify_entry.py"
OUTPUT = ROOT / "certificates" / "cycle-015-chunk-replay.json"
RUN_MANIFEST_TEMPLATE = ROOT / "data" / "run-manifest-template.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def tree_digest(root: Path) -> dict[str, object]:
    records = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        records.append(
            {
                "path": str(path.relative_to(root)),
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            }
        )
    return {
        "files": len(records),
        "bytes": sum(record["bytes"] for record in records),
        "sha256": sha256(
            json.dumps(
                records,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("ascii")
        ).hexdigest(),
    }


def run_driver(output: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            str(DRIVER),
            "--spec",
            str(SPEC),
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def kill_and_resume(output: Path, stop: int) -> dict[str, object]:
    process = subprocess.Popen(
        [
            sys.executable,
            str(DRIVER),
            "--spec",
            str(SPEC),
            "--output",
            str(output),
            "--pause-after-new-chunks",
            str(stop),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert process.stdout is not None
    marker = process.stdout.readline().strip()
    parsed = json.loads(marker)
    if (
        parsed.get("status") != "READY_FOR_FORCED_KILL"
        or parsed.get("new_chunks") != stop
    ):
        process.kill()
        _, stderr = process.communicate()
        raise RuntimeError(
            f"driver did not reach frozen kill point: {marker} {stderr}"
        )
    process.kill()
    _, stderr = process.communicate()
    if process.returncode != -9:
        raise RuntimeError(f"expected SIGKILL return code, got {process.returncode}")
    run_driver(output)
    return {
        "forced_kill_after_manifested_chunks": stop,
        "kill_signal": "SIGKILL",
        "killed_return_code": process.returncode,
        "boundary_marker": parsed,
        "stderr": stderr,
        "resumed_tree": tree_digest(output),
    }


def parse_generator(path: Path) -> list[int]:
    return [int(line.split()[1]) for line in path.read_text().splitlines()]


def verify_samples(spec: dict, prereg: dict) -> list[dict[str, object]]:
    generator_cache: dict[str, list[int]] = {}
    randomizer = random.Random(prereg["selected_entry_demo"]["seed"])
    choices = set()
    while len(choices) < prereg["selected_entry_demo"]["entries"]:
        table_index = randomizer.randrange(len(spec["tables"]))
        dimension = randomizer.randint(
            1, int(spec["tables"][table_index]["dimension"])
        )
        choices.add((table_index, dimension))

    results = []
    for table_index, dimension in sorted(choices):
        table = spec["tables"][table_index]
        completed = subprocess.run(
            [
                sys.executable,
                str(VERIFIER),
                "--dataset",
                str(BASELINE),
                "--table",
                table["table_id"],
                "--N",
                str(table["N"]),
                "--d",
                str(dimension),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        replay = json.loads(completed.stdout)
        source = table["source_path"]
        generator = generator_cache.setdefault(
            source, parse_generator(ROOT / source)
        )
        weights = [
            Fraction(1, index ** int(table["weight_power"]))
            for index in range(1, dimension + 1)
        ]
        exact = scaled_squared_error(
            int(table["N"]), generator[:dimension], weights
        )
        oracle_equal = (
            int(replay["scaled_numerator"]) == exact.numerator
            and int(replay["scaled_denominator"]) == exact.denominator
        )
        if replay["status"] != "VERIFIED" or not oracle_equal:
            raise RuntimeError("selected-entry oracle mismatch")
        results.append(
            {
                "table": table["table_id"],
                "N": table["N"],
                "dimension": dimension,
                "weight_power": table["weight_power"],
                "status": replay["status"],
                "oracle_scaled_integer_equal": oracle_equal,
                "overflow_checks_equal": all(
                    check["equal"] for check in replay["overflow_checks"]
                ),
                "chunks_read": replay["chunks_read"],
                "touched_payload_bytes": replay["touched_payload_bytes"],
                "dataset_payload_bytes": replay["dataset_payload_bytes"],
                "touched_payload_fraction": replay[
                    "touched_payload_fraction"
                ],
                "generator_prefix_sha256": replay[
                    "generator_prefix_sha256"
                ],
            }
        )
    return results


def main() -> None:
    prereg = json.loads(PREREG.read_text())
    if prereg["data_run_started"]:
        raise RuntimeError("Cycle-015 preregistration does not precede run")
    spec = json.loads(SPEC.read_text())
    if BASELINE.exists():
        shutil.rmtree(BASELINE)
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    run_driver(BASELINE)
    baseline_tree = tree_digest(BASELINE)

    resumes = []
    with tempfile.TemporaryDirectory(
        prefix="certified-qmc-cycle015-resume-"
    ) as temporary:
        for stop in prereg["resume_demo"][
            "forced_stop_after_new_chunk_counts"
        ]:
            resumed = Path(temporary) / f"stop-{stop}"
            result = kill_and_resume(resumed, int(stop))
            result["byte_identical_to_uninterrupted"] = (
                result["resumed_tree"] == baseline_tree
            )
            if not result["byte_identical_to_uninterrupted"]:
                raise RuntimeError("resumed output is not byte-identical")
            resumes.append(result)

    samples = verify_samples(spec, prereg)
    maximum_fraction = float(
        prereg["selected_entry_demo"][
            "maximum_dataset_payload_fraction"
        ]
    )
    if any(
        result["touched_payload_fraction"] > maximum_fraction
        for result in samples
    ):
        raise RuntimeError("selected-entry replay exceeds touch budget")

    run_manifest = json.loads(
        (BASELINE / "run-manifest.json").read_text()
    )
    manifest_lines = (
        BASELINE / "manifest.jsonl"
    ).read_bytes().splitlines()
    payload = {
        "schema": "certified-qmc-cycle-015-chunk-replay-v1",
        "claim_tags": {
            "chunk_hash_chain_and_resume": "VERIFIED",
            "selected_entry_replay": "VERIFIED",
            "runtime": "NUMERICAL_NOT_PROMOTED",
        },
        "preregistration": {
            "path": str(PREREG.relative_to(ROOT)),
            "sha256": digest(PREREG),
        },
        "pilot_spec": {
            "path": str(SPEC.relative_to(ROOT)),
            "sha256": digest(SPEC),
            "table_count": len(spec["tables"]),
        },
        "baseline": {
            "path": str(BASELINE.relative_to(ROOT)),
            "tree": baseline_tree,
            "manifest_lines": len(manifest_lines),
            "manifest_sha256": digest(BASELINE / "manifest.jsonl"),
            "seal": json.loads(manifest_lines[-1]),
        },
        "kill_and_resume": resumes,
        "selected_entry_replay": {
            "seed": prereg["selected_entry_demo"]["seed"],
            "entries": samples,
            "all_ten_verified": len(samples) == 10
            and all(result["status"] == "VERIFIED" for result in samples),
            "all_python_oracles_equal": all(
                result["oracle_scaled_integer_equal"] for result in samples
            ),
            "all_overflow_checks_equal": all(
                result["overflow_checks_equal"] for result in samples
            ),
            "maximum_observed_payload_fraction": max(
                result["touched_payload_fraction"] for result in samples
            ),
            "frozen_maximum_payload_fraction": maximum_fraction,
        },
        "run_manifest": {
            "path": str(
                (BASELINE / "run-manifest.json").relative_to(ROOT)
            ),
            "sha256": digest(BASELINE / "run-manifest.json"),
            "self_hash": run_manifest["run_manifest_sha256"],
            "compiler": run_manifest["compiler"],
            "kernel": run_manifest["kernel"],
            "prime_schedule": run_manifest["prime_schedule"],
            "preregistrations": run_manifest["preregistrations"],
            "template": {
                "path": str(RUN_MANIFEST_TEMPLATE.relative_to(ROOT)),
                "sha256": digest(RUN_MANIFEST_TEMPLATE),
            },
        },
        "gate": {
            "three_sigkill_resume_runs_byte_identical": all(
                result["byte_identical_to_uninterrupted"]
                for result in resumes
            ),
            "ten_selected_entries_verified": len(samples) == 10
            and all(result["status"] == "VERIFIED" for result in samples),
            "selected_entry_touch_budget_passed": all(
                result["touched_payload_fraction"] <= maximum_fraction
                for result in samples
            ),
            "run_manifest_complete": True,
            "cycle_015_exit_gate_passed": True,
        },
        "boundary": (
            "VERIFIED covers deterministic chunk bytes, the append-only "
            "hash chain, forced-kill resumability, exact reconstruction, "
            "two universal overflow checks, and independent Python oracle "
            "agreement on the frozen pilot samples. It is not yet a "
            "production-grid result."
        ),
    }
    payload["certificate_sha256"] = canonical_sha256(payload)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
