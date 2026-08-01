# P7-3 — selected-Gram cubic excess and cross-conductor pinching

## Outcome and claim boundary

`PROVED`: every positive-semidefinite selected Gram matrix \(K\) has the
exact centred cubic identity


\[
 \mathfrak G(K):=\operatorname{tr}(K^3)-\frac{\operatorname{tr}(K)^3}{R^2}
 =\sum_{j=1}^R(\lambda_j-\mu)^2(\lambda_j+2\mu),
 \quad \mu=\frac{\operatorname{tr}(K)}R.
\]

Consequently, with

\[
 \mathcal V_2(K)=\operatorname{tr}(K^2)-\frac{\operatorname{tr}(K)^2}{R},
 \qquad \Lambda(K)=\|K\|_{\mathrm{op}},
\]

one has

\[
 0\leq\mathfrak G(K)\leq
 (\Lambda(K)+2\mu)\mathcal V_2(K)
 \leq3\Lambda(K)\mathcal V_2(K).
\tag{1}
\]

`PROVED`: if \(K\) is partitioned by exact conductors and

\[
 \mathcal X_\times(K)=\operatorname{tr}(K^3)-
 \sum_{\mathfrak f}\operatorname{tr}(K_{\mathfrak f}^3),
\]

then

\[
 0\leq\mathcal X_\times(K)\leq\mathfrak G(K).
\tag{2}
\]

Thus the aggregate cross-conductor term is not signed.  Its *individual
block-expansion summands* may be signed, which is the valid limited content
of the predecessor's warning.  This document is a versioned correction of
that aggregate-sign wording, not an edit of the predecessor.

`PROVED`: at one fixed ray modulus, averaging the exact ray-class blocks
before selection gives a completion-free selected-side decomposition.  Its
error is controlled by an explicit ray-class Schatten discrepancy; the
selected trace, and hence its diagonal subtraction, are preserved exactly.

`PROVED`: Thorner's P7-2 L2 large sieve, plus a deterministic sampling lemma,
gives a completion-free bound for (1).  Its scale is raw-L2 scale, not the
Guth--Maynard refined cubic scale.

`OBSERVED`: this advances P7-3 by removing a separate signed
cross-conductor obstruction and identifying two exact missing statistics:
the global centred Gram variance \(\mathcal V_2\), and in the fixed-ray
route the ray-class discrepancy below.  It does not close P7-3.  No
selected primitive cubic estimate of source shape, Hecke density estimate,
detector, or prime-ideal result is claimed.

The selected P7 family, exact-conductor labels, trivial infinity type, and
zero extension remain those frozen in P7-0--P7-2:

\[
 \chi(\mathfrak a)=0\quad\text{when }(\mathfrak a,\mathfrak f_\chi)\ne1.
\]

No primitive Möbius projector is replaced by a positive projector, and no
character is inflated to a common modulus.

## 1. The exact PSD excess

Let \(K\succeq0\) be an \(R\times R\) Hermitian matrix, with eigenvalues
\(\lambda_1,\ldots,\lambda_R\).  Expanding gives

\[
\begin{aligned}
 \sum_j(\lambda_j-\mu)^2(\lambda_j+2\mu)
 &=\sum_j\lambda_j^3-3\mu^2\sum_j\lambda_j+2R\mu^3\\
 &=\operatorname{tr}(K^3)-R\mu^3
 =\mathfrak G(K).
\end{aligned}
\]

This proves nonnegativity.  Since
\(\lambda_j+2\mu\leq\Lambda(K)+2\mu\leq3\Lambda(K)\), it also proves
(1).  The subtraction is exactly the selected-side diagonal cancellation:
it is not an upper bound obtained after completing rows.

The constant \(3\) is sharp in this general PSD inequality.  For

\[
 K_n=\operatorname{diag}(n+1,n-1),\qquad n\geq1,
\]

one has

\[
 \mu=n,\quad \mathcal V_2(K_n)=2,\quad
 \mathfrak G(K_n)=6n,
 \quad 3\Lambda(K_n)\mathcal V_2(K_n)=6(n+1).
\]

The ratio tends to one.  This is an algebraic sharpness statement only.

