# SIC--Stark research cycle 15: the determinantal target

Date: 2026-07-27

## Outcome

Cycle 15 replaces the quadratic ghost equation by an equivalent
rank-one system.  This is an exact reduction, not a proof of TCC.

Let \(A=\mathcal Z_\sigma(F)\) be the raw cycle-12 Zak matrix and use
the cycle-13 scale \(C=sA\).  The matrix whose rank matters is not
\(A\) itself but the scalar shift

\[
K=C+\kappa I,\qquad
\kappa=\frac d2\left(\sqrt{d+1}-\sqrt{d-3}\right).
\]

Up to the harmless conjugations already recorded in cycle 13,

\[
\boxed{K=d\sqrt{d+1}\,\widetilde\Pi.}
\]

Since \(\operatorname{Tr}\widetilde\Pi=1\),

\[
\boxed{
\mathrm{TCC}
\iff
\widetilde\Pi^2=\widetilde\Pi
\iff
\operatorname{rank}K=1
\iff
\bigwedge^2K=0.
}
\]

Thus TCC is equivalent to the vanishing of all \(2\times2\) minors of
a single explicitly shifted RM Zak matrix.  This formulation is
insensitive to Jordan blocks and exposes the missing analytic theorem
as a bilinear partial-Fourier exchange identity.

## 1. Why rank one is equivalent to idempotency

If \(\widetilde\Pi^2=\widetilde\Pi\), then its rank equals its trace,
which is one.  Conversely, if
\(\operatorname{rank}\widetilde\Pi=1\), write

\[
\widetilde\Pi=uv^{\mathsf T}.
\]

The automatic trace identity gives

\[
v^{\mathsf T}u=\operatorname{Tr}\widetilde\Pi=1,
\]

so

\[
\widetilde\Pi^2
=u(v^{\mathsf T}u)v^{\mathsf T}
=\widetilde\Pi.
\]

This argument needs neither Hermiticity nor a spectral
diagonalization.

## 2. Explicit partial-Fourier entries

Use the standard Weyl convention

\[
D_{a,b}=\tau_d^{ab}X^aZ^b.
\]

If \(\mu_{a,b}\) denotes the ghost Weyl coefficient, then

\[
d\,\widetilde\Pi_{j,k}
=
\sum_{b\bmod d}
\mu_{j-k,b}\,
\tau_d^{\,b(j+k)}.
\]

Define the sheared partial Fourier transform

\[
W(a,k)
=
\sum_{b\bmod d}
\mu_{a,b}\,
\tau_d^{\,b(a+2k)}.
\]

Then

\[
d\,\widetilde\Pi_{j,k}=W(j-k,k).
\]

For rows \(j,\ell\) and columns \(k,m\), the minor equation is

\[
\boxed{
W(j-k,k)W(\ell-m,m)
-
W(j-m,m)W(\ell-k,k)=0.
}
\]

Each product contains \(d^2\) explicit bilinear RM terms.  There are

\[
\binom d2^2
\]

such minors in the redundant global system.

For adjacent rows and columns the equation takes the
Hirota/Casoratian form

\[
W(a,k)W(a,k+1)
=
W(a-1,k+1)W(a+1,k).
\]

Cycle 10 showed that the analogous identity fails before the partial
Fourier transform.  The present identity is different: it is exactly
equivalent to rank one after the shear and must therefore detect the
cycle-9 deformation.

## 3. Local pivot charts

On a chart where \(K_{h,h}\ne0\), rank one is equivalent to the
\((d-1)^2\) fan minors

\[
K_{i,j}K_{h,h}-K_{i,h}K_{h,j}=0,
\qquad i,j\ne h.
\]

The trace of \(K\) is nonzero, so at least one diagonal chart exists,
but the currently proved identities do not select a universal
index \(h\).  A global proof must either:

- prove one specified diagonal entry never vanishes;
- work on the union of the \(d\) diagonal charts; or
- prove the coordinate-free equation \(\bigwedge^2K=0\).

Adjacent minors alone are unsafe when entries may vanish: local
zero patterns can satisfy a subset of adjacent equations without
having rank one.

## 4. Zauner blocks

In a Zauner eigenbasis write

\[
K=K_0\oplus K_1\oplus K_2,
\qquad
\dim K_a=n_a.
\]

The exterior square decomposes as

\[
\bigwedge^2K
=
\bigoplus_a\bigwedge^2K_a
\oplus
\bigoplus_{a<b}(K_a\otimes K_b).
\]

Therefore rank one requires:

1. each block \(K_a\) has rank at most one;
2. at most one block is nonzero.

On a chart with a nonzero pivot in block \(a\), a local system consists
of the \((n_a-1)^2\) fan minors within that block plus all entries of
the other two blocks.  Its equation count is

\[
\sum_b n_b^2-2n_a+1.
\]

The occupied Zauner eigencharacter is not known a priori, so all three
charts are needed.  Computational-basis minors are mixed by
\(\bigwedge^2U_{\rm Z}\); they are not simply permuted in
characteristic orbits.  Consequently the scalar orbit count from
cycles 3 and 13 cannot be reused as a minor-orbit reduction.

## 5. Positive-metric sufficient certificate

The automatic identities

\[
\operatorname{Tr}\widetilde\Pi
=\operatorname{Tr}\widetilde\Pi^2=1
\]

would prove idempotency if one could establish a positive metric
\(\eta>0\) satisfying

\[
\eta\widetilde\Pi
=\widetilde\Pi^\dagger\eta,
\qquad
\eta\widetilde\Pi\succeq0.
\]

Indeed,

\[
P_\eta
=\eta^{1/2}\widetilde\Pi\eta^{-1/2}
\]

