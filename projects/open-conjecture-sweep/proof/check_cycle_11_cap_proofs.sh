#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
checker="$root/discovery/out/cycle11-tools/drat-trim-2e5e29cb0019d5cfd547d4208dca1b3ec290349f/drat-trim"
rows="$root/discovery/out/cycle11-certified-sat/p199"

check_one() {
  row=$1
  cpu=$2
  /usr/bin/time -v -o "$rows/$row.recheck.time" \
    timeout --signal=TERM --kill-after=5 2500 \
    taskset -c "$cpu" \
    prlimit --as=5368709120 --fsize=32212254720 -- \
    "$checker" "$rows/$row.cnf" "$rows/$row.drat" \
    > "$rows/$row.recheck.txt"
  grep -q VERIFIED "$rows/$row.recheck.txt"
}

check_one 000 0 &
left=$!
check_one 002 1 &
right=$!
wait "$left"
wait "$right"
printf '%s\n' 'PASS rows=000,002 proofs=VERIFIED'
