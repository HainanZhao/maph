from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]


class G0SixRouteResourceGateV2Tests(unittest.TestCase):
    def test_independent_cycle1_readonly_routes(self) -> None:
        for script in ("replay_cycle1_route_a_readonly_v1.py", "replay_cycle1_route_b_readonly_v1.py"):
            completed = subprocess.run([sys.executable, str(PROJECT / "proof" / script)], cwd=PROJECT, check=True, capture_output=True, text=True)
            self.assertEqual(json.loads(completed.stdout)["status"], "PASS")

    def test_config_and_six_measurements(self) -> None:
        subprocess.run([sys.executable, str(PROJECT / "proof/run_g0_resource_gate_v2.py"), "--check-config", str(PROJECT / "artifacts/g0-six-route-resource-gate-config-v2.json")], check=True)
        config = json.loads((PROJECT / "artifacts/g0-six-route-resource-gate-config-v2.json").read_text())
        observed = json.loads((PROJECT / "artifacts/g0-six-route-resource-gate-performance-v2.json").read_text())
        self.assertEqual(len(config["routes"]), len(observed["route_results"]))
        self.assertEqual(len(config["routes"]), 6)
        self.assertEqual([row["id"] for row in config["routes"]], [row["id"] for row in observed["route_results"]])
        self.assertEqual(observed["resource_gate"]["gate_status"], "PASS")
        for row in observed["route_results"]:
            self.assertEqual(row["gate_status"], "PASS")
            self.assertLess(Decimal(row["wall_seconds"]), Decimal(60))
            self.assertLess(row["max_rss_kib"], 262144)


if __name__ == "__main__":
    unittest.main()
