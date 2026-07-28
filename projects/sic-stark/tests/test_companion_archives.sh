#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd -P)"
readonly BUILDER="$ROOT/scripts/build_companion_archives.sh"

work_dir=$(mktemp -d)
cleanup() {
    rm -rf -- "$work_dir"
}
trap cleanup EXIT HUP INT TERM

first="$work_dir/first"
second="$work_dir/second"
mkdir -p -- "$first" "$second"

"$BUILDER" --output-dir "$first" >/dev/null
"$BUILDER" --output-dir "$second" >/dev/null

for paper in I II; do
    archive="sic-stark-paper-$paper.tar.gz"
    cmp --silent "$first/$archive" "$second/$archive" || {
        printf 'FAIL: Paper %s archives differ\n' "$paper" >&2
        exit 1
    }
    extract="$work_dir/extract-$paper"
    mkdir -p -- "$extract"
    tar -xzf "$first/$archive" -C "$extract"
    (
        cd -- "$extract/sic-stark-paper-$paper"
        sha256sum --check --strict ARCHIVE_CONTENTS.sha256 >/dev/null
        PYTHONPATH=scripts python3 -m unittest discover -s tests \
            >/dev/null
    )
    for metadata in CITATION.cff .zenodo.json LICENSE LICENSE-CODE \
        requirements-lock.txt REPRODUCE.md; do
        grep -Fq "sic-stark-paper-$paper/$metadata" < <(
            tar -tzf "$first/$archive"
        )
    done
done

paper_one_members=$(tar -tzf "$first/sic-stark-paper-I.tar.gz")
paper_two_members=$(tar -tzf "$first/sic-stark-paper-II.tar.gz")

grep -Fq "sic-stark-paper-I/paper/sic-stark-dimensions-four-five.pdf" \
    <<<"$paper_one_members"
if grep -Fq "dimension_eight" <<<"$paper_one_members"; then
    printf '%s\n' "FAIL: Paper I contains dimension-eight artifacts" >&2
    exit 1
fi

grep -Fq "sic-stark-paper-II/paper/sic-stark-dimensions-seven-eight.pdf" \
    <<<"$paper_two_members"
grep -Fq "dimension_eight_maximal_sign_audit.py" \
    <<<"$paper_two_members"
grep -Fq "dimension_seven_exact_tcc.gp" <<<"$paper_two_members"

printf '%s\n' \
    "PASS: both companion archives are deterministic and self-checksumming"
