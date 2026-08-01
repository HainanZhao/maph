"""Hostile correction tests for Stream C Route A v3."""
import ast, importlib.util, json, subprocess, sys, unittest
from pathlib import Path
PROJECT=Path(__file__).resolve().parents[1]; SCRIPT=PROJECT/"proof/replay_cycle2_stream_c_route_a_v3.py"; ARTIFACT=PROJECT/"artifacts/cycle-2-stream-c-route-a-v3.json"
def load():
    s=importlib.util.spec_from_file_location("stream_c_a_v3",SCRIPT); assert s and s.loader; m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
class TestStreamCARouteAV3(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.m=load()
    def test_catches_alpha_half_failure_and_closes_with_arbitrary_t(self):
        b=self.m.bookkeeping(); self.assertIn("NOT admissible",b["almost_all"]["CHJ_I_alpha_half"]); self.assertEqual(b["almost_all"]["T_power_before_subpower"],"13/15"); self.assertIn("admissible",b["almost_all"]["arbitrary_T_formula"])
    def test_formula_conventions_and_prime_transfer(self):
        b=self.m.bookkeeping(); self.assertIn("T-1/T",b["modulus_boundary"]); self.assertIn("multiplicity",b["multiplicity"]); self.assertIn("partial summation",b["prime_powers"].lower())
    def test_no_float_literals(self):
        tree=ast.parse(SCRIPT.read_text()); self.assertEqual([n.value for n in ast.walk(tree) if isinstance(n,ast.Constant) and isinstance(n.value,float)],[])
    def test_replay_hash(self):
        subprocess.run([sys.executable,str(SCRIPT),"--write"],check=True,cwd=PROJECT); first=ARTIFACT.read_bytes(); subprocess.run([sys.executable,str(SCRIPT),"--write"],check=True,cwd=PROJECT); self.assertEqual(first,ARTIFACT.read_bytes()); subprocess.run([sys.executable,str(SCRIPT),"--check"],check=True,cwd=PROJECT); a=json.loads(ARTIFACT.read_text()); body={k:v for k,v in a.items() if k not in {"exact_replay_sha256","replay"}}; self.assertEqual(a["exact_replay_sha256"],self.m.canonical_sha256(body)); self.assertEqual(a["replay"]["script_sha256"],self.m.sha256(SCRIPT)); self.assertNotIn("wall_time_ns",a["replay"])
if __name__=="__main__": unittest.main()
