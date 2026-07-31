# Cycle 075 — corrected B2 integral-basis Artin transport

## Correction

`PROVED_EXACT_TRANSPORT`: Frobenius is checked on a full integral
basis, not only on the packet polynomial generator.

For RQ-007519 at \(p=5\), congruences on every element of `nf.zk`
select one Frobenius automorphism. The constructor \(\gamma\) is its
inverse. Since both real-base primes above \(5\) have
source-character value \(i\), the corrected result is
\[
\theta(\gamma)=-i.
\]
Thus the Dedekind coefficient uses the inverse analytic orientation.

The final exact table is:

| case | \(\theta(\gamma)\) | orientation |
|---|---:|---|
| RQ-000129 | \(-i\) | inverse |
| RQ-001280 | \(-i\) | inverse |
| RQ-001569 | \(i\) | direct |
| RQ-001894 | \(i\) | direct |
| RQ-007519 | \(-i\) | inverse |

The two non-quarantined routes for each of the four later controls
share the same exact source character. RQ-000129's second route
remains quarantined and is not used for promotion.

## One-orientation replay

`OBSERVED`: the sealed one-orientation numerical replay matches one
quarter turn in all five cases and never searches the conjugate
orientation. The weak-unit coefficient is still a point evaluation
from an exact unit rather than an Arb enclosure, so the five-row
statement is not tagged proof or certified numerical.

## Preserved failures and boundary

The generator-only false transport, the resulting RQ-007519 halt, and
the preregistration input exposure are preserved in cycle 074 and
`artifacts/b2-artin-transport-v1.json`.

The final exact replay is target-free at the code level, but it ran
after the contained exposure and is not labeled chronologically
pristine. No theorem statement relies on the numerical five-row
match: B1 remains the proof route.

## Replay

```bash
python3 proof/audit_b2_artin_transport.py
python3 proof/replay_b2_oriented_phase.py
```

No submission, circulation, or outbound message is authorized.
