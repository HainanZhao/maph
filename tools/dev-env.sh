# Source from any directory inside this Git checkout:
#   source "$(git rev-parse --show-toplevel)/tools/dev-env.sh"

RESEARCH_REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || {
  echo "dev-env.sh: run this from inside a Git working tree" >&2
  return 1 2>/dev/null || exit 1
}

case ":${PATH}:" in
  *":${RESEARCH_REPO_ROOT}/tools:"*) ;;
  *) export PATH="${RESEARCH_REPO_ROOT}/tools:${PATH}" ;;
esac

unset RESEARCH_REPO_ROOT
