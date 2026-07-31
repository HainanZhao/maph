# Cycle 074 — preliminary B2 transport and contained halt

## Preliminary outcome

`SUPERSEDED_PRELIMINARY_TRANSPORT`: target-free exact arithmetic
initially appeared to transport the constructor automorphism
\(\gamma\) to the frozen analytic source character as follows:

| case | preliminary \(\theta(\gamma)\) | orientation |
|---|---:|---|
| RQ-000129 | \(-i\) | inverse |
| RQ-001280 | \(-i\) | inverse |
| RQ-001569 | \(i\) | direct |
| RQ-001894 | \(i\) | direct |
| RQ-007519 | \(i\) | direct |

The preliminary Frobenius test compared the packet polynomial
generator with its \(p\)-th power modulo a separator prime. It did not
read a phase, rotation, logarithmic coefficient, or \(L'\) value.

## Preregistered halt

When that sealed preliminary transport was used for a one-orientation
replay, four rows matched and RQ-007519 did not. Its minimum
componentwise gap was approximately \(10.58\), so the branch halted
under the preregistered disagreement rule. No inverse search was used
to repair the row.

Heightened scrutiny then falsified the preliminary Frobenius test.
At RQ-007519 the packet polynomial generator does not generate the
full residue field at \(5\). Two primitive automorphisms can therefore
agree on that residue even though they differ on the ring of integers.
This cycle is preserved as a failed path and is superseded by the
full-integral-basis correction in cycle 075.

## Contained preregistration violation

`PREREGISTRATION_INPUT_VIOLATION_CONTAINED`: after the preliminary
five-case output had been computed, a provenance check opened the
RQ-000129 auxiliary-prime certificate. That certificate also embeds
an already-known primitive \(L'\) ball. The value was not used by the
transport logic.

The final full-integral-basis correction was computed after this
exposure. Its code is target-free and independently inspectable, but
the chronology is not called pristine.

## Preserved evidence

The false assumption, preliminary result, correction, and exposure
are all recorded in `artifacts/b2-artin-transport-v1.json`. The
corrected replay is:

```bash
python3 proof/audit_b2_artin_transport.py
```
