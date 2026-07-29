from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import shutil
import struct
import tempfile
import unittest
from unittest.mock import patch

from flint import ctx

from src.arb_power2_fastcbc import (
    arb_power2_candidate_scores,
    initial_running_product,
    update_running_product,
)
from src.certificate import canonical_sha256
from src.crt import choose_moduli
from src.native_cycle009 import (
    build_cycle009_ntt,
    compiled_candidate_scores,
)
from src.ntt_prime import generate_ntt_prime_schedule
from src.power2_fastcbc import (
    direct_power2_candidate_scores,
    stratified_ntt_candidate_scores,
)
from src.scaled_integer import (
    candidate_difference_bound,
    scaled_squared_error,
)
from src.shadow_decision import candidate_score_fraction
import scripts.run_cycle009_arb106 as target_run
from scripts.run_cycle009_arb106 import verify_release_boundary


@unittest.skipUnless(
    shutil.which("cc") and shutil.which("make"),
    "C compiler required",
)
class NativeCycle009Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.binary: Path = build_cycle009_ntt()
        prime = generate_ntt_prime_schedule(1)[0]
        cls.prime = int(prime["prime"])
        cls.root = int(prime["primitive_root"])

    def test_compiled_scores_match_both_small_oracles(self):
        prefixes = {
            32: [1, 5, 13],
            64: [1, 5, 13, 25],
            256: [1, 53, 17, 101],
        }
        for modulus, prefix in prefixes.items():
            weights = [
                Fraction(1, index * index)
                for index in range(1, len(prefix) + 2)
            ]
            _, direct = direct_power2_candidate_scores(
                modulus, prefix, weights, self.prime
            )
            _, python_ntt = stratified_ntt_candidate_scores(
                modulus, prefix, weights, self.prime, self.root
            )
            compiled = compiled_candidate_scores(
                modulus,
                self.prime,
                self.root,
                prefix,
                binary=self.binary,
            )
            self.assertEqual(compiled, direct)
            self.assertEqual(compiled, python_ntt)

    def test_compiled_scores_match_python_ntt_at_n4096(self):
        modulus = 4096
        prefix = [1, 275, 179, 319, 299, 451, 417, 167]
        weights = [
            Fraction(1, index * index)
            for index in range(1, len(prefix) + 2)
        ]
        _, expected = stratified_ntt_candidate_scores(
            modulus, prefix, weights, self.prime, self.root
        )
        actual = compiled_candidate_scores(
            modulus,
            self.prime,
            self.root,
            prefix,
            binary=self.binary,
        )
        self.assertEqual(actual, expected)

    def test_banked_compiled_ntt_gate_replays(self):
        root = Path(__file__).resolve().parents[1]
        artifact = json.loads(
            (
                root
                / "certificates"
                / "cycle-009-compiled-ntt-gate.json"
            ).read_text()
        )
        supplied = artifact.pop("certificate_sha256")
        self.assertEqual(supplied, canonical_sha256(artifact))
        self.assertTrue(
            artifact["gate"][
                "cycle009_compiled_ntt_correctness_gate_passed"
            ]
        )
        source = root / artifact["kernel"]["source"]
        self.assertEqual(
            artifact["kernel"]["source_sha256"],
            sha256(source.read_bytes()).hexdigest(),
        )
        for row in artifact["cases"]:
            scores = compiled_candidate_scores(
                int(row["N"]),
                int(row["prime"]),
                int(row["primitive_root"]),
                row["prefix"],
                binary=self.binary,
            )
            digest = sha256(
                b"".join(struct.pack("<Q", value) for value in scores)
            ).hexdigest()
            self.assertEqual(digest, row["score_sha256_u64le"])

    def test_integrated_preflight_certificate_is_self_hashed(self):
        root = Path(__file__).resolve().parents[1]
        artifact = json.loads(
            (
                root
                / "certificates"
                / "cycle-009-integrated-preflight.json"
            ).read_text()
        )
        supplied = artifact.pop("certificate_sha256")
        self.assertEqual(supplied, canonical_sha256(artifact))
        gate = artifact["gate"]
        self.assertTrue(gate["cycle009_integrated_preflight_passed"])
        self.assertTrue(
            gate[
                "every_exact_escalation_path_agrees_with_direct_oracle"
            ]
        )
        self.assertTrue(
            gate["per_dimension_checkpoint_and_sha_replay_passed"]
        )
        self.assertEqual(
            artifact["compiled_exact_fallback"][
                "candidate_pair_count"
            ],
            28,
        )

    def test_target_driver_rejects_unpublished_release_boundary(self):
        certificate = {
            "schema": "test-release",
            "published": False,
            "announcement_permitted": False,
            "doi": None,
        }
        certificate["certificate_sha256"] = canonical_sha256(
            certificate
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "release.json"
            path.write_text(
                json.dumps(certificate, sort_keys=True) + "\n"
            )
            with self.assertRaisesRegex(
                ValueError, "only after published DOI"
            ):
                verify_release_boundary(path)

    def test_target_tournament_and_final_merit_on_small_exact_case(self):
        root = Path(__file__).resolve().parents[1]
        prime_records = json.loads(
            (
                root
                / "certificates"
                / "cycle-009-prime-schedule-40.json"
            ).read_text()
        )["primes"]
        primes = [int(row["prime"]) for row in prime_records]
        modulus = 32
        stage = 4
        prefix = [1, 5, 13]
        weights = [
            Fraction(1, index * index)
            for index in range(1, stage + 1)
        ]
        score_vectors = [
            compiled_candidate_scores(
                modulus,
                int(row["prime"]),
                int(row["primitive_root"]),
                prefix,
                binary=self.binary,
            )
            for row in prime_records
        ]
        with ctx.workprec(106):
            state = initial_running_product(modulus)
            for component, weight in zip(prefix, weights[:-1]):
                state = update_running_product(
                    state, component, weight
                )
            candidates, balls = arb_power2_candidate_scores(
                modulus, state, weights[-1], precision=106
            )
        exact_scores = [
            candidate_score_fraction(
                modulus, prefix, weights, candidate
            )
            for candidate in candidates
        ]
        expected_winner = min(
            range(len(candidates)),
            key=lambda index: (exact_scores[index], index),
        )
        bound = candidate_difference_bound(
            modulus, weights[:-1], weights[-1]
        )
        work_count = len(choose_moduli(primes[:38], bound))
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            stage_dir = output / "stages" / "d04"
            stage_dir.mkdir(parents=True)
            for index, scores in enumerate(score_vectors):
                (stage_dir / f"p{index:02d}.bin").write_bytes(
                    b"".join(
                        struct.pack("<Q", value) for value in scores
                    )
                )
            with (
                patch.object(target_run, "MODULUS", modulus),
                patch.object(
                    target_run,
                    "COMPARISONS_PER_STAGE",
                    modulus // 4 - 1,
                ),
            ):
                winner, histogram, trace, _ = (
                    target_run.run_tournament(
                        output,
                        stage,
                        balls,
                        prime_records,
                        bound,
                        work_count,
                    )
                )
            self.assertEqual(winner, expected_winner)
            self.assertEqual(
                histogram["arb_resolved"]
                + histogram["exact_crt_resolved"],
                modulus // 4 - 1,
            )
            self.assertEqual(trace["record_count"], modulus // 4 - 1)
            final_prefix = [*prefix, candidates[winner]]
            records = [
                {
                    "event": "STAGE",
                    "stage": stage,
                    "winning_exponent": winner,
                }
            ]
            with (
                patch.object(target_run, "MODULUS", modulus),
                patch.object(target_run, "DIMENSION", stage),
            ):
                merit = target_run.final_exact_merit(
                    output,
                    final_prefix,
                    records,
                    prime_records,
                )
            direct = scaled_squared_error(
                modulus, final_prefix, weights
            )
            self.assertEqual(
                int(merit["scaled_numerator"]), direct.numerator
            )
            self.assertEqual(
                int(merit["scaled_denominator"]), direct.denominator
            )
            self.assertTrue(
                all(
                    row["equal"]
                    for row in merit["overflow_checks"]
                )
            )


if __name__ == "__main__":
    unittest.main()
