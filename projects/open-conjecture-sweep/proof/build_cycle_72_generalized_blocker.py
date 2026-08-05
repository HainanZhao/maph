"""Seal the C72 generalized blocker theorem and the D>=6 consequence."""
from __future__ import annotations

import json
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-72-b072-defect-core-extension-v1.json"
HASHES = {
    "prior": ("artifacts/cycle-71-b071-high-star-defect-v1.json", "8417835fce57465f4f400c43999920adb4e25dc880e1ba72879dffcecfa9d8ba"),
    "prereg": ("docs/cycle-72-b072-defect-core-extension-preregistration-v1.md", "e25ab79b5741eb6b34808bd72309fc05e2b5debcbe0cf00b9a4fd97fee62afa8"),
    "idea": ("discovery/cycle72_defect_core_extension_idea_selection.md", "c90f57a86ed04dc8495f9b60d6a987e4af1d90f11195c0d2c4c444472b01c5f6"),
    "primary": ("proof/cycle72_bad_core_search.cpp", "7af6c5fe9c0be8c43ffb4109022453d99759958094ec83b2363c2c73be662c21"),
    "primary_checker": ("proof/check_cycle72_bad_core_search.py", "4668fb14e2e68b33a7f2dd66521d3d1e9b0e7759b04700b572fb513a935e97a2"),
    "independent": ("proof/cycle72_independent_blocker_replay.cpp", "00a14c04f3d607e9a2768397dcbbaf22c494817fc6113071efc9b68e52da6eea"),
    "replay_checker": ("proof/check_cycle72_independent_replay.py", "1885f7cac852cdb72dd79ec45f728dd2c43d2f62cceaca389a76f685eac57af7"),
    "reduction": ("proof/cycle72_universal_blocker_reduction.md", "e61165fc971d533d573286042c1237ea68f2a074efe706eb7ede0a1a09ade640"),
    "side_reduction": ("proof/cycle72_side_shape_reduction.md", "14e252f53765c726d7aad5c451f9977fac39e6ae880b591e972bf6fac2140601"),
    "theorem": ("proof/cycle72_generalized_blocker_theorem.md", "01ac5511b8ee791116c0eec783d61abbff60313d0b3d7daca4a2f38fac53fc81"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}
SHAPES = {
    "distinct": {"filter": 51, "cores": 20383920, "traces": 18, "hash_sum": 15509334374960293578, "hash_xor": 15723684813517967096},
    "double": {"filter": 14, "cores": 4013280, "traces": 6, "hash_sum": 18070918136567069852, "hash_xor": 5941124876935265852},
    "double-double": {"filter": 10, "cores": 1831680, "traces": 5, "hash_sum": 8202618639237995866, "hash_xor": 15911616773689284708},
}


def run_shards(commands, paths):
    processes = [subprocess.Popen(command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, text=True)
                 for command in commands]
    try:
        for process, path in zip(processes, paths):
            stdout, stderr = process.communicate(timeout=1800)
            require(process.returncode == 0, f"replay failed: {stderr[-2000:]}")
            path.write_text(stdout)
    finally:
        for process in processes:
            if process.poll() is None:
                process.kill()


def audit():
    started = time.monotonic()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    with tempfile.TemporaryDirectory(prefix="c72-replay-") as name:
        work = Path(name)
        primary = work / "primary"
        independent = work / "independent"
        compile_flags = ["g++", "-std=c++20", "-O3", "-DNDEBUG"]
        subprocess.run(compile_flags + [str(ROOT / HASHES["primary"][0]),
                       "-o", str(primary)], check=True)
        subprocess.run(compile_flags + [str(ROOT / HASHES["independent"][0]),
                       "-o", str(independent)], check=True)
        rows = {}
        for shape, expected in SHAPES.items():
            primary_paths = [work / f"{shape}-primary-{shard}.json"
                             for shard in range(3)]
            independent_paths = [work / f"{shape}-independent-{shard}.json"
                                 for shard in range(3)]
            run_shards([
                [str(primary), str(shard), "3", "10000000",
                 str(expected["filter"])] for shard in range(3)
            ], primary_paths)
            run_shards([
                [str(independent), shape, str(shard), "3", "10000000"]
                for shard in range(3)
            ], independent_paths)
            primary_check = json.loads(subprocess.check_output([
                sys.executable, str(ROOT / HASHES["primary_checker"][0]),
                *map(str, primary_paths)], text=True))
            require(primary_check["status"] == "PASS", "primary check failed")
            agreement = json.loads(subprocess.check_output([
                sys.executable, str(ROOT / HASHES["replay_checker"][0]), shape,
                *map(str, primary_paths), *map(str, independent_paths)],
                text=True))
            require(agreement["status"] == "PASS", "replay check failed")
            observed = agreement["agreement"]
            require(observed == {
                "cases": 52 * 15**5,
                "realized_cores": expected["cores"],
                "maximum_extension_traces": expected["traces"],
                "hash_sum": expected["hash_sum"],
                "hash_xor": expected["hash_xor"],
            }, f"unexpected {shape} census")
            rows[shape] = observed
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "finite_theorem": "Every generalized rooted D=5 equality core has a universal blocker of at most five core vertices.",
        "consequence": "Every intersecting six-partite six-uniform H with tau(H)=6 has D(H)>=6.",
        "shapes": rows,
        "outer_cases": sum(row["cases"] for row in rows.values()),
        "realized_cores": sum(row["realized_cores"] for row in rows.values()),
        "independent_routes": [
            "vertex-bitset trace recursion plus memoized blocker search",
            "per-part line-signature exact partitions plus memo-free iterative-deepening blocker search",
        ],
        "resource_observation": {
            "wall_seconds": round(time.monotonic() - started, 3),
            "child_user_seconds": round(after.ru_utime - before.ru_utime, 3),
            "peak_child_rss_kib": after.ru_maxrss,
            "worker_processes": 3,
        },
        "claim_boundary": "Necessary-condition theorem only; not Ryser r=6, not a D=6 classification or defect ladder, and no novelty claim.",
    }


def payload():
    result = audit()
    return {
        "artifact_id": "cycle-72-b072-defect-core-extension-v1",
        "budget_ordinal": "B072",
        "cycle": 72,
        "record_type": "PROVED_GENERALIZED_BLOCKER_AND_DEFECT_SIX_THEOREM",
        "recorded_at_utc": "2026-08-05T16:17:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "All 26,228,880 generalized D=5 equality cores have a universal five-blocker; consequently tau=6 forces D>=6.",
        "claim_boundary": result["claim_boundary"],
        "audit": result,
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short (Oracle)",
            "companion_advice": "Run exactly one orthogonal exhaustive replay; on full count/hash agreement seal immediately and select the next attack afresh.",
            "decision": "The independent replay agreed exactly on all three shapes, so seal the C72 theorem and end this research block.",
            "falsifier": "A legal core with trace-family transversal number at least six, any count/hash disagreement, or an H with tau=6 and D<=5.",
        },
        "frozen_hashes": freeze_inputs(
            ROOT, {key: (ROOT / path, digest)
                   for key, (path, digest) in HASHES.items()}),
        "runtime": check_runtime("c72"),
        "sealer": {"path": "proof/build_cycle_72_generalized_blocker.py",
                   "sha256": sha256(Path(__file__))},
        "replay": {
            "check": "python3 proof/build_cycle_72_generalized_blocker.py --check",
            "workers": 3,
            "expected_wall_minutes": "approximately 7",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT,
                             payload_factory=payload))
