# Mathematical notebook

## 1. Edge moment model

Let \(G=(V,E)\) be a connected undirected graph.  A complex voltage vector
\(v\in\mathbb C^V\) produces the Hermitian rank-one matrix

\[
W=vv^*,\qquad W_{ij}=v_i\overline{v_j}.
\]

Assume \(W_{ii}>0\) is specified for every vertex and \(W_{ij}\) is specified
for every edge.  Each edge-local \(2\times2\) positive-semidefinite condition
is

\[
|W_{ij}|^2\leq W_{ii}W_{jj}.
\]

Define the **radial defect**

\[
r_{ij}=1-\frac{|W_{ij}|^2}{W_{ii}W_{jj}}\in[0,1].
\]

When \(W_{ij}\neq0\), define its normalized phase

\[
u_{ij}=\frac{W_{ij}}{|W_{ij}|},\qquad u_{ji}=\overline{u_{ij}}.
\]

For an oriented cycle
\(C=(i_0,i_1,\ldots,i_{q-1},i_0)\), define its holonomy

\[
H_C=\prod_{t=0}^{q-1}u_{i_t i_{t+1}},
\qquad
h_C=|1-H_C|.
\]

## 2. Exact completion theorem

**Theorem 1 (rank-one edge completion).**
The specified diagonal and edge moments admit a voltage vector \(v\), unique
up to a global phase, satisfying

\[
W_{ii}=|v_i|^2,\qquad W_{ij}=v_i\overline{v_j}
\quad(ij\in E)
\]

if and only if:

1. \(r_{ij}=0\) for every edge; and
2. \(H_C=1\) for every cycle.

It is enough to check the cycles of any cycle basis.

**Proof.** Necessity follows by telescoping:

\[
\prod_{(i,j)\in C}
\frac{v_i\overline{v_j}}{|v_i||v_j|}=1,
\]

and every rank-one edge saturates the \(2\times2\) determinant inequality.

For sufficiency, choose a root \(o\), set \(v_o=\sqrt{W_{oo}}>0\), and choose
a spanning tree.  Propagate phases along each tree edge so that
\(v_i\overline{v_j}\) has phase \(u_{ij}\), while setting
\(|v_i|=\sqrt{W_{ii}}\).  Edge saturation then gives equality with every tree
moment.  For a non-tree edge, the fundamental cycle condition says that its
phase agrees with the propagated endpoint phases; saturation gives the
magnitude.  Uniqueness follows because a connected graph fixes all relative
phases. \(\square\)

**Corollary 1 (unicyclic case).**
For a connected unicyclic graph, edge saturation and one scalar cycle
condition are necessary and sufficient.

## 3. A challenged assumption

A phase-only “cycle defect” cannot certify voltage recoverability.

**Counterexample 1.** Let all \(W_{ii}=1\) on a triangle and all edge moments
equal the same real number \(\rho\in(0,1)\).  The cycle holonomy is exactly
\(1\), yet every radial defect equals \(1-\rho^2>0\), so no rank-one voltage
vector matches the edge moments.

Therefore any useful certificate must include at least:

- edge magnitude/rank defects; and
- cycle phase inconsistency.

This already modifies the initial research pitch: the obstruction is not
carried by cycles alone.

## 4. Exact spanning-tree recovery residual

Choose a spanning tree \(T\) and reconstruct \(\widehat v\) from the
diagonals and tree-edge phases as in Theorem 1.  For any oriented edge
\((i,j)\), write

\[
a_{ij}=\sqrt{W_{ii}W_{jj}},\qquad b_{ij}=|W_{ij}|,
\]

and let \(\delta_{ij}\) be the phase difference between
\(\widehat v_i\overline{\widehat v_j}\) and \(W_{ij}\).  Then

\[
\left|\widehat v_i\overline{\widehat v_j}-W_{ij}\right|^2
=a_{ij}^2+b_{ij}^2-2a_{ij}b_{ij}\cos\delta_{ij}.
\tag{1}
\]

