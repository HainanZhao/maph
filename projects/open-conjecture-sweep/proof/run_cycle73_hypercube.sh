#!/usr/bin/env bash
set -u

if [[ $# -ne 2 ]]; then
  echo "usage: run_cycle73_hypercube.sh calibrate|q7 OUTPUT_DIR" >&2
  exit 2
fi

mode=$1
output_dir=$2
project_dir=$(cd "$(dirname "$0")/.." && pwd)
cnf_builder="$output_dir/cycle73-hypercube-cnf"
drat_checker=/tmp/c73-drat-trim

mkdir -p "$output_dir"
g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic \
  "$project_dir/proof/cycle73_hypercube_cnf.cpp" -o "$cnf_builder"

run_sat () {
  local dimension=$1
  local target=$2
  local max_degree=${3:--1}
  local branch_suffix=""
  local builder_args=("$dimension" "$target")
  if [[ $max_degree -ne -1 ]]; then
    branch_suffix="-delta${max_degree}"
    builder_args+=("$max_degree")
  fi
  local stem="$output_dir/q${dimension}-${target}${branch_suffix}"
  "$cnf_builder" "${builder_args[0]}" "${builder_args[1]}" "$stem.cnf" \
    "${builder_args[@]:2}" > "$stem.cnf.json"
  /usr/bin/time -v -o "$stem.cadical.time" \
    timeout --signal=TERM 3600 cadical --check=1 --no-binary -q \
      "$stem.cnf" "$stem.drat" > "$stem.cadical.out"
  local rc=$?
  printf '%s\n' "$rc" > "$stem.cadical.rc"
  if [[ $rc -eq 10 ]]; then
    "$project_dir/.venv/bin/python" \
      "$project_dir/proof/check_cycle73_hypercube.py" \
      "$stem.cadical.out" --dimension "$dimension" --minimum "$target" \
      > "$stem.model-check.json"
  elif [[ $rc -eq 20 ]]; then
    "$drat_checker" "$stem.cnf" "$stem.drat" > "$stem.drat-check.txt"
  fi
  return 0
}

run_ilp () {
  local dimension=$1
  local stem="$output_dir/q${dimension}-ilp"
  /usr/bin/time -v -o "$stem.time" \
    timeout --signal=TERM 3600 "$project_dir/.venv/bin/python" \
      "$project_dir/proof/cycle73_hypercube_ilp.py" "$dimension" \
      --time-limit 3600 --output "$stem.json" > "$stem.out"
  local rc=$?
  printf '%s\n' "$rc" > "$stem.rc"
  if [[ $rc -eq 0 && -s "$stem.json" ]]; then
    "$project_dir/.venv/bin/python" \
      "$project_dir/proof/check_cycle73_hypercube.py" \
      "$stem.json" --minimum 1 > "$stem.model-check.json"
  fi
  return 0
}

if [[ $mode == calibrate ]]; then
  run_sat 6 132
  run_sat 6 133
  run_ilp 6
elif [[ $mode == q7 ]]; then
  sat_pids=()
  for maximum_degree in 5 6 7; do
    run_sat 7 305 "$maximum_degree" &
    sat_pids+=("$!")
  done
  for sat_pid in "${sat_pids[@]}"; do wait "$sat_pid"; done
  run_ilp 7
else
  echo "unknown mode: $mode" >&2
  exit 2
fi
