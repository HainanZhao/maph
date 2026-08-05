#!/bin/sh
set -u

expected_source=2e2ccebba549ec194df2f6d2c63dc3815701077645fd46cb3dc5034bc3b7736b
actual_source=$(sha256sum discovery/lrc_coverage_partitioned.cpp | awk '{print $1}')
test "$actual_source" = "$expected_source" || exit 2
test ! -e discovery/out/cycle4-work || exit 2

ulimit -v 8388608
printf 'virtual_memory_limit_kib=%s\n' "$(ulimit -v)" >&2
printf 'temporary_disk_limit_bytes=%s\n' 137438953472 >&2
printf 'filesystem_before_bytes=' >&2
df -B1 --output=size,used,avail,target . | tail -1 | awk '{$1=$1; print}' >&2

taskset -c 0-2 discovery/out/lrc_coverage_partitioned \
  --k 13 --p 199 --threads 3 \
  --state-cap 586985072 --edge-cap 5869850724 --leaf-cap 29565371 \
  --disk-cap-bytes 137438953472 --max-seconds 3600 \
  --output discovery/out/partitioned-k13-p199-128g.txt
run_rc=$?

printf 'filesystem_after_cleanup_bytes=' >&2
df -B1 --output=size,used,avail,target . | tail -1 | awk '{$1=$1; print}' >&2
exit "$run_rc"
