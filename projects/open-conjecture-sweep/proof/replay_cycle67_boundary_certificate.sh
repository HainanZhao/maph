#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "$0")/.." && pwd)"
if [[ $# -gt 1 ]]; then
  echo "usage: $0 [OUTPUT_DIR]" >&2
  exit 2
fi
if [[ $# -eq 1 ]]; then
  replay_dir="$1"
  mkdir -p "$replay_dir"
else
  replay_dir="$(mktemp -d)"
fi
threads="${C67_REPLAY_THREADS:-3}"
if [[ "$threads" -lt 1 || "$threads" -gt 3 ]]; then
  echo "C67_REPLAY_THREADS must be in [1,3]" >&2
  exit 2
fi

proof_dir="$project_dir/proof"
input_dir="$project_dir/discovery/out/cycle63-orbit-minimizer"
bin_dir="$replay_dir/bin"
mkdir -p "$bin_dir"

g++ -O3 -DNDEBUG -std=c++20 -fopenmp "$proof_dir/cycle67_boundary_grid.cpp" -o "$bin_dir/grid"
g++ -O3 -DNDEBUG -std=c++20 -fopenmp "$proof_dir/cycle67_expand_charts_fast.cpp" -o "$bin_dir/expand_invariant"
g++ -O3 -DNDEBUG -std=c++20 -fopenmp "$proof_dir/cycle67_expand_pullbacks_fast.cpp" -o "$bin_dir/expand_source"
g++ -O3 -DNDEBUG -std=c++20 -fopenmp "$proof_dir/cycle67_tensor_bernstein.cpp" -o "$bin_dir/tensor"

python3 "$proof_dir/cycle67_boundary_pullbacks.py" \
  "$input_dir/source-polynomial.tsv" "$input_dir/orbit-polynomial.tsv" "$replay_dir"
"$bin_dir/grid" "$replay_dir" "$replay_dir/grid"

python3 "$proof_dir/cycle67_emit_scaled_chart_forms.py" "$replay_dir/chart-forms.tsv"
python3 "$proof_dir/cycle67_emit_scaled_pullback_forms.py" "$replay_dir/pullback-chart-forms.tsv"
C67_THREADS="$threads" "$bin_dir/expand_invariant" \
  "$replay_dir/chart-forms.tsv" "$input_dir/orbit-polynomial.tsv" "$replay_dir/blowup-fast"
C67_THREADS="$threads" "$bin_dir/expand_source" \
  "$replay_dir/pullback-chart-forms.tsv" "$replay_dir" "$replay_dir/blowup-source-fast"

python3 "$proof_dir/cycle67_strip_boundary_factors.py" "$replay_dir/blowup-fast" "$replay_dir/blowup-stripped"
python3 "$proof_dir/check_cycle67_boundary_factors.py" "$replay_dir/blowup-fast" "$replay_dir/blowup-stripped"

python3 "$proof_dir/cycle67_trans_hessian_quotients.py" "$replay_dir/blowup-stripped" "$replay_dir/equal-hessian-quotients"
C67_THREADS="$threads" "$bin_dir/tensor" "$replay_dir/equal-hessian-quotients" "$replay_dir/equal-hessian-tensor" 1000
python3 "$proof_dir/cycle67_trans_curve_restrictions.py" "$replay_dir/blowup-stripped" "$replay_dir/equal-curve-restrictions"
C67_THREADS="$threads" "$bin_dir/tensor" "$replay_dir/equal-curve-restrictions" "$replay_dir/equal-curve-tensor" 1000
python3 "$proof_dir/cycle67_trans_joint_blowup.py" "$replay_dir/blowup-stripped" "$replay_dir/equal-joint-blowup"
C67_THREADS="$threads" "$bin_dir/tensor" "$replay_dir/equal-joint-blowup" "$replay_dir/equal-joint-tensor" 1000

python3 "$proof_dir/cycle67_transzero_joint_blowup.py" "$replay_dir/blowup-stripped" "$replay_dir/transzero-joint-blowup"
C67_THREADS="$threads" "$bin_dir/tensor" "$replay_dir/transzero-joint-blowup" "$replay_dir/transzero-joint-tensor" 1000
python3 "$proof_dir/cycle67_cyclezero_corner_blowup.py" \
  "$replay_dir/blowup-stripped/cycle_zero_cycle_dominant.tsv" "$replay_dir/cyclezero-corner-blowup"
C67_THREADS="$threads" "$bin_dir/tensor" "$replay_dir/cyclezero-corner-blowup" "$replay_dir/cyclezero-corner-tensor" 1000
C67_THREADS=1 "$bin_dir/tensor" "$replay_dir/blowup-stripped" "$replay_dir/cyclezero-trans-direct-tensor" 1000 cycle_zero_trans_dominant

python3 "$proof_dir/check_cycle67_boundary_certificate.py" "$replay_dir"
echo "replay directory: $replay_dir"