would be positive semidefinite and similar to
\(\widetilde\Pi\).  Its nonnegative eigenvalues would have sum and
sum of squares both equal to one, forcing the spectrum
\((1,0,\ldots,0)\).  Hermiticity then gives
\(P_\eta^2=P_\eta\), hence
\(\widetilde\Pi^2=\widetilde\Pi\).

This certificate is only useful if \(\eta\) comes from independent RM
positivity or modular data.  Solving for an arbitrary \(\eta\) after
knowing the spectrum would be circular.

The authors' double-sine implementation was used to reconstruct the
actual dimension-four ghost numerically.  It gave

\[
\|\widetilde\Pi^2-\widetilde\Pi\|_{\max}
<8\times10^{-17},
\qquad
\max|\text{\(2\times2\) minor}|
<4\times10^{-17},
\]

which independently checks the determinantal normalization.

For an already idempotent \(G\), the canonical metric

\[
\eta_0
=G^\dagger G+(I-G)^\dagger(I-G)
\]

is positive and intertwines \(G\) with \(G^\dagger\).  This is exact
but circular: its construction already uses the desired idempotent.
On the numerical \(d=4\) ghost, the linear intertwining equation has
no nonzero diagonal solution and no nonzero Hermitian circulant
solution.

A parity-commuting positive metric is also ruled out structurally.
For a rank-one ghost

\[
G=\frac{\psi\phi^\dagger}{\phi^\dagger\psi},
\qquad \phi=P\psi,
\]

pseudo-Hermiticity requires \(\eta\psi=k\phi\).  If
\([\eta,P]=0\), then \(\eta\phi=k\psi\), so the directions
\(\psi+\phi\) and \(\psi-\phi\) acquire opposite signs.  Such a
metric is indefinite or singular.  Any useful metric must therefore
use finer RM or correctly normalized Zauner structure, not merely
parity, diagonality, or circulancy.

## 6. Why the standard determinant identities do not close it

A genuine proof through Fay, Plücker, Casoratian, or quantum
dilogarithm identities must produce the shifted matrix \(K\), not the
raw Zak matrix \(A\), and must pass four tests:

1. retain the exceptional zero-characteristic scalar \(\kappa I\);
2. prove the bilinear identity for the signed RM values, not only
   their absolute squares;
3. remain valid for both parities and for \(3\mid d\);
4. fail on the exact reciprocal/Zauner countermodels from cycles 8,
   9, and 14.

The classical Fay identity rewrites a difference of two products as a
third theta product.  That third product is generically nonzero; it
vanishes only on a theta divisor or at a collision.  The Frobenius
elliptic Cauchy determinant makes this explicit: its \(2\times2\)
minor is a quotient containing nonzero row and column Vandermonde
factors.  Hyperbolic and quantum-dilogarithmic Cauchy determinants
have the same behavior.  The quantum dilogarithms factor out by rows
and columns, leaving a generically nonzero Cauchy minor.

A Casoratian identity could propagate minor vanishing if every pair of
Zak columns solved the same second-order scalar difference equation.
It cannot supply the first vanishing anchor, and the phase \(2bj\)
makes the presently available characteristic recurrences
column-dependent.

Ordinary Plücker identities also do not help: they are three-term
relations among minors valid on the whole rank-two Grassmannian.  The
rank-one locus needed here requires every minor itself to vanish.

There is a decisive algebraic sanity check.  For fixed \(a\), the map

\[
\{\mu_{a,b}\}_{b\bmod d}
\longmapsto
\{W(a,k)\}_{k\bmod d}
\]

is an invertible discrete Fourier transform.  It is independent for
each \(a\).  Hence the Weyl/Zak change of coordinates alone allows an
arbitrary \(d\times d\) matrix and imposes no rank constraint.
Whatever proves rank one must be a new RM-specific identity surviving
the finite root filter.

The clean missing theorem would be either the direct factorization

\[
W(j-k,k)=R_jC_k
\]

or a root-filtered Fay identity whose normally nonzero third product
vanishes identically at the signed Stark characteristics.  No
published identity located in this cycle provides that vanishing.
Treating \(A\) rather than \(K\) would also prove the wrong rank
statement.

## 7. Claim ledger

Proved in this cycle:

- the exact shifted-Zak matrix proportional to the ghost operator;
- equivalence of TCC, ghost idempotency, rank one, and vanishing
  \(2\times2\) minors;
- the explicit sheared partial-Fourier formula for every minor;
- the local fan-minor chart reduction;
- the correct exterior-square decomposition in Zauner blocks;
- a sufficient positive-metric criterion.

Still open:

- a Fay or quantum-dilogarithm identity forcing the minors;
- a non-circular positive metric from RM data;
- TCC itself.

## Sources

- N. Matthes, *An algebraic characterization of the Kronecker
  function*, Proposition 2.3,
  [arXiv:1806.04948](https://arxiv.org/abs/1806.04948).
- A. Prokofev and A. Zabrodin, *Elliptic Cauchy matrices*,
  equation (2.1),
  [arXiv:2305.02837](https://arxiv.org/abs/2305.02837).
- R. Kashaev and M. Mariño, *Operators from mirror curves and the
  quantum dilogarithm*,
  [arXiv:1501.01014](https://arxiv.org/abs/1501.01014).
- M. Mariño and S. Zakany, *Matrix models from operators and topological
  strings*, equation (2.24),
  [arXiv:1502.02958](https://arxiv.org/abs/1502.02958).
- A. Levin, M. Olshanetsky, and A. Zotov, *Quantum Baxter--Belavin
  R-matrices and multidimensional Lax pairs*, equation (r101),
  [arXiv:1501.07351](https://arxiv.org/abs/1501.07351).
- S. Flammia et al., *Zauner.jl* numerical implementation,
  [GitHub repository](https://github.com/sflammia/Zauner.jl).
