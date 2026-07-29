"""Deterministic certificate construction and replay."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Mapping, Sequence

from .exact_error import (
    CONVENTION,
    RuleSpec,
    exact_squared_error,
    fraction_records,
    master_denominator,
    term_digest,
)


SCHEMA = "certified-qmc-exact-b2-error-v1"
AUDIT_SCHEMA = "certified-qmc-audit-wrapper-v1"


class CertificateError(ValueError):
    """Raised when an exact-error certificate does not replay."""


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")


def _payload_digest(payload: Mapping[str, Any]) -> str:
    return sha256(_canonical_bytes(payload)).hexdigest()


def canonical_sha256(payload: Mapping[str, Any]) -> str:
    """Return the canonical JSON digest used by project certificates."""

    return _payload_digest(payload)


def build_certificate(
    modulus: int,
    generator: Sequence[int],
    weights: Sequence[Fraction | int | str],
) -> dict[str, Any]:
    """Build a deterministic, self-contained exact merit certificate."""

    spec = RuleSpec.create(modulus, generator, weights)
    result = exact_squared_error(
        spec.modulus,
        spec.generator,
        spec.weights,
    )
    bound = master_denominator(spec)
    if bound % result.denominator:
        raise ArithmeticError("reduced denominator does not divide bound")

    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "tag": "VERIFIED",
        "definition": {
            "convention": CONVENTION,
            "kernel": "B2(x)=x^2-x+1/6",
            "quantity": (
                "-1+(1/N)*sum_k product_j"
                "(1+gamma_j*B2({k*z_j/N}))"
            ),
            "claim_boundary": (
                "squared shift-averaged worst-case error in the frozen "
                "product-weight beta=0 convention; not an integrand error"
            ),
        },
        "input": {
            "modulus": spec.modulus,
            "dimension": spec.dimension,
            "generator_mod_N": list(spec.generator),
            "weights": fraction_records(spec.weights),
            "all_generator_components_are_units": (
                spec.all_components_are_units
            ),
        },
        "result": {
            "numerator": str(result.numerator),
            "denominator": str(result.denominator),
        },
        "denominator_proof": {
            "formula": "N*product_j(6*den(gamma_j)*N^2)",
            "master_denominator": str(bound),
            "master_bit_length": bound.bit_length(),
            "reduced_denominator_divides_master": True,
            "quotient": str(bound // result.denominator),
        },
        "replay": {
            "algorithm": "direct exact Fraction sum-product",
            "exact_summand_sha256": term_digest(spec),
        },
    }
    payload["certificate_sha256"] = _payload_digest(payload)
    return payload


def verify_certificate(certificate: Mapping[str, Any]) -> bool:
    """Replay a certificate and reject any semantic or hash mismatch."""

    supplied = deepcopy(dict(certificate))
    supplied_hash = supplied.pop("certificate_sha256", None)
    if not isinstance(supplied_hash, str):
        raise CertificateError("certificate_sha256 is missing")
    if _payload_digest(supplied) != supplied_hash:
        raise CertificateError("certificate payload hash mismatch")
    if supplied.get("schema") != SCHEMA:
        raise CertificateError("unsupported certificate schema")
    if supplied.get("tag") != "VERIFIED":
        raise CertificateError("exact certificate must have VERIFIED tag")

    try:
        inputs = supplied["input"]
        weights = [
            Fraction(int(item["numerator"]), int(item["denominator"]))
            for item in inputs["weights"]
        ]
        expected = build_certificate(
            int(inputs["modulus"]),
            [int(value) for value in inputs["generator_mod_N"]],
            weights,
        )
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise CertificateError(f"malformed certificate: {error}") from error

    actual = deepcopy(dict(certificate))
    if actual != expected:
        raise CertificateError(
            "certificate does not equal deterministic exact replay"
        )
    return True


def build_audit_wrapper(
    core_certificate: Mapping[str, Any],
    audit_target: Mapping[str, Any],
    *,
    tag: str = "VERIFIED_PREFIX",
) -> dict[str, Any]:
    """Authenticate audit provenance around a strict core certificate."""

    verify_certificate(core_certificate)
    payload: dict[str, Any] = {
        "schema": AUDIT_SCHEMA,
        "tag": tag,
        "audit_target": deepcopy(dict(audit_target)),
        "core_certificate": deepcopy(dict(core_certificate)),
    }
    payload["audit_sha256"] = canonical_sha256(payload)
    return payload


def verify_audit_wrapper(wrapper: Mapping[str, Any]) -> bool:
    """Verify both the outer provenance record and exact inner result."""

    supplied = deepcopy(dict(wrapper))
    supplied_hash = supplied.pop("audit_sha256", None)
    if not isinstance(supplied_hash, str):
        raise CertificateError("audit_sha256 is missing")
    if canonical_sha256(supplied) != supplied_hash:
        raise CertificateError("audit wrapper hash mismatch")
    if supplied.get("schema") != AUDIT_SCHEMA:
        raise CertificateError("unsupported audit wrapper schema")
    if supplied.get("tag") not in {"VERIFIED_PREFIX", "VERIFIED_TABLE"}:
        raise CertificateError("unsupported audit wrapper tag")
    try:
        verify_certificate(supplied["core_certificate"])
    except KeyError as error:
        raise CertificateError("core_certificate is missing") from error
    return True
