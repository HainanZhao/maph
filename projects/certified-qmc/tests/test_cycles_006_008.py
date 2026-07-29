from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import random
import shutil
import unittest

from src.exact_error import RuleSpec
from src.modular_error import error_numerator_residue
from src.native_baseline import (
    build_native_baseline,
    native_error_numerator_residue,
)
from src.ntt import direct_cyclic_convolution, ntt_cyclic_convolution
from src.ntt_prime import generate_ntt_prime_schedule
from src.power2_fastcbc import (
    direct_power2_candidate_scores,
    power2_strata,
    stratified_ntt_candidate_scores,
)


PROJECT = Path(__file__).resolve().parents[1]
GENERATOR = [1, 275, 179, 319, 299, 451, 417, 167,
             289, 109, 395, 81, 215, 115, 143, 361]


def digest(values) -> str:
    return sha256(
        "".join(f"{index}:{value}\n" for index, value in enumerate(values))
        .encode("ascii")
    ).hexdigest()


class LaterCycleArtifactTests(unittest.TestCase):
    def load(self, name: str):
        return json.loads((PROJECT / "certificates" / name).read_text())

    @unittest.skipUnless(shutil.which("cc") and shutil.which("make"), "C compiler required")
    def test_cycle006_native_validation_replays(self):
        artifact = self.load("cycle-006-native-baseline.json")
        source_hash = sha256(
            (PROJECT / "native" / "direct_modular.c").read_bytes()
        ).hexdigest()
        self.assertEqual(artifact["source_sha256"], source_hash)
        binary = build_native_baseline()
        for row in artifact["validation"]:
            dimension = int(row["dimension"])
            prime = int(row["prime"])
            weights = [
                Fraction(1, j * j) for j in range(1, dimension + 1)
            ]
            spec = RuleSpec.create(
                1024, GENERATOR[:dimension], weights
            )
            native = native_error_numerator_residue(
                1024,
                spec.generator,
                spec.weights,
                prime,
                binary=binary,
            )
            self.assertEqual(native, int(row["residue"]))
            self.assertEqual(native, error_numerator_residue(spec, prime))

    def test_cycle007_convolution_digests_replay(self):
        artifact = self.load("cycle-007-ntt-validation.json")
        prime = int(artifact["prime"])
        root = int(artifact["primitive_root"])
        source = random.Random(int(artifact["seed"]))
        for row in artifact["convolutions"]:
            length = int(row["length"])
            left = [source.randrange(prime) for _ in range(length)]
            right = [source.randrange(prime) for _ in range(length)]
            direct = direct_cyclic_convolution(left, right, prime)
            fast = ntt_cyclic_convolution(left, right, prime, root)
            self.assertEqual(fast, direct)
            self.assertEqual(digest(direct), row["result_sha256"])

    def test_cycle008_mapping_digest_replays(self):
        artifact = self.load("cycle-008-power2-fastcbc.json")
        frozen = artifact["frozen_case"]
        prime_record = generate_ntt_prime_schedule(1)[0]
        prime = int(prime_record["prime"])
        root = int(prime_record["primitive_root"])
        prefix = [int(value) for value in frozen["prefix"]]
        weights = [
            Fraction(1, j * j)
            for j in range(1, int(frozen["new_dimension"]) + 1)
        ]
        direct_candidates, direct_scores = direct_power2_candidate_scores(
            1024, prefix, weights, prime
        )
        fast_candidates, fast_scores = stratified_ntt_candidate_scores(
            1024, prefix, weights, prime, root
        )
        self.assertEqual(
            (fast_candidates, fast_scores),
            (direct_candidates, direct_scores),
        )
        self.assertEqual(digest(direct_candidates), frozen["candidate_sha256"])
        self.assertEqual(digest(direct_scores), frozen["score_sha256"])
        self.assertEqual(frozen["strata"], power2_strata(1024))