On a tree edge, \(\delta_{ij}=0\), so the residual is exactly
\(a_{ij}-b_{ij}\).  On the unique non-tree edge of a unicyclic graph,
\(\delta_{ij}\) is the cycle holonomy angle.

Equivalently,

\[
|\,\widehat W_{ij}-W_{ij}\,|^2
=(a_{ij}-b_{ij})^2+2a_{ij}b_{ij}(1-\cos\delta_{ij}).
\tag{2}
\]

This gives an exact decomposition into radial and angular error.  The next
step is to write it directly in terms of \(r_{ij}\) and \(h_C\).

Since \(b_{ij}=a_{ij}\sqrt{1-r_{ij}}\) and
\(h=|1-e^{i\delta}|\), Eq. (2) gives:

\[
|\,\widehat W_{ij}-W_{ij}\,|
=a_{ij}
\sqrt{
  (1-\sqrt{1-r_{ij}})^2
  +\sqrt{1-r_{ij}}\,h^2
}.
\tag{3}
\]

For a tree edge, take \(h=0\).  For the unique chord of a unicyclic graph,
\(h=h_C\).  Thus Eq. (3) is an exact, rather than asymptotic, recovery-error
formula.

## 5. Propagation to AC bus injections

Let \(Y\) be the network admittance matrix.  In the bus-injection model,

\[
S_i(W)=\sum_j \overline{Y_{ij}}W_{ij}.
\]

The spanning-tree reconstruction preserves every \(W_{ii}\).  Therefore:

**Theorem 2 (local injection-residual certificate).**

\[
|S_i(\widehat W)-S_i(W)|
\leq
\sum_{j:ij\in E}|Y_{ij}|\,
|\widehat W_{ij}-W_{ij}|,
\tag{4}
\]

where every term on the right is computed exactly from Eq. (3), using zero
phase defect on tree edges and fundamental-cycle holonomy on chords.

**Proof.** The diagonal term cancels, and Eq. (4) is the triangle inequality
applied to the remaining linear terms in \(S_i\). \(\square\)

Consequently, if a relaxed moment point satisfies specified active and
reactive injections, Eq. (4) certifies a disk containing the injection
produced by its recovered voltage vector.  This is a physical residual
certificate, not yet a feasibility repair or an optimality certificate.

## 6. Status boundaries

Theorem 1 proves a statement about completing edge moments to a voltage
vector.  It does **not** prove:

- that an SOCP or SDP relaxation is exact;
- that the recovered voltage satisfies every original inequality;
- that a feasible recovered point is globally optimal;
- or that small edge residual implies a small objective gap without further
  regularity assumptions.

## 7. Small residual does not imply nearby feasibility

Consider a lossless three-bus triangle with unit voltage magnitudes, unit
line susceptance magnitudes, and bus \(0\) as the angle reference.  The
active injections at buses 1 and 2 are

\[
\begin{aligned}
P_1(\theta)
 &=\sin\theta_1+\sin(\theta_1-\theta_2),\\
P_2(\theta)
 &=\sin\theta_2+\sin(\theta_2-\theta_1).
\end{aligned}
\tag{5}
\]

Their sum is

\[
P_1(\theta)+P_2(\theta)=\sin\theta_1+\sin\theta_2\leq2.
\tag{6}
\]

At \(\theta^\dagger=(\pi/2,\pi/2)\), the injection is \((1,1)\) and the
Jacobian is singular.

**Counterexample 2 (arbitrarily small infeasible residual).**
For any \(\epsilon>0\), the target \(p=(1+\epsilon,1+\epsilon)\) has residual
\(\epsilon\) in infinity norm at \(\theta^\dagger\), but no solution exists,
because its injection sum is \(2+2\epsilon>2\), contradicting Eq. (6).

Thus no theorem of the form

\[
\text{small recovered injection residual}
\Longrightarrow
\text{nearby feasible AC point}
\]