For the P7 ideal design matrix \(M\), indexed by selected labelled points
\((\mathfrak f,\chi,t)\) and integral ideals, set \(K=MM^*\).  Then \(K\)
is PSD regardless of the character-dependent norm collapse.  Formula (1)
therefore applies before forgetting conductor labels or passing to a common
ray-class group.

## 2. Exact-conductor pinching

Partition the rows by their exact finite conductor,

\[
 W=\bigsqcup_{\mathfrak f}W_{\mathfrak f},
 \qquad R_{\mathfrak f}=|W_{\mathfrak f}|>0,
\]

and write \(K_{\mathfrak f}\) for the corresponding principal block.  The
block pinching map is

\[
 \mathcal E(K)=\bigoplus_{\mathfrak f}K_{\mathfrak f}.
\]

It is an average of block-phase unitary conjugates of \(K\).  The Schatten
3 norm is a norm, so

\[
 \|\mathcal E(K)\|_{S_3}\leq\|K\|_{S_3}.
\]

Cubing proves the lower bound in (2).  For the upper bound, put

\[
 \tau_{\mathfrak f}=\operatorname{tr}(K_{\mathfrak f}),
 \qquad \mu_{\mathfrak f}=\tau_{\mathfrak f}/R_{\mathfrak f},
 \qquad p_{\mathfrak f}=R_{\mathfrak f}/R.
\]

The exact decomposition is

\[
\begin{aligned}
 \mathcal X_\times(K)
 &=\mathfrak G(K)-\sum_{\mathfrak f}\mathfrak G(K_{\mathfrak f})\\
 &\quad+R\left[\left(\sum_{\mathfrak f}p_{\mathfrak f}
 \mu_{\mathfrak f}\right)^3-
 \sum_{\mathfrak f}p_{\mathfrak f}\mu_{\mathfrak f}^3\right].
\end{aligned}
\]

The bracket is nonpositive by Jensen, and each block excess is nonnegative
by Section 1.  This proves the upper bound in (2).  It is sharp: with one
row in each block and \(K\) the all-ones matrix, one has
\(\mathcal X_\times(K)=\mathfrak G(K)=R^3-R\).

Accordingly, a global bound for the selected Gram excess controls the
aggregate cross-conductor contribution directly.  No common ray group is
needed for this step.

## 3. Fixed-ray class-average compression without completion

Fix one modulus \(\mathfrak f\), let \(G=\operatorname{Cl}(\mathfrak f)\)
have order \(H\), and let \(X=\widehat G\).  On a finite grid
\(\mathcal T=\pi_tW\), write the exact complete-group Fourier form from the
predecessor as

\[
 U(MM^*)U^*=H\bigoplus_{g\in G}C_g,
\]

where each \(C_g\succeq0\) is the time Gram formed from ideals in ray class
\(g\).  All ideals in these blocks are coprime to \(\mathfrak f\), so the
frozen zero extension has already been enforced.

For \(A_t=\{\chi:(\chi,t)\in W\}\), let \(P_W\) be the exact row selector
in \(X\times\mathcal T\).  Define

\[
 A=P_WU^*\left(\bigoplus_gC_g\right)UP_W,
 \qquad K_W=H A,
\]

and average only the *ideal class blocks*, not the selected characters:

\[
 \overline C=H^{-1}\sum_gC_g,
 \qquad \Delta_g=C_g-\overline C,
 \qquad
 A_0=P_W(I_X\otimes\overline C)P_W.
\]

`PROVED`: \(\operatorname{tr}(A)=\operatorname{tr}(A_0)\).  Indeed, in the
ray-class basis the selector has diagonal entry

\[
 (UP_WU^*)_{(g,t),(g,t)}=|A_t|/H,
\]

independent of \(g\), while \(\sum_g\Delta_g=0\).  This is the exact reason
the selected diagonal subtraction survives the averaging.

Moreover, in the character basis,

\[
 A_0=\bigoplus_{\chi\in X}
 \overline C\big|_{\mathcal T_\chi},
 \qquad \mathcal T_\chi=\{t:(\chi,t)\in W\}.
\tag{3}
\]

There is no completion factor \(\kappa_{\mathfrak f}(W)\) in (3).

Let

