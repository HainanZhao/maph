#!/usr/bin/env bash
set -euo pipefail

# Build a deterministic publication/reproducibility tar archive.

readonly ARCHIVE_ROOT="sic-stark-reproducibility"
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd -P)"
readonly DEFAULT_OUTPUT="$ROOT/dist/sic-stark-reproducibility.tar.gz"

output="$DEFAULT_OUTPUT"
core_only=false
list_only=false
verify_checksums=true
strict_release_metadata=false

usage() {
    cat <<'EOF'
Usage: scripts/build_publication_archive.sh [OPTIONS]

Build a deterministic publication/reproducibility .tar.gz archive.

Options:
  --output PATH                 Set the output archive path.
  --core-only                   Exclude dimension-six/eight outlook material.
  --list                        Print archive inputs without building.
  --skip-checksum-verification Skip certificates/SHA256SUMS verification.
  --strict-release-metadata     Require all release metadata files.
  -h, --help                    Show this help.
EOF
}

while (($#)); do
    case "$1" in
        --output)
            if (($# < 2)); then
                printf '%s\n' "error: --output requires a path" >&2
                exit 2
            fi
            output=$2
            shift 2
            ;;
        --core-only)
            core_only=true
            shift
            ;;
        --list)
            list_only=true
            shift
            ;;
        --skip-checksum-verification)
            verify_checksums=false
            shift
            ;;
        --strict-release-metadata)
            strict_release_metadata=true
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

readonly RELEASE_METADATA=(
    "CITATION.cff"
    ".zenodo.json"
    "LICENSE"
    "LICENSE-CODE"
    "requirements-lock.txt"
    "REPRODUCE.md"
)

work_dir=$(mktemp -d)
cleanup() {
    rm -rf -- "$work_dir"
}
trap cleanup EXIT HUP INT TERM

files="$work_dir/files"
missing="$work_dir/missing"
: >"$files"
: >"$missing"

add_file() {
    printf '%s\n' "$1" >>"$files"
}

add_file "README.md"
add_file "paper/sic-stark-dimensions-four-five.tex"
add_file "paper/sic-stark-dimensions-four-five.pdf"
add_file "docs/referee-package.md"
add_file "certificates/SHA256SUMS"
add_file "certificates/test-suite.txt"
add_file "certificates/dimension-four-certificate.json"
add_file "certificates/pari-audit.txt"
add_file "certificates/double-sine-audit.txt"
add_file "certificates/dimension-five-bridge.json"
add_file "certificates/dimension-five-character-support.json"
add_file "certificates/dimension-five-double-sine-intervals.txt"
add_file "certificates/dimension-five-embedding-certificate.txt"
add_file "certificates/dimension-five-exact-minors.txt"
add_file "certificates/dimension-five-finite.json"
add_file "certificates/dimension-five-local-isolation.txt"
add_file "certificates/dimension-five-numerical.txt"
add_file "certificates/dimension-five-pari.txt"
add_file "certificates/dimension-five-root-isolation.txt"
add_file "certificates/dimension-five-shintani.txt"
add_file "certificates/dimension-five-unit-lattice.txt"
add_file "scripts/analyze_dimension_five_character.py"
add_file "scripts/analyze_dimension_five_finite.py"
add_file "scripts/build_publication_archive.sh"
add_file "scripts/certify_dimension_five_double_sine.py"
add_file "scripts/dimension_five_embedding_certificate.gp"
add_file "scripts/dimension_five_local_isolation.gp"
add_file "scripts/dimension_five_pari_audit.gp"
add_file "scripts/dimension_five_root_isolation.gp"
add_file "scripts/dimension_five_shintani_audit.gp"
add_file "scripts/dimension_five_special_reduction_audit.gp"
add_file "scripts/dimension_five_unit_lattice_audit.gp"
add_file "scripts/explore_dimension_four_double_sine.py"
add_file "scripts/generate_dimension_five_bridge.py"
add_file "scripts/generate_referee_certificates.py"
add_file "scripts/referee_pari_audit.gp"
add_file "scripts/verify_dimension_five_conjugates.gp"
add_file "scripts/verify_referee_certificate.py"

