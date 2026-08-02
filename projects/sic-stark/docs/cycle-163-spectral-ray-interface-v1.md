# Cycle 163 / B001: fixed-full-ray selector prototype

## Outcome

PROVED: the preregistered fixed-full-ray direct-selector class is
falsified. With the frozen positive lift in Q(sqrt(21)), exactly 18 of the
36 characteristics generate an ideal coprime to the finite modulus 6; the
other 18 do not. A direct assignment of every additive coefficient to a
class in one fixed Cl_(6)infinity_2 is therefore not defined on its
declared domain.

PROVED: the two independently frozen orientation anchors survive the
domain test: (3,5) and (3,4) are eligible for the full modulus, with the
previously certified ray-log conventions g^1 and g^2.

## Exact derivation

The replay enumerates the lexicographic 6-by-6 characteristic grid. For
each (a,b), it selects the maximal p-star congruent to a modulo 6 for which
b*(5-sqrt(21))/2-p-star is positive. The comparison is made by a squared
integer inequality with a sign guard; no floating-point arithmetic is used.
It then evaluates

    N(b*beta-p-star) = p-star^2 - 5*p-star*b + b^2

and applies the preregistered eligibility predicate gcd(abs(N),6)=1.

The executable checks the 36 exact rows, the frozen Shintani action, and
the orientation anchors. The totality prerequisite fails before a
ray-discrete-log multiplicity test is meaningful. This result is
independent of a logarithm branch, a boundary finite part, packet
evaluation, or an AFK-cocycle identification.

## Containment and gate

This result does not disprove a characteristic-dependent conductor-lowering
or ray-monoid lift, the analytic coefficient-to-cocycle interface, fusion
continuity, a Stark identity, or dimension-six TCC. Those would require
additional data that the direct selector intentionally does not supply.

STRATEGIC_DECISION: adopt the companion recommendation to seal this scoped
exact falsifier and make Cycle 164 / B002 the first prototype for an
orientation-preserving characteristic-dependent conductor-lowering /
ray-monoid state space. Its advance condition must include an explicit map
from every reduced object back to one common primitive target; lowered
absolute values or an unspecified lift do not advance the gate.

The decision would be invalidated if a later claim treats the 18
noncoprime rows as an obstruction outside this frozen positive-lift,
fixed-full-modulus construction class.

## Reproduction

```sh
python3 proof/verify_cycle_163_fixed_full_ray_selector.py \
  --output discovery/cycle-163-fixed-full-ray-selector-prototype-v1.json
python3 proof/build_cycle_163_spectral_ray_interface_v1.py --check
python3 -m unittest tests.test_cycle_163_fixed_full_ray_selector -v
```

The canonical pre-execution freeze is
docs/cycle-163-spectral-ray-interface-preregistration-v1.md.