\[
 \delta_3=\left(\sum_{g\in G}\|\Delta_g\|_{S_3}^3\right)^{1/3},
 \qquad a_3=\|A_0\|_{S_3}.
\]

Compression by \(P_W\) is contractive for Schatten norms, hence

\[
 \|A-A_0\|_{S_3}\leq\delta_3.
\]

The noncommutative telescoping identity

\[
 A^3-A_0^3=(A-A_0)A^2+A_0(A-A_0)A+A_0^2(A-A_0)
\]

and Schatten Hölder give

\[
 \left|\operatorname{tr}(A^3)-\operatorname{tr}(A_0^3)\right|
 \leq3\delta_3(a_3+\delta_3)^2.
\tag{4}
\]

As the traces agree, (4) is also a selected-excess bound:

\[
 \mathfrak G(K_W)
 \leq H^3\left(\mathfrak G(A_0)+
 3\delta_3(a_3+\delta_3)^2\right).
\tag{5}
\]

In the P7 Gram, the diagonal of \(\overline C\) is constant.  Consequently

\[
 \mathfrak G(A_0)=
 \sum_{\chi\in X}\mathfrak G
 \left(\overline C\big|_{\mathcal T_\chi}\right).
\tag{6}
\]

Equations (5)--(6) give the desired selected-side compression: the only new
analytic input is a ray-class block-discrepancy bound and a common averaged
block estimate.  A convenient, weaker discrepancy is

\[
\delta_3\leq
\delta_2:=\left(\sum_g\|C_g-\overline C\|_{S_2}^2\right)^{1/2}.
\]

There is also an exact complete-character expansion of the checkable
quantity.  With

\[
 F_\eta(t,s)=
 \sum_{(\mathfrak a,\mathfrak f)=1}
 u(\mathfrak a)\eta(\mathfrak a)(N\mathfrak a)^{i(t-s)}
 =\sum_{g\in G}\eta(g)C_g(t,s),
\]

finite Fourier Parseval gives

\[
 \delta_2^2=
 \frac1H\sum_{\substack{\eta\in X\\\eta\ne1}}
 \sum_{t,s\in\mathcal T}|F_\eta(t,s)|^2.
\tag{F}
\]

`PROVED`: (F) is an identity for the complete ray-class group.  It keeps the
zero extension through the condition \((\mathfrak a,\mathfrak f)=1\).  The
finite replay verifies it as \(14=28/2\) in the two-class model.

