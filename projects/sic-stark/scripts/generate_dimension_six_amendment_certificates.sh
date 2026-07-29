#!/usr/bin/env bash
set -euo pipefail

# Regenerate the executable certificate packet for Cycles 144'--151.

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd -P)"
readonly CERTIFICATE_DIR="$ROOT/certificates"

python_bin=${SIC_STARK_PYTHON:-python3}
if ! "$python_bin" -c 'import flint' >/dev/null 2>&1; then
    printf '%s\n' \
        "error: SIC_STARK_PYTHON must name a Python with python-flint" >&2
    exit 1
fi

work_dir=$(mktemp -d)
cleanup() {
    rm -rf -- "$work_dir"
}
trap cleanup EXIT HUP INT TERM

run_python() {
    local output=$1
    shift
    PYTHONPATH="$ROOT/scripts" "$python_bin" "$@" >"$work_dir/$output"
}

run_python dimension-six-cycle144-two-base.txt \
    "$ROOT/scripts/dimension_six_two_base_lens.py" \
    --digits 30 --tolerance 1e-14

{
    PYTHONPATH="$ROOT/scripts" "$python_bin" \
        "$ROOT/scripts/dimension_five_two_base_calibration.py" \
        --digits 30 --tolerance 1e-12
    PYTHONPATH="$ROOT/scripts" "$python_bin" \
        "$ROOT/scripts/dimension_four_two_base_calibration.py" \
        --digits 30 --tolerance 1e-12
} >"$work_dir/dimension-six-cycle145-calibrations.txt"

for cycle in \
    146:ss_evaluation_audit \
    147:interior_factorization_audit \
    148:boundary_integral_audit \
    149:stabilizer_ledger \
    150:adversarial_sweep
do
    cycle_number=${cycle%%:*}
    script_suffix=${cycle#*:}
    run_python \
        "dimension-six-cycle${cycle_number}-${script_suffix}.json" \
        "$ROOT/scripts/dimension_six_${script_suffix}.py"
done

run_python dimension-six-cycle149-grade2-equivalence.json \
    "$ROOT/scripts/dimension_six_grade2_equivalence.py"
run_python dimension-six-cycle150-checkpoint-gates.json \
    "$ROOT/scripts/dimension_six_checkpoint_gates.py"
run_python dimension-six-cycle153-tilted-finite-part.json \
    "$ROOT/scripts/dimension_six_tilted_finite_part.py" --arb
run_python dimension-six-cycle154-conditioning-comparison.json \
    "$ROOT/scripts/dimension_six_conditioning_comparison.py"
run_python dimension-six-cycle154-fresnel-stratum.json \
    "$ROOT/scripts/dimension_six_fresnel_stratum_audit.py"

mkdir -p -- "$CERTIFICATE_DIR"
for generated in "$work_dir"/dimension-six-cycle*; do
    cp -- "$generated" "$CERTIFICATE_DIR/$(basename -- "$generated")"
done

manifest="$CERTIFICATE_DIR/dimension-six-amendment-SHA256SUMS"
(
    cd -- "$ROOT"
    find certificates -maxdepth 1 -type f \
        \( -name 'dimension-six-cycle14[4-9]-*' -o \
        -name 'dimension-six-cycle150-*' -o \
        -name 'dimension-six-cycle153-*' -o \
        -name 'dimension-six-cycle154-*' \) |
        LC_ALL=C sort |
        xargs sha256sum
) >"$manifest"

(
    cd -- "$ROOT"
    sha256sum --check --strict \
        certificates/dimension-six-amendment-SHA256SUMS
)

printf 'MANIFEST=%s\n' "$manifest"
printf 'MANIFEST_SHA256=%s\n' \
    "$(sha256sum -- "$manifest" | cut -d' ' -f1)"
