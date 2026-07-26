# SIC--Stark research cycle 3: exact Zauner reduction of TCC

Date: 2026-07-26

## Outcome

The characteristic-covariance question left open in cycle 2 has an exact
answer:

\[
\boxed{
\mathfrak S^{\,L_d\boldsymbol q/d}_{A_d^\epsilon}(\beta_d)
=
\mathfrak S^{\,\boldsymbol q/d}_{A_d^\epsilon}(\beta_d),
\qquad \epsilon\in\{1,-1\}.
}
\]

There is no phase defect. Consequently, the canonical TCC residual is
constant on Zauner orbits of its output index. The zero-output equation is
already a proved identity. The number of unresolved equations is therefore

\[
M_d=
\begin{cases}
(d^2-1)/3,&3\nmid d,\\
d^2/3+1,&3\mid d.
\end{cases}
\]

This is an exact reduction, not a proof of the remaining \(M_d\) identities.

## 1. The source transformation theorem

Theorem `lem:MTransformOfSFmodular` in Appleby--Flammia--Kopp states the
following. Let \(t=(d,r,Q)\), let \(M\in GL_2(\mathbb Z)\), and let \(t_M\)
be the tuple formed using the transformed quadratic form. For either
\(B_t=A_t\) or \(B_t=A_t^{-1}\),

\[
\mathfrak S^{\,\boldsymbol p/d}_{B_{t_M}}(\beta_{t_M})
=
\mathfrak S^{\,\ell M\boldsymbol p/d}_{B_t}(\beta_t)
\qquad(\det M=1),
\]

where

\[
\ell=\operatorname{sgn}(j_{M^{-1}}(\beta_t)).
\]

The theorem explicitly includes the zero characteristic and every
nonzero residue characteristic needed by TCC.

## 2. Specialization to the canonical form

Take

\[
Q_d(x,y)=x^2+(1-d)xy+y^2,\qquad
L_d=\begin{pmatrix}d-1&-1\\1&0\end{pmatrix}.
\]

Direct substitution proves

\[
Q_d(L_d(x,y))=Q_d(x,y).
\]

Thus \(Q_{d,L_d}=Q_d\), so \(t_{L_d}=t\). Also

\[
L_d\cdot\beta_d=\beta_d,\qquad
A_d=L_d^3,\qquad
L_d^{-1}A_dL_d=A_d.
\]

Finally,

\[
L_d^{-1}=
\begin{pmatrix}0&1\\-1&d-1\end{pmatrix},
\qquad
j_{L_d^{-1}}(\beta_d)=d-1-\beta_d=\beta_d^{-1}>0.
\]

Hence \(\ell=1\). Applying the transformation theorem with \(M=L_d\)
separately for \(B_t=A_t\) and \(B_t=A_t^{-1}\) proves

\[
\mathfrak S^{\,L_d\boldsymbol q/d}_{A_d^\epsilon}(\beta_d)
=
\mathfrak S^{\,\boldsymbol q/d}_{A_d^\epsilon}(\beta_d),
\qquad \epsilon\in\{1,-1\}.
\]

This uses a proved functional equation; it does not assume TCC, Stark's
conjecture, or algebraicity of the special values.

For compactness, set

\[
u_d(\boldsymbol q):=
\mathfrak S^{\,\boldsymbol q/d}_{A_d}(\beta_d).
\]

Because \(A_d\) fixes \(\beta_d\), the cocycle inverse law gives

\[
\mathfrak S^{\,\boldsymbol q/d}_{A_d^{-1}}(\beta_d)
=u_d(\boldsymbol q)^{-1}.
\]

## 3. Covariance of the convolution

For the shift-one canonical kernel \(Z=I+L_d\), define

\[
R_d(\boldsymbol p)=
\sum_{\boldsymbol q\in\mathcal I_{\boldsymbol p}}
\omega_d^{\langle\boldsymbol p,Z\boldsymbol q\rangle}
\frac{u_d(\boldsymbol q)}
{u_d(\boldsymbol q-\boldsymbol p)}.
\]

Cycle 2 proved

\[
\langle L_d\boldsymbol p,ZL_d\boldsymbol q\rangle
=\langle\boldsymbol p,Z\boldsymbol q\rangle\pmod d.
\]