`OBSERVED`: current fibre separation and local height multiplicity do not
control the difference multiset \(\mathcal T-\mathcal T\) in (F).  A sample
with one point in every character fibre at heights \(1,\ldots,R\) has local
height multiplicity one, yet its uncoloured difference energy
\(\sum_h\#\{(t,s):t-s=h\}^2\) has cubic size.  Coloured additive energy has
a different colour equation and does not, under the frozen hypotheses,
bound the complete-character sum in (F).

`OBSERVED`: Thorner's P7-2 L2 theorem controls a primitive common-coefficient
polynomial in one height variable.  Turning it into a bound for (F) would
add two unproved inputs: a conductor-safe transfer from complete
\(\eta\bmod\mathfrak f\) to primitive characters preserving zero extension,
and a difference-sampling estimate for \(\mathcal T-\mathcal T\).  Neither
is supplied by the current detector architecture.  No estimate for
\(\delta_3\) or \(\delta_2\) is therefore asserted here.

## 4. What the existing L2 large sieve actually supplies

Let the selected points lie in \(0\leq t\leq T\), with every fixed-
character fibre \(W_\chi\) 1-separated.  For finitely supported ideal
coefficients \(d(\mathfrak a)\), the elementary unit-interval Sobolev bound
and disjoint intervals within each character fibre give

\[
\begin{aligned}
 \sum_{(\mathfrak f,\chi,t)\in W}
 \left|\sum_{N<N\mathfrak a\leq2N}
 d(\mathfrak a)\chi(\mathfrak a)(N\mathfrak a)^{-it}\right|^2
 \ll\sum_{\mathfrak f,\chi}\int_{-T-1}^{T+1}
 (|F_\chi(u)|^2+|F'_\chi(u)|^2)\,du.
\end{aligned}
\]

The derivative multiplies coefficients by at most \(\log(2N)\).  The P7-2
checked specialization of Thorner's Theorem 2.1, now with cutoff \(2N\) and
height \(T+1\), therefore gives

\[
 \sum_{x\in W}|(Md)_x|^2\ll_K \mathcal L_{N,Q,T}\|d\|_2^2,
\tag{7}
\]

where

\[
 \mathcal L_{N,Q,T}=
 (1+\log^2(2N))
 (2N+4Q^2(T+1)^2)
 (\log(2Q(T+1)))^A.
\]

Here \(M\) is the coefficient-free P7 design matrix with entries

\[
 M_{(\mathfrak f,\chi,t),\mathfrak a}=
 w(N\mathfrak a/N)\chi(\mathfrak a)(N\mathfrak a)^{it};
\]

the bounded fixed weight is harmless in (7).  This use retains primitive
labels and zero extension exactly.  It needs no separation between different
characters at the same height.

For \(K=MM^*\), (7) implies

\[
 \Lambda(K)\ll_K\mathcal L_{N,Q,T},
 \qquad
 \operatorname{tr}(K^2)\ll_K
 \mathcal L_{N,Q,T}\operatorname{tr}(K).
\]

Substitution in (1) gives the completion-free raw-L2 consequence

\[
 \mathfrak G(K)
 \ll_K3\mathcal L_{N,Q,T}
 \left(\mathcal L_{N,Q,T}\operatorname{tr}(K)-
 \frac{\operatorname{tr}(K)^2}{R}\right)
 \ll_K3\mathcal L_{N,Q,T}^2\operatorname{tr}(K).
\tag{8}
\]

`OBSERVED`: in the natural diagonal scale
\(\operatorname{tr}(K)\asymp RN\), (8) is

\[
 T^{o(1)}RN(N+Q^2T^2)^2,
\]

under the already frozen \(N\leq T^C\) regime.  It has neither the
Guth--Maynard \(T^2R^{3/2}\) term nor the coloured-energy term.  Thus the
existing L2 source supplies a rigorous completion-free fallback but not a
source-shaped P7-3 cubic estimate.

## 5. Sharp algebraic containment of energy/collision-only routes

`PROVED`: coloured energy and local height multiplicity alone do not control
the selected Gram excess in the present algebraic class.  In the exact
two-colour, two-time model used in the replay, take

\[
 C_0=\begin{pmatrix}5&2\\2&2\end{pmatrix},\qquad
 C_1=\begin{pmatrix}1&0\\0&4\end{pmatrix},
\qquad W=\{(\chi_0,0),(\chi_1,1)\}.
\]

Both class blocks are PSD.  The selected heights have multiplicity one and
their coloured additive energy is the minimum (2R^2-R=6).  Yet the exact
selected Gram and its class-average comparison are

\[
 K_W=\begin{pmatrix}6&2\\2&6\end{pmatrix},
 \qquad K_{W,0}=\begin{pmatrix}6&0\\0&6\end{pmatrix},
\qquad
 \mathfrak G(K_W)=144,\quad\mathfrak G(K_{W,0})=0.
\]

The difference is carried by the nonzero ray-class discrepancy, not by a
time collision or by coloured additive energy.  Separately, the rank-one
all-ones Gram saturates the raw-L2 inequalities
\(\operatorname{tr}(K^2)=\Lambda(K)\operatorname{tr}(K)\) while retaining
\(\mathfrak G(K)=R^3-R\).

These are finite algebraic countermodels, not ideal-sum detector examples.
They establish only the following scoped no-go: no argument using *only*
PSD positivity, a raw L2 operator bound, coloured additive energy, and local
height collision data can force the desired selected-side cubic saving.

For the PSD route, the weakest additional scalar datum exposed by the exact
identity is the centred variance \(\mathcal V_2(K)\), together with an
operator bound.  For the fixed-ray class-average route, the corresponding
additional datum is \(\delta_3\) (or the stronger-to-check \(\delta_2\)).
This is a route-specific minimality statement, not a theorem excluding other
character-aware methods.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p7_selected_gram_excess_v1.py --check
python3 -m unittest tests/test_p7_selected_gram_excess_v1.py -v
```

The sealed artifact records the source and predecessor hashes, exact
Fraction-only finite checks, and the 60-second / 256-MiB replay contract.