can hold without a conditioning or solvability-margin hypothesis.

## 8. Conditional local repair certificate

Let \(F(x)=p\) be a reduced, square power-flow system after fixing a reference
angle and selecting the controlled variables.  At a recovered point \(x_0\),
let

\[
J_0=DF(x_0),\quad
\eta=\|J_0^{-1}(F(x_0)-p)\|,\quad
\beta=\|J_0^{-1}\|.
\]

Suppose \(J\) is \(L\)-Lipschitz in a suitable neighborhood, and define

\[
h=\beta L\eta.
\]

A standard Newton--Kantorovich argument certifies a solution when
\(h\leq1/2\), within radius

\[
t_*=\frac{1-\sqrt{1-2h}}{\beta L}.
\tag{7}
\]

For the lossless triangle in Eq. (5), using infinity norms, a global
Jacobian Lipschitz bound for line weights \(b_{01},b_{12},b_{02}>0\) is

\[
L\leq
\max\{b_{01}+4b_{12},\,b_{02}+4b_{12}\}.
\tag{8}
\]

This certificate is deliberately conservative and is established
mathematics, not a novelty claim.  Its role here is diagnostic: it exposes
the missing condition number between a moment-defect certificate and
physical feasibility.

## 9. Composed defect-to-feasibility certificate

Theorems 1–2 and the conditional repair result can be composed.

Let \(d_{ij}\) denote the exact edge recovery error from Eq. (3), and let

\[
\rho_i=\sum_{j:ij\in E}|Y_{ij}|d_{ij}.
\]

Choose a norm on the reduced real power-flow system and let \(\rho\) be the
corresponding bound assembled from the buswise active/reactive residual
bounds.  Suppose

\[
\|J_0^{-1}\|\leq\beta
\quad\text{and}\quad
\|J(x)-J(y)\|\leq L\|x-y\|
\]

throughout the required neighborhood.

**Theorem 3 (conditional defect-to-feasibility certificate).**
If

\[
\overline h=\beta^2L\rho\leq\frac12,
\tag{9}
\]

then the reduced power-flow equations have a solution within distance

\[
\overline t=
\frac{1-\sqrt{1-2\overline h}}{\beta L}
\tag{10}
\]

of the spanning-tree recovery, subject to the usual
Newton--Kantorovich neighborhood assumptions.

**Proof.** Theorem 2 gives
\(\|F(x_0)-p\|\leq\rho\), hence
\(\|J_0^{-1}(F(x_0)-p)\|\leq\beta\rho\).  Substitute this upper bound for
\(\eta\) in Eq. (7). \(\square\)

The theorem is useful because its first input, \(\rho\), is determined by
the relaxation's edge-rank and cycle defects.  It is conservative: using
the actual residual and actual Newton direction can certify cases rejected
by Eq. (9).

It also suggests the algorithmic product:

1. solve a cheap relaxation;
2. compute edge defects and \(\rho\);
3. estimate the local inverse-Jacobian norm;
4. certify repair if Eq. (9) holds;
5. otherwise strengthen only the implicated cycles or invoke a robust
   nonlinear/global method.

The composition is proved, but its novelty and practical value depend on
whether it is sharper or cheaper than existing solvability tests on real
benchmarks.

## 10. Spanning-tree recovery is generally not the best projection

Theorem 1 uses a spanning tree because it is exact when the data are
consistent.  With inconsistent relaxed moments, it concentrates all angular
error on the non-tree edges.  That is convenient, but not generally optimal
for either moment error or the injection certificate.

Consider a unit-magnitude triangle whose normalized oriented edge phases
have principal holonomy angle \(\delta\in[-\pi,\pi]\).  A spanning-tree
recovery can put zero phase error on two edges and error \(\delta\) on the
third, giving total squared edge error

\[
E_{\mathrm{tree}}=4\sin^2(\delta/2).
\tag{11}
\]

