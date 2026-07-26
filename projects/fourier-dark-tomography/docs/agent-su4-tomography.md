# Dark-event tomography of off-diagonal four-mode errors

Date: 2026-07-26

This note asks whether four-photon dark-event counts, assisted by
calibrated output probes, can identify all twelve off-diagonal
coordinates of a small \(SU(4)\) error.  It records one obstruction and
one exact full-rank construction.

The calculations are reproduced by

```text
python3 scripts/search_su4_dark_tomography.py
```

All darkness and rank tests use exact Gaussian-integer or rational
arithmetic.

## 1. Local signed-probe observable

Order the twelve real coordinates as

\[
\theta=(x_{01},y_{01},x_{02},y_{02},x_{03},y_{03},
        x_{12},y_{12},x_{13},y_{13},x_{23},y_{23}),
\]

where

\[
X_{pq}=|p\rangle\langle q|+|q\rangle\langle p|,
\qquad
Y_{pq}=-i|p\rangle\langle q|+i|q\rangle\langle p|.
\]

Let

\[
U(\theta)=\exp\!\left(i\sum_\mu\theta_\mu G_\mu\right)F_4.
\]

For a target event \(e\) that is dark at \(F_4\), write
\(v_{e,\mu}\) for its normalized complex amplitude derivative along
\(G_\mu\).  Append a known signed output probe
\(\exp(\mathord\pm i\epsilon H)\), with coordinate vector \(h\).  To
leading order,

\[
\boxed{
\Delta P_{e,h}
:=P_e(+\epsilon h)-P_e(-\epsilon h)
=4\epsilon\,
\operatorname{Re}\!\left[
 (v_e\mathbin{\cdot}h)^*(v_e\mathbin{\cdot}\theta)
\right]
+O\!\left(
\epsilon\|\theta\|^2+\epsilon^2\|\theta\|+\epsilon^3
\right).
}
\tag{1}
\]

An unprobed exact-dark probability starts quadratically in \(\theta\)
and therefore does not determine the sign of a small error.  Equation
(1) uses the known probe amplitude as a local oscillator.  It converts
photon counts, rather than unobservable complex amplitudes, into a
signed linear measurement.

For one event, all possible probe differentials lie in the real span of
\(\operatorname{Re}v_e\) and \(\operatorname{Im}v_e\).  One dark event
therefore supplies at most two independent real rows.

## 2. No-go theorem for Fock-state inputs

Number-state inputs cannot identify all twelve coordinates, regardless
of which output probabilities or appended calibrated output probes are
used.

Let \(D=\operatorname{diag}(d_0,d_1,d_2,d_3)\) be real and traceless,
and set

\[
G=F_4DF_4^\dagger.
\]

Because the diagonal of \(G\) is \(\operatorname{tr}D/4=0\), \(G\)
lies entirely in the twelve-dimensional off-diagonal coordinate
space.  Nevertheless, for every Fock input \(|r\rangle\),

\[
e^{iG}F_4|r\rangle
=F_4e^{iD}|r\rangle
=e^{i\sum_jd_jr_j}F_4|r\rangle.
\tag{2}
\]

The error produces only a global phase.  If an arbitrary calibrated
output unitary \(V\) is appended, both sides of (2) are simply
multiplied by \(V\), so the obstruction persists.

In the coordinate convention above, an explicit basis of the
three-dimensional invisible subspace is

\[
\begin{aligned}
K_A&=X_{01}+X_{03}+X_{12}+X_{23},\\
K_B&=Y_{01}-Y_{03}+Y_{12}+Y_{23},\\
K_C&=X_{02}+X_{13}.
\end{aligned}
\tag{3}
\]

This is the right-diagonal input-phase gauge transported through
\(F_4\).  Removing output diagonal phases from the parameterization does
not remove this second gauge.

An exhaustive search over all four-photon Fock occupations found 184
dark transitions whose complex derivative vector has real rank two.
Their combined exact rank is only nine, with nullspace (3).  Five dark
events attain rank nine, which is minimal because each event contributes
at most two rows.  With the single input \((1,1,1,1)\), five dark
outputs also attain rank nine.  Thus the computation saturates, rather
than merely failing to find, the observable Fock-state quotient.

Here is an exact normalized certificate for that saturation.  Use input
\((1,1,1,1)\) and the following output/probe pairs, in the displayed row
order:

