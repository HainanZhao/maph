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
    "$PREFIX/scripts/dimension_eight_cm_descent.gp"
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
