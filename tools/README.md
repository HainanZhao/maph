# Shared DuckDB tools

`duckdb_tools.py` is schema-agnostic. It opens an existing local DuckDB file
read-only and provides `tables`, `schema`, and one-statement read-only `sql`.
Each project owns the code that builds its database and any domain-specific
commands.

Install the shared pin in a project virtual environment:

```sh
.venv/bin/pip install -r /root/projects/maph/tools/requirements-duckdb.txt
```

Example:

```sh
.venv/bin/python /root/projects/maph/tools/duckdb_tools.py \
  --database .research/index.duckdb tables
```