\[
\begin{array}{c|c}
\text{output}&\text{probe}\\ \hline
(0,0,1,3)&X_{03}\\
(0,0,1,3)&Y_{03}\\
(0,0,2,2)&X_{02}\\
(0,0,2,2)&Y_{02}\\
(0,0,3,1)&X_{12}\\
(0,0,3,1)&Y_{12}\\
(0,1,1,2)&X_{23}\\
(0,1,1,2)&Y_{23}\\
(0,2,2,0)&Y_{02}
\end{array}
\]

Define the leading physical contrast Jacobian by

\[
(J_F)_{e,\mu}
=
\left.
\frac{\partial}{\partial\theta_\mu}
\lim_{\epsilon\to0}
\frac{\Delta P_{e,h}(\theta,\epsilon)}{\epsilon}
\right|_{\theta=0}.
\tag{4}
\]

In the twelve-coordinate order stated above,

\[
J_F=
\begin{pmatrix}
0&0&0&0&\frac32&0&0&0&0&0&-\frac32&0\\
0&0&0&0&0&\frac32&0&0&0&0&0&\frac32\\
0&0&1&0&0&0&0&0&-1&0&0&0\\
0&0&0&1&0&0&0&0&0&-1&0&0\\
0&0&0&0&0&0&\frac32&0&0&0&-\frac32&0\\
0&0&0&0&0&0&0&\frac32&0&0&0&-\frac32\\
-1&0&0&0&0&0&-1&0&0&0&2&0\\
0&-1&0&0&0&0&0&-1&0&0&0&2\\
0&0&0&1&0&0&0&0&0&1&0&0
\end{pmatrix}.
\tag{5}
\]

Every row annihilates the three vectors (3).  Conversely, the
\(9\times9\) minor in columns

\[
(x_{01},y_{01},x_{02},y_{02},x_{03},y_{03},x_{12},y_{12},y_{13})
\]

has determinant \(81/8\).  Hence \(\operatorname{rank}J_F=9\), and the
three vectors (3) are its complete nullspace.

## 3. Coherent-input construction with full rank

The missing phase reference can be supplied by the four-mode
four-photon cat state

\[
|\Psi_{\rm cat}\rangle
=\frac12\left(
|4,0,0,0\rangle+|0,4,0,0\rangle
+|0,0,4,0\rangle+|0,0,0,4\rangle
\right).
\tag{6}
\]

For an output occupation \(s\), put

\[
Q(s)=\sum_{j=0}^3j\,s_j\pmod4.
\]

The four components in (6) have equal-magnitude amplitudes with relative
phases \(i^{jQ(s)}\).  Consequently,

\[
\mathcal A_{\Psi_{\rm cat},s}(F_4)
\ \propto\ \sum_{j=0}^3i^{jQ(s)}=0
\qquad\text{when }Q(s)\ne0.
\tag{7}
\]

There are 25 such dark four-photon outputs.

The modular-sector identity used here is known.  Vourdas and
Dunningham, Phys. Rev. A **71**, 013809 (2005), give the
phase-twisted all-bunched construction and its Fourier output rule, and
Dittel et al. later place such rules in a general permutation-symmetry
framework.  The new claim below is the local-identifiability certificate
and its comparison with the Fock-input gauge, not the selection rule.

Use the two calibrated multi-pair probes

\[
H_X=X_{01}-X_{02},
\qquad
H_Y=Y_{01}-Y_{02}.
\tag{8}
\]

They are the two phase quadratures coupling mode \(0\) to the
antisymmetric supermode \((|1\rangle-|2\rangle)/\sqrt2\).  At first
order they may also be synthesized from calibrated pairwise mixers.

Six \(H_X\) differentials and six \(H_Y\) differentials suffice.  In the
column orders

\[
(x_{01},x_{02},x_{03},x_{12},x_{13},x_{23})
\quad\text{and}\quad
(y_{01},y_{02},y_{03},y_{12},y_{13},y_{23}),
\]

respectively.  Define the physical Jacobians \(J_X,J_Y\) by the limiting
convention (4).  Equivalently, locally,

\[
\frac{\Delta P_{s,H_X}}{\epsilon}
=(J_X\theta_X)_s+O_2,
\qquad
\frac{\Delta P_{s,H_Y}}{\epsilon}
=(J_Y\theta_Y)_s+O_2,
\tag{9}
\]

where
\(O_2=O(\|\theta\|^2+\epsilon\|\theta\|+\epsilon^2)\).
Thus the displayed \(J\) is the \(\epsilon\to0\) Jacobian of
\(\Delta P/\epsilon\), not an exact finite-\(\epsilon\) response
matrix.  For the output
orders displayed below,

