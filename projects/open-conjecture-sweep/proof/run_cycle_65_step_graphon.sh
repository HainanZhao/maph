#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "$0")/.." && pwd)"
out="$project_root/discovery/out/cycle65-step-graphon"
mkdir -p "$out/bin" "$out/search" "$out/exact" "$out/runtime"
g++ --version > "$out/runtime/compiler.txt"

g++ -O3 -march=native -DNDEBUG -std=c++20 \
  "$project_root/discovery/cycle65_step_graphon_search.cpp" -o "$out/bin/search"
g++ -O3 -march=native -DNDEBUG -std=c++20 \
  "$project_root/proof/cycle65_step_graphon_exact.cpp" -o "$out/bin/exact"

/usr/bin/time -v -o "$out/runtime/search-650651.txt" \
  "$out/bin/search" 650651 "$out/search" & pid1=$!
/usr/bin/time -v -o "$out/runtime/search-650652.txt" \
  "$out/bin/search" 650652 "$out/search" & pid2=$!
/usr/bin/time -v -o "$out/runtime/search-650653.txt" \
  "$out/bin/search" 650653 "$out/search" & pid3=$!
wait "$pid1"
wait "$pid2"
wait "$pid3"

/usr/bin/time -v -o "$out/runtime/exact.txt" \
  "$out/bin/exact" "$out/exact" \
  "$out/search/candidates-650651.tsv" \
  "$out/search/candidates-650652.tsv" \
  "$out/search/candidates-650653.tsv"
python3 "$project_root/proof/check_cycle_65_step_graphon_packet.py"
