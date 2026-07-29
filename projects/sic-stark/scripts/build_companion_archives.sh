#!/usr/bin/env bash
set -euo pipefail

# Build deterministic, submission-specific archives for Papers I and II.

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd -P)"
readonly DEFAULT_OUTPUT_DIR="$ROOT/dist"

output_dir="$DEFAULT_OUTPUT_DIR"
selection="both"
list_only=false

usage() {
    cat <<'EOF'
Usage: scripts/build_companion_archives.sh [OPTIONS]

Options:
  --paper I|II|both   Select an archive (default: both).
  --output-dir PATH   Output directory (default: dist).
  --list              Print selected source files without building.
  -h, --help          Show this help.
EOF
}

while (($#)); do
    case "$1" in
        --paper)
            (($# >= 2)) || {
                printf '%s\n' "error: --paper requires I, II, or both" >&2
                exit 2
            }
            selection=$2
            shift 2
            ;;
        --output-dir)
            (($# >= 2)) || {
                printf '%s\n' "error: --output-dir requires a path" >&2
                exit 2
            }
            output_dir=$2
            shift 2
            ;;
        --list)
            list_only=true
            shift
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
    *)
        printf 'error: invalid paper selection: %s\n' "$selection" >&2
        exit 2
        ;;
esac

if [[ "$output_dir" != /* ]]; then
    output_dir="$PWD/$output_dir"
fi
mkdir -p -- "$output_dir"
output_dir="$(cd -- "$output_dir" && pwd -P)"

work_dir=$(mktemp -d)
cleanup() {
    rm -rf -- "$work_dir"
}
trap cleanup EXIT HUP INT TERM

add_existing() {
    local list=$1
    local relative=$2
    [[ -f "$ROOT/$relative" ]] || {
        printf 'error: missing archive input: %s\n' "$relative" >&2
        exit 1
    }
    printf '%s\n' "$relative" >>"$list"
}

common_release_files() {
    local list=$1
    add_existing "$list" "LICENSE"
    add_existing "$list" "LICENSE-CODE"
    add_existing "$list" "requirements-lock.txt"
}

add_matches() {
    local list=$1
    local directory=$2
    local expression=$3
    while IFS= read -r relative; do
        printf '%s\n' "$relative" >>"$list"
    done < <(
        cd -- "$ROOT"
        find "$directory" -type f -regextype posix-extended \
            -regex "$expression" \
            ! -path '*/__pycache__/*' \
            ! -name '*.pyc' \
            -print
    )
}

paper_one_files() {
    local list=$1
    common_release_files "$list"
    add_existing "$list" "publication/paper-I-CITATION.cff"
    add_existing "$list" "publication/paper-I-zenodo.json"
    add_existing "$list" "paper/sic-stark-dimensions-four-five.tex"
    add_existing "$list" "paper/sic-stark-dimensions-four-five.pdf"
    add_existing "$list" "publication/paper-I-README.md"
    add_existing "$list" "publication/paper-I-REPRODUCE.md"
    add_existing "$list" "docs/referee-package.md"
    add_existing "$list" "docs/sic-stark-dimension-five.md"
    add_existing "$list" \
        "docs/sic-stark-dimension-five-unconditional-closure.md"
    add_matches "$list" "certificates" \
        'certificates/(dimension-four|dimension-five|double-sine|pari-audit|test-suite).*'
    add_matches "$list" "scripts" \
        'scripts/(analyze_dimension_five|certify_dimension_five|dimension_five|explore_dimension_four|generate_dimension_five|generate_referee|referee_pari|verify_dimension_five|verify_referee).*'
    add_matches "$list" "src" 'src/.*'
    add_matches "$list" "tests" \
        'tests/(test_sic|test_sic_stark|test_dimension_five_artifacts|test_dimension_five_character)\.py'
}

paper_two_files() {
    local list=$1
    common_release_files "$list"
    add_existing "$list" "publication/paper-II-CITATION.cff"
    add_existing "$list" "publication/paper-II-zenodo.json"
    add_existing "$list" "paper/sic-stark-dimensions-seven-eight.tex"
    add_existing "$list" "paper/sic-stark-dimensions-seven-eight.pdf"
    add_existing "$list" "publication/paper-II-README.md"
    add_existing "$list" "publication/paper-II-REPRODUCE.md"
    add_existing "$list" \
        "certificates/dimension-eight-cm-orientation.txt"
    add_existing "$list" \
        "certificates/dimension-eight-cm-descent.txt"
    add_existing "$list" \
        "certificates/dimension-eight-maximal-signs.txt"
    add_existing "$list" "certificates/test-suite.txt"
    add_existing "$list" "scripts/certify_dimension_five_double_sine.py"
    add_existing "$list" "scripts/explore_dimension_four_double_sine.py"
    add_matches "$list" "docs" \
        'docs/(sic-stark-cycle(4[6-9]|5[0-8]|7[2-9]|8[0-9]|9[0-2])|sic-stark-dimension-eight.*)\.md'
    add_matches "$list" "scripts" \
        'scripts/((analyze|certify|explore|generate|verify)_dimension_(seven|eight).*|dimension_(seven|eight).*)'
    add_matches "$list" "tests" \
        'tests/(test_dimension_seven_closure|test_dimension_eight_maximal_signs|test_dimension_eight_unconditional_closure)\.py'
}

build_one() {
    local paper=$1
    local list="$work_dir/paper-$paper-files"
    : >"$list"
    if [[ "$paper" == "I" ]]; then
        paper_one_files "$list"
    else
        paper_two_files "$list"
    fi
    LC_ALL=C sort -u "$list" -o "$list"

    if $list_only; then
        sed "s#^#PAPER_$paper #g" "$list"
        return
    fi

    local archive_name="sic-stark-paper-$paper"
    local stage="$work_dir/stage-$paper"
    local package="$stage/$archive_name"
    mkdir -p -- "$package"

    while IFS= read -r relative; do
        local target=$relative
        if [[ "$relative" == "publication/paper-$paper-README.md" ]]; then
            target="README.md"
        elif [[ "$relative" == \
            "publication/paper-$paper-REPRODUCE.md" ]]; then
            target="REPRODUCE.md"
        elif [[ "$relative" == \
            "publication/paper-$paper-CITATION.cff" ]]; then
            target="CITATION.cff"
        elif [[ "$relative" == \
            "publication/paper-$paper-zenodo.json" ]]; then
            target=".zenodo.json"
        fi
        mkdir -p -- "$package/$(dirname -- "$target")"
        cp -- "$ROOT/$relative" "$package/$target"
    done <"$list"

    local manifest="$work_dir/paper-$paper-contents.sha256"
    (
        cd -- "$package"
        find . -type f -print0 |
            LC_ALL=C sort -z |
            xargs -0 sha256sum |
            sed 's#  \./#  #' >"$manifest"
    )
    cp -- "$manifest" "$package/ARCHIVE_CONTENTS.sha256"

    find "$package" -type d -exec chmod 755 {} +
    find "$package" -type f -exec chmod 644 {} +

    local output="$output_dir/$archive_name.tar.gz"
    tar \
        --sort=name \
        --mtime='UTC 1970-01-01' \
        --owner=0 \
        --group=0 \
        --numeric-owner \
        -C "$stage" \
        -cf - "$archive_name" |
        gzip -n >"$output"

    printf 'BUILT=%s\n' "$output"
    printf 'FILE_COUNT=%d\n' \
        "$(tar -tzf "$output" | grep -vc '/$')"
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
