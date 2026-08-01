# P7-3B — fixed-ray discrepancy transfer and the difference-sampling gate

## Outcome and claim boundary

`PROVED`: at one fixed finite ray modulus \(\mathfrak f\), the complete
character sum in the exact discrepancy identity can be reindexed by the
unique primitive exact conductors \(\mathfrak d\mid\mathfrak f\), before the
source large sieve is used.  With

\[
u_{\mathfrak f}(\mathfrak a)=u(\mathfrak a)
\mathbf 1_{(\mathfrak a,\mathfrak f)=1},\qquad
u(\mathfrak a)=|c(\mathfrak a)|^2w(N\mathfrak a/N)^2,
\]

this preserves the frozen zero extension exactly.  Thorner's Theorem 2.1
therefore supplies a valid fixed-ray continuous \(L^2\) bound for the full
complete-character discrepancy family.  There is no divisor sum, completion
factor, or change of conductor convention in this transfer.

`PROVED`: the unresolved conversion is a local uncoloured
**difference-sampling multiplicity**, not an ordinary coloured energy.  For
\(\mathcal T\subset[0,T]\) and \(0<\Delta<1/2\), define

\[
\mathcal D_\Delta(\mathcal T)=\sup_{v\in\mathbb R}
\#\{(t,s)\in\mathcal T^2: |(t-s)-v|\leq\Delta\}.
\tag{D}
\]

The available L2 inputs bound \(\delta_2\) only after multiplication by
\(\mathcal D_\Delta(\mathcal T)\).  Per-character 1-separation yields
only \(\mathcal D_\Delta\leq|\mathcal T|P_{\mathfrak f}\), where
\(P_{\mathfrak f}\) is the number of eligible exact-primitive characters;
this is combinatorially sharp.  It can be a fixed power of the relevant
parameters.  Thus these inputs do not yield a Guth--Maynard-shaped selected
cubic bound under the frozen P7 hypotheses.

`PROVED`: a local uncoloured difference energy only gives
\(\mathcal D_\Delta^2\leq\mathcal E^{\rm diff}_{2\Delta}\).  Even for a
globally separated arithmetic progression, this costs \(|\mathcal T|^{1/2}\)
in the bound for \(\delta_2^2\), hence \(|\mathcal T|^{1/4}\) in a
perturbative cubic error.  The exact \(\mathcal D_\Delta\), or an equivalent
localized sampling statement, is the minimal statistic for the current
L2-to-discrete route.

`OBSERVED`: this closes the conductor-safe part of the previously open
fixed-ray L2 transfer.  The difference-sampling statistic and the common
averaged-block cubic estimate remain open.  No selected primitive cubic
estimate, Hecke large-value theorem, density theorem, detector, or
prime-ideal result is claimed.

This is research-stage source/algebra/replay work only. No hostile audit is
initiated.

## 1. Exact conductor-safe transfer

Fix \(\mathfrak f\), write

\[
G=\operatorname{Cl}(\mathfrak f),\quad X=\widehat G,\quad
H=|X|,\quad q=N\mathfrak f.
\]

Every \(\eta\in X\) has a unique primitive finite conductor
\(\mathfrak d_\eta\mid\mathfrak f\) and primitive ancestor
\(\eta^\star\bmod\mathfrak d_\eta\).  On ideals coprime to
\(\mathfrak f\), \(\eta=\eta^\star\).  On the remaining ideals both sides
below are zero because the coefficient has been restricted, not because a
character was silently inflated:

\[
F_\eta(v)=\sum_{\mathfrak a}u(\mathfrak a)\eta(\mathfrak a)
(N\mathfrak a)^{iv}
=\sum_{\mathfrak a}u_{\mathfrak f}(\mathfrak a)\eta^\star(\mathfrak a)
(N\mathfrak a)^{iv}.
\tag{1}
\]

The right side has one common ideal coefficient function, independent of
\(\mathfrak d_\eta,\eta^\star\), and \(v\). Reindexing the complete group by
its primitive ancestors and enlarging to Thorner's nonnegative source sum
gives, for \(B\geq2\),

\[
\sum_{\eta\in X}\int_{-B}^{B}|F_\eta(v)|^2\,dv
\ll_K(2N+q^2B^2)(\log(qB))^A\|u_{\mathfrak f}\|_2^2.
\tag{2}
\]

