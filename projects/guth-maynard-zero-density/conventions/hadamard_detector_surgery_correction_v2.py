"""Exact prime-count remainder correction for Cycle 27 v2."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def finite_remainder_check() -> dict[str, int]:
    prime_count = 11
    blocks = 4
    retained = blocks * (prime_count // blocks)
    discarded = prime_count - retained
    require(retained == 8 and discarded == 3, "finite remainder mismatch")
    require(discarded < blocks, "discard cap mismatch")
    return {"prime_count": prime_count, "blocks": blocks, "retained": retained, "discarded": discarded}


def exponent_check() -> dict[str, Fraction | str]:
    detector = Q(7, 10)
    mass = Q(1)
    block_count = Q(0)  # J=X^o(1)
    detector_relative_loss = block_count - detector
    mass_relative_loss = block_count - mass
    require(detector_relative_loss == Q(-7, 10), "detector loss exponent mismatch")
    require(mass_relative_loss == -1, "mass loss exponent mismatch")
    return {
        "detector": detector,
        "mass": mass,
        "block_count": "X^o(1)",
        "discard_over_detector": "X^(-7/10+o(1))",
        "discard_over_mass": "X^(-1+o(1))",
        "detector_relative_loss_exponent": detector_relative_loss,
        "mass_relative_loss_exponent": mass_relative_loss,
    }


def verify_all() -> dict[str, object]:
    return {
        "finite_remainder": finite_remainder_check(),
        "exponents": exponent_check(),
        "repair": "retain J floor(M/J), discard r<J, replace V by V-r",
    }