Alternatively, distribute the correction equally, with phase error
\(\delta/3\) on every edge.  This is cycle consistent and gives

\[
E_{\mathrm{bal}}=12\sin^2(\delta/6).
\tag{12}
\]

For \(0<|\delta|\leq\pi\),

\[
E_{\mathrm{bal}}<E_{\mathrm{tree}}.
\tag{13}
\]

For small \(\delta\), the ratio
\(E_{\mathrm{tree}}/E_{\mathrm{bal}}\to3\).

**Proof of Eq. (13).** Put \(x=|\delta|/6\in(0,\pi/6]\).
Using \(\sin(3x)=\sin x(3-4\sin^2x)\),

\[
\frac{E_{\mathrm{tree}}}{E_{\mathrm{bal}}}
=\frac{\sin^2(3x)}{3\sin^2x}
=\frac{(3-4\sin^2x)^2}{3}>1
\]

for \(x\in(0,\pi/6]\). \(\square\)

Therefore spanning-tree recovery should remain a proof device, not the
default algorithm.  The algorithmic target becomes a weighted angular
projection minimizing the downstream certificate

\[
\max_i\sum_j |Y_{ij}|\,|\widehat W_{ij}-W_{ij}|
\]

or the composed quantity \(\beta^2L\rho\).  Angular synchronization and
state-estimation recovery already exist; the potentially distinct idea is
to optimize the *rigorous repair certificate* rather than raw phasor error.

## 11. Minimax injection projection on a symmetric triangle

Squared edge error is not the certificate used in Theorem 3.  On a
unit-weight triangle, let nonnegative \(y_1,y_2,y_3\) allocate a principal
holonomy magnitude \(\delta\in[0,\pi]\):

\[
y_1+y_2+y_3=\delta.
\]

The unit edge residual function is

\[
f(y)=2\sin(y/2),
\]

and the worst-bus injection bound is

\[
M(y)=\max\{
 f(y_1)+f(y_2),
 f(y_2)+f(y_3),
 f(y_3)+f(y_1)
\}.
\tag{14}
\]

Corrections of mixed signs cannot improve the optimum: cancelling equal
amounts from an oppositely signed pair preserves total signed correction and
weakly decreases every incident residual.  It is therefore enough to use
nonnegative allocations.

**Theorem 4 (balanced minimax projection).**
For the symmetric triangle and \(0\leq\delta\leq\pi\),

\[
\min_{y_1+y_2+y_3=\delta}M(y)
=4\sin(\delta/6),
\tag{15}
\]

attained by \(y_1=y_2=y_3=\delta/3\).

**Proof.** Order \(y_1\leq y_2\leq y_3\), so
\(M=f(y_2)+f(y_3)\) and \(y_1\leq\delta/3\).  With \(y_1\) fixed,
\(f(y_2)+f(\delta-y_1-y_2)\) is concave in \(y_2\); its minimum on the
ordered interval occurs either at \(y_2=y_1\) or at
\(y_2=y_3=(\delta-y_1)/2\).

The second endpoint gives at least \(2f(\delta/3)\).  At the first endpoint,
the function

\[
f(y_1)+f(\delta-2y_1)
\]

is concave on \([0,\delta/3]\), so its minimum occurs at an endpoint.  The
\(y_1=\delta/3\) endpoint equals \(2f(\delta/3)\).  The other endpoint is
\(f(\delta)\), and

\[
f(\delta)\geq2f(\delta/3)
\]

for \(\delta\leq\pi\), since for \(x=\delta/6\leq\pi/6\),
\(\sin(3x)=\sin x(3-4\sin^2x)\geq2\sin x\).
Thus \(M\geq2f(\delta/3)=4\sin(\delta/6)\), with equality at the balanced
allocation. \(\square\)

For small \(\delta\), the best tree has bound approximately \(\delta\),
whereas the balanced optimum has bound approximately \(2\delta/3\): a
factor \(3/2\) improvement in the actual worst-bus certificate.