Here Theorem 2.1 is used with ideal cutoff \(2N\), conductor cutoff \(q\),
and its sole torsion-free parameter fixed to \(m=0\). Every
\(\eta^\star\) occurring in (1) is one term in that source sum. This is a
restriction/enlargement of a nonnegative sum, not a signed primitive-projector
argument. The sign \(iv\) is removed by \(v\mapsto-v\). Applying the same
theorem to \(u_{\mathfrak f}(\mathfrak a)\log N\mathfrak a\) adds
\(\log^2(2N)\).

This is deliberately narrow: it supplies exactly the fixed-modulus
complete-character L2 statement needed in the discrepancy identity. It does
not turn complete characters into selected primitive large values and makes
no varying-conductor claim.

## 2. Exact local sampling reduction

The selected-Gram result gives

\[
\delta_2^2=\frac1H\sum_{\substack{\eta\in X\\\eta\ne1}}
\sum_{t,s\in\mathcal T}|F_\eta(t-s)|^2.
\tag{3}
\]

For every \(C^1\) function \(F\), local Sobolev averaging gives

\[
|F(x)|^2\leq\Delta^{-1}\!\int_{x-\Delta}^{x+\Delta}|F(y)|^2dy+
2\Delta\!\int_{x-\Delta}^{x+\Delta}|F'(y)|^2dy.
\tag{4}
\]

Summing (4) over the difference multiset covers each \(y\) at most
\(\mathcal D_\Delta(\mathcal T)\) times. Take \(B=T+\Delta\). Equations
(2)--(4) prove

\[
\delta_2^2\ll_K\frac{\mathcal D_\Delta(\mathcal T)}H
\Gamma_{\rm Th}(N,q,B,\Delta)\|u_{\mathfrak f}\|_2^2,
\tag{5}
\]

\[
\Gamma_{\rm Th}=(\Delta^{-1}+2\Delta\log^2(2N))
(2N+q^2B^2)(\log(qB))^A.
\tag{6}
\]

This is the strongest conclusion available from the checked Thorner source
and deterministic sampling alone.

There is a completion-free elementary companion. Collapse only norms:

\[
F_\eta(v)=\sum_{N<n\leq2N}b_\eta(n)n^{iv},\qquad
b_\eta(n)=\sum_{N\mathfrak a=n}u_{\mathfrak f}(\mathfrak a)\eta(\mathfrak a).
\]

Expanding the integral and applying the harmonic-series Schur bound to
\((\log m-\log n)^{-1}\) gives

\[
\int_{-B}^{B}\Big|\sum_{N<n\leq2N}b(n)n^{iv}\Big|^2dv
\ll(B+N(1+\log(2N)))\sum_{N<n\leq2N}|b(n)|^2.
\tag{7}
\]

Complete character orthogonality and Cauchy in each norm fibre give

\[
\sum_{\eta\in X}\sum_n|b_\eta(n)|^2
\leq H\,\Delta_K(N)\|u_{\mathfrak f}\|_2^2,
\quad \Delta_K(N)=\max_{N<n\leq2N}a_{\mathbb Q(i)}(n)
\leq\max_{N<n\leq2N}\tau(n).
\tag{8}
\]

Thus

\[
\delta_2^2\ll\mathcal D_\Delta(\mathcal T)
\Gamma_{\rm MV}(N,B,\Delta)\|u_{\mathfrak f}\|_2^2,
\tag{9}
\]

\[
\Gamma_{\rm MV}=(\Delta^{-1}+2\Delta\log^2(2N))
(B+N(1+\log(2N)))\Delta_K(N).
\tag{10}
\]

The factor \(H\) in (8) cancels the \(H^{-1}\) in (3). If \(N\leq T^C\)
for fixed \(C\), then \(\Delta_K(N)=T^{o(1)}\) by the pinned P7-1
normalization. Formula (9) is often stronger than (5), but it is still a
raw L2/difference-sampling bound.

## 3. Separation, difference energy, and sharpness

Let \(P_{\mathfrak f}\) be the number of primitive exact-conductor characters
eligible in the selected sample and put \(m=|\mathcal T|\). If every fixed
character fibre is 1-separated, then every interval of length
\(2\Delta<1\) contains at most \(P_{\mathfrak f}\) distinct selected times.
For fixed \(t\), the admissible \(s\)'s in (D) lie in one such interval.
Hence

\[
\mathcal D_\Delta(\mathcal T)\leq mP_{\mathfrak f}\leq mH.
\tag{11}
\]

`PROVED`: (11) is sharp from fibrewise separation alone. Take \(P\) colours,
\(J\) blocks, and times

