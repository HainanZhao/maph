#!/bin/sh
set -eu

ulimit -v 8388608
printf 'virtual_memory_limit_kib=%s\n' "$(ulimit -v)" >&2
exec taskset -c 0-2 discovery/out/lrc_coverage_levels \
  --k 13 --p 199 --threads 3 \
  --state-cap 586985072 --edge-cap 5869850724 --leaf-cap 29565371 \
  --max-seconds 3600 --output discovery/out/coverage-k13-p199.txt
