# SIC--Stark research cycle 16: one positive exterior-square target

Date: 2026-07-27

## Outcome

Cycle 16 compresses the complete determinantal system from cycle 15
to one nonnegative scalar identity.  This is an exact reduction, not a
proof of TCC.

Let

\[
K=d\sqrt{d+1}\,\widetilde\Pi
\]

be the scalar-shifted RM Zak matrix from cycle 15.  Define

\[
\Delta _2(K)
=\frac12\left[
  \bigl(\operatorname{Tr}K^\dagger K\bigr)^2
  -\operatorname{Tr}\bigl((K^\dagger K)^2\bigr)
\right].
\]

Cauchy--Binet gives

\[
\boxed{
\Delta _2(K)
=\|\mathop{\bigwedge\nolimits^2}K\|_F^2
=\sum_{\substack{|I|=2\\|J|=2}}
  |\det K_{I,J}|^2.
}
\]

The trace of \(K\) is nonzero.  Consequently,

\[
\boxed{
\mathrm{TCC}
\iff \operatorname{rank}K=1
\iff \Delta _2(K)=0.
}
\]

Unlike a selected minor, \(\Delta _2\) is global, chart-free, and
positive in the distinguished complex embedding.  A proof may
therefore target one scalar boundary identity or estimate rather than
\(\binom d2^2\) separate cancellations.

## 1. Singular-value proof

Let \(s_1,\ldots,s_d\) be the singular values of \(K\).  Then

\[
\operatorname{Tr}K^\dagger K=\sum_i s_i^2,\qquad
\operatorname{Tr}\bigl((K^\dagger K)^2\bigr)=\sum_i s_i^4,
\]

and hence

\[
\Delta _2(K)=\sum_{i<j}s_i^2s_j^2.
\]

Every summand is nonnegative.  Thus \(\Delta _2(K)=0\) exactly when
at most one singular value is nonzero.  Since
\(\operatorname{Tr}K=d\sqrt{d+1}\ne0\), rank zero is excluded.

This argument avoids eigenvalues, Jordan blocks, pivot charts, and
the unsafe inference that a sum of signed principal minors vanishes
term by term.

## 2. Explicit RM partial-Fourier form

Cycle 15 defined

\[
W(a,k)
=\sum_{b\bmod d}\mu_{a,b}\tau_d^{\,b(a+2k)}
\]

so that

\[
d\,\widetilde\Pi_{j,k}=W(j-k,k).
\]

For \(j<\ell\) and \(k<m\), put

\[
E(j,\ell;k,m)
=W(j-k,k)W(\ell-m,m)
-W(j-m,m)W(\ell-k,k).
\]

Because \(K_{j,k}=\sqrt{d+1}\,W(j-k,k)\), every \(2\)-minor of
\(K\) is \((d+1)E(j,\ell;k,m)\).  Therefore

\[
\boxed{
\Delta _2(K)
=(d+1)^2
\sum_{j<\ell}\sum_{k<m}
|E(j,\ell;k,m)|^2.
}
\]

This is the promised single, explicit, positive RM identity.  It
retains the signed phases inside each exchange residual; the absolute
square is taken only after the bilinear cancellation.

## 3. Zauner sectors

If \(K=K_0\oplus K_1\oplus K_2\), then

\[
\mathop{\bigwedge\nolimits^2}K
=\bigoplus_a\mathop{\bigwedge\nolimits^2}K_a
\oplus\bigoplus_{a<b}(K_a\otimes K_b).
\]

Orthogonality of the character sectors gives a positive decomposition
of \(\Delta _2\) into the norms of these six pieces.  If the block
dimensions are \(n_0,n_1,n_2\), their total target dimension is

\[
\sum_a\binom{n_a}{2}+\sum_{a<b}n_an_b
=\binom d2.
\]

Thus Zauner symmetry organizes the certificate but does not reduce
its algebraic content.  Positivity does imply that a zero total forces
every sector norm to vanish, without having to know beforehand which
Zauner block contains the rank-one image.

## 4. What the compression does and does not solve

The certificate is not holomorphic: it uses complex conjugation in
the distinguished embedding.  It therefore does not directly become
an identity of modular cocycles over a formal coefficient field.
Its advantage is instead analytic.  Any argument establishing

\[
\bigl(\operatorname{Tr}K^\dagger K\bigr)^2
=\operatorname{Tr}\bigl((K^\dagger K)^2\bigr)
\]

automatically proves all minor identities at once.

The cycle-14 constant-overlap countermodel remains a decisive gate.
It is Hermitian and has
\(\operatorname{Tr}\widetilde\Pi
=\operatorname{Tr}\widetilde\Pi^2=1\), but it has positive and
negative nonzero eigenvalues.  Hence it has at least two nonzero
singular values and \(\Delta _2>0\).  The new fourth-order positive
moment is therefore genuinely stronger than the two automatic trace
moments.

The most concrete next analytic question is now:

\[
\textit{Can RM reflection or a boundary integral compute the fourth
positive moment }\operatorname{Tr}((K^\dagger K)^2)\textit{?}
\]

Reflection alone computes algebraic products without the adjoint and
does not answer this.  A successful theorem must connect the
distinguished complex conjugation to the RM characteristic involution
while retaining the exceptional zero characteristic.

## 5. Claim ledger

Proved in this cycle:

- the Cauchy--Binet sum-of-squares compression of all ghost minors;
- equivalence of TCC to the single scalar equation
  \(\Delta _2(K)=0\);
- the exact sheared partial-Fourier sum-of-squares formula;
- the positive Zauner-sector decomposition and its unchanged total
  dimension;
- separation of this fourth positive moment from the automatic
  algebraic trace moments.

Still open:

- an RM formula or bound forcing \(\Delta _2(K)=0\);
- a boundary identity relating the adjoint to characteristic
  reflection;
- TCC itself.

## Sources

- R. A. Horn and C. R. Johnson, *Topics in Matrix Analysis*,
  sections on compound matrices and singular values.
- T. Ishibashi, *Cyclic quantum Teichmüller theory*,
  [arXiv:2501.02316](https://arxiv.org/abs/2501.02316).
- G. Kopp, *The Shintani--Faddeev modular cocycle*,
  [arXiv:2411.06763](https://arxiv.org/abs/2411.06763).
- D. M. Appleby, S. T. Flammia, and G. S. Kopp,
  *A constructive approach to Zauner's conjecture via the Stark
  conjectures*, [arXiv:2501.03970](https://arxiv.org/abs/2501.03970).