## 12. Weighted and conditioning-aware projection

The balanced rule fails when edge weights differ.  A finite grid search at
\(\delta=0.6\) gives:

| Edge weights | Best tree | Balanced | Grid optimum | Grid allocation |
|---|---:|---:|---:|---|
| \((1,1,1)\) | 0.591040 | 0.399334 | 0.399334 | \((0.2,0.2,0.2)\) |
| \((5,1,1)\) | 0.591040 | 1.198001 | 0.544306 | \((0.054,0.271,0.275)\) |
| \((4,2,1)\) | 0.591040 | 1.198001 | 0.591040 | \((0,0,0.6)\) |

These are computational results on a grid of 600 subdivisions, not
continuous optimality proofs.  They show that a certificate-aware solution
can interpolate between a distributed correction and a tree correction.

Minimizing the injection residual \(\rho\) is still incomplete because the
recovered angles change the inverse-Jacobian norm \(\beta\).  The actual
sufficient condition uses

\[
\overline h=\beta(\widehat\theta)^2L\rho(\widehat\theta).
\tag{16}
\]

Near the collapse point, a projection with small \(\rho\) may have infinite
or enormous \(\beta\).  On the test triangle at base angle \(1.3\), a
holonomy \(0.01\) yields a grid-optimized
\(\overline h\approx0.484\), while holonomy \(0.03\) yields
\(\overline h\approx1.569\).  Only the first is certified by Theorem 3.

This produces two separate optimization layers:

1. a convex or nearly convex phase-projection problem minimizing \(\rho\);
2. a nonconvex conditioning-aware problem minimizing
   \(\beta^2L\rho\).

The second is the meaningful target, but also the harder one.

## 13. A scalable linear-programming surrogate

Fix a winding branch and let

\[
x_e=(B^\mathsf{T}\theta-\alpha)_e
\]

be the unwrapped phase correction on edge \(e\), with
\(|x_e|\leq\gamma\leq\pi\).  For bus-edge weights \(q_{ie}\geq0\), define

\[
\begin{aligned}
\Phi(\theta)
  &=\max_i\sum_{e\ni i}q_{ie}\,2\sin(|x_e|/2),\\
\Psi(\theta)
  &=\max_i\sum_{e\ni i}q_{ie}\,|x_e|.
\end{aligned}
\tag{17}
\]

On a fixed winding branch, minimizing \(\Psi\) is a linear program.  Introduce
\(u_e\geq|x_e|\) and \(t\), then impose

\[
\begin{aligned}
-u_e&\leq(B^\mathsf{T}\theta-\alpha)_e\leq u_e,\\
\sum_{e\ni i}q_{ie}u_e&\leq t
\quad\text{for every bus }i,
\end{aligned}
\]

and minimize \(t\).

Let

\[
c_\gamma=\frac{2\sin(\gamma/2)}{\gamma},
\qquad c_0=1.
\]

**Theorem 5 (physical-certificate approximation).**
On the fixed branch \(|x_e|\leq\gamma\),

\[
c_\gamma\Psi(\theta)\leq\Phi(\theta)\leq\Psi(\theta).
\tag{18}
\]

If \(\theta_{\rm LP}\) minimizes \(\Psi\) and \(\theta_*\) minimizes \(\Phi\)
on the same branch, then

\[
\Phi(\theta_{\rm LP})
\leq
\frac{1}{c_\gamma}\Phi(\theta_*)
=
\frac{\gamma}{2\sin(\gamma/2)}\Phi(\theta_*).
\tag{19}
\]

**Proof.** On \([0,\gamma]\), the function
\(2\sin(x/2)/x\) decreases from \(1\) to \(c_\gamma\).  Apply the resulting
scalar bounds termwise, preserve them under nonnegative weighted sums and
the maximum over buses, and compare the two minimizers. \(\square\)

