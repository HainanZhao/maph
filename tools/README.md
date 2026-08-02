# Shared DuckDB tools

`duckdb_tools.py` is schema-agnostic. It opens an existing local DuckDB file
read-only and provides `tables`, `schema`, and one-statement read-only `sql`.
Each project owns the code that builds its database and any domain-specific
commands.

`research_records.py` builds, validates, and queries the standard immutable
cycle-record schema. A project supplies only `research-records.json`, which
declares record paths, local index/status locations, legacy migration
exceptions, and status presentation.

Install the shared pin in a project virtual environment:

```sh
.venv/bin/pip install -r /root/projects/maph/tools/requirements-duckdb.txt
```

Example:

```sh
.venv/bin/python /root/projects/maph/tools/duckdb_tools.py \
  --database .research/index.duckdb tables

.venv/bin/python /root/projects/maph/tools/research_records.py \
  --project research-records.json rebuild
```

For ordinary work, change into a profiled project and use the short wrapper:

```sh
cd projects/guth-maynard-zero-density
../../tools/research rebuild
../../tools/research check
../../tools/research cycle 151
../../tools/research search negative-tail
../../tools/research db tables
../../tools/research db sql "SELECT status, count(*) FROM artifacts GROUP BY status"
```
