#!/usr/bin/env bash
# Clean direct-source replay of the C68 fixed-S3 secant certificate.
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 REPLAY_DIR" >&2
  exit 2
fi

root=$(cd "$(dirname "$0")/.." && pwd)
target=$1
canonical="$root/discovery/out/cycle68-interior-chord"
mkdir -p "$target/bin" "$target/c63"

g++ -std=c++20 -O3 "$root/proof/cycle63_s3_source_polynomial.cpp" -o "$target/bin/c63-source"
"$target/bin/c63-source" "$target/c63"
cmp "$target/c63/source-polynomial.tsv" "$root/discovery/out/cycle63-orbit-minimizer/source-polynomial.tsv"
python3 "$root/proof/cycle63_reduce_orbit.py" "$target/c63/source-polynomial.tsv" "$target/c63"
cmp "$target/c63/orbit-polynomial.tsv" "$root/discovery/out/cycle63-orbit-minimizer/orbit-polynomial.tsv"

python3 "$root/proof/cycle68_secant_polynomials.py" "$target/c63/orbit-polynomial.tsv" "$target/secant"
diff -qr "$target/secant" "$canonical/secant"
python3 "$root/proof/cycle68_strip_boundary_factors.py" "$target/secant" "$target/secant-stripped"
diff -qr "$target/secant-stripped" "$canonical/secant-stripped"
# The separate simultaneous-SymPy audit is retained as frozen evidence, but
# exceeds the interactive replay budget.  This replay instead uses the
# independent sparse exact audit below, after reconstructing the charts from
# the direct six-value source.

python3 "$root/proof/cycle68_secant_equality_blowup.py" "$target/secant-stripped" "$target/primary"
diff -qr "$target/primary" "$canonical/secant-blowup"
python3 "$root/proof/cycle68_secant_secondary_blowup.py" "$target/primary/high-below-second_scale-dominant.tsv" "$target/secondary"
diff -qr "$target/secondary" "$canonical/secant-secondary-blowup"

g++ -std=c++20 -O3 -DNDEBUG -fopenmp "$root/proof/cycle68_monotonicity_bernstein.cpp" -o "$target/bin/bernstein"
env C68_THREADS=2 "$target/bin/bernstein" "$target/primary" "$target/primary-root" 100 0
cmp "$target/primary-root/monotonicity-summary.json" "$canonical/secant-blowup-root/monotonicity-summary.json"
env C68_THREADS=2 "$target/bin/bernstein" "$target/primary" "$target/primary-subdivision" 10000 10 high-below-cycle-dominant high-below-second_scale-dominant
cmp "$target/primary-subdivision/monotonicity-summary.json" "$canonical/secant-blowup-remaining-depth10/monotonicity-summary.json"
env C68_THREADS=1 "$target/bin/bernstein" "$target/secondary" "$target/secondary-root" 100 0
cmp "$target/secondary-root/monotonicity-summary.json" "$canonical/secant-secondary-root/monotonicity-summary.json"

python3 "$root/proof/cycle68_blowup_sparse_audit.py" "$target/secant-stripped" "$target/primary" "$target/secondary" "$target/blowup-sparse-audit.json" --workers 3
cmp "$target/blowup-sparse-audit.json" "$canonical/secant-blowup-sparse-audit.json"
python3 "$root/proof/check_cycle68_secant_cover.py" \
  "$root/artifacts/cycle-67-b067-s3-boundary-positivity-v1.json" \
  "$target/c63/source-polynomial.tsv" \
  "$target/secant/secant-summary.json" \
  "$target/secant-stripped/factor-report.json" \
  "$target/primary/blowup-summary.json" \
  "$target/primary-root/monotonicity-summary.json" \
  "$target/primary-subdivision/monotonicity-summary.json" \
  "$target/secondary/secondary-blowup-summary.json" \
  "$target/secondary-root/monotonicity-summary.json" \
  "$target/cover-audit.json"
cmp "$target/cover-audit.json" "$canonical/secant-cover-audit.json"

printf 'C68 direct-source replay: PASS\n'
