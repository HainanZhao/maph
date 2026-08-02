#!/usr/bin/env python3
"""Rebuild and query a project index of immutable cycle records.

The database is deliberately derived state.  The version-controlled sources of
truth are artifacts/cycle-*.json and the linked docs/, proof/, and tests/ files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterator

try:
    import duckdb
except ModuleNotFoundError as exc:  # pragma: no cover - depends on local setup
    raise SystemExit(
        "DuckDB is required. Create .venv and run .venv/bin/pip install -r "
        "requirements-research.txt."
    ) from exc


ROOT: Path
ARTIFACTS: Path
DATABASE: Path
STATUS: Path
LEGACY_EXCEPTIONS: Path
CYCLE_RE: re.Pattern[str]
PROFILE: dict[str, Any]
VALID_TAGS = {"PROVED", "CERTIFIED_NUMERICAL", "RECOGNIZED", "OBSERVED", "CONJECTURED"}


def configure(profile_path: Path) -> None:
    """Load the only project-specific part: paths and status presentation."""
    global ROOT, ARTIFACTS, DATABASE, STATUS, LEGACY_EXCEPTIONS, CYCLE_RE, PROFILE
    profile_path = profile_path.resolve()
    PROFILE = json.loads(profile_path.read_text())
    ROOT = profile_path.parent
    ARTIFACTS = ROOT / PROFILE["artifact_glob"].split("/")[0]
    DATABASE = ROOT / PROFILE["database_path"]
    STATUS = ROOT / PROFILE["status_path"]
    LEGACY_EXCEPTIONS = ROOT / PROFILE["legacy_exceptions_path"]
    CYCLE_RE = re.compile(PROFILE.get("cycle_pattern", r"^cycle-(\d+)(?:-|$)"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact_paths() -> list[Path]:
    return sorted(ROOT.glob(PROFILE["artifact_glob"]))


def tracked_artifact_paths() -> set[str]:
    """Return cycle artifact paths present in the Git index (staged counts)."""
    result = subprocess.run(
        ["git", "ls-files", "--", PROFILE["artifact_glob"]],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return {line for line in result.stdout.splitlines() if line}


def legacy_exception_data() -> dict[str, Any]:
    return json.loads(LEGACY_EXCEPTIONS.read_text())


def legacy_evidence_exceptions() -> dict[tuple[str, str, str], str]:
    data = legacy_exception_data()
    return {
        (row["artifact_id"], row["evidence_key"], row["path"]): row["reason"]
        for row in data["evidence_exceptions"]
    }


def cycle_number(artifact_id: str) -> int | None:
    match = CYCLE_RE.match(artifact_id)
    return int(match.group(1)) if match else None


def text_of(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def tagged_claims(value: Any, prefix: str = "") -> Iterator[tuple[str, str, str]]:
    """Yield every explicitly tagged claim, retaining its JSON location."""
    if isinstance(value, dict):
        tag = value.get("epistemic_status")
        if tag in VALID_TAGS:
            statement = value.get("statement") or value.get("boundary") or text_of(value)
            yield prefix or "artifact", tag, str(statement)
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            yield from tagged_claims(child, child_prefix)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from tagged_claims(child, f"{prefix}[{index}]")


def create_schema(con: duckdb.DuckDBPyConnection) -> None:
    con.execute("""
        CREATE TABLE artifacts (
          artifact_id VARCHAR PRIMARY KEY,
          cycle_number INTEGER,
          artifact_path VARCHAR NOT NULL,
          artifact_sha256 VARCHAR NOT NULL,
          epistemic_status VARCHAR,
          status VARCHAR,
          claim_boundary VARCHAR,
          remaining_target VARCHAR,
          replay_check VARCHAR,
          replay_test VARCHAR,
          replay_write VARCHAR,
          sealer_path VARCHAR,
          sealer_sha256 VARCHAR
        );
        CREATE TABLE claims (
          artifact_id VARCHAR NOT NULL,
          json_path VARCHAR NOT NULL,
          epistemic_status VARCHAR NOT NULL,
          statement VARCHAR NOT NULL,
          PRIMARY KEY (artifact_id, json_path)
        );
        CREATE TABLE evidence (
          artifact_id VARCHAR NOT NULL,
          evidence_key VARCHAR NOT NULL,
          path VARCHAR NOT NULL,
          sha256 VARCHAR NOT NULL,
          exists_now BOOLEAN NOT NULL,
          sha256_matches BOOLEAN,
          PRIMARY KEY (artifact_id, evidence_key)
        );
        CREATE TABLE dependencies (
          artifact_id VARCHAR NOT NULL,
          dependency_key VARCHAR NOT NULL,
          dependency_artifact_id VARCHAR,
          PRIMARY KEY (artifact_id, dependency_key)
        );
    """)


def rebuild(database: Path | None = None) -> None:
    database = database or DATABASE
    database.parent.mkdir(parents=True, exist_ok=True)
    if database.exists():
        database.unlink()
    con = duckdb.connect(str(database))
    create_schema(con)
    con.execute("BEGIN TRANSACTION")
    seen: set[str] = set()
    artifact_rows: list[list[Any]] = []
    claim_rows: list[list[str]] = []
    evidence_rows: list[list[Any]] = []
    dependency_rows: list[list[str | None]] = []
    for path in artifact_paths():
        data = json.loads(path.read_text())
        # The immutable filename is the stable record identifier.  A few
        # legacy artifacts reused an internal artifact_id across corrections,
        # so that field cannot serve as a primary key.
        artifact_id = path.stem
        if artifact_id in seen:
            raise ValueError(f"duplicate artifact_id: {artifact_id}")
        seen.add(artifact_id)
        replay = data.get("replay", {})
        target = data.get("remaining_target", {})
        sealer = data.get("sealer", {})
        artifact_rows.append([
            artifact_id, cycle_number(artifact_id), str(path.relative_to(ROOT)), sha256(path),
            data.get("epistemic_status"), data.get("status"), data.get("claim_boundary"),
            target.get("statement") if isinstance(target, dict) else text_of(target),
            replay.get("check_command"), replay.get("test_command"), replay.get("write_command"),
            sealer.get("path"), sealer.get("sha256"),
        ])
        for json_path, tag, statement in tagged_claims(data):
            claim_rows.append([artifact_id, json_path, tag, statement])
        for key, item in data.get("frozen_hashes", {}).items():
            if not isinstance(item, dict) or "path" not in item or "sha256" not in item:
                continue
            evidence_path = ROOT / item["path"]
            exists = evidence_path.is_file()
            actual = sha256(evidence_path) if exists else None
            evidence_rows.append([artifact_id, key, item["path"], item["sha256"], exists, actual == item["sha256"] if exists else None])
            dep = item["path"] if item["path"].startswith("artifacts/") else None
            dependency_rows.append([artifact_id, key, Path(dep).stem if dep else None])
    con.executemany("INSERT INTO artifacts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", artifact_rows)
    con.executemany("INSERT INTO claims VALUES (?, ?, ?, ?)", claim_rows)
    con.executemany("INSERT INTO evidence VALUES (?, ?, ?, ?, ?, ?)", evidence_rows)
    con.executemany("INSERT INTO dependencies VALUES (?, ?, ?)", dependency_rows)
    con.execute("COMMIT")
    con.close()


def connect() -> duckdb.DuckDBPyConnection:
    if not DATABASE.exists():
        rebuild()
    return duckdb.connect(str(DATABASE), read_only=True)


def render_status(con: duckdb.DuckDBPyConnection) -> str:
    count = con.execute("SELECT count(*) FROM artifacts").fetchone()[0]
    tracked_count = len(tracked_artifact_paths())
    latest = con.execute("""
        SELECT artifact_id, cycle_number, epistemic_status, status, claim_boundary, remaining_target
        FROM artifacts ORDER BY cycle_number DESC NULLS LAST, artifact_id DESC LIMIT 1
    """).fetchone()
    artifact_tags = con.execute("SELECT coalesce(epistemic_status, 'LEGACY_UNTAGGED'), count(*) FROM artifacts GROUP BY 1 ORDER BY 1").fetchall()
    indexed_fields = con.execute("SELECT count(*) FROM claims").fetchone()[0]
    recent = con.execute("""
        SELECT cycle_number, artifact_id, epistemic_status, status, remaining_target
        FROM artifacts ORDER BY cycle_number DESC NULLS LAST, artifact_id DESC LIMIT 8
    """).fetchall()
    handoff = PROFILE.get("cold_start_handoff", {})
    lines = [
        PROFILE.get("status_title", "Research status (generated)"),
        "",
        "Do not edit this file. Rebuild with `tools/research_records.py --project <profile> rebuild`.",
        "Canonical evidence is the Git-tracked per-cycle artifact and its linked files; `.research/index.duckdb` is a local derived index.",
        "",
    ]
    if handoff:
        lines += [
            "## Cold-start handoff",
            "",
            f"- Project outcome ({handoff['project_outcome']['epistemic_status']}): {handoff['project_outcome']['statement']}",
            f"- Why the active gate matters ({handoff['why_active_gate_matters']['epistemic_status']}): {handoff['why_active_gate_matters']['statement']}",
            f"- Progress criterion ({handoff['progress_criterion']['epistemic_status']}): {handoff['progress_criterion']['statement']}",
            f"- Explicitly deferred: {handoff['deferred_work']}",
            "",
            "### Start here (from this project directory)",
            "",
            *[f"- `{command}`" for command in handoff["start_commands"]],
            "",
            "Read the listed record and its linked preregistration, proof document, conventions, builder, and test before changing mathematics or code. Do not infer a theorem from this handoff; its claim tags and boundaries are in the canonical record.",
            "",
        ]
    lines += [
        "## Index coverage",
        "",
        f"- Cycle artifact files found in the working tree: {count}",
        f"- Cycle artifacts present in the Git index: {tracked_count}",
        "- Artifacts by top-level epistemic status: " + ", ".join(f"{tag}={number}" for tag, number in artifact_tags),
        f"- Recursively tagged fields indexed for search (not independent claims): {indexed_fields}",
        "",
        "## Current gate",
        "",
        f"- Latest record: `{latest[0]}` (Cycle {latest[1]}, `{latest[2]}`)",
        f"- Status: `{latest[3]}`",
        f"- Boundary: {latest[4]}",
        f"- Next mathematical target: {latest[5]}",
        "",
        "## Recent sealed records",
        "",
        "| Cycle | Record | Tag | Gate | Next target |",
        "|---:|---|---|---|---|",
    ]
    for number, artifact_id, tag, gate, target in recent:
        lines.append(f"| {number} | `{artifact_id}` | `{tag}` | `{gate}` | {target} |")
    lines += [
        "",
        "## Useful queries",
        "",
        "```sh",
        *PROFILE.get("query_examples", []),
        "```",
        "",
    ]
    return "\n".join(lines)


def check(con: duckdb.DuckDBPyConnection, include_acknowledged: bool = False) -> int:
    artifact_count = con.execute("SELECT count(*) FROM artifacts").fetchone()[0]
    source_count = len(artifact_paths())
    bad = con.execute("SELECT artifact_id, evidence_key, path FROM evidence WHERE NOT exists_now OR sha256_matches IS NOT TRUE").fetchall()
    untagged = con.execute("SELECT artifact_id FROM artifacts WHERE epistemic_status IS NULL OR epistemic_status NOT IN ('PROVED','CERTIFIED_NUMERICAL','RECOGNIZED','OBSERVED','CONJECTURED')").fetchall()
    exceptions = legacy_evidence_exceptions()
    allowed_untagged = set(legacy_exception_data()["untagged_artifacts"])
    acknowledged = [row for row in bad if tuple(row) in exceptions]
    unacknowledged = [row for row in bad if tuple(row) not in exceptions]
    untagged_ids = {row[0] for row in untagged}
    unexpected_untagged = sorted(untagged_ids - allowed_untagged)
    missing_legacy_untagged = sorted(allowed_untagged - untagged_ids)
    if artifact_count != source_count or bad or untagged:
        if artifact_count != source_count:
            print(f"artifact count mismatch: database={artifact_count}, files={source_count}", file=sys.stderr)
        for row in acknowledged:
            print(f"acknowledged legacy evidence drift: {row[0]} {row[1]} {row[2]}", file=sys.stderr)
        for row in unacknowledged:
            print(f"UNACKNOWLEDGED frozen evidence mismatch: {row[0]} {row[1]} {row[2]}", file=sys.stderr)
        for artifact_id in sorted(untagged_ids & allowed_untagged):
            print(f"acknowledged pre-tag artifact: {artifact_id}", file=sys.stderr)
        for artifact_id in unexpected_untagged:
            print(f"UNACKNOWLEDGED untagged artifact: {artifact_id}", file=sys.stderr)
        for artifact_id in missing_legacy_untagged:
            print(f"stale untagged exception: {artifact_id}", file=sys.stderr)
        if artifact_count != source_count or unacknowledged or unexpected_untagged or missing_legacy_untagged or (include_acknowledged and (acknowledged or untagged_ids)):
            return 1
    print(f"OK: {artifact_count} artifacts; no unacknowledged frozen-evidence drift.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True, help="path to research-records.json")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("rebuild")
    check_parser = sub.add_parser("check")
    check_parser.add_argument("--include-acknowledged", action="store_true", help="also fail on the explicit legacy migration exceptions")
    status_parser = sub.add_parser("status")
    status_parser.add_argument("--write", action="store_true", help="regenerate STATUS.md")
    cycle_parser = sub.add_parser("cycle")
    cycle_parser.add_argument("number", type=int)
    search_parser = sub.add_parser("search")
    search_parser.add_argument("text")
    args = parser.parse_args()
    configure(args.project)
    if args.command == "rebuild":
        rebuild()
        con = connect()
        STATUS.write_text(render_status(con))
        con.close()
        print(f"rebuilt {DATABASE.relative_to(ROOT)} and {STATUS.name}")
        return 0
    con = connect()
    if args.command == "check":
        return check(con, include_acknowledged=args.include_acknowledged)
    if args.command == "status":
        rendered = render_status(con)
        if args.write:
            STATUS.write_text(rendered)
        else:
            print(rendered, end="")
        return 0
    if args.command == "cycle":
        rows = con.execute("SELECT artifact_id, status, claim_boundary, remaining_target, replay_check FROM artifacts WHERE cycle_number = ? ORDER BY artifact_id", [args.number]).fetchall()
        for row in rows:
            print("\n".join(str(field or "") for field in row))
        return 0 if rows else 1
    if args.command == "search":
        query = f"%{args.text.lower()}%"
        rows = con.execute("SELECT artifact_id, json_path, epistemic_status, statement FROM claims WHERE lower(statement) LIKE ? ORDER BY artifact_id, json_path", [query]).fetchall()
        for artifact_id, path, tag, statement in rows:
            print(f"{artifact_id}\t{tag}\t{path}\t{statement}")
        return 0
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
