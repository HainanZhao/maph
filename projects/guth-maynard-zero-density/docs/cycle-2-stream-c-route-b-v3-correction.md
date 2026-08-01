# Cycle 2 — Stream C Route B v3 correction

Claim boundary: `OBSERVED` is the status of the full Route-B source chain in
this version. The external truncated-explicit-formula theorem cited by
Guth--Maynard has not yet been checked against a pinned primary source.
`PROVED` labels below apply only to the stated correction or exact transfer.
V1 and v2 are preserved unchanged.

## Correction 1: Huxley bibliographic identity

`PROVED`: v2 misidentified its frozen Huxley source. The correct citation is

> M. N. Huxley, *On the difference between consecutive primes*, Invent.
> Math. 15 (1972), 164–170.

The v2 citation to “The distribution of zeros of the Riemann zeta-function,”
pp. 141–163, is wrong. The cause was a metadata transcription error. The
frozen volume itself and Guth--Maynard's bibliography identify the corrected
article.

`PROVED`: the affected mathematics is unchanged. Equation (1.9), at printed
p. 164 / PDF p. 173, still gives

\[
N(s,T)\ll T^{3(1-s)/(3s-1)}(\log T)^{44}
\]

uniformly on (3/4le sle1), with (-Tlegammale T). On
(4/5le sle1), the exact retained comparison is

\[
\frac{30}{13}-\frac3{3s-1}
=\frac{3(30s-23)}{13(3s-1)}\ge\frac {15}{91}.
\]

Thus only the bibliographic identity, not the theorem, its locator,
conventions, log factor, or exponent computation, is corrected.

## Correction 2: full-route status

`PROVED`: Guth--Maynard's TeX lines 2407–2417 visibly display a truncated
explicit formula and cite Davenport, Chapter 17. That display is not itself
the required external-source audit. The theorem's endpoint conventions,
zero-sum and multiplicity convention, uniformity, and error term have not
yet been independently checked.

`OBSERVED`: the external truncated-explicit-formula node is consequently
retained as a blocker. The full Stream-C Route-B and G0 labels are **not** a
PASS in v3. The previously checked Huxley, Ford, Platt--Trudgian,
Hasanalizade--Shen--Wong, and Bui--Heath-Brown nodes remain individual
`PROVED` partial closures.

Next authorized action: verify the literature agent's pinned
truncated-explicit-formula ledger, including all conventions, before any
whole-route promotion.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/replay_short_intervals_stream_c_route_b_v3.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-route-b-v3.json
python3 -m unittest discover -s projects/guth-maynard-zero-density/tests -p 'test_*.py'
```

The versioned machine record is
[cycle-2-stream-c-route-b-v3.json](../artifacts/cycle-2-stream-c-route-b-v3.json)
and the corrected ledger is
[cycle-2-stream-c-source-ledger-v3.json](../artifacts/cycle-2-stream-c-source-ledger-v3.json).
