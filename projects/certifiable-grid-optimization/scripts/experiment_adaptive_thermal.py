"""Run recovery-informed thermal tightening on pinned PGLib cases."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.adaptive_thermal import adaptive_thermal_recovery
from src.matpower import load_matpower_case


DATA = Path(__file__).resolve().parents[1] / "data" / "pglib-opf-v23.07"
CASES = (
    "pglib_opf_case5_pjm.m",
    "pglib_opf_case14_ieee.m",
    "pglib_opf_case5_pjm__api.m",
    "pglib_opf_case14_ieee__api.m",
)


def main() -> None:
    print(
        "| case | converged | iterations | original lower | feasible upper | "
        "certified gap | initial overload | final overload |"
    )
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    for filename in CASES:
        case = load_matpower_case(DATA / filename)
        result = adaptive_thermal_recovery(case)
        print(
            f"| {filename.removesuffix('.m')} | {result.converged} | "
            f"{len(result.history) - 1} | "
            f"{result.original_lower_bound:.6f} | "
            f"{result.feasible_upper_bound:.6f} | "
            f"{result.certified_gap_percent:.4f}% | "
            f"{result.history[0].maximum_overload_mva:.6f} | "
            f"{result.history[-1].maximum_overload_mva:.6f} |"
        )
        for entry in result.history:
            print(
                f"  iteration {entry.iteration}: relaxation="
                f"{entry.relaxation_objective:.6f}, dispatch="
                f"{entry.dispatch_objective:.6f}, overload="
                f"{entry.maximum_overload_mva:.6f} MVA, tightened="
                f"{entry.tightened_branch_count}"
            )


if __name__ == "__main__":
    main()
