# SIC--Stark research cycle 148': boundary-integral audit

Date: 2026-07-28

## Direct contour verdict

\[
\boxed{\text{the original vertical contour is not absolutely
convergent at }g=Q,\ \tau=\beta_6.}
\]

At the positive real boundary periods, Sarkissian--Spiridonov
equations (40)--(41) give, for \(y=i\lambda\),

\[
 \Gamma_M(y,m)
 \sim Z(m)e^{-\pi iB_{2,2}(y)/(48)},
\]

\[
 \Gamma_M(Q-y,-m)
 \sim Z(-m)^{-1}e^{+\pi iB_{2,2}(Q-y)/(48)}.
\]

Since

\[
 B_{2,2}(Q-y)=B_{2,2}(y),
\]

the quadratic exponentials cancel and the kernel tends to the nonzero
constant \(Z(m)/Z(-m)\).

The remaining equation-(66) phase has modulus

\[
 \left|
 e^{\pi i\alpha(2i\lambda-Q)/(24\omega_1)}
 \right|
 =
 e^{-2\pi\alpha\lambda/(24\omega_1)}.
\]

For \(\alpha>0\) it grows at the negative end; for \(\alpha<0\) it
grows at the positive end; for \(\alpha=0\) it does not decay at
either end. Hence there is no single absolutely convergent vertical
contour for all 36 frequencies.

The convergent six-gamma beta integral in the main theorem does not
retain its decay after the degeneration \(g=Q\). Equation (66) still
evaluates the result meromorphically:

\[
 24\Gamma_M(-\alpha,4-N)
   \Gamma_M(\alpha,N)\Gamma_M(Q,0),
\]

but this is an analytic-continuation/distributional value, not the
original vertical integral.

## Single residual lemma

Only one honest boundary statement remains:

> **Arithmetic fusion-continuity lemma.** The meromorphic spectral
> periodization from the two-base chamber has a boundary value at
> \(\tau=\beta_6\), with
> \(\beta_6+\beta_6^{-1}=5\), equal to the convention-matched AFK
> double-sine cocycle packet, preserving all lens labels and the odd
> multiplier \(\psi^2(A_6)=-1\).

This is the successor closure target. Treating fusion as a generic
removable singularity would discard the trace-integrality condition
and is not permitted.

## Status

| Statement | Status |
|---|---|
| Meromorphic equation-(66) boundary value | `VERIFIED` |
| Original vertical endpoint contour | `EXCLUDED` |
| Arithmetic fusion-continuity lemma | `OPEN` |
