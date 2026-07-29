# SIC--Stark research cycle 161: dimension-seven discriminant-eight closure

Date: 2026-07-29

## Purpose

Cycle 160 correctly withdrew the universal dimension-seven statement:
the existing certificate covered the conductor-two, discriminant-32
stratum, while admissibility also permits the conductor-one,
discriminant-8 stratum.  This cycle constructs and verifies the missing
packet independently.

## Tuple and analytic formula

For
\[
Q_{7,1}=\langle1,-4,2\rangle,\qquad \rho=2+\sqrt2,
\]
the AFK definitions give
\[
L_{7,1}=\begin{pmatrix}7&-4\\2&-1\end{pmatrix},\qquad
A_{7,1}=L_{7,1}^3=
\begin{pmatrix}239&-140\\70&-41\end{pmatrix}.
\]
The exact Rademacher invariant is zero.  The canonical
\(\mathrm{PSL}_2(\mathbb Z)\) word is
\([4,2,4,2,4,2,0]\), so the direct cocycle has six double-sine
factors with alternating periods \(2+\sqrt2\) and
\((2+\sqrt2)/2\).  This is a different analytic packet from the
discriminant-32 word \([6,6,6,0]\).

## Numerical gate

`scripts/dimension_seven_maximal_tuple_audit.gp` computes all 48
ray-class partial-zeta derivatives.  The one-place and two-place
ray groups modulo seven are \(C_6\) and \(C_6\times C_2\).
`scripts/dimension_seven_maximal_cocycle.py` takes signs from the
direct six-factor formula and magnitudes independently from those ray
derivatives.  It reports

```text
RECIPROCAL_MAX_RESIDUAL=1.110e-16
SHIFT_1_IDEMPOTENCY_RESIDUAL=8.711e-16
SHIFT_1_MAXIMUM_MINOR=4.063e-16
SHIFT_0_IDEMPOTENCY_RESIDUAL=5.624e-16
SHIFT_0_MAXIMUM_MINOR=3.257e-16
```

This result is `NUMERICAL`; it was the entry gate, not the proof.

## Analytic identification

`scripts/certify_dimension_seven_maximal_cocycle.py` evaluates the
six-factor magnitudes with Arb.  It isolates all six scalar-packet
roots and the two quartic roots.  At tolerance \(10^{-10}\),

```text
MAXIMUM_LOG_DIFFERENCE=[+/- 2.30e-11]
SHINTANI_SAFE_EXPONENT=16128
POWERED_HEIGHT_UPPER_BOUND=[+/- 3.71e-7]
VOUTIER_MINIMUM_DEGREE_3_TO_24=5.22795...e-5
HEIGHT_GAP_CERTIFIED=True
```

The exact phase calculation in
`scripts/dimension_seven_maximal_sign_audit.py` cancels every
\(2+\sqrt2\) coefficient and audits all 48 signs.  Thus the Arb
magnitude identification and the root labels determine the complete
signed packet without using binary64 signs as proof input.

## Exact packet and finite closure

The six nonquadratic signed values are the real roots used from
\[
\begin{aligned}
G(X)={}&X^{12}+4X^{11}-2X^{10}-22X^9-18X^8+16X^7\\
 &+41X^6+16X^5-18X^4-22X^3-2X^2+4X+1.
\end{aligned}
\]
The two exceptional values are the negative real roots of
\[
R(X)=X^4+2X^3+X^2+2X+1.
\]
Both polynomials are derived exactly by taking signed square roots of
the previously certified squared Stark-unit polynomials.  Both embed
in the degree-24 ray-14 overlap field.

`scripts/dimension_seven_maximal_exact_tcc.gp` selects every root by a
rational Sturm interval, installs the sixteen Zauner orbits using
\[
(a,b)\longmapsto(3b,2a-b)\pmod 7,
\]
and works in the same degree-48 compositum with
\(\mathbb Q(\zeta_{56})\) as the discriminant-32 proof.  For both
formal shifts it proves exactly

```text
TRACE_IS_ONE=1
NONZERO_IDEMPOTENCY_ENTRIES=0
MINOR_COUNT=441
NONZERO_MINORS=0
```

## Consequence

The missing representative \(Q_{7,1}\) is now proved.  Its
discriminant-8 order has wide class number one, so AFK covariance
transports the result to that complete stratum.  Together with the
banked discriminant-32 proof, this restores the universal
dimension-seven quantifier in Paper II.  Dimension eight remains
unchanged: both its conductor-one and conductor-three strata were
already proved independently.

## Publication hardening

The strengthened dimension-seven suite reports 12/12 tests in
43.5 seconds with peak RSS 179 MB.  The clean Paper-II extraction
reports 20/20 tests in 58.6 seconds.  The companion archive contains
115 files and rebuilt byte-identically twice.

One manifest-regeneration attempt failed before hashing because the
loop variable `path` overwrote zsh's special `PATH` array.  The empty
generated manifest was restored from the banked Git commit; no source,
certificate, or paper artifact was affected.  Regeneration was rerun
with a non-special variable and all 166 root-manifest entries verified.

## Tags

- tuple, ray structures, polynomial factorizations, sign table, and
  all finite minors: **VERIFIED**;
- direct analytic magnitude values: **ENCLOSED**;
- exploratory combined reconstruction: **NUMERICAL**;
- universal dimension-seven theorem: **VERIFIED** after the warning-free
  manuscript build, clean archive replay, deterministic arXiv build,
  and `certificates/paper-II-cycle161-release-seal.json`.
