# P7-1 norm aggregation: v2 reconciliation correction

## Boundary

`PROVED`: the mathematical P7-1 conclusion of v1 is unchanged:

\[
A_{\chi_{(3)}}(17)=-2,\quad A_{\chi_{(1+i)^4}}(17)=2,
\quad a_{\mathbb Q(i)}(n)=\sum_{d\mid n}\chi_{-4}(d)\leq\tau(n).
\]

`PROVED_CONDITIONAL_ON_LENGTH_HEIGHT_RELATION`: the divisor normalization is
exponent-harmless for the cited single-polynomial Guth--Maynard Theorem 1.1
only in \(N\leq T^C\) for fixed \(C\), including the source proof's \(N<T\)
reduction.  No unrestricted \((N,T)\) absorption is asserted.

This correction repairs two label-only test assertions in the initial P7-1
reconciliation path.  It does not alter a calculation, source byte, or claim
boundary.  It remains a lightweight source/algebra/replay result, not a
hostile audit and not a Hecke-family theorem.

## Corrections retained

Route B v1 spelled its second aggregate as `A_chi_pi4(17)` while Route A used
`A_chi_pi4_17`; the intervening Route B v2 correction records the exact
bijection.  The original v1 reconciliation test then asked for the literal
phrase “cannot be invoked verbatim,” whereas its own artifact correctly said
“prevent verbatim use.”  The v2 replay checks the semantic boundary rather
than that accidental exact substring.  The original artifacts remain intact.

The pre-existing P7 preregistration-v2 unit-test spelling issue is likewise
retained as a contained test-assertion defect: its builder replay and sealed
artifact bytes agree, but the test expects a short list element while the
immutable artifact stores the longer phrase ending in “boundary.”

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/run_p7_norm_aggregation_route_a_v1.py --check
python3 proof/run_p7_norm_aggregation_route_b_v1.py --check
python3 proof/correct_p7_norm_aggregation_route_b_v2.py --check
python3 proof/reconcile_p7_norm_aggregation_v2_correction.py --check
python3 -m unittest tests/test_p7_norm_aggregation_v2.py -v
```
