#!/bin/sh
set -u

expected_source=77d82ab2dafd5dfb4c54749fd376b38ea04c7f3785e5422f7c18c91c8a57baef
actual_source=$(sha256sum discovery/lrc_coverage_packing.cpp | awk '{print $1}')
test "$actual_source" = "$expected_source" || exit 2
test ! -e discovery/out/cycle4-work || exit 2

reserve_bytes=5368709120
frozen_cap_bytes=173296054272
available_bytes=$(df -B1 --output=avail . | tail -1 | tr -d ' ')
runtime_cap_bytes=$((available_bytes - reserve_bytes))
test "$runtime_cap_bytes" -gt 0 || exit 2
if test "$runtime_cap_bytes" -gt "$frozen_cap_bytes"; then
  runtime_cap_bytes=$frozen_cap_bytes
fi

ulimit -v 8388608
printf 'virtual_memory_limit_kib=%s\n' "$(ulimit -v)" >&2
printf 'filesystem_reserve_bytes=%s\n' "$reserve_bytes" >&2
printf 'filesystem_available_before_bytes=%s\n' "$available_bytes" >&2
printf 'temporary_disk_limit_bytes=%s\n' "$runtime_cap_bytes" >&2
printf 'filesystem_before_bytes=' >&2
df -B1 --output=size,used,avail,target . | tail -1 | awk '{$1=$1; print}' >&2

taskset -c 0-2 discovery/out/lrc_coverage_packing \
  --k 13 --p 199 --threads 3 \
  --state-cap 586985072 --edge-cap 5869850724 --leaf-cap 29565371 \
  --disk-cap-bytes "$runtime_cap_bytes" --max-seconds 3600 \
  --output discovery/out/packing-k13-p199.txt
run_rc=$?

printf 'filesystem_after_cleanup_bytes=' >&2
df -B1 --output=size,used,avail,target . | tail -1 | awk '{$1=$1; print}' >&2
exit "$run_rc"
