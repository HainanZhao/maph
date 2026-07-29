from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from src.certificate import (
    CertificateError,
    build_audit_wrapper,
    build_certificate,
    canonical_sha256,
    verify_audit_wrapper,
    verify_certificate,
)


class CertificateTests(unittest.TestCase):
    def setUp(self):
        self.certificate = build_certificate(
            8,
            [1, 3],
            [1, Fraction(1, 2)],
        )

    def test_certificate_replays(self):
        self.assertTrue(verify_certificate(self.certificate))
        self.assertEqual(self.certificate["tag"], "VERIFIED")

    def test_result_tampering_is_detected(self):
        altered = deepcopy(self.certificate)
        altered["result"]["numerator"] = str(
            int(altered["result"]["numerator"]) + 1
        )
        with self.assertRaises(CertificateError):
            verify_certificate(altered)

    def test_rehashed_semantic_tampering_is_detected_by_replay(self):
        altered = deepcopy(self.certificate)
        altered["definition"]["claim_boundary"] = "broader false claim"
        payload = deepcopy(altered)
        payload.pop("certificate_sha256")
        altered["certificate_sha256"] = canonical_sha256(payload)
        with self.assertRaises(CertificateError):
            verify_certificate(altered)

    def test_audit_wrapper_authenticates_provenance_and_core(self):
        wrapper = build_audit_wrapper(
            self.certificate,
            {
                "id": "frozen-example",
                "upstream_sha256": "a" * 64,
            },
        )
        self.assertTrue(verify_audit_wrapper(wrapper))
        wrapper["audit_target"]["upstream_sha256"] = "b" * 64
        with self.assertRaises(CertificateError):
            verify_audit_wrapper(wrapper)


if __name__ == "__main__":
    unittest.main()