# Every certificate-manifest target must be present in the archive.
while read -r digest relative extra; do
    [[ -z "${digest:-}" ]] && continue
    if [[ -n "${extra:-}" || "$relative" = /* || "/$relative/" == *"/../"* ]]; then
        printf 'error: unsafe checksum-manifest entry: %s\n' \
            "$digest ${relative:-} ${extra:-}" >&2
        exit 1
    fi
    add_file "$relative"
done <"$ROOT/certificates/SHA256SUMS"

while IFS= read -r relative; do
    add_file "$relative"
done < <(
    cd -- "$ROOT"
    find src tests -type f \
        ! -path '*/__pycache__/*' \
        ! -name '*.pyc' \
        ! -name '*.pyo' \
        -print
)

if ! $core_only; then
    add_file "docs/sic-stark-dimension-eight-cm-descent.md"
    add_file "docs/sic-stark-dimension-eight-canonical-closure.md"
    add_file "docs/sic-stark-dimension-eight-unconditional-closure.md"
    add_file "certificates/dimension-eight-cm-descent.txt"
    add_file "scripts/dimension_eight_linear_cm_reinduction.gp"
    add_file "scripts/dimension_eight_cm_unit_lattice.gp"
    add_file "scripts/certify_dimension_eight_cm_orientation.py"
    add_file "scripts/dimension_eight_cm_real_unit_bridge.gp"
    add_file "scripts/dimension_eight_maximal_tuple_audit.gp"
    add_file "scripts/dimension_eight_maximal_quadratic_units.gp"
    add_file "scripts/certify_dimension_eight_maximal_cocycle.py"
    add_file "scripts/dimension_eight_maximal_sign_audit.py"
    add_file "scripts/dimension_eight_maximal_exact_tcc.py"
    for cycle in {82..92}; do
        add_file "docs/sic-stark-cycle${cycle}.md"
    done

    # Include every script cited in the manuscript's composite-dimension
    # section, so new cited audits are automatically picked up.
    while IFS= read -r relative; do
        [[ "$relative" == scripts/* ]] && add_file "$relative"
    done < <(
        awk '
            index($0, "\\section{Composite dimensions") { inside = 1 }
            index($0, "\\section{Scope and reproducibility}") { inside = 0 }
            inside { print }
        ' "$ROOT/paper/sic-stark-dimensions-four-five.tex" |
            sed -n 's/.*\\path{\([^}]*\)}.*/\1/p'
    )
fi

missing_metadata=()
for relative in "${RELEASE_METADATA[@]}"; do
    if [[ -f "$ROOT/$relative" ]]; then
        add_file "$relative"
    else
        missing_metadata+=("$relative")
    fi
done

if $strict_release_metadata && ((${#missing_metadata[@]})); then
    printf '%s\n' "error: release metadata is missing:" >&2
    printf '  %s\n' "${missing_metadata[@]}" >&2
    exit 1
fi

LC_ALL=C sort -u "$files" -o "$files"

while IFS= read -r relative; do
    if [[ "$relative" = /* || "/$relative/" == *"/../"* ]]; then
        printf 'error: unsafe archive path: %s\n' "$relative" >&2
        exit 1
    fi
    [[ -f "$ROOT/$relative" ]] || printf '%s\n' "$relative" >>"$missing"
done <"$files"

if [[ -s "$missing" ]]; then
    printf '%s\n' "error: archive input is missing:" >&2
    sed 's/^/  /' "$missing" >&2
    exit 1
fi

if $verify_checksums; then
    (
        cd -- "$ROOT"
        sha256sum --check --strict certificates/SHA256SUMS
    ) >/dev/null
fi

if $list_only; then
    cat "$files"
    exit 0
fi

if [[ "$output" != /* ]]; then
    output="$PWD/$output"
fi
output_dir=$(dirname -- "$output")
mkdir -p -- "$output_dir"
output_dir=$(cd -- "$output_dir" && pwd -P)
output="$output_dir/$(basename -- "$output")"

stage="$work_dir/stage"
package="$stage/$ARCHIVE_ROOT"
mkdir -p -- "$package"

executables="$work_dir/executables"
: >"$executables"
while IFS= read -r relative; do
    [[ -x "$ROOT/$relative" ]] && printf '%s\n' "$relative" >>"$executables"
    mkdir -p -- "$package/$(dirname -- "$relative")"
    cp -- "$ROOT/$relative" "$package/$relative"
done <"$files"

# Normalize modes, ownership, names, and timestamps for byte-reproducibility.
find "$package" -type d -exec chmod 755 {} +
find "$package" -type f -exec chmod 644 {} +
while IFS= read -r relative; do
    [[ -n "$relative" ]] && chmod 755 "$package/$relative"
done <"$executables"

(
    cd -- "$ROOT"
    while IFS= read -r relative; do
        digest=$(sha256sum -- "$relative")
        printf '%s  %s\n' "${digest%% *}" "$relative"
    done <"$files"
) >"$package/ARCHIVE_CONTENTS.sha256"
chmod 644 "$package/ARCHIVE_CONTENTS.sha256"

temporary_archive=$(mktemp "$output_dir/.publication-archive.XXXXXX")
tar \
    --sort=name \
    --mtime='@0' \
    --owner=0 \
    --group=0 \
    --numeric-owner \
    --format=gnu \
    -C "$stage" \
    -cf - \
    "$ARCHIVE_ROOT" |
    gzip -n -9 >"$temporary_archive"
mv -- "$temporary_archive" "$output"

archive_digest=$(sha256sum -- "$output")
file_count=$(wc -l <"$files")
printf 'ARCHIVE=%s\n' "$output"
printf 'FILE_COUNT=%d\n' "$((file_count + 1))"
printf 'SHA256=%s\n' "${archive_digest%% *}"

if ((${#missing_metadata[@]})); then
    metadata_csv=$(IFS=,; printf '%s' "${missing_metadata[*]}")
    printf 'WARNING_MISSING_RELEASE_METADATA=%s\n' "$metadata_csv"
fi
