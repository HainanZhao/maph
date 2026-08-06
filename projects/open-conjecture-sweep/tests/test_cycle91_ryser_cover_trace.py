import runpy
from pathlib import Path


def test_c91_cover_trace_routes_agree():
    path = Path(__file__).parents[1] / "proof/check_cycle91_ryser_cover_trace.py"
    namespace = runpy.run_path(str(path))
    result = namespace["payload"]()
    assert result["status"] == "PASS"
    assert result["route_a_csp"] == result["route_b_csp"]
    assert len(result["family_counts"]) == 13
