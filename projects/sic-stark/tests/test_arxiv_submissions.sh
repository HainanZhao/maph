#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd -P)"
readonly BUILDER="$ROOT/scripts/build_arxiv_submissions.sh"

work_dir=$(mktemp -d)
cleanup() {
    rm -rf -- "$work_dir"
}
trap cleanup EXIT HUP INT TERM

mkdir -p -- "$work_dir/first" "$work_dir/second"
"$BUILDER" --output-dir "$work_dir/first" >/dev/null
"$BUILDER" --output-dir "$work_dir/second" >/dev/null

for paper in I II; do
    archive="sic-stark-paper-$paper-arxiv.tar.gz"
    cmp --silent "$work_dir/first/$archive" "$work_dir/second/$archive"

    extract="$work_dir/extract-$paper"
    mkdir -p -- "$extract"
    tar -xzf "$work_dir/first/$archive" -C "$extract"
    (
        cd -- "$extract"
        pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
        pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
        test -s main.pdf
    )
done

printf '%s\n' "PASS: arXiv source archives are deterministic and compile cleanly"
