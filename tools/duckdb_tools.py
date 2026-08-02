#!/usr/bin/env python3
"""Shared read-only DuckDB API and CLI for repository research indexes.

This module deliberately knows no project schema. Projects own their build
pipelines and domain-specific convenience methods; this provides the small
common layer for opening a database, returning structured rows, formatting
results, inspecting schemas, and issuing read-only SQL.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

try:
    import duckdb
except ModuleNotFoundError as exc:  # pragma: no cover - local environment
    raise SystemExit("DuckDB is required; install tools/requirements-duckdb.txt in your project virtual environment.") from exc


READ_ONLY_PREFIXES = ("SELECT", "WITH", "SHOW", "DESCRIBE", "EXPLAIN")


class DuckDBReader:
    """Minimal reusable read-only query interface returning JSON-ready rows."""

    def __init__(self, database: Path | str) -> None:
        self.database = Path(database)
        self.connection = duckdb.connect(str(self.database), read_only=True)

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "DuckDBReader":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def query(self, sql: str, parameters: Sequence[Any] | None = None) -> list[dict[str, Any]]:
        cursor = self.connection.execute(sql, list(parameters or []))
        columns = [item[0] for item in cursor.description]
        return [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]

    def tables(self) -> list[dict[str, Any]]:
        return self.query("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE'
            ORDER BY table_schema, table_name
        """)

    def schema(self, table: str) -> list[dict[str, Any]]:
        return self.query("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'main' AND table_name = ?
            ORDER BY ordinal_position
        """, [table])


def require_read_only(sql: str) -> None:
    statement = sql.strip().rstrip(";").upper()
    if not statement.startswith(READ_ONLY_PREFIXES) or ";" in statement:
        raise ValueError("Only one SELECT/WITH/SHOW/DESCRIBE/EXPLAIN statement is accepted.")


def emit(rows: Any, output_format: str = "json") -> None:
    if output_format == "json":
        print(json.dumps(rows, indent=2, sort_keys=True, default=str))
        return
    if isinstance(rows, dict):
        rows = [rows]
    if not rows:
        return
    columns = list(rows[0])
    if output_format == "tsv":
        print("\t".join(columns))
        for row in rows:
            print("\t".join(str(row.get(column, "")) for column in columns))
        return
    widths = {column: max(len(column), *(len(str(row.get(column, ""))) for row in rows)) for column in columns}
    print("  ".join(column.ljust(widths[column]) for column in columns))
    print("  ".join("-" * widths[column] for column in columns))
    for row in rows:
        print("  ".join(str(row.get(column, "")).ljust(widths[column]) for column in columns))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--format", choices=("json", "table", "tsv"), default="json")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("tables")
    schema = sub.add_parser("schema")
    schema.add_argument("table")
    sql = sub.add_parser("sql")
    sql.add_argument("statement")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    with DuckDBReader(args.database) as db:
        if args.command == "tables":
            result: Any = db.tables()
        elif args.command == "schema":
            result = db.schema(args.table)
        else:
            require_read_only(args.statement)
            result = db.query(args.statement)
    emit(result, args.format)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
