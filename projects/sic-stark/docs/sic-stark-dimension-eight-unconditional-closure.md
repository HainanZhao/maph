# Unconditional closure of the formal TCC in dimension eight

## Theorem

For every dimension-eight admissible tuple \(t\),
\[
0,1\in\mathcal Z_t.
\]
If \(t,t'\) have forms of the same discriminant, then
\(\mathcal Z_t=\mathcal Z_{t'}\).  Thus the complete dimension-eight
instance of the formal Twisted Convolution Conjecture holds
unconditionally.

## Why there are two proofs

Dimension-eight admissibility has \(j=2\) and \(f_2=3\).  The form
conductor can therefore be \(3\) or \(1\), giving discriminants \(45\)
and \(5\).  AFK covariance transports within a fixed discriminant, not
between these two strata, so both must be closed separately.

### Discriminant 45

For the canonical conductor-three tuple, the order-ray packet is
transported to maximal-order conductor \(24\).  Its two missing quartic
orientations admit genuine linear Artin reinduction to quartic
characters over \(\mathbb Q(\sqrt{-6})\), with an independent check
over \(\mathbb Q(\sqrt{-30})\).  Stark's proved rank-one theorem over
an imaginary quadratic base supplies an integral oriented unit
resolvent.  Rigorous Arb balls isolate its unique unit coordinates,
and exact identities in the common normal closure return the
orientation to the original real-quadratic units.  The complete proof
and reproduction commands are in
`docs/sic-stark-dimension-eight-canonical-closure.md`.

### Discriminant 5

For \(Q=\langle1,-3,1\rangle\),
\[
A_t=\begin{pmatrix}377&-144\\144&-55\end{pmatrix}.
\]
The one-place ray group is \(C_2^2\), Kopp's exponent is one, and the
two supported characters are quadratic.  Their fields and oriented
units are
\[
\begin{aligned}
L_0&:\ h^4-h^2-1=0,
&u_0&=\phi+h,\\
L_1&:\ r^4-2r^2-4=0,
&u_1&=\frac{r+\phi}{r-\phi}.
\end{aligned}
\]
Both fields have class number one and successful unconditional
`bnfcertify` certificates.  The analytic class-number formula gives
\[
L'(0,\chi_0)=\log u_0,\qquad
L'(0,\chi_1)=\log u_1.
\]

The generic AFK evaluator has continued-fraction word
\([3,3,3,3,3,3,0]\).  Its magnitudes follow from these two quadratic
ray units and the exact lower-conductor correction.  Its signs are
also exact: factor
\[
1-e^{2\pi i t}=-2i e^{\pi i t}\sin(\pi t)
\]
in every finite \(q\)-Pochhammer product, shift each reciprocal double
sine into its positive fundamental interval, and reduce the remaining
phase in
\(\mathbb Q(\beta)\), \(\beta^2-3\beta+1=0\).
For all 63 nonzero characteristics the \(\beta\)-coefficient cancels
and the phase is an integral multiple of \(\pi\).  Its parity gives
the full radical table without numerical sign selection.

Writing
\[
x^2=u_0,\qquad d^2=\sqrt{u_1/u_0},\qquad a=xd,
\]
the table contains only
\[
\pm1,\ \pm x^2,\ \pm x^{-2},\
\pm d,\ \pm d^{-1},\ \pm a,\ \pm a^{-1}.
\]
After exact gluing with \(\mathbb Q(\zeta_{16})\), the two reconstructed
matrices each have trace one, zero idempotency defect, and all
\(784\) rank-two minors equal to zero.

The maximal-order proof is reproduced by:

```bash
gp -q scripts/dimension_eight_maximal_tuple_audit.gp
gp -q scripts/dimension_eight_maximal_quadratic_units.gp
python3 scripts/dimension_eight_maximal_sign_audit.py
python3 scripts/dimension_eight_maximal_exact_tcc.py
```

## Form-class completion

The maximal order of \(\mathbb Q(\sqrt5)\) has narrow class number one,
so every discriminant-five admissible form is transported from
\(\langle1,-3,1\rangle\).  The discriminant-45 order has ring class
number one, so the canonical conductor-three proof transports across
that stratum.  These are all divisors of \(f_2=3\), completing the
formal TCC in dimension eight.
