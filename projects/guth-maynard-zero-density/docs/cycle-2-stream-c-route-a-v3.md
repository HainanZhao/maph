# Cycle 2, Stream C, Route A v3: hostile correction and closure

## Outcome and correction

`PROVED`: Route A v2 overstated its explicit-formula closure.  Its CHJ-I
input has (\alpha\le1/2), so it reaches the uniform truncation
(T\asymp x^{13/30}), but not the almost-all truncation
(T\asymp X^{13/15}).  Its phrase “all zeros” also did not independently
state a multiplicity convention.  v2 is retained unchanged; v3 replaces
only that dependency path.

`PROVED`: v2 also embedded `wall_time_ns` in its mathematical artifact, so a
replay changed its bytes.  v3 has deterministic `--write` and `--check`
commands; optional runtime capture is isolated in a separate performance
artifact and is not evidence for any mathematical claim.

`PROVED`: the published-primary access record for Iwaniec Theorem 10.1,
corroborated by the now-frozen Kedlaya archival theorem, gives an arbitrary-
(T) half-weighted von-Mangoldt formula.  This covers both truncation scales.
The formula is converted at integer endpoints, so its nearest-other-prime-
power term is harmless.  No new density theorem, prime theorem, or exponent
is claimed.

## Formula and conventions

For (z\ge2), arbitrary (T>0), the source chain gives a zero sum truncated
by ordinate and remainder

\[
O\!\left(\frac zT\log^2(zT)+\log z\min\{1,z/(T\langle z\rangle)\}\right).
\]

At integer endpoints the half-weight change is (O(\log X)) and
\(\langle z\rangle\ge1\).  Thus for (2\le T\le X) subtraction at the
two endpoints yields GM's weaker (O(X(\log X)^3/T)) formula.

The residue of (-\zeta'/\zeta) at an order-(m) zero is (m), fixing the
formula's zero sum to the multiplicity convention independently of CHJ's
wording.  HSW plus Bui--Heath-Brown supplies the corresponding local count.
Also, (0<\Re\rho<1) shows that the cutoff conventions 
\(|\rho|<T\) and \(|\Im\rho|<T\) differ only in
\(T-1/T<|\Im\rho|\le T\); the boundary contribution is
\(O(X\log T/T)\), absorbed by the formula error.

## Both scales

- `PROVED` uniform: (T=x/y\,e^{2(\log x)^{1/4}}) has endpoint power
  (13/30<1/2), hence both CHJ-I and the arbitrary-(T) chain are valid.

- `PROVED` almost-all: with
  (\delta=X^{-13/15+\epsilon/2}),
  (T=\delta^{-1}e^{4(\log X)^{1/4}}) has power (13/15>1/2).
  CHJ-I is invalid here; the arbitrary-(T) chain is valid because
  (2\le T\le X) eventually.

Huxley retains the near-one logarithmic density input, Ford plus
Platt--Trudgian the all-height VK cutoff, and HSW--Bui the pair kernel.
Prime powers contribute
\(O((y/X^{1/2}+1)(\log X)^2)\), negligible at
\(y\ge X^{2/15+\epsilon}\); partial summation then gives the stated prime
counts, with a weaker permitted error.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/replay_cycle2_stream_c_route_a_v3.py --write
python3 projects/guth-maynard-zero-density/proof/replay_cycle2_stream_c_route_a_v3.py --check
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle2_stream_c_route_a_v3.py -v
```

Optional non-deterministic timing is written separately by `--write-performance`.