The worst-case approximation factor is at most \(\pi/2\) for principal
corrections and is approximately \(1+\gamma^2/24\) for small \(\gamma\).
This makes the LP a near-exact surrogate in the regime where local repair is
most likely to be certifiable.

The qualification “fixed winding branch” matters.  Choosing windings on a
general meshed graph is discrete and can reintroduce combinatorial
complexity.  A unicyclic network has only one independent winding choice.

This theorem is proved but not yet claimed as novel.  Robust
\(\ell_1\)-synchronization is established literature; novelty depends on the
OPF-specific minimax weighting and the downstream certificate.

## 14. Residual ordering and certificate ordering can disagree

The LP in Section 13 optimizes the physical residual surrogate, not the
composed repair score

\[
\overline h(\theta)=\beta(\theta)^2L\rho(\theta).
\tag{20}
\]

There is no general monotonicity implication

\[
\rho(\theta_a)<\rho(\theta_b)
\quad\Longrightarrow\quad
\overline h(\theta_a)<\overline h(\theta_b),
\tag{21}
\]

because the inverse-Jacobian factor is evaluated at the recovered point.
The following four-bus, five-edge numerical witness makes this failure
explicit.  Edges are oriented
\((0,1),(1,2),(2,3),(3,0),(0,2)\), with target phases

\[
(0.0717428315,-0.6000636418,1.2868594768,
 -0.7038597628,-0.5328325737)
\]

and susceptance magnitudes

\[
(0.5949593988,0.5346125006,0.7588295036,
 0.7638047260,1.2140368523).
\]

Using the global Lipschitz bound implemented in `lossless_graph.py` gives:

| Recovery | \(\rho\) | \(\beta\) | \(\overline h\) | Certified |
|---|---:|---:|---:|---|
| Minimax LP | 0.0308973 | 1.5917183 | 0.5000405 | no |
| Weighted least squares | 0.0309594 | 1.5848813 | 0.4967503 | yes |

Thus the LP wins its intended residual objective but crosses the sufficient
certificate threshold in the wrong direction.  The example is checked as a
regression test.  It has two consequences:

1. residual-only improvement must not be advertised as a universal
   certification improvement;
2. a practical method can cheaply generate multiple recovered points and
   select the one with the smallest independently computed
   \(\overline h\), or optimize a conditioning-aware upper surrogate
   directly.

The second direction is the more interesting mathematical target.  The
inverse-Jacobian norm is nonsmooth and diverges near singularity, so a useful
surrogate will need a certified lower bound on Jacobian distance to
singularity, not merely another phase-fitting norm.

## 15. A conditioning-aware trust-region family

Let \(\theta_0\) be a reference point with nonsingular Jacobian \(J_0\), set
\(\beta_0=\|J_0^{-1}\|\), and suppose

\[
\|J(\theta)-J(\theta_0)\|
\leq L\|\theta-\theta_0\|
\tag{22}
\]

in the norm of interest.

**Theorem 6 (trust-region inverse bound).**
For every \(\theta\) with
\(\|\theta-\theta_0\|\leq r\) and

\[
\beta_0Lr<1,
\tag{23}
\]

the Jacobian \(J(\theta)\) is nonsingular and

\[
\|J(\theta)^{-1}\|
\leq
\frac{\beta_0}{1-\beta_0Lr}.
\tag{24}
\]

**Proof.** Write

\[
J(\theta)
=J_0\left[I+J_0^{-1}(J(\theta)-J_0)\right].
\]

The perturbation inside brackets has norm at most
\(\beta_0Lr<1\).  Its inverse exists by the Neumann series and has norm at
most \(1/(1-\beta_0Lr)\).  Multiplication by \(J_0^{-1}\) gives
Eq. (24). \(\square\)

For each radius \(r\), add the box

\[
\|\theta-\theta_0\|_\infty\leq r
\tag{25}
\]

to the fixed-winding LP in Section 13.  This remains a linear program.  If
\(\theta_r\) is its solution, then the composed repair quantity has the
computable upper bound

