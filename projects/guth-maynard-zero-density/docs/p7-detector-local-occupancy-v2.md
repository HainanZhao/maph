# P7-3C — detector-side local occupancy and the uncoloured difference gate (corrected companion v2)

## Status and claim boundary

**PROVED:** This companion restates the mathematical result sealed in
p7-detector-local-occupancy-v1 with corrected TeX rendering. The immutable v1
builder and artifact remain valid. The v2 correction also repairs two
case-sensitive regression-test assertions; it changes no mathematical claim.

**PROVED:** An exact primitive P7 Hecke character over \(\mathbb Q(i)\) has
only logarithmically many zeros in a unit height interval. This fact cannot
remove the cross-character loss in the uncoloured time projection: once every
fixed-character fibre is \(1\)-separated, it already has at most one selected
time in each interval of radius \(<1/2\).

**PROVED:** If \(\mathcal T=\pi_tW\), \(m=|\mathcal T|\), and

\[
\mathcal M_\Delta(\mathcal T)
=\sup_{u\in\mathbb R}\#\bigl(\mathcal T\cap[u-\Delta,u+\Delta]\bigr),
\]

then

\[
\mathcal D_\Delta(\mathcal T)
\leq m\,\mathcal M_\Delta(\mathcal T),
\qquad
\mathcal D_\Delta(\mathcal T)
=\sup_v\#\{(t,s)\in\mathcal T^2:|(t-s)-v|\leq\Delta\}.
\tag{1}
\]

The factor \(m\mathcal M_\Delta\) is sharp under the stated detector
geometry. Therefore the P7 cubic gate remains open: neither individual local
zero counts nor primitive-family cardinality supplies an unconditional
source-scale \(\mathcal D_\Delta\) bound.

**PROVED, conditional on a precise detector premise:** A joint
character--height large-sieve bound controls \(\mathcal M_\Delta\) if one
common ideal polynomial has a uniform large value at every detector row. No
such P7 detector is source-checked yet. Even a successful difference bound
would leave the separate averaged-block \(A_0\) cubic input open.

No P7 detector, large-value theorem, zero-density theorem, or prime-ideal
interval theorem is claimed here. This is research-stage source/algebra/replay
work only; no hostile audit is initiated.

## 1. Exact conductor and zero extension

Let

\[
W\subset\{(\mathfrak f,\chi,t):
Q<N\mathfrak f\leq2Q,\ 
\chi\text{ primitive of exact finite conductor }\mathfrak f,\
0\leq t\leq T\}.
\tag{2}
\]

Every row retains

\[
\chi(\mathfrak a)=0\qquad\text{when }(\mathfrak a,\mathfrak f)\ne1.
\tag{3}
\]

The local zero count below applies to \(L(s,\chi)\) at this exact primitive
conductor. No character is completed, inflated, or reinterpreted at another
modulus.

The diagonal pairs \(t=s\) give the unavoidable floor

\[
\mathcal D_\Delta(\mathcal T)\geq m.
\tag{4}
\]

Consequently an L2-to-discrete target
\(\mathcal D_{\rm target}<m\) cannot be reached by any detector occupancy
input.

## 2. Source-checked unit-window zero count

The pinned Thorner--Zaman source proves that, for \(s=\sigma+iu\),
\(\sigma>1\), and \(0<r\leq1\),

\[
N_\chi(r;s)\leq
\left\{
4\log D_K+2\log N\mathfrak f_\chi
+2n_K\log(|u|+3)+2n_K+4+4\delta(\chi)
\right\}r+4+4\delta(\chi).
\tag{5}
\]

The proof uses the zero multiset in its explicit formula; hence (5) is valid
for a multiplicity-preserving detector and, a fortiori, for distinct zero
ordinates.

For \(K=\mathbb Q(i)\), use the circle centered at \(21/20+iu\) with radius
\(3/4\). Every zero \(\rho=\beta+i\gamma\) satisfying
\(\beta\geq1/2\) and \(|\gamma-u|\leq1/2\) lies inside, since

\[
\left(\frac{21}{20}-\beta\right)^2+(\gamma-u)^2
\leq
\left(\frac{11}{20}\right)^2+\left(\frac12\right)^2
=\frac{221}{400}
<\frac{225}{400}
=\left(\frac34\right)^2.
\tag{6}
\]

For \(\beta<1/2\), the functional equation
\(\xi(s,\chi)=w(\chi)\xi(1-s,\overline\chi)\) maps the zero to
\(1-\beta-i\gamma\) for \(\overline\chi\), in the unit window centered at
\(-u\). Applying (5) to the two halves, with \(D_K=4\), \(n_K=2\), and
\(\delta(\chi)\leq1\), proves

\[
Z_\chi(u):=
\#\{\rho:0<\Re\rho<1,\ |\Im\rho-u|\leq\tfrac12\}
\leq L_0(N\mathfrak f_\chi,u),
\tag{7}
\]

\[
L_0(q,u)
=3\log q+6\log(|u|+3)+6\log4+34.
\tag{8}
\]

This is an individual-character statement; it has no cancellation across
different \(\chi\)'s.

## 3. What local zeros and family cardinality actually imply

If a detector associates each selected \(t\) with a zero of the same
exact primitive \(L(s,\chi)\) within \(\alpha\), with at most \(b\) selected
rows per zero, then \(\alpha+\Delta\leq1/2\) gives

\[
\#\{t\in\mathcal T_\chi:|t-u|\leq\Delta\}
\leq bL_0(N\mathfrak f,u).
\tag{9}
\]

If, as in the standard large-value thinning, every \(\mathcal T_\chi\) is
\(1\)-separated, its left-hand side is already at most \(1\) for
\(\Delta<1/2\). Thus the local-zero count does not improve the selected
fibre bound.