\[
t_{j,c}=3j+\frac{c}{8P}\qquad(0\leq j<J,\ 0\leq c<P).
\tag{12}
\]

Assign \(t_{j,c}\) to colour \(c\). Each fibre is 3-separated, but at
\(\Delta=1/4\), all \(JP^2=mP\) within-block differences lie in the same
local window. No colour-independent or subpower bound for
\(\mathcal D_\Delta\) follows from the frozen separation convention.

The relevant uncoloured local difference energy is

\[
\mathcal E^{\rm diff}_{2\Delta}(\mathcal T)=
\#\{(t_1,t_2,t_3,t_4)\in\mathcal T^4:
|(t_1-t_2)-(t_3-t_4)|\leq2\Delta\}.
\tag{13}
\]

Always \(\mathcal D_\Delta^2\leq\mathcal E^{\rm diff}_{2\Delta}\). But
energy is not a sharp substitute. For the globally 1-separated progression
\(\{0,\ldots,m-1\}\), with \(\Delta=1/4\),

\[
\mathcal D_\Delta=m,\qquad
\mathcal E^{\rm diff}_{2\Delta}=
\sum_{h=-(m-1)}^{m-1}(m-|h|)^2=\frac{2m^3+m}{3}.
\tag{14}
\]

Replacing \(\mathcal D_\Delta\) by
\((\mathcal E^{\rm diff}_{2\Delta})^{1/2}\) loses \(m^{1/2}\) in (5) or
(9), even here. The preceding P7 coloured energy has a different character
equation and does not bound (13).

## 4. Exact cubic budget and gate

Put \(a_3=\|A_0\|_{S_3}\). The class-average comparison is

\[
\mathfrak G(K_W)\leq H^3\bigl(\mathfrak G(A_0)+
3\delta_2(a_3+\delta_2)^2\bigr).
\tag{15}
\]

For a desired discrepancy budget \(\mathcal B>0\), define
\(z_{\mathcal B}(a_3,H)>0\) by

\[
3H^3z_{\mathcal B}(a_3+z_{\mathcal B})^2=\mathcal B.
\tag{16}
\]

Then the Thorner route meets that budget if, up to its fixed source constant,

\[
\mathcal D_\Delta(\mathcal T)\ll_K
\frac{H z_{\mathcal B}^2}
{\Gamma_{\rm Th}(N,q,B,\Delta)\|u_{\mathfrak f}\|_2^2};
\tag{17}
\]

the norm-collapsed route has the same condition without the numerator \(H\)
and with \(\Gamma_{\rm MV}\). This is the precise
**difference-sampling gate** for the existing class-average reduction. A
source-shaped estimate for \(\mathfrak G(A_0)\) remains separately needed.

If \(\mathcal D_\Delta=T^\kappa\) relative to a subpower benchmark, then
\(\delta_2^2\) loses \(T^\kappa\) and \(\delta_2\) loses
\(T^{\kappa/2}\). In the perturbative regime \(\delta_2\leq a_3\), the
cubic error in (15) has the same \(T^{\kappa/2}\) cost; if
\(\delta_2\geq a_3\), its cubic part has \(T^{3\kappa/2}\) cost. Under
only fibrewise separation, (11) permits
\(\kappa=\log_T(mP_{\mathfrak f})\). This prevents the available L2
technology from recovering the pinned
\(T^2R^{3/2}+TNR^{1/2}E^{1/2}\) source shape.

## 5. Scoped conclusion

`PROVED`: the fixed-modulus conductor transfer is available, but Thorner L2,
the norm-collapsed L2 companion, and per-character separation reach only (5)
or (9), with the sharp local statistic \(\mathcal D_\Delta\). It is not
controlled by the frozen P7 detector geometry and cannot be replaced sharply
by ordinary difference energy or coloured energy.

`CONJECTURED`: a successful continuation needs either a source-scale bound
for \(\mathcal D_\Delta\) at the budget (17), or a localized
higher-moment/ray-class distribution theorem that bypasses L2 sampling. It
must then be combined with a source-shaped averaged-block cubic estimate.
This reduction does not rule out extra detector arithmetic or a new Poisson
method.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p7_fixed_ray_discrepancy_transfer_v1.py --check
python3 -m unittest tests/test_p7_fixed_ray_discrepancy_transfer_v1.py -v
```

The sealed replay validates source/predecessor pins and performs exact
Fraction-only checks of the zero-extension logic, sharp fibrewise difference
construction, progression energy calculation, and cubic-budget bookkeeping.
