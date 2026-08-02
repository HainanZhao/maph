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
source "$(git rev-parse --show-toplevel)/tools/dev-env.sh"
cd projects/guth-maynard-zero-density
research rebuild
research check
research cycle 151
research search negative-tail
research db tables
research db sql "SELECT status, count(*) FROM artifacts GROUP BY status"
```

## Preregistration preflight

New research cycles use one machine-readable freeze manifest embedded in their
canonical preregistration (not a second log or configuration file). Before
creating or running executable discovery, proof, or replay code, run:

```sh
research prereg check docs/cycle-<n>-<slug>-preregistration-v1.md \
  --expected-cycle <n>
```

The check validates typed parameters and resource caps, formula families,
selection and failure rules, a pre-execution Git boundary, and declared input
paths. It prints the preregistration hash that the cycle builder must freeze.
A later replay after a commit may use `--allow-head-drift`; the frozen
preregistration hash still detects mutation. Sealed legacy cycles without a
manifest remain immutable and are reported as legacy-unprotected rather than
being rewritten.