**PROVED:** The frozen P7 cardinality statements are

\[
P\leq |X(\mathfrak f)|\leq N\mathfrak f\leq2Q
\quad\text{at one fixed modulus,}
\tag{10}
\]

and

\[
P\leq\mathcal F_{\rm prim}(Q)
<12Q^2
\quad\text{over the dyadic shell.}
\tag{11}
\]

Therefore one-separated fibres give only

\[
\mathcal D_\Delta(\mathcal T)\leq2mQ
\quad\text{at fixed }\mathfrak f,
\qquad
\mathcal D_\Delta(\mathcal T)<12mQ^2
\quad\text{over the shell.}
\tag{12}
\]

For \(Q=T^\vartheta\), fixed \(\vartheta>0\), these losses are respectively
\(T^\vartheta\) and \(T^{2\vartheta}\), up to logarithms. They are subpower
only under the additional, unfrozen restriction \(Q=T^{o(1)}\).

## 4. Sharp cross-character obstruction

For \(P\) colours and \(J\) blocks, put

\[
t_{j,c}=3j+\frac{c}{8P}
\qquad(0\leq j<J,\ 0\leq c<P),
\tag{13}
\]

and assign \(t_{j,c}\) to colour \(c\). Each colour fibre is
\(3\)-separated and has at most one point in every unit interval. At
\(\Delta=1/4\),

\[
|\mathcal T|=m=JP,\qquad
\mathcal M_{1/4}(\mathcal T)=P,\qquad
\mathcal D_{1/4}(\mathcal T)=JP^2=mP.
\tag{14}
\]

The replay verifies this exactly at \(P=3,J=4\). This is a finite
combinatorial geometry model, not a construction of Hecke zeros or a P7
detector. It proves precisely that fibrewise spacing, individual unit-window
counts, and family cardinality cannot imply \(o(mP)\) for
\(\mathcal D_\Delta\).

## 5. Conditional joint character--height sampling

The existing joint L2 source can see cross-character clustering if a detector
provides one common coefficient function. Assume

\[
D_\chi(t)=
\sum_{N<N\mathfrak a\leq2N}
c(\mathfrak a)\chi(\mathfrak a)(N\mathfrak a)^{-it},
\qquad
|D_\chi(t)|\geq V
\tag{15}
\]

for every detector row, where the same ideal function \(c\) is used for
every \(\mathfrak f,\chi,t\). This commonness is essential.

Fix a local center \(u\), retain one labelled row above each distinct time
in \(\mathcal T\cap[u-1/4,u+1/4]\), and replace

\[
c(\mathfrak a)\longmapsto
c_u(\mathfrak a)=c(\mathfrak a)(N\mathfrak a)^{-iu}.
\tag{16}
\]

Its \(\ell^2\) norm and support are unchanged, and (3) is unchanged exactly.
With Sobolev radius \(1/4\), the within-character sampling intervals are
disjoint and lie in \([-1/2,1/2]\) after translation. Enlarge to
\([-2,2]\) and apply Thorner's Theorem 2.1 with source ideal cutoff \(2N\),
conductor cutoff \(2Q\), height \(2\), and archimedean parameter \(m=0\).
This proves, under the displayed detector hypotheses,

\[
\mathcal M_{1/4}(\mathcal T)V^2
\ll_K\mathcal L_{\rm loc}(N,Q)\|c\|_2^2,
\tag{17}
\]

\[
\mathcal L_{\rm loc}(N,Q)
=\left(4+\frac12\log^2(2N)\right)
(2N+16Q^2)(\log(4Q))^A.
\tag{18}
\]

Hence

\[
\mathcal D_{1/4}(\mathcal T)
\ll_K
m\,\frac{\mathcal L_{\rm loc}(N,Q)\|c\|_2^2}{V^2}.
\tag{19}
\]

Taking \(c\) supported at the unit ideal illustrates the limitation of the
unconditional L2 input: it only gives a \(Q^2\)-scale local count, not a
subpower bound. The exact extra detector requirement for a desired
\(\mathcal D_{\rm target}\) is

\[
\frac{\mathcal L_{\rm loc}(N,Q)\|c\|_2^2}{V^2}
\ll_K\frac{\mathcal D_{\rm target}}m.
\tag{20}
\]

No P7 detector currently furnishes this common \(c\), uniform \(V\), and
range.

## 6. Weakest occupancy hypothesis and gate effect

The direct missing input for the current L2-to-discrete route is

\[
\mathcal D_\Delta(\mathcal T)\leq\mathcal D_{\rm target}.
\tag{21}
\]

Among one-point, cross-character height hypotheses, the weakest natural
form is

\[
\operatorname{OCC}_\Delta(M):
\qquad
\mathcal M_\Delta(\mathcal T)\leq M.
\tag{22}
\]

Equation (1) makes
\(\operatorname{OCC}_\Delta(\mathcal D_{\rm target}/m)\) sufficient, and
(14) proves the multiplier \(mM\) sharp. A labelled occupancy hypothesis is
stronger than necessary, because repeated labels at one height do not enlarge
\(\mathcal T\).

**OBSERVED:** This is a sharper diagnosis and an exact detector-side target,
not an analytic closure. P7-3 remains open, and an \(A_0\) cubic estimate
would still be needed after any successful \(\mathcal D_\Delta\) bound.

## Replay

Run the following from the project root:

    python3 proof/build_p7_detector_local_occupancy_v1.py --check
    python3 proof/build_p7_detector_local_occupancy_v2.py --check
    python3 -m unittest tests/test_p7_detector_local_occupancy_v2.py -v