\[
J_X=
\begin{pmatrix}
0&-\frac32&0&0&-\frac32&0\\
\frac34&0&0&\frac34&0&\frac32\\
\frac94&0&0&\frac34&0&0\\
\frac34&0&\frac34&0&0&\frac32\\
0&-4&0&0&0&0\\
\frac34&0&\frac32&\frac34&0&0
\end{pmatrix},
\tag{10}
\]

and

\[
J_Y=
\begin{pmatrix}
0&-\frac32&0&0&-\frac32&0\\
\frac34&0&0&\frac34&0&\frac32\\
0&-\frac32&0&0&\frac32&0\\
\frac94&0&0&\frac34&0&0\\
\frac34&0&-\frac34&0&0&\frac32\\
\frac34&0&-\frac32&\frac34&0&0
\end{pmatrix}.
\tag{11}
\]

For every \(H_X\) row, all six \(Y\)-coordinate derivatives are exactly
zero; for every \(H_Y\) row, all six \(X\)-coordinate derivatives are
exactly zero.  The reproduction script asserts these omitted cross
blocks entry by entry before forming the displayed block determinant.

These constants include Fock-state normalization and the \(1/2\) in
the cat state.  More explicitly, for a component input
\(|4_j\rangle\) and output \(s\), put

\[
D_s=2^4\sqrt{4!\prod_ks_k!}.
\]

If \(M_{s,\mu}^{(j)}\) is the Gaussian-integer common-denominator
numerator of
\(\langle s|\widehat G_\mu F_4|4_j\rangle\), then

\[
v_{s,\mu}
=\frac{i}{2D_s}\sum_{j=0}^3M_{s,\mu}^{(j)}.
\tag{12}
\]

Substitution into (1) gives (10)--(11) without any floating-point
amplitude tests.

For a smaller exact rank certificate, independent row rescaling reduces
the two physical blocks to

\[
B_X=
\begin{pmatrix}
0&1&0&0&1&0\\
1&0&0&1&0&2\\
3&0&0&1&0&0\\
1&0&1&0&0&2\\
0&1&0&0&0&0\\
1&0&2&1&0&0
\end{pmatrix},
\qquad
\det B_X=-16,
\tag{13}
\]

using outputs

\[
(0,0,2,2),\ (0,1,1,2),\ (0,3,1,0),\
(1,0,2,1),\ (1,0,3,0),\ (1,1,0,2),
\]

and

\[
B_Y=
\begin{pmatrix}
0&1&0&0&1&0\\
1&0&0&1&0&2\\
0&1&0&0&-1&0\\
3&0&0&1&0&0\\
1&0&-1&0&0&2\\
1&0&-2&1&0&0
\end{pmatrix},
\qquad
\det B_Y=32,
\tag{14}
\]

using outputs

\[
(0,0,2,2),\ (0,1,1,2),\ (0,2,2,0),\
(0,3,1,0),\ (1,0,2,1),\ (1,1,0,2).
\]

The full Jacobian is block diagonal after the displayed ordering, and

\[
\det B_X\det B_Y=-512\ne0.
\tag{15}
\]

Equivalently,

\[
\det J_X=-\frac{243}{8},\qquad
\det J_Y=\frac{729}{32},\qquad
\det\operatorname{diag}(J_X,J_Y)
=-\frac{177147}{256}\ne0.
\tag{16}
\]

Thus twelve signed probability differentials locally identify all
twelve off-diagonal coordinates, conditional on calibrated cat and
probe phases.  Twelve is the dimension lower bound for regular local
identification by scalar probability differentials.

Four programmed settings suffice: the positive and negative
versions of \(H_X\) and \(H_Y\).  All relevant output counts are
recorded simultaneously in each setting.  Setting-count minimality is
not claimed.

## 4. Conditioning and count scale

Keeping the physical probability normalization rather than the
independent row rescalings in (11)--(12), the selected \(12\times12\)
Jacobian has singular-value condition number approximately

\[
\kappa_{\rm raw}=7.05.
\]

After normalizing each row to isolate its angular geometry,

\[
\kappa_{\rm row}=4.86.
\]

For an ideal background-free Poisson approximation, weighting by the
probe-induced count probabilities gives

\[
\kappa_{\rm Pois}=4.79.
\]

The probe-only leading probability coefficients for the selected
outputs range from \(3/16\) to \(1\), so none of the twelve reference
signals is parametrically weak.

