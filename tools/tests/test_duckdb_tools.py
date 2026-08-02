from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.duckdb_tools import DuckDBReader, duckdb, require_read_only


class DuckDBToolsTest(unittest.TestCase):
    def test_read_only_helpers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "example.duckdb"
            con = duckdb.connect(str(database))
            con.execute("CREATE TABLE samples (id INTEGER, label VARCHAR)")
            con.execute("INSERT INTO samples VALUES (1, 'alpha')")
            con.close()
            with DuckDBReader(database) as db:
                self.assertEqual(db.tables(), [{"table_schema": "main", "table_name": "samples"}])
                self.assertEqual(db.query("SELECT label FROM samples"), [{"label": "alpha"}])
                self.assertEqual(db.schema("samples")[0]["column_name"], "id")
        require_read_only("SELECT 1")
        with self.assertRaises(ValueError):
            require_read_only("DELETE FROM samples")