If \(\mathcal I_{\boldsymbol p}\) is an allowed transversal containing
\(\boldsymbol0\) and \(\boldsymbol p\), then
\(L_d\mathcal I_{\boldsymbol p}\) is an allowed transversal containing
\(\boldsymbol0\) and \(L_d\boldsymbol p\). Changing variables
\(\boldsymbol q\mapsto L_d\boldsymbol q\), and using special-value
invariance in the numerator and denominator, gives

\[
\boxed{R_d(L_d\boldsymbol p)=R_d(\boldsymbol p).}
\]

This also handles even dimensions without reducing transformed integer
representatives: TCC permits any complete transversal, and the source
transformation theorem is stated for unreduced integer characteristics.

## 4. The zero-output equation is already proved

The source TeX contains a subtle transcription hazard:
`A\vpu{-1}_t` uses `\vpu` only to insert an invisible superscript for
vertical spacing. It denotes \(A_t\), not \(A_t^{-1}\). The second TCC
factor is genuinely indexed by \(A_t^{-1}\).

For \(\boldsymbol p=\boldsymbol0\), the phase is \(1\), and every summand is

\[
\mathfrak S^{\,\boldsymbol q/d}_{A_d}(\beta_d)
\mathfrak S^{\,\boldsymbol q/d}_{A_d^{-1}}(\beta_d)
=u_d(\boldsymbol q)u_d(\boldsymbol q)^{-1}=1.
\]

There are \(d^2\) representatives, so

\[
\boxed{R_d(\boldsymbol0)=d^2}
\]

unconditionally. This is also stated explicitly at the end of the source's
proof of `thm:ghstExist`. The zero orbit does not require proof.

## 5. Equation count

The action of \(L_d\) on \((\mathbb Z/d\mathbb Z)^2\) has order three.
It has one fixed point when \(3\nmid d\) and three fixed points when
\(3\mid d\). All other orbits have size three. Therefore

\[
\#\bigl((\mathbb Z/d\mathbb Z)^2/\langle L_d\rangle\bigr)
=
\begin{cases}
(d^2+2)/3,&3\nmid d,\\
d^2/3+2,&3\mid d.
\end{cases}
\]

Removing the already-proved zero orbit leaves

\[
\boxed{
M_d=
\begin{cases}
(d^2-1)/3,&3\nmid d,\\
d^2/3+1,&3\mid d.
\end{cases}
}
\]

`canonical_tcc_equation_representatives()` returns exactly these nonzero
output indices.

`canonical_tcc_formal_signature()` replaces each special value by a formal
variable indexed by its Zauner orbit and records every phase-weighted formal
quotient. The test suite verifies, as a symbolic identity rather than a
floating-point sample, that the signatures for \(\boldsymbol p\) and
\(L_d\boldsymbol p\) coincide.

## 6. What remains

The automatic symmetry and normalization layers are now exhausted. The next
work should attack a genuinely nonzero convolution identity.

The most promising questions are:

1. **Primitive-output identity.** After inserting the cycle-2
   three-\(S\)-kernel expression, can one prove the representative equation
   at \(\boldsymbol p=(1,0)\),
   \[
   \sum_{\boldsymbol q}
   \omega_d^{\langle(1,0),Z\boldsymbol q\rangle}
   \frac{u_d(\boldsymbol q)}
   {u_d(\boldsymbol q-(1,0))}=0,
   \]
   by a double-sine distribution relation?
2. **Finite-correction telescope.** Do the modular-to-Jacobi finite
   q-Pochhammer corrections telescope inside that quotient?
3. **Cyclotomic Fourier transform.** Does the orbit-reduced convolution
   diagonalize after a finite symplectic Fourier transform?
4. **Formal countermodel.** Which known functional equations, beyond
   Zauner covariance and reciprocal pairing, are necessary to force
   idempotency?

Question 1 is now the smallest nontrivial scalar identity and is the
recommended cycle-4 target.

## Primary-source anchors

- Appleby--Flammia--Kopp, arXiv:2501.03970:
  Theorems `thm:AtmrhotmExpressions` and
  `lem:MTransformOfSFmodular`, the transformed-transversal calculation in
  the proof of `thm:MtransformedTuples`, and the automatic zero-output
  identity at the end of the proof of `thm:ghstExist`.
- Kopp, arXiv:2411.06763:
  Theorem 4.37, cited by the transformation theorem above.
