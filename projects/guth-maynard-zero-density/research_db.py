#!/usr/bin/env python3
"""Small reusable API and CLI for the local research DuckDB index.

Examples:
    from research_db import ResearchDB

    with ResearchDB() as db:
        print(db.artifact(151))
        print(db.claims("negative-tail", tag="PROVED"))

The CLI emits JSON by default so agents can consume it without writing parser
scripts. Use ``--format table`` for a compact human-readable view.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import research_index

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from tools.duckdb_tools import DuckDBReader, emit


class ResearchDB(DuckDBReader):
    """Read-only convenience interface over the rebuildable research index."""

    def __init__(self, database: Path | str = research_index.DATABASE, *, rebuild_if_missing: bool = True) -> None:
        database_path = Path(database)
        if not database_path.exists():
            if not rebuild_if_missing:
                raise FileNotFoundError(database_path)
            research_index.rebuild(database_path)
        super().__init__(database_path)

    def summary(self) -> dict[str, Any]:
        latest = self.query("""
            SELECT artifact_id, cycle_number, epistemic_status, status,
                   claim_boundary, remaining_target
            FROM artifacts
            ORDER BY cycle_number DESC NULLS LAST, artifact_id DESC LIMIT 1
        """)[0]
        tags = self.query("""
            SELECT coalesce(epistemic_status, 'LEGACY_UNTAGGED') AS epistemic_status,
                   count(*) AS artifact_count
            FROM artifacts GROUP BY 1 ORDER BY 1
        """)
        return {
            "artifact_files": self.query("SELECT count(*) AS count FROM artifacts")[0]["count"],
            "git_index_artifacts": len(research_index.tracked_artifact_paths()),
            "artifact_status_counts": tags,
            "latest": latest,
        }

    def recent(self, limit: int = 10, tag: str | None = None) -> list[dict[str, Any]]:
        where = "WHERE epistemic_status = ?" if tag else ""
        parameters: list[Any] = [tag] if tag else []
        parameters.append(limit)
        return self.query(f"""
            SELECT artifact_id, cycle_number, epistemic_status, status,
                   claim_boundary, remaining_target
            FROM artifacts {where}
            ORDER BY cycle_number DESC NULLS LAST, artifact_id DESC LIMIT ?
        """, parameters)

    def artifact(self, identity: int | str) -> list[dict[str, Any]]:
        if isinstance(identity, int) or str(identity).isdigit():
            return self.query("""
                SELECT * FROM artifacts WHERE cycle_number = ? ORDER BY artifact_id
            """, [int(identity)])
        return self.query("SELECT * FROM artifacts WHERE artifact_id = ?", [str(identity)])

    def claims(self, text: str, *, tag: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
        clauses = ["lower(c.statement) LIKE ?"]
        parameters: list[Any] = [f"%{text.lower()}%"]
        if tag:
            clauses.append("c.epistemic_status = ?")
            parameters.append(tag)
        parameters.append(limit)
        return self.query(f"""
            SELECT c.artifact_id, c.json_path, c.epistemic_status, c.statement
            FROM claims AS c JOIN artifacts AS a USING (artifact_id)
            WHERE {' AND '.join(clauses)}
            ORDER BY a.cycle_number NULLS LAST, c.artifact_id, c.json_path LIMIT ?
        """, parameters)

    def gates(self, text: str = "OPEN", limit: int = 50) -> list[dict[str, Any]]:
        return self.query("""
            SELECT artifact_id, cycle_number, epistemic_status, status,
                   remaining_target
            FROM artifacts WHERE lower(coalesce(status, '')) LIKE ?
            ORDER BY cycle_number DESC NULLS LAST, artifact_id DESC LIMIT ?
        """, [f"%{text.lower()}%", limit])

    def dependencies(self, artifact_id: str, *, reverse: bool = False) -> list[dict[str, Any]]:
        if reverse:
            return self.query("""
                SELECT artifact_id AS dependent_artifact_id, dependency_key
                FROM dependencies WHERE dependency_artifact_id = ?
                ORDER BY artifact_id, dependency_key
            """, [artifact_id])
        return self.query("""
            SELECT dependency_key, dependency_artifact_id
            FROM dependencies WHERE artifact_id = ? AND dependency_artifact_id IS NOT NULL
            ORDER BY dependency_key
        """, [artifact_id])

    def evidence(self, artifact_id: str, *, problems_only: bool = False) -> list[dict[str, Any]]:
        suffix = "AND (NOT exists_now OR sha256_matches IS NOT TRUE)" if problems_only else ""
        return self.query(f"""
            SELECT evidence_key, path, sha256, exists_now, sha256_matches
            FROM evidence WHERE artifact_id = ? {suffix} ORDER BY evidence_key
        """, [artifact_id])


def add_limit(parser: argparse.ArgumentParser, default: int = 50) -> None:
    parser.add_argument("--limit", type=int, default=default)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=research_index.DATABASE)
    parser.add_argument("--format", choices=("json", "table", "tsv"), default="json")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("summary")
    recent = sub.add_parser("recent")
    add_limit(recent, 10)
    recent.add_argument("--tag", choices=sorted(research_index.VALID_TAGS))
    artifact = sub.add_parser("artifact")
    artifact.add_argument("identity", help="cycle number or exact artifact id")
    claims = sub.add_parser("claims")
    claims.add_argument("text")
    claims.add_argument("--tag", choices=sorted(research_index.VALID_TAGS))
    add_limit(claims)
    gates = sub.add_parser("gates")
    gates.add_argument("text", nargs="?", default="OPEN")
    add_limit(gates)
    dependencies = sub.add_parser("deps")
    dependencies.add_argument("artifact_id")
    dependencies.add_argument("--reverse", action="store_true")
    evidence = sub.add_parser("evidence")
    evidence.add_argument("artifact_id")
    evidence.add_argument("--problems-only", action="store_true")
    sql = sub.add_parser("sql")
    sql.add_argument("statement", help="one read-only SQL statement")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    with ResearchDB(args.database) as db:
        if args.command == "summary":
            result: Any = db.summary()
        elif args.command == "recent":
            result = db.recent(args.limit, args.tag)
        elif args.command == "artifact":
            result = db.artifact(args.identity)
        elif args.command == "claims":
            result = db.claims(args.text, tag=args.tag, limit=args.limit)
        elif args.command == "gates":
            result = db.gates(args.text, args.limit)
        elif args.command == "deps":
            result = db.dependencies(args.artifact_id, reverse=args.reverse)
        elif args.command == "evidence":
            result = db.evidence(args.artifact_id, problems_only=args.problems_only)
        elif args.command == "sql":
            result = db.query(args.statement)
        else:  # pragma: no cover
            raise AssertionError(args.command)
    emit(result, args.format)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
