#!/usr/bin/env python3
"""Aggregate-budget coordinator for the exhaustive C(23,6,2) SAT split.

This script is deliberately inert unless ``--execute`` and every resource
limit are supplied.  The eleven branches are the exhaustive canonical-star
orbits proved in ``cover_23_6_2_encoding.md``.  A SAT model is promoted only
after direct pair recounting.  An UNSAT result is promoted only after an
external DRAT checker accepts the retained CNF/proof pair.

The aggregate compute meter is conservative: it charges one core-second for
every second occupied by a solver/checker slot, plus coordinator CPU time.
Thus waits and I/O are charged as compute rather than undercounted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Any

from cover_23_6_2_sat import B, V, build as build_four, parse_model, verify
from cover_23_6_2_star_cases import SUPPORTS, build as build_case


BRANCHES = ("4", *sorted(SUPPORTS))
GIB = 1024**3
SYSTEM_DISK_RESERVE = 5 * GIB
POLL_SECONDS = 2.0
FROZEN_INPUTS = (
    Path(__file__),
    Path(__file__).with_name("cover_23_6_2_sat.py"),
    Path(__file__).with_name("cover_23_6_2_star_cases.py"),
    Path(__file__).with_name("cover_23_6_2_encoding.md"),
    Path(__file__).with_name("cover_23_6_2_excess_spectral.md"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def tree_rss_bytes(root_pids: list[int]) -> int:
    """Return Linux RSS for the supplied processes and their descendants."""
    parent: dict[int, int] = {}
    rss: dict[int, int] = {}
    page_size = os.sysconf("SC_PAGE_SIZE")
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            fields = (entry / "stat").read_text(encoding="ascii").split()
            parent[int(entry.name)] = int(fields[3])
            rss[int(entry.name)] = int(fields[23]) * page_size
        except (FileNotFoundError, PermissionError, IndexError, ValueError):
            continue
    wanted = set(root_pids)
    changed = True
    while changed:
        changed = False
        for pid, ppid in parent.items():
            if ppid in wanted and pid not in wanted:
                wanted.add(pid)
                changed = True
    return sum(rss.get(pid, 0) for pid in wanted)


def known_bytes(root: Path) -> int:
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())


def make_branch(branch: str):
    if branch == "4":
        cnf, variables = build_four(star_repeats=1)
    else:
        cnf, variables, _ = build_case(branch)
    return cnf, variables


def decode_and_verify(branch: str, model: Path) -> dict[str, Any]:
    _, variables = make_branch(branch)
    values = parse_model(model)
    if values is None:
        raise RuntimeError("UNSAT output passed to SAT decoder")
    blocks = [
        [point for point in range(V) if variables[block][point] in values]
        for block in range(B)
    ]
    checked = verify(blocks)
    if checked["status"] != "VERIFIED_20_BLOCK_COVER":
        raise RuntimeError(f"direct witness verification failed for {branch}")
    checked["branch"] = branch
    return checked


@dataclass
class Task:
    branch: str
    kind: str
    process: subprocess.Popen[bytes]
    stream: IO[bytes]
    started: float
    command: list[str]


def terminate(tasks: list[Task]) -> None:
    for task in tasks:
        if task.process.poll() is None:
            try:
                os.killpg(task.process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and any(
        task.process.poll() is None for task in tasks
    ):
        time.sleep(0.1)
    for task in tasks:
        if task.process.poll() is None:
            try:
                os.killpg(task.process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass


def launch(command: list[str], log: Path, branch: str, kind: str) -> Task:
    stream = log.open("wb")
    process = subprocess.Popen(
        command,
        stdout=stream,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    return Task(branch, kind, process, stream, time.monotonic(), command)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory", action="store_true", help="print the branch inventory and exit"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="run the experiment (inert without this explicit switch)",
    )
    parser.add_argument("--core-hours", type=float)
    parser.add_argument("--wall-hours", type=float)
    parser.add_argument("--prior-core-seconds", type=float, default=0.0)
    parser.add_argument("--prior-wall-seconds", type=float, default=0.0)
    parser.add_argument("--max-workers", type=int)
    parser.add_argument("--memory-gib", type=float)
    parser.add_argument("--disk-gib", type=float)
    parser.add_argument("--solver", type=Path)
    parser.add_argument("--checker", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def require_executable(path: Path | None, label: str) -> Path:
    if path is None:
        raise SystemExit(f"--{label} is required")
    resolved = Path(shutil.which(str(path)) or path).resolve()
    if not resolved.is_file() or not os.access(resolved, os.X_OK):
        raise SystemExit(f"{label} is not executable: {resolved}")
    return resolved


def validate_execution(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    required = {
        "core-hours": args.core_hours,
        "wall-hours": args.wall_hours,
        "max-workers": args.max_workers,
        "memory-gib": args.memory_gib,
        "disk-gib": args.disk_gib,
        "output": args.output,
    }
    missing = [name for name, value in required.items() if value is None]
    if missing:
        raise SystemExit("--execute requires: " + ", ".join(f"--{x}" for x in missing))
    if any(
        value <= 0
        for value in (args.core_hours, args.wall_hours, args.memory_gib, args.disk_gib)
    ):
        raise SystemExit("all resource caps must be positive")
    if args.prior_core_seconds < 0 or args.prior_wall_seconds < 0:
        raise SystemExit("prior resource use cannot be negative")
    remaining_core = args.core_hours * 3600 - args.prior_core_seconds
    remaining_wall = args.wall_hours * 3600 - args.prior_wall_seconds
    if remaining_core <= 0 or remaining_wall <= 0:
        raise SystemExit("prior resource use exhausts the fixed allocation")
    if args.max_workers < 1 or args.max_workers > max(1, (os.cpu_count() or 1) - 1):
        raise SystemExit("--max-workers must leave at least one host CPU unused")
    if args.max_workers * remaining_wall > remaining_core + 1e-9:
        raise SystemExit(
            "max-workers * remaining wall time exceeds the remaining core budget"
        )
    solver = require_executable(args.solver, "solver")
    checker = require_executable(args.checker, "checker")
    output = args.output.resolve()
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing output directory: {output}")
    free = shutil.disk_usage(output.parent.resolve()).free
    requested = int(args.disk_gib * GIB)
    if requested > free - SYSTEM_DISK_RESERVE:
        raise SystemExit(
            f"disk cap {requested} exceeds free-space-safe cap "
            f"{max(0, free - SYSTEM_DISK_RESERVE)}"
        )
    return solver, checker, output


def main() -> None:
    args = parse_args()
    if args.inventory or not args.execute:
        print(json.dumps({"branch_count": len(BRANCHES), "branches": BRANCHES}, indent=2))
        if not args.execute:
            return

    solver, checker, output = validate_execution(args)
    output.mkdir(parents=False)
    started_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    experiment_start = time.monotonic()
    coordinator_cpu_start = time.process_time()
    caps = {
        "core_seconds": args.core_hours * 3600,
        "wall_seconds": args.wall_hours * 3600,
        "max_workers": args.max_workers,
        "memory_bytes": int(args.memory_gib * GIB),
        "disk_bytes": int(args.disk_gib * GIB),
        "system_disk_reserve_bytes": SYSTEM_DISK_RESERVE,
    }
    prior = {
        "core_seconds": args.prior_core_seconds,
        "wall_seconds": args.prior_wall_seconds,
    }
    state: dict[str, Any] = {
        "claim_boundary": (
            "SAT requires direct pair verification; UNSAT requires the external "
            "checker; limits or incomplete branches decide neither covering number"
        ),
        "caps": caps,
        "prior_consumption": prior,
        "started_utc": started_utc,
        "solver": str(solver),
        "solver_sha256": sha256(solver),
        "checker": str(checker),
        "checker_sha256": sha256(checker),
        "command": [str(value) for value in os.sys.argv],
        "frozen_inputs": {
            str(path.resolve()): sha256(path.resolve()) for path in FROZEN_INPUTS
        },
        "python": os.sys.version,
        "branches": {},
        "status": "RUNNING",
    }
    atomic_json(output / "summary.json", state)
    peak_rss_bytes = tree_rss_bytes([os.getpid()])
    peak_known_output_bytes = known_bytes(output)

    # CNF construction is sequential so the encoder's transient Python memory
    # is never multiplied by worker count.
    for branch in BRANCHES:
        cnf, _ = make_branch(branch)
        cnf_path = output / f"{branch}.cnf"
        cnf.write(cnf_path)
        state["branches"][branch] = {
            "clauses": len(cnf.clauses),
            "variables": cnf.nvars,
            "cnf": cnf_path.name,
            "cnf_sha256": sha256(cnf_path),
            "status": "QUEUED",
        }
        del cnf
        encoding_rss = tree_rss_bytes([os.getpid()])
        peak_rss_bytes = max(peak_rss_bytes, encoding_rss)
        peak_known_output_bytes = max(peak_known_output_bytes, known_bytes(output))
        if encoding_rss > caps["memory_bytes"]:
            state["status"] = "MEMORY_CAP_DURING_ENCODING"
            atomic_json(output / "summary.json", state)
            raise SystemExit("aggregate memory cap reached during CNF construction")
        if known_bytes(output) > caps["disk_bytes"]:
            state["status"] = "DISK_CAP_DURING_ENCODING"
            atomic_json(output / "summary.json", state)
            raise SystemExit("aggregate disk cap reached during CNF construction")
        atomic_json(output / "summary.json", state)

    queued: list[tuple[str, str]] = [(branch, "solve") for branch in BRANCHES]
    active: list[Task] = []
    charged_slot_seconds = 0.0
    stop_reason: str | None = None
    peak_rss_bytes = max(peak_rss_bytes, tree_rss_bytes([os.getpid()]))

    try:
        while queued or active:
            now = time.monotonic()
            current_wall_used = now - experiment_start
            wall_used = prior["wall_seconds"] + current_wall_used
            running_charge = sum(now - task.started for task in active)
            compute_used = (
                prior["core_seconds"]
                + charged_slot_seconds
                + running_charge
                + (time.process_time() - coordinator_cpu_start)
            )
            rss = tree_rss_bytes([os.getpid(), *[t.process.pid for t in active]])
            disk = known_bytes(output)
            free = shutil.disk_usage(output).free
            peak_rss_bytes = max(peak_rss_bytes, rss)
            peak_known_output_bytes = max(peak_known_output_bytes, disk)
            if wall_used >= caps["wall_seconds"]:
                stop_reason = "WALL_CAP"
            elif compute_used >= caps["core_seconds"]:
                stop_reason = "COMPUTE_CAP"
            elif rss >= caps["memory_bytes"]:
                stop_reason = "MEMORY_CAP"
            elif disk >= caps["disk_bytes"]:
                stop_reason = "DISK_CAP"
            elif free < SYSTEM_DISK_RESERVE:
                stop_reason = "SYSTEM_DISK_RESERVE"
            if stop_reason:
                terminate(active)
                break

            while queued and len(active) < caps["max_workers"]:
                branch, kind = queued.pop(0)
                branch_state = state["branches"][branch]
                remaining_wall = max(1, int(caps["wall_seconds"] - wall_used))
                if kind == "solve":
                    proof = output / f"{branch}.drat"
                    log = output / f"{branch}.solver.log"
                    command = [
                        str(solver),
                        "-t",
                        str(remaining_wall),
                        str(output / branch_state["cnf"]),
                        str(proof),
                    ]
                    branch_state.update(
                        {"status": "SOLVING", "proof": proof.name, "solver_log": log.name}
                    )
                else:
                    log = output / f"{branch}.checker.log"
                    command = [
                        str(checker),
                        str(output / branch_state["cnf"]),
                        str(output / branch_state["proof"]),
                        "-t",
                        str(remaining_wall),
                    ]
                    branch_state.update({"status": "CHECKING_UNSAT", "checker_log": log.name})
                task = launch(command, log, branch, kind)
                active.append(task)
                atomic_json(output / "summary.json", state)

            time.sleep(POLL_SECONDS)
            finished = [task for task in active if task.process.poll() is not None]
            for task in finished:
                task.stream.close()
                elapsed = time.monotonic() - task.started
                charged_slot_seconds += elapsed
                active.remove(task)
                branch_state = state["branches"][task.branch]
                branch_state.setdefault("commands", []).append(task.command)
                branch_state.setdefault("charged_slot_seconds", 0.0)
                branch_state["charged_slot_seconds"] += elapsed
                returncode = task.process.returncode
                if task.kind == "solve":
                    if returncode == 10:
                        witness = decode_and_verify(
                            task.branch, output / branch_state["solver_log"]
                        )
                        witness_path = output / f"{task.branch}.witness.json"
                        atomic_json(witness_path, witness)
                        branch_state.update(
                            {
                                "status": "SAT_VERIFIED",
                                "witness": witness_path.name,
                                "witness_sha256": sha256(witness_path),
                            }
                        )
                        stop_reason = "VERIFIED_20_BLOCK_COVER"
                        terminate(active)
                        queued.clear()
                        break
                    if returncode == 20:
                        proof_path = output / branch_state["proof"]
                        branch_state["proof_sha256"] = sha256(proof_path)
                        branch_state["status"] = "UNSAT_PROOF_PENDING_CHECK"
                        queued.insert(0, (task.branch, "check"))
                    elif returncode == 0:
                        branch_state["status"] = "UNKNOWN_SOLVER_LIMIT"
                    else:
                        branch_state.update(
                            {"status": "SOLVER_ERROR", "returncode": returncode}
                        )
                        stop_reason = "SOLVER_ERROR"
                        terminate(active)
                        queued.clear()
                        break
                else:
                    if returncode == 0:
                        branch_state["status"] = "UNSAT_CERTIFIED"
                    else:
                        branch_state.update(
                            {"status": "UNSAT_CHECK_FAILED", "returncode": returncode}
                        )
                        stop_reason = "UNSAT_CHECK_FAILED"
                        terminate(active)
                        queued.clear()
                        break
                atomic_json(output / "summary.json", state)
            if stop_reason:
                break
    except BaseException:
        terminate(active)
        interrupted_now = time.monotonic()
        interrupted_slot_seconds = charged_slot_seconds + sum(
            interrupted_now - task.started for task in active
        )
        state["status"] = "INTERRUPTED"
        state["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        state["current_wall_seconds"] = interrupted_now - experiment_start
        state["aggregate_wall_seconds"] = (
            prior["wall_seconds"] + state["current_wall_seconds"]
        )
        state["current_charged_slot_seconds"] = interrupted_slot_seconds
        state["aggregate_charged_seconds"] = (
            prior["core_seconds"]
            + interrupted_slot_seconds
            + (time.process_time() - coordinator_cpu_start)
        )
        state["known_output_bytes"] = known_bytes(output)
        state["peak_known_output_bytes"] = max(
            peak_known_output_bytes, state["known_output_bytes"]
        )
        state["peak_rss_bytes"] = peak_rss_bytes
        atomic_json(output / "summary.json", state)
        raise
    finally:
        for task in active:
            task.stream.close()

    final_now = time.monotonic()
    charged_slot_seconds += sum(final_now - task.started for task in active)
    final_output_bytes = known_bytes(output)
    peak_known_output_bytes = max(peak_known_output_bytes, final_output_bytes)
    if stop_reason:
        for task in active:
            branch_state = state["branches"][task.branch]
            if branch_state["status"] in {"SOLVING", "CHECKING_UNSAT"}:
                branch_state["status"] = f"INTERRUPTED_BY_{stop_reason}"
        for branch, _ in queued:
            branch_state = state["branches"][branch]
            if branch_state["status"] == "QUEUED":
                branch_state["status"] = f"NOT_STARTED_BEFORE_{stop_reason}"
    statuses = [entry["status"] for entry in state["branches"].values()]
    if stop_reason == "VERIFIED_20_BLOCK_COVER":
        final_status = stop_reason
    elif statuses and all(status == "UNSAT_CERTIFIED" for status in statuses):
        final_status = "ALL_BRANCHES_UNSAT_CERTIFIED"
    elif stop_reason:
        final_status = stop_reason
    else:
        final_status = "INCOMPLETE"
    state.update(
        {
            "status": final_status,
            "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "current_wall_seconds": final_now - experiment_start,
            "aggregate_wall_seconds": (
                prior["wall_seconds"] + final_now - experiment_start
            ),
            "current_charged_slot_seconds": charged_slot_seconds,
            "aggregate_charged_seconds": (
                prior["core_seconds"]
                + charged_slot_seconds
                + time.process_time()
                - coordinator_cpu_start
            ),
            "coordinator_cpu_seconds": time.process_time() - coordinator_cpu_start,
            "known_output_bytes": final_output_bytes,
            "peak_known_output_bytes": peak_known_output_bytes,
            "peak_rss_bytes": peak_rss_bytes,
        }
    )
    atomic_json(output / "summary.json", state)
    print(json.dumps(state, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