\[
\overline h(\theta_r)
\leq
\left(
  \frac{\beta_0}{1-\beta_0Lr}
\right)^2
L\rho(\theta_r),
\qquad \beta_0Lr<1.
\tag{26}
\]

A one-dimensional sweep over radii therefore trades decreasing residual
against worsening certified conditioning using only LPs.  The implemented
algorithm also evaluates the actual Jacobian at each returned candidate and
selects the smallest verified \(\overline h\).  Including \(r=0\), the
least-squares reference, and the unconstrained LP ensures that finite
candidate selection is never worse than either endpoint under the computed
score.

Theorem 6 is a standard matrix-perturbation consequence and is not claimed
as new.  Convex inner restrictions of AC power-flow feasibility already use
nonsingular base points and fixed-point bounds.  The research question is
whether coupling this guard to *relaxation-specific cycle/radial defect
projection* yields a sharper or cheaper recovery decision.

## 16. Radial-aware phase projection

Let an edge-relaxed moment satisfy

\[
W_{ii}>0,\qquad W_{jj}>0,\qquad
|W_{ij}|^2\leq W_{ii}W_{jj}.
\]

Write

\[
r=\sqrt{W_{ii}W_{jj}},\qquad
a=|W_{ij}|,\qquad c=r-a\geq0,
\]

and let \(x\) be the phase correction applied during rank-one recovery.  The
exact recovered edge error is

\[
d(x)=|re^{ix}-a|
=\sqrt{c^2+4ra\sin^2(x/2)}.
\tag{27}
\]

The radial-aware linear surrogate is

\[
g(x)=c+r|x|.
\tag{28}
\]

The radial term \(c\) is a fixed buswise offset, so minimizing the maximum
admittance-weighted sum of \(g(x)\) remains a linear program.

Assume \(|x|\leq\gamma\leq\pi\) and a nondegeneracy ratio
\(a/r\geq\kappa>0\).  Define

\[
K_\gamma=\frac{\gamma}{2\sin(\gamma/2)}.
\]

**Theorem 7 (radial-aware approximation).**
For every eligible edge,

\[
d(x)\leq g(x)
\leq
\sqrt{1+\frac{K_\gamma^2}{\kappa}}\,d(x).
\tag{29}
\]

Consequently, if \(\theta_{\rm LP}\) minimizes the maximum buswise weighted
sum of \(g\), and \(\theta_*\) minimizes the corresponding exact sum of
\(d\), then

\[
\Phi(\theta_{\rm LP})
\leq
\sqrt{1+\frac{K_\gamma^2}{\kappa}}\,
\Phi(\theta_*).
\tag{30}
\]

**Proof.** The triangle inequality and chord bound give

\[
d(x)
\leq c+2r\sin(|x|/2)
\leq c+r|x|=g(x).
\]

Let \(q=2\sqrt{ra}\sin(|x|/2)\), so
\(d(x)=\sqrt{c^2+q^2}\).  Monotonicity of
\(x/[2\sin(x/2)]\) and \(a/r\geq\kappa\) imply

\[
r|x|
\leq K_\gamma\,2r\sin(|x|/2)
\leq\frac{K_\gamma}{\sqrt{\kappa}}q.
\]

Cauchy--Schwarz now yields the second inequality in Eq. (29).  Nonnegative
weighted sums, the maximum over buses, and comparison of the two minimizers
give Eq. (30). \(\square\)

The constant is conservative and becomes weak when an edge is far from
rank-one saturation.  In the radial-free case \(a=r\), Theorem 5 gives the
sharper factor \(K_\gamma\).

Theorem 7 validates the radial-offset LP as an approximation to the exact
*moment residual certificate*.  It does not say that this objective
minimizes the actual Newton correction or maximizes repair success.  The
full-AC experiments in `full-ac-benchmark.md` show that these orderings can
disagree substantially.