These numbers establish reasonable local geometry, not an optimized
experimental design.  A proper design must include multinomial count
covariance, state-preparation infidelity, partial distinguishability,
loss, dark counts, a finite probe angle, and unequal shot allocation.

## 5. Minimality and interpretation

- Twelve scalar differentials are necessary for regular local
  identification in this twelve-parameter model, and the construction
  uses exactly twelve.
- Fock inputs can recover at most nine coordinates; this is an exact
  gauge obstruction, not a conditioning problem.
- Five rank-two Fock dark events are necessary and sufficient for that
  nine-dimensional quotient within the infinitesimal
  dark-amplitude/signed-probe protocol.
- Four coordinate-axis probes are necessary in the exhaustive
  coordinate-axis search for the fixed Fock or cat constructions.
- The two combined probes (8) suffice for the cat construction.
  A general proof that no single arbitrary multi-pair probe can work has
  not been obtained; finite searches reached rank eleven at most, so
  two-probe minimality should not yet be claimed as a theorem.

The practical price of full identifiability is the coherent state (6).
Preparing a phase-stable four-mode four-photon cat state is much harder
than preparing \(|1,1,1,1\rangle\).  The experimentally conservative
proposal is therefore nine-parameter tomography modulo input phase
gauge with Fock inputs.  The cat-state construction is an exact
full-identifiability benchmark and a clear statement of which extra
resource removes the obstruction.

This statement is local and model-relative.  It concerns only the twelve
off-diagonal generators, not the three output-diagonal directions or
global \(SU(4)\) tomography.  The cat retains discrete global phase
aliases.  More importantly, three unknown relative phases in its
preparation are locally confounded with precisely the three transported
input-phase directions in Eq. (3); those phases require independent
calibration or additional reference data.

## 6. Known general Fourier-cat dark family

For completeness, recall that the dark-state construction extends
exactly to every Fourier multiport and every positive photon number.

Let

\[
F_m(k,j)=\frac{\omega^{kj}}{\sqrt m},
\qquad
\omega=e^{2\pi i/m},
\]

and, for \(n\geq1\), define the phase-twisted all-bunched cat state

\[
|\Psi_{\ell}^{(m,n)}\rangle
=\frac1{\sqrt m}\sum_{j=0}^{m-1}
\omega^{-\ell j}|n e_j\rangle,
\qquad 0\leq\ell<m.
\tag{17}
\]

Here \(|n e_j\rangle\) means that all \(n\) photons occupy input mode
\(j\).  For an output occupation \(s\) of total size \(n\), put

\[
Q(s)=\sum_{k=0}^{m-1}k s_k\pmod m.
\]

Then the normalized transition amplitude is

\[
\boxed{
\mathcal A_{\Psi_\ell^{(m,n)},s}(F_m)
=
\sqrt{\frac{n!}{\prod_ks_k!}}\,
m^{(1-n)/2}\,
\mathbf 1_{\{Q(s)=\ell\}}.
}
\tag{18}
\]

In particular, every output in the other \(m-1\) modular sectors is
exactly dark.

To prove (18), first use a single all-bunched component.  Every term in
its repeated-column permanent has the same phase, so

\[
\mathcal A_{|ne_j\rangle,s}(F_m)
=
\sqrt{\frac{n!}{\prod_ks_k!}}\,
m^{-n/2}\omega^{jQ(s)}.
\]

Superposing the \(m\) components with the coefficients in (17) gives

\[
\frac1{\sqrt m}\sum_{j=0}^{m-1}
\omega^{j(Q(s)-\ell)}
=
\sqrt m\,\mathbf 1_{\{Q(s)=\ell\}},
\]

which proves the result.

This is the standard cyclic selection mechanism applied to a coherent
all-bunched input, not a new suppression law.  Its relevance here is
operational: unlike a number-state input, it fixes relative input-mode
phases and therefore removes the right-diagonal gauge.

The no-go theorem also generalizes.  For every \(m\), the
\((m-1)\)-dimensional family

\[
G=F_mDF_m^\dagger,\qquad
D=D^\dagger\ \text{diagonal},\quad\operatorname{tr}D=0,
\]

has zero diagonal and is invisible to all number-state input
probabilities, even after an arbitrary calibrated output unitary.
The cat state supplies sensitivity to those relative phases.  Whether
the two-probe full-rank tomography construction extends with similarly
small resources for arbitrary \(m,n\) is a separate design problem and
is not claimed by (16).
