#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd -P)"
readonly BUILDER="$ROOT/scripts/build_publication_archive.sh"
readonly PREFIX="sic-stark-reproducibility"

work_dir=$(mktemp -d)
cleanup() {
    rm -rf -- "$work_dir"
}
trap cleanup EXIT HUP INT TERM

first="$work_dir/first.tar.gz"
second="$work_dir/second.tar.gz"
members="$work_dir/members"
extracted="$work_dir/extracted"

"$BUILDER" --output "$first" >/dev/null
"$BUILDER" --output "$second" >/dev/null

if ! cmp --silent "$first" "$second"; then
    printf '%s\n' "FAIL: independently built archives differ" >&2
    exit 1
fi

tar -tzf "$first" >"$members"
required=(
    "$PREFIX/README.md"
    "$PREFIX/paper/sic-stark-dimensions-four-five.pdf"
    "$PREFIX/certificates/dimension-five-shintani.txt"
    "$PREFIX/certificates/dimension-eight-cm-orientation.txt"
    "$PREFIX/scripts/dimension_eight_cm_descent.gp"
    "$PREFIX/scripts/dimension_eight_linear_cm_reinduction.gp"
    "$PREFIX/scripts/dimension_eight_cm_unit_lattice.gp"
    "$PREFIX/scripts/certify_dimension_eight_cm_orientation.py"
    "$PREFIX/scripts/dimension_eight_cm_real_unit_bridge.gp"
    "$PREFIX/scripts/dimension_eight_maximal_tuple_audit.gp"
    "$PREFIX/scripts/dimension_eight_maximal_quadratic_units.gp"
    "$PREFIX/scripts/certify_dimension_eight_maximal_cocycle.py"
    "$PREFIX/scripts/dimension_eight_maximal_sign_audit.py"
    "$PREFIX/scripts/dimension_eight_maximal_exact_tcc.py"
    "$PREFIX/docs/sic-stark-cycle92.md"
    "$PREFIX/docs/sic-stark-dimension-eight-unconditional-closure.md"
    "$PREFIX/ARCHIVE_CONTENTS.sha256"
)

for member in "${required[@]}"; do
    if ! grep -Fqx -- "$member" "$members"; then
        printf 'FAIL: required archive member is missing: %s\n' \
            "$member" >&2
        exit 1
    fi
done

mkdir -p -- "$extracted"
tar -xzf "$first" -C "$extracted"

(
    cd -- "$extracted/$PREFIX"
    sha256sum --check --strict ARCHIVE_CONTENTS.sha256 >/dev/null
    sha256sum --check --strict certificates/SHA256SUMS >/dev/null
)

digest=$(sha256sum -- "$first")
payload_count=$(wc -l <"$extracted/$PREFIX/ARCHIVE_CONTENTS.sha256")
printf '%s\n' "PASS: publication archive is deterministic and self-checksumming"
printf 'FILE_COUNT=%d\n' "$((payload_count + 1))"
printf 'SHA256=%s\n' "${digest%% *}"
