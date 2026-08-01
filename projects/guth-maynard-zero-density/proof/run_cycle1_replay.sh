#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

python3 "$project_dir/proof/verify_source_manifest.py" \
  > "$project_dir/artifacts/source-manifest-verification-v1.json"

python3 -m unittest discover -s "$project_dir/tests" -p 'test_*.py' -v

if [ -f "$project_dir/proof/replay_baseline_route_a.py" ]; then
  python3 "$project_dir/proof/replay_baseline_route_a.py"
fi

if [ -f "$project_dir/proof/replay_baseline_route_b.py" ]; then
  python3 "$project_dir/proof/replay_baseline_route_b.py" \
    --check "$project_dir/artifacts/cycle-1-route-b-baseline.json"
fi

python3 "$project_dir/proof/replay_bottleneck_cell_route_b_v2.py" \
  --check "$project_dir/artifacts/cycle-1-route-b-v2-bottleneck-cell.json"

python3 "$project_dir/proof/replay_theorem_1_2_case_split_route_a_v4.py"

python3 "$project_dir/proof/replay_theorem_1_2_case_split_route_b_v3.py" \
  --check "$project_dir/artifacts/cycle-1-route-b-v3-theorem-1-2-case-split.json"

python3 "$project_dir/proof/audit_cycle1_routes.py" \
  --write "$project_dir/artifacts/cycle-1-route-reconciliation-v3.json"
