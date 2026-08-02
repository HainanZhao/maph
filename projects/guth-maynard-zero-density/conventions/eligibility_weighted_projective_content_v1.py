"""Exact divisor-content ledger for Cycle 171 projective lifts."""
from __future__ import annotations

from fractions import Fraction as Q
from math import gcd


def _ceil(value: Q) -> int:
    return -((-value.numerator) // value.denominator)


def _cube_ceil(value: int) -> int:
    if value <= 0:
        raise ValueError("positive cube threshold required")
    answer = 1
    while answer**3 < value:
        answer += 1
    return answer


def _sqrt_ceil(value: Q) -> int:
    if value <= 0:
        raise ValueError("positive square threshold required")
    answer = 1
    while answer * answer < value:
        answer += 1
    return answer


def euler_phi(value: int) -> int:
    if value <= 0:
        raise ValueError("positive divisor required")
    result, remaining, prime = value, value, 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            while remaining % prime == 0:
                remaining //= prime
            result -= result // prime
        prime += 1
    if remaining > 1:
        result -= result // remaining
    return result


def divisor_content(content: int) -> int:
    """Exact Euler divisor expansion sum_{r|g} phi(r)=g."""
    if content <= 0:
        raise ValueError("positive content required")
    total = 0
    for divisor in range(1, content + 1):
        if content % divisor == 0:
            total += euler_phi(divisor)
    if total != content:
        raise RuntimeError("Euler divisor expansion")
    return total


def factor_content(*, d: int, b: int, q: int, a: int) -> dict[str, int]:
    """Factor gcd(qd, a(d+b)) into source, numerator, denominator factors."""
    if d == 0 or q <= 0 or a <= 0 or gcd(q, a) != 1:
        raise ValueError("invalid reduced-rational projective data")
    c = gcd(abs(d), abs(b))
    d0, b0 = d // c, b // c
    u = gcd(abs(d0), a)
    v = gcd(q, abs(d0 + b0))
    D = q * d
    N = a * (d + b) - q * d
    content = gcd(abs(D), abs(N))
    if content != c * u * v:
        raise RuntimeError("projective content factorization")
    if gcd(u, v) != 1:
        raise RuntimeError("cross-edge factor coprimality")
    return {"D": D, "N": N, "g": content, "c": c, "u": u, "v": v}


def required_content(*, load: Q, D: int, critical_depth: int, height_cap: int) -> int:
    """Least integral g certifying both Cycle-170 depth constraints."""
    if load < 0 or D == 0 or critical_depth <= 0 or height_cap <= 0:
        raise ValueError("invalid deep-packet threshold")
    return _ceil(max(load * critical_depth, Q(abs(D) * critical_depth, height_cap)))


def is_deep(*, content: int, load: Q, D: int, critical_depth: int, height_cap: int) -> bool:
    """Exact equivalence to simultaneous error and capacity depth at least L."""
    if content <= 0:
        raise ValueError("positive content required")
    return content >= required_content(load=load, D=D, critical_depth=critical_depth, height_cap=height_cap)


def cycle170_depth_failure(*, content: int, load: Q, D: int, critical_depth: int, height_cap: int) -> str:
    """Retain Cycle 170's ordered error/capacity failure within preeligible rows."""
    if content <= 0:
        raise ValueError("positive content required")
    error_required = _ceil(load * critical_depth)
    capacity_required = _ceil(Q(abs(D) * critical_depth, height_cap))
    if content < error_required:
        return "error_supported_depth"
    if content < capacity_required:
        return "denominator_capacity"
    return "seeded_deep_packet"


def factor_allocation(required: int) -> dict[str, int]:
    """Frozen log-balanced thresholds whose product is at least required."""
    if required <= 0:
        raise ValueError("positive required content")
    c_min = _cube_ceil(required)
    u_min = _sqrt_ceil(Q(required, c_min))
    v_min = _ceil(Q(required, c_min * u_min))
    if c_min * u_min * v_min < required:
        raise RuntimeError("allocation product")
    return {"c_min": c_min, "u_min": u_min, "v_min": v_min}


def low_content_reason(*, c: int, u: int, v: int, required: int) -> str:
    """First retained divisor coordinate preventing a deep content certificate."""
    if min(c, u, v, required) <= 0:
        raise ValueError("positive divisor data")
    if c * u * v >= required:
        return "deep_content"
    allocation = factor_allocation(required)
    if c < allocation["c_min"]:
        return "source_core"
    if u < allocation["u_min"]:
        return "numerator_absorption"
    if v < allocation["v_min"]:
        return "denominator_absorption"
    raise RuntimeError("incomplete low-content allocation")


def normalized_cap(*, D: int, required: int, critical_depth: int, height_cap: int) -> Q:
    """Return the uniform H/L cap implied by the retained capacity threshold."""
    if D == 0 or min(required, critical_depth, height_cap) <= 0:
        raise ValueError("invalid normalized cap")
    actual = Q(abs(D), required)
    cap = Q(height_cap, critical_depth)
    if actual > cap:
        raise RuntimeError("capacity cap lost")
    return cap


def moment_population_lower_bound(*, weighted_content: Q, eligible_mass: Q, critical_depth: int, height_cap: int) -> Q:
    """Sharp pointwise lower bound from M=sum w*g/G to deep eligible mass."""
    if eligible_mass < 0 or critical_depth <= 0 or height_cap <= critical_depth:
        raise ValueError("requires H>L and nonnegative mass")
    return max(Q(0), (weighted_content - eligible_mass) / (Q(height_cap, critical_depth) - 1))


def verify_weighted_transfer(*, rows: list[tuple[Q, Q]], cap: Q) -> dict[str, Q]:
    """Verify the sharp pointwise moment ledger for labelled eligible rows."""
    if cap <= 1:
        raise ValueError("requires cap greater than one")
    mass = Q(0)
    moment = Q(0)
    deep_mass = Q(0)
    for weight, normalized_content in rows:
        if weight < 0 or normalized_content <= 0 or normalized_content > cap:
            raise ValueError("invalid labelled row")
        mass += weight
        moment += weight * normalized_content
        if normalized_content >= 1:
            deep_mass += weight
    lower = max(Q(0), (moment - mass) / (cap - 1))
    if deep_mass < lower:
        raise RuntimeError("moment population transfer")
    return {"mass": mass, "moment": moment, "deep_mass": deep_mass, "lower_bound": lower}


def verify_all() -> dict[str, object]:
    # Exhaustive small signed range checks the factorization and ordered web.
    checked = 0
    for d in range(-8, 9):
        if d == 0:
            continue
        for b in range(-8, 9):
            for q in range(1, 8):
                for a in range(1, 8):
                    if gcd(a, q) != 1:
                        continue
                    data = factor_content(d=d, b=b, q=q, a=a)
                    checked += 1
                    required = required_content(load=Q(17, 6), D=data["D"], critical_depth=5, height_cap=20)
                    if is_deep(content=data["g"], load=Q(17, 6), D=data["D"], critical_depth=5, height_cap=20) != (data["g"] >= required):
                        raise RuntimeError("depth equivalence")
                    depth_reason = cycle170_depth_failure(content=data["g"], load=Q(17, 6), D=data["D"], critical_depth=5, height_cap=20)
                    if (depth_reason == "seeded_deep_packet") != (data["g"] >= required):
                        raise RuntimeError("ordered Cycle-170 failure")
                    reason = low_content_reason(c=data["c"], u=data["u"], v=data["v"], required=required)
                    if (reason == "deep_content") != (data["g"] >= required):
                        raise RuntimeError("obstruction equivalence")
                    normalized_cap(D=data["D"], required=required, critical_depth=5, height_cap=20)
    if divisor_content(15) != 15 or divisor_content(60) != 60:
        raise RuntimeError("divisor expansion")
    # M=1-epsilon on unit mass has no forced deep mass; M=4 on cap 4 forces all mass.
    if moment_population_lower_bound(weighted_content=Q(1), eligible_mass=Q(1), critical_depth=5, height_cap=20) != 0:
        raise RuntimeError("subcritical moment")
    if moment_population_lower_bound(weighted_content=Q(4), eligible_mass=Q(1), critical_depth=5, height_cap=20) != 1:
        raise RuntimeError("sharp cap moment")
    ledger = verify_weighted_transfer(rows=[(Q(1, 2), Q(99, 100)), (Q(1, 2), Q(4))], cap=Q(4))
    if ledger["deep_mass"] != Q(1, 2) or ledger["lower_bound"] > Q(1, 2):
        raise RuntimeError("labelled transfer ledger")
    return {
        "factorization": "gcd(|qd|,|a(d+b)-qd|)=c*u*v with c=gcd(|d|,|b|), u=gcd(|d/c|,a), v=gcd(q,|d/c+b/c|); gcd(u,v)=1, while c may share primes with either factor",
        "eligibility": "for seed/range-valid pairs, g>=ceil(max(L Lambda,L|D|/H)) iff both Cycle-170 depths reach L, including Lambda=0",
        "cap": "g/G_req<=H/L because g divides D and G_req>=|D|L/H",
        "divisor_expansion": "g=sum_{r|cuv} phi(r), with every divisor row retaining its original eligible pair label and factor triple",
        "transfer": "if M=sum w g/G_req and W=sum w on an eligible bank with H>L, deep mass is at least max(0,(M-W)/(H/L-1)); this is supremally sharp as subcritical normalized content tends to 1 from below and deep content tends to H/L",
        "obstruction": "below required content, retain Cycle 170's error-before-capacity failure and independently route the factor deficit by an exhaustive frozen source-core/numerator-absorption/denominator-absorption order",
        "exhaustive_cases": checked,
        "boundary": "This is a finite eligibility-weighted divisor-content classifier and conditional moment transfer. It proves no actual moment lower bound, compatible population, recurrence, skeleton, density, or interval gain.",
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
