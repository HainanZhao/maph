import runpy
from pathlib import Path

def test_c92_routes_and_witnesses():
    ns = runpy.run_path(str(Path(__file__).parents[1] / "proof/check_cycle92_frankl_temperature.py"))
    result = ns["payload"]()
    assert result["status"] == "PASS" and result["route_agreement"]
