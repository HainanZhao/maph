#!/usr/bin/env bash
set -euo pipefail

# Build deterministic, source-only arXiv submission archives.

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd -P)"
readonly DEFAULT_OUTPUT_DIR="$ROOT/dist"

output_dir="$DEFAULT_OUTPUT_DIR"
selection="both"

usage() {
    printf '%s\n' \
        "Usage: scripts/build_arxiv_submissions.sh [--paper I|II|both] [--output-dir PATH]"
}

while (($#)); do
    case "$1" in
        --paper)
            (($# >= 2)) || { usage >&2; exit 2; }
            selection=$2
            shift 2
            ;;
        --output-dir)
            (($# >= 2)) || { usage >&2; exit 2; }
            output_dir=$2
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            printf 'error: unknown option: %s\n' "$1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

case "$selection" in
    I|II|both) ;;
    *) printf 'error: invalid paper selection: %s\n' "$selection" >&2; exit 2 ;;
esac

if [[ "$output_dir" != /* ]]; then
    output_dir="$PWD/$output_dir"
fi
mkdir -p -- "$output_dir"
output_dir="$(cd -- "$output_dir" && pwd -P)"

build_one() {
    local paper=$1
    local source
    if [[ "$paper" == "I" ]]; then
        source="$ROOT/paper/sic-stark-dimensions-four-five.tex"
    else
        source="$ROOT/paper/sic-stark-dimensions-seven-eight.tex"
    fi
    [[ -f "$source" ]] || {
        printf 'error: missing manuscript source: %s\n' "$source" >&2
        exit 1
    }

    local work_dir
    work_dir=$(mktemp -d)
    cp -- "$source" "$work_dir/main.tex"
    chmod 644 "$work_dir/main.tex"

    local output="$output_dir/sic-stark-paper-$paper-arxiv.tar.gz"
    tar \
        --sort=name \
        --mtime='UTC 1970-01-01' \
        --owner=0 \
        --group=0 \
        --numeric-owner \
        -C "$work_dir" \
        -cf - main.tex |
        gzip -n >"$output"
    rm -rf -- "$work_dir"

    printf 'BUILT=%s\n' "$output"
    printf 'SHA256=%s\n' "$(sha256sum "$output" | cut -d' ' -f1)"
}

case "$selection" in
    I) build_one I ;;
    II) build_one II ;;
    both)
        build_one I
        build_one II
        ;;
esac
