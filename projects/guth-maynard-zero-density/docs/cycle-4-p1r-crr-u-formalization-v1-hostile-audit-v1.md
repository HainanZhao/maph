# Cycle 4 CRR-U formalization v1: hostile audit v1

## Outcome

`OBSERVED`: **FAIL**. The sealed v1 files are preserved unchanged. This audit
does not decide CRR-U and does not authorize a search.

The formalization has soundly separated its new rational predicate from the
Guth--Maynard heuristic remark, fixed one common pair `(b,W)`, and prohibited
discovery. Its source-bound compatibility claim nevertheless fails for its
own slackened witness thresholds.

## F1: source threshold versus the admitted Base(v) threshold

`PROVED`: Guth--Maynard's relevant large-value/energy applications require a
pointwise hypothesis of the form `|D_N(t)| >= N^sigma` (GM source lines
732--740 and 1803--1808). V1 fixes `N=L=v^10` but permits only

```text
|D_v(t)| >= v^(7-delta(v)),  delta(v)=1/sqrt(log v).
```

Thus the source parameter matching the admitted witness is exactly

```text
sigma_v = 7/10 - delta(v)/10,
```

not the fixed `7/10` used to produce v1's claimed exact lists. Direct
substitution gives the large-value rows

```text
6+2delta, 8+4delta, 8+4delta,
```

the energy rows at the cardinality upper edge

```text
20+5delta, 20+(37/8)delta, 20+5delta,
```

and the four S3 rows

```text
36+(3/2)delta, 36+3delta, 36+3delta, 36+(45/16)delta.
```

These are compatible at leading exponent, but they are not the asserted
exact `[6,8,8]`, `[20,20,20]`, and `[36,36,36,36]` identities for the actual
v1 witness. This is a source-application defect, not evidence against a
future compatibility or incompatibility theorem.

## F2: rational/affine slack is omitted

`PROVED`: v1's RationalMass(v) asks for a set of measure at least
`v^(-4-delta)` on which `Rtilde >= v^(6-delta)`. For
`f=psi*|Rtilde|^2`, this yields lower moment exponents

```text
integral f >= v^(8-3delta),
integral f^2 >= v^(20-5delta).
```

With `M=v^2`, the two affine expressions from GM Proposition `propsumaff`
(lines 1408--1422) have exponents `28-6delta` and `28-5delta`, respectively.
They are not the v1 code's exact `[28,28]` tie.

## F3: Fourier phase/reality label is incomplete

`PROVED`: for real `w` and
`hat(f)(xi)=integral f(u)e(-xi*u)du`, one has

```text
conjugate(hat(h_a)(mL)) = hat(h_(-a))(-mL).
```

After reversing `t2` and `t3`, the exact induced involution is

```text
conjugate(I_(m1,m2,m3)) = I_(-m3,-m2,-m1).
```

The all-nonzero-coordinate sum is invariant under this full map, so its
reality is recoverable. V1 says only “`m -> -m`” without the required
coordinate permutation. That fails the repository requirement to derive and
pin phase/label identities exactly.

## Consequence

`OBSERVED`: v1 is `CONTAINED_FAIL`; CRR-U remains `CONJECTURED` and open.
Search remains prohibited. A correction must create a new formalization
version, carry all explicit slack coefficients (or use exact non-slack
thresholds), supply the full phase involution, and pass a fresh hostile audit.
