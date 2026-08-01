#!/usr/bin/env python3
"""Measure the four preregistered Cycle-2 per-route replays fail-closed.

The deterministic configuration contains only commands and ceilings.  Runtime
and RSS observations are emitted only to an OBSERVED performance artifact.
This operational gate cannot promote G0.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "artifacts/cycle-2-g0-per-route-resource-gate-config-v1.json"
DEFAULT_OUTPUT = ROOT / "artifacts/cycle-2-g0-per-route-resource-gate-performance-v1.json"
TIME = Path("/usr/bin/time")
MAX_SECONDS = 60
MAX_RSS_KIB = 256 * 1024


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def config() -> dict[str, Any]:
    python = "python3"
    return {
        "artifact_id": "cycle-2-g0-per-route-resource-gate-config-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Deterministic operational gate configuration only. Passing these resource limits does not establish any mathematical theorem or G0 PASS.",
        "limits": {"wall_seconds_strictly_less_than": MAX_SECONDS, "max_rss_kib_strictly_less_than": MAX_RSS_KIB, "max_rss_mib_strictly_less_than": 256},
        "measurement": {"program": "/usr/bin/time", "arguments": ["-v"], "parse_fields": ["Elapsed (wall clock) time", "Maximum resident set size (kbytes)", "Exit status"]},
        "routes": [
            {"id": "stream-b-route-a-v3", "command": [python, "proof/audit_cycle2_stream_b_route_a_v3.py", "--check", "artifacts/cycle-2-stream-b-route-a-v3.json"], "sealed_source_check": "Route-A v3 check hashes and anchors its GM source input."},
            {"id": "stream-b-route-b-v1", "command": [python, "proof/replay_cycle2_stream_b_route_b.py", "--check", "artifacts/cycle-2-stream-b-route-b-v1.json"], "sealed_source_check": "Route-B v1 check verifies frozen sources and source anchors."},
            {"id": "stream-c-route-a-v5", "command": [python, "proof/replay_cycle2_stream_c_route_a_v5.py", "--check", "artifacts/cycle-2-stream-c-route-a-v5.json"], "sealed_source_check": "Route-A v5 check verifies official SWORD, official PDFs, metadata, source-closure v4, and mutool 1.23.10."},
            {"id": "stream-c-route-b-v5", "command": [python, "proof/replay_short_intervals_stream_c_route_b_v5.py", "--check"], "sealed_source_check": "Route-B v5 check invokes the official source checker and independent SWORD audit."},
        ],
        "required_outcome": "Every route command must exit zero, yield parseable GNU-time fields, have wall_seconds<60, and have max_rss_kib<262144. Any other result is fail-closed.",
        "non_promotion": "This gate does not claim G0 PASS; it only checks the preregistered per-route resource ceiling.",
    }


def render_config() -> str:
    return json.dumps(config(), sort_keys=True, indent=2) + "\n"


def elapsed_seconds(value: str) -> float:
    fields = value.strip().split(":")
    assert 1 <= len(fields) <= 3, f"unparseable elapsed time: {value!r}"
    seconds = float(fields[-1])
    if len(fields) >= 2:
        seconds += 60 * int(fields[-2])
    if len(fields) == 3:
        seconds += 3600 * int(fields[0])
    return seconds


def parse_time_report(text: str) -> tuple[float, int, int]:
    wall = re.search(r"^\s*Elapsed \(wall clock\) time \(h:mm:ss or m:ss\):\s*(.+)$", text, re.MULTILINE)
    rss = re.search(r"^\s*Maximum resident set size \(kbytes\):\s*(\d+)\s*$", text, re.MULTILINE)
    status = re.search(r"^\s*Exit status:\s*(\d+)\s*$", text, re.MULTILINE)
    assert wall and rss and status, "missing required /usr/bin/time -v field"
    return elapsed_seconds(wall.group(1)), int(rss.group(1)), int(status.group(1))


def version(command: list[str]) -> str:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return (result.stdout + result.stderr).strip()


def run_route(route: dict[str, Any]) -> dict[str, Any]:
    assert TIME.is_file(), f"required time program missing: {TIME}"
    with tempfile.TemporaryDirectory(prefix="g0-resource-") as temporary:
        report = Path(temporary) / "time-v.txt"
        result = subprocess.run([str(TIME), "-v", "-o", str(report), *route["command"]], cwd=ROOT, capture_output=True, text=True)
        timing = report.read_text(encoding="utf-8") if report.exists() else ""
    try:
        wall, rss, timed_exit = parse_time_report(timing)
        parse_error = None
    except (AssertionError, ValueError) as error:
        wall, rss, timed_exit, parse_error = None, None, None, str(error)
    passed = parse_error is None and result.returncode == 0 and timed_exit == 0 and wall is not None and rss is not None and wall < MAX_SECONDS and rss < MAX_RSS_KIB
    return {
        "id": route["id"],
        "epistemic_status": "OBSERVED",
        "gate_status": "PASS" if passed else "FAIL",
        "command": route["command"],
        "sealed_source_check": route["sealed_source_check"],
        "subprocess_returncode": result.returncode,
        "time_exit_status": timed_exit,
        "wall_seconds": None if wall is None else f"{wall:.6f}",
        "max_rss_kib": rss,
        "strict_limits": {"wall_seconds": f"< {MAX_SECONDS}", "max_rss_kib": f"< {MAX_RSS_KIB}"},
        "parse_error": parse_error,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "time_v_report": timing,
    }


def performance() -> dict[str, Any]:
    assert CONFIG.read_text(encoding="utf-8") == render_config(), "resource-gate config differs from deterministic harness; regenerate it"
    routes = config()["routes"]
    results = [run_route(route) for route in routes]
    return {
        "artifact_id": "cycle-2-g0-per-route-resource-gate-performance-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Host-specific runtime/RSS observations for the four preregistered route checks. They are operational evidence only and do not establish G0 PASS.",
        "config_sha256": sha256(CONFIG),
        "harness_sha256": sha256(Path(__file__)),
        "environment": {"python_executable": shutil.which("python3"), "python_version": sys.version, "python_implementation": platform.python_implementation(), "time_version": version([str(TIME), "--version"]), "mutool_version": version(["mutool", "-v"])},
        "limits": config()["limits"],
        "route_results": results,
        "resource_gate": {"gate_status": "PASS" if all(result["gate_status"] == "PASS" for result in results) else "FAIL", "non_promotion": "Even PASS is not G0 PASS; the analytic and reconciliation gates remain separately required."},
        "replay": {"write_command": "python3 projects/guth-maynard-zero-density/proof/run_cycle2_g0_resource_gate_v1.py --write-performance projects/guth-maynard-zero-density/artifacts/cycle-2-g0-per-route-resource-gate-performance-v1.json", "check_config_command": "python3 projects/guth-maynard-zero-density/proof/run_cycle2_g0_resource_gate_v1.py --check-config projects/guth-maynard-zero-density/artifacts/cycle-2-g0-per-route-resource-gate-config-v1.json"},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-config", type=Path, metavar="PATH")
    mode.add_argument("--check-config", type=Path, metavar="PATH")
    mode.add_argument("--write-performance", type=Path, metavar="PATH")
    args = parser.parse_args()
    if args.write_config:
        args.write_config.parent.mkdir(parents=True, exist_ok=True)
        args.write_config.write_text(render_config(), encoding="utf-8")
        return
    if args.check_config:
        if args.check_config.read_text(encoding="utf-8") != render_config():
            raise SystemExit("resource-gate config mismatch; regenerate with --write-config")
        return
    output = performance()
    args.write_performance.parent.mkdir(parents=True, exist_ok=True)
    args.write_performance.write_text(json.dumps(output, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    if output["resource_gate"]["gate_status"] != "PASS":
        raise SystemExit("G0 resource gate failed closed; inspect the performance artifact")


if __name__ == "__main__":
    main()
