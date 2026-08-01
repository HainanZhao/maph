# Stream-B Route Reconciliation v2

**PROVED claim boundary.** This is a deterministic comparison of the
pinned-source Route A v3 and Route B v1 application audits. It does not
re-prove the cited analytic theorems, establish a new zero-density estimate,
or promote G0. Stream C is outside scope.

Route A v3 adds the three coverage nodes left open in reconciliation v1:

- The three Theorem 1.1 terms are bounded by
  `A(sigma)=15(1-sigma)/(3+5sigma)` on `7/10 <= sigma <= 4/5`.
- The mean-value branch has the strictly positive exact residual
  `[250(sigma-3/4)^2+3/8]/[2(3+5sigma)(9-10sigma)]`.
- The Type-II comparison, absence of real non-trivial zeros, and positive
  dyadic-shell reassembly are explicit.

The old beta-cutoff wording is also corrected: `beta >= sigma` is a count
restriction, not part of the MP Type-I detector definition. The previous v1
and v2 records remain unmodified.

The resulting status is **PROVED: independent-route NARROW PASS for Stream B
only**. G0 remains **OBSERVED** pending Stream C. Reproduce and verify with:

```sh
python3 projects/guth-maynard-zero-density/proof/audit_cycle2_stream_b_route_a_v3.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-b-route-a-v3.json
python3 projects/guth-maynard-zero-density/proof/reconcile_cycle2_stream_b_routes_v2.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-b-route-reconciliation-v2.json
```
