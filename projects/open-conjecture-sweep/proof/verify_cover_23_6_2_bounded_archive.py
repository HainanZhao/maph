#!/usr/bin/env python3
"""Verify the canonical files and terminal logs of the bounded C(23,6,2) run."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT / "discovery" / "out"
sys.path.insert(0, str(PROJECT / "discovery"))

from cover_23_6_2_bounded_experiment import make_branch  # noqa: E402
WAVES = {
    "cover-23-6-2-bounded-balanced-20260807": (
        "4",
        "222-double-disjoint",
        "222-double-share",
        "222-path",
        "222-path-edge",
        "222-star",
    ),
    "cover-23-6-2-wave3-20260807": (
        "222-triangle",
        "222-triple",
        "32-overlap0",
    ),
    "cover-23-6-2-wave4-20260807": (
        "32-overlap1",
        "32-overlap2",
    ),
}
PRECURSOR_SUMMARIES = (
    "cover-23-6-2-bounded-20260807",
    "cover-23-6-2-bounded-binary-20260807",
    "cover-23-6-2-bounded-decision-20260807",
)
EXPECTED_PRIORS = {
    "cover-23-6-2-wave3-20260807": {
        "core_seconds": 43300.0,
        "wall_seconds": 14500.0,
    },
    "cover-23-6-2-wave4-20260807": {
        "core_seconds": 63800.0,
        "wall_seconds": 21400.0,
    },
}
CURRENT_INPUTS = {
    "cover_23_6_2_bounded_experiment.py",
    "cover_23_6_2_encoding.md",
    "cover_23_6_2_excess_spectral.md",
    "cover_23_6_2_sat.py",
    "cover_23_6_2_star_cases.py",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_terminal_log(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="ascii", errors="strict")
    statuses = re.findall(r"^s (SATISFIABLE|UNSATISFIABLE|UNKNOWN)$", text, re.MULTILINE)
    process = re.findall(
        r"^c total process time since initialization:\s+([0-9.]+)\s+seconds$",
        text,
        re.MULTILINE,
    )
    real = re.findall(
        r"^c total real time since initialization:\s+([0-9.]+)\s+seconds$",
        text,
        re.MULTILINE,
    )
    rss = re.findall(
        r"^c maximum resident set size of process:\s+([0-9.]+)\s+MB$",
        text,
        re.MULTILINE,
    )
    conflicts = re.findall(r"^c conflicts:\s+([0-9]+)\s+", text, re.MULTILINE)
    decision_counts = re.findall(r"^c decisions:\s+([0-9]+)\s+", text, re.MULTILINE)
    exits = re.findall(r"^c exit ([0-9]+)$", text, re.MULTILINE)
    terminal_groups = (process, real, rss, conflicts, decision_counts, exits)
    if not any(terminal_groups):
        assert not statuses
        return {"status": "LIVE", "log_sha256": sha256(path)}
    assert all(len(group) == 1 for group in terminal_groups)
    exit_code = int(exits[0])
    if statuses == ["SATISFIABLE"]:
        assert exit_code == 10
        status = "SATISFIABLE"
    elif statuses == ["UNSATISFIABLE"]:
        assert exit_code == 20
        status = "UNSATISFIABLE"
    else:
        assert not statuses and exit_code == 0
        status = "UNKNOWN_SOLVER_LIMIT"
    return {
        "status": status,
        "process_seconds": float(process[0]),
        "real_seconds": float(real[0]),
        "maximum_rss_mb": float(rss[0]),
        "conflicts": int(conflicts[0]),
        "decisions": int(decision_counts[0]),
        "exit_code": exit_code,
        "log_sha256": sha256(path),
    }


def regenerate_cnf(branch: str) -> dict[str, object]:
    """Regenerate one DIMACS byte stream without retaining a derived file."""

    cnf, _ = make_branch(branch)
    digest = hashlib.sha256()
    digest.update(f"p cnf {cnf.nvars} {len(cnf.clauses)}\n".encode("ascii"))
    for clause in cnf.clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return {
        "clauses": len(cnf.clauses),
        "cnf_sha256": digest.hexdigest(),
        "variables": cnf.nvars,
    }


def relocated_path(recorded: str) -> Path:
    path = Path(recorded)
    if path.exists():
        return path
    marker = "/discovery/"
    assert marker in recorded
    suffix = recorded.split(marker, 1)[1]
    return PROJECT / "discovery" / suffix


def utc_seconds(started: str, finished: str) -> float:
    pattern = "%Y-%m-%dT%H:%M:%SZ"
    return (datetime.strptime(finished, pattern) - datetime.strptime(started, pattern)).total_seconds()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-live",
        action="store_true",
        help="accept live Wave 4 logs while validating all currently frozen evidence",
    )
    args = parser.parse_args()

    rows: dict[str, dict[str, object]] = {}
    summaries: dict[str, dict[str, object]] = {}
    precursors = {
        name: json.loads(
            (OUTPUT / name / "summary.json").read_text(encoding="utf-8")
        )
        for name in PRECURSOR_SUMMARIES
    }
    regenerated_cnfs: dict[str, dict[str, object]] = {}
    for wave, branches in WAVES.items():
        directory = OUTPUT / wave
        summary = json.loads((directory / "summary.json").read_text(encoding="utf-8"))
        summaries[wave] = summary
        assert set(branches).issubset(summary["branches"])
        if wave in EXPECTED_PRIORS:
            assert summary["prior_consumption"] == EXPECTED_PRIORS[wave]
        for branch in branches:
            state = summary["branches"][branch]
            regenerated_cnfs.setdefault(branch, regenerate_cnf(branch))
            assert regenerated_cnfs[branch] == {
                "clauses": state["clauses"],
                "cnf_sha256": state["cnf_sha256"],
                "variables": state["variables"],
            }
            log = directory / f"{branch}.solver.log"
            row = parse_terminal_log(log)
            row["wave"] = wave
            rows[branch] = row

    balanced_name = "cover-23-6-2-bounded-balanced-20260807"
    balanced_summary = summaries[balanced_name]

    initial = precursors[PRECURSOR_SUMMARIES[0]]
    binary = precursors[PRECURSOR_SUMMARIES[1]]
    decision = precursors[PRECURSOR_SUMMARIES[2]]
    assert initial["status"] == binary["status"] == decision["status"] == "INTERRUPTED"
    initial_wall = utc_seconds(initial["started_utc"], initial["finished_utc"])
    assert binary["prior_consumption"]["wall_seconds"] >= initial_wall
    assert binary["prior_consumption"]["core_seconds"] >= 3 * initial_wall
    assert decision["prior_consumption"]["wall_seconds"] >= binary["aggregate_wall_seconds"]
    assert decision["prior_consumption"]["core_seconds"] >= binary["aggregate_charged_seconds"]
    assert balanced_summary["prior_consumption"]["wall_seconds"] >= decision["aggregate_wall_seconds"]
    assert balanced_summary["prior_consumption"]["core_seconds"] >= decision["aggregate_charged_seconds"]

    cross_wave_matches = 0
    for wave in (
        "cover-23-6-2-wave3-20260807",
        "cover-23-6-2-wave4-20260807",
    ):
        for branch in WAVES[wave]:
            original = balanced_summary["branches"][branch]
            regenerated = summaries[wave]["branches"][branch]
            assert original["cnf_sha256"] == regenerated["cnf_sha256"]
            assert original["variables"] == regenerated["variables"]
            assert original["clauses"] == regenerated["clauses"]
            cross_wave_matches += 1

    assert len(rows) == 11
    final_branches = set(WAVES["cover-23-6-2-wave4-20260807"])
    assert all(
        rows[branch]["status"] == "UNKNOWN_SOLVER_LIMIT"
        for branch in set(rows).difference(final_branches)
    )
    live = sorted(branch for branch, row in rows.items() if row["status"] == "LIVE")
    if live:
        assert args.allow_live, (
            f"unfinished solver logs: {', '.join(live)}; terminal replay must wait"
        )
        assert live == ["32-overlap1", "32-overlap2"]
    for branch in set(rows).difference(live):
        assert rows[branch]["status"] in {
            "UNKNOWN_SOLVER_LIMIT",
            "SATISFIABLE",
            "UNSATISFIABLE",
        }

    wave4 = summaries["cover-23-6-2-wave4-20260807"]
    wave3 = summaries["cover-23-6-2-wave3-20260807"]
    balanced_rows = [rows[branch] for branch in WAVES[balanced_name]]
    wave3_rows = [rows[branch] for branch in WAVES["cover-23-6-2-wave3-20260807"]]
    assert wave3["prior_consumption"]["core_seconds"] >= (
        balanced_summary["prior_consumption"]["core_seconds"]
        + sum(row["real_seconds"] for row in balanced_rows)
    )
    assert wave3["prior_consumption"]["wall_seconds"] >= (
        balanced_summary["prior_consumption"]["wall_seconds"]
        + sum(row["real_seconds"] for row in balanced_rows) / 3
    )
    assert wave4["prior_consumption"]["core_seconds"] >= (
        wave3["prior_consumption"]["core_seconds"]
        + sum(row["real_seconds"] for row in wave3_rows)
    )
    assert wave4["prior_consumption"]["wall_seconds"] >= (
        wave3["prior_consumption"]["wall_seconds"]
        + max(row["real_seconds"] for row in wave3_rows)
    )
    assert set(wave4["selected_branches"]) == final_branches
    assert wave4["caps"] == {
        "branch_seconds": 7400,
        "core_seconds": 86400.0,
        "disk_bytes": 120259084288,
        "max_workers": 3,
        "memory_bytes": 10737418240,
        "system_disk_reserve_bytes": 5368709120,
        "wall_seconds": 28800.0,
    }
    for recorded, expected in wave4["frozen_inputs"].items():
        path = relocated_path(recorded)
        assert path.name in CURRENT_INPUTS
        assert sha256(path) == expected
    assert {Path(path).name for path in wave4["frozen_inputs"]} == CURRENT_INPUTS
    tool_checks: dict[str, str] = {}
    for label in ("solver", "checker"):
        recorded = wave4[label]
        path = Path(recorded)
        if not path.exists() and "/discovery/" in recorded:
            path = relocated_path(recorded)
        if path.exists():
            assert sha256(path) == wave4[f"{label}_sha256"]
            tool_checks[label] = "LOCAL_HASH_MATCH"
        else:
            tool_checks[label] = "RECORDED_HASH_ONLY"

    if not live:
        assert wave4["status"] != "RUNNING"
        assert "finished_utc" in wave4
        has_sat = any(row["status"] == "SATISFIABLE" for row in rows.values())
        all_unknown = all(
            row["status"] == "UNKNOWN_SOLVER_LIMIT" for row in rows.values()
        )
        wall_exhausted = (
            wave4["aggregate_wall_seconds"] >= wave4["caps"]["wall_seconds"]
        )
        compute_exhausted = (
            wave4["aggregate_charged_seconds"]
            >= wave4["caps"]["core_seconds"]
        )
        # If every internally limited solver exits during the same poll, the
        # coordinator's loop can empty naturally before assigning stop_reason.
        # Preserve the raw INCOMPLETE summary and derive the resource outcome
        # only when its own recorded aggregate meter proves that a cap was met.
        derived_terminal_status = wave4["status"]
        if (
            derived_terminal_status == "INCOMPLETE"
            and all_unknown
            and wall_exhausted
        ):
            derived_terminal_status = "WALL_CAP_DERIVED"
        if not has_sat:
            assert derived_terminal_status in {
                "WALL_CAP",
                "WALL_CAP_DERIVED",
                "COMPUTE_CAP",
            }
        if wave4["status"] == "WALL_CAP":
            assert wall_exhausted
        if wave4["status"] == "COMPUTE_CAP":
            assert compute_exhausted
        assert wave4["peak_rss_bytes"] < wave4["caps"]["memory_bytes"]
        assert wave4["peak_known_output_bytes"] < wave4["caps"]["disk_bytes"]
    else:
        derived_terminal_status = "LIVE"

    terminal_rows = [row for row in rows.values() if row["status"] != "LIVE"]
    print(
        json.dumps(
            {
                "branches": rows,
                "budget_chain": "CONSERVATIVE_PRIORS_PASS",
                "conflict_range": [
                    min(row["conflicts"] for row in terminal_rows),
                    max(row["conflicts"] for row in terminal_rows),
                ],
                "cross_wave_cnf_matches": cross_wave_matches,
                "decision_range": [
                    min(row["decisions"] for row in terminal_rows),
                    max(row["decisions"] for row in terminal_rows),
                ],
                "derived_wave4_status": derived_terminal_status,
                "live_branches": live,
                "regenerated_cnfs": len(regenerated_cnfs),
                "status": "ARCHIVE_LIVE_PREFIX_PASS" if live else "ARCHIVE_TERMINAL_PASS",
                "tool_checks": tool_checks,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
