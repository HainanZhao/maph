# SIC--Stark research cycle 48: the exact dimension-seven SF phase

## Result

The AFK Shintani--Faddeev phase is now explicit for all \(48\) nonzero
characteristics.

For

\[
 A=\begin{pmatrix}204&-35\\35&-6\end{pmatrix},
\]

the Dedekind sum and Rademacher invariant are

\[
 s(204,35)=-\frac{37}{70},\qquad \Psi(A)=9.
\]

Because \(d=7\), \(j=m=1\), and \(f_{jm}/f=1\), AFK Definition 1.30 reduces
to

\[
 \phi_p
 =-\exp\!\left(-\frac{3\pi i}{4}\right)
   \xi_7^{-Q(p)}.
\]

Writing \(\zeta_{56}=\exp(2\pi i/56)\) and using
\(\xi_7=\zeta_{56}^{32}\), this becomes

\[
 \boxed{\phi_p=\zeta_{56}^{\,7-32Q(p)}}.
\]

Thus every raw cocycle phase is also exact:

\[
 \arg_{\zeta_{56}}\!\left(\operatorname{shin}_p\right)
 =
 \arg_{\zeta_{56}}(\widetilde\nu_p)
 -(7-32Q(p)).
\]

The normalized overlap is real, so its phase exponent is \(0\) or \(28\).

## Verification

`scripts/dimension_seven_phase_audit.py`:

- computes the Dedekind sum using exact rational arithmetic;
- checks \(\Psi(A)=9\);
- emits all \(48\) SF and raw-shin phase exponents; and
- verifies \(\widetilde\nu_p\widetilde\nu_{-p}=1\) to
  \(1.8\cdot10^{-9}\).

The phase gate is closed.  No numerical argument selection is used.

