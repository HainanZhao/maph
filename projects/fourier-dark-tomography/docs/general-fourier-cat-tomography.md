# General Fourier-cat identifiability theorem

Date: 2026-07-26

Status: proved algebraically and checked by an independent exact-integer
certificate for \(3\leq m\leq 9\) at \(n=m\), for \(2\leq m\leq8\) at
\(n=2m\), and by independent defining-polynomial derivative checks including
\((m,n)=(2,4)\).  The proof is uniform in \(m\), so the finite checks are
regression tests rather than evidence for an unproved extrapolation.  A
targeted prior-art audit found the Fourier-cat suppression rule and
displaced-null principle separately, but no direct antecedent for the
combined identifiability construction.

## Result

Let
\[
F_m(a,j)=m^{-1/2}\omega^{aj},\qquad
\omega=e^{2\pi i/m},
\]
and prepare the charge-zero Fourier cat
\[
|\mathrm{Cat}_{m,n}\rangle
=\frac1{\sqrt m}\sum_{j=0}^{m-1}|n e_j\rangle ,
\qquad n\equiv0\pmod m,\qquad n>2.
\]
The unknown coherent output error is
\[
e^{i\widehat H},\qquad H=H^\dagger,\qquad H_{aa}=0.
\]
Thus the parameter space is the \(m(m-1)\)-real-dimensional space
\(\mathcal H_{\rm off}(m)\) of off-diagonal Hermitian matrices.

### Theorem

For every \(m\geq2\) and every \(n>2\) divisible by \(m\), there are
\[
E=\frac{m(m-1)}2
\]
nominally dark photon-counting outcomes and two fixed calibrated Hermitian
probes \(R,T\) such that the two signed-probe contrasts for every outcome
have a full-rank \(m(m-1)\times m(m-1)\) limiting Jacobian on
\(\mathcal H_{\rm off}(m)\).

Consequently the finite-angle contrast map is locally invertible for all
sufficiently small nonzero calibrated probe angles.  The construction uses
four programmed settings, \(+\epsilon R,-\epsilon R,+\epsilon T,-\epsilon
T\).  All selected outcomes are collected in parallel.  Both the number of
outcomes and scalar contrasts attain the dimension/Jacobian-rank lower
bounds required for regular local identification:
\[
E\geq\frac{\dim\mathcal H_{\rm off}(m)}2,\qquad
N_{\rm scalar}\geq\dim\mathcal H_{\rm off}(m).
\]

For the most economical family \(m\geq3\), take \(n=m\).  Thus this is an
arbitrary-mode theorem, not an extrapolation of an \(F_4\) parity argument.
The exceptional two-mode case is included by taking \(n=4,6,\ldots\).

## Step 1: exact Fourier-cat amplitudes

For an output occupation \(s=(s_0,\ldots,s_{m-1})\), write
\[
|s|=\sum_a s_a=n,\qquad Q(s)=\sum_a a s_a\pmod m.
\]
Direct expansion of the cat gives
\[
\begin{aligned}
A_s(F_m)
&=\sqrt{\frac{n!}{\prod_a s_a!}}\,
  \frac1{\sqrt m}\sum_{j=0}^{m-1}
  \prod_a F_m(a,j)^{s_a}\\
&=\sqrt{\frac{n!}{\prod_a s_a!}}\,
  m^{-(n+1)/2}\sum_{j=0}^{m-1}\omega^{jQ(s)}\\
&=\sqrt{\frac{n!}{\prod_a s_a!}}\,
  m^{(1-n)/2}\,\mathbf 1_{\{Q(s)=0\}}.
\end{aligned}
\]
Hence every sector \(Q(s)=c\neq0\) is exactly dark.

## Step 2: closed-form dark-amplitude gradient

Put \(U(\theta)=e^{i\theta H}F_m\).  Differentiating the output polynomial at
\(\theta=0\) gives
\[
\left.\frac{d A_s(U(\theta))}{d\theta}\right|_0
=i\alpha_s\sum_{a=0}^{m-1}s_aH_{a,a-c},
\qquad
\alpha_s=
\sqrt{\frac{n!}{\prod_a s_a!}}\,m^{(1-n)/2},
\tag{1}
\]
for \(Q(s)=c\neq0\), with indices modulo \(m\).

For completeness, the Fourier sum in the differentiated term is
\[
\sum_j\omega^{j(Q(s)+b-a)}
=m\,\mathbf 1_{\{b=a-c\}}.
\]
This proves (1) without a permanent identity or a finite computation.
Define the phase-free amplitude functional
\[
\ell_s(H)=\alpha_s\sum_a s_aH_{a,a-c}.
\tag{2}
\]

## Step 3: selected outcomes

Choose one representative
\[
c=1,\ldots,\left\lfloor\frac m2\right\rfloor
\]
from each pair of cyclic edge classes \(\{c,-c\}\).  For
\(2c\not\equiv0\pmod m\), select all \(m\) occupations
\[
s_{p,c}=(n-1)e_p+e_{p+c},\qquad p=0,\ldots,m-1.
\tag{3}
\]
Their charge is
\[
Q(s_{p,c})=(n-1)p+(p+c)=np+c\equiv c\pmod m,
\]
so they are dark.

The only self-conjugate class occurs when \(m\) is even and \(c=m/2\).
There select (3) only for \(p=0,\ldots,m/2-1\), one outcome per antipodal
mode pair.  Counting gives
\[
\begin{cases}
\frac{m-1}{2}m,&m\ \text{odd},\\[2mm]
(\frac m2-1)m+\frac m2,&m\ \text{even},
\end{cases}
=\frac{m(m-1)}2.
\]

## Step 4: invertibility of every cyclic block

Let \(\mathcal V_c\) be the Hermitian matrices supported on the undirected
edges \(\{a,a-c\}\).

If \(2c\not\equiv0\), the entries
\[
z_a=H_{a,a-c}\in\mathbb C,\qquad a=0,\ldots,m-1,
\]
are independent complex coordinates on \(\mathcal V_c\).  Equations
(2)--(3) give
\[
\frac{\ell_{p,c}(H)}{\alpha}
=(n-1)z_p+z_{p+c}.
\tag{4}
\]
In vector form this is \(((n-1)I+P_c)z\), where \(P_c\) is a unitary
permutation.  If this vector vanished, then
\[
(n-1)\|z\|=\|P_cz\|=\|z\|.
\]
Because \(n>2\), this forces \(z=0\).  The \(m\) complex functionals
\(\ell_{p,c}\) therefore span all \(2m\) real directions in
\(\mathcal V_c\).

If \(m\) is even and \(c=m/2\), put
\(z_p=H_{p,p+c}=x_p+iy_p\) for \(0\leq p<m/2\).  Hermiticity gives
\(H_{p+c,p}=z_p^*\), and hence
\[
\frac{\ell_{p,c}(H)}{\alpha}
=(n-1)z_p+z_p^*
=n x_p+i(n-2)y_p.
\tag{5}
\]
This is an invertible real map because \(n>2\).

The spaces \(\mathcal V_c\) are a direct-sum partition of all off-diagonal
Hermitian entries.  Equations (4)--(5) therefore prove that the selected
complex amplitude functionals have full real span.

## Step 5: two fixed probes recover both quadratures

Define the real complete-graph probe
\[
R_{ab}=1\quad(a\neq b),\qquad R_{aa}=0.
\]
Define an oriented-imaginary complete-graph probe \(T\) as follows.  For
every non-antipodal representative \(c<m/2\), set
\[
T_{a,a-c}=i,\qquad T_{a-c,a}=-i
\]
for every \(a\).  If \(m\) is even, orient each antipodal edge by
\[
T_{p,p+m/2}=i,\qquad T_{p+m/2,p}=-i,
\quad 0\leq p<m/2.
\]
Every undirected edge belongs to exactly one of these rules, so \(T\) is
well defined and Hermitian.

For every non-antipodal selected event,
\[
\ell_{p,c}(R)=\alpha n,\qquad
\ell_{p,c}(T)=i\alpha n.
\tag{6}
\]
For an antipodal selected event,
\[
\ell_{p,c}(R)=\alpha n,\qquad
\ell_{p,c}(T)=i\alpha(n-2).
\tag{7}
\]
Both references are nonzero and in phase quadrature.

For a nominally dark event, the calibrated signed-probe contrast has
limiting differential
\[
D C_{s,h}(0)[H]
=\operatorname{Re}\!\left[\ell_s(h)^*\ell_s(H)\right].
\tag{8}
\]
Equations (6)--(8) show that \(R\) and \(T\) separately extract nonzero
multiples of the real and imaginary parts of every selected functional.
Combining this with the block proof completes the rank theorem.

Analytic dependence on the probe angle implies that the same square
Jacobian remains nonsingular for all sufficiently small nonzero
\(\epsilon\), after subtracting the calibrated probe-only baseline.
This is the ordinary local inverse-function theorem; no global or
polynomial inverse is asserted.

## Minimality and conditioning

One dark outcome has one complex amplitude derivative and therefore supplies
at most two independent real limiting contrast rows, regardless of how many
probe directions are applied.  The construction uses exactly two rows for
each of \(m(m-1)/2\) outcomes, proving outcome minimality.  Its
\(m(m-1)\) scalar contrasts also attain the dimension bound.

The non-antipodal amplitude block \((n-1)I+P_c\) has singular values
\[
|n-1+\lambda|,\qquad |\lambda|=1,
\]
and hence condition number at most
\[
\frac n{n-2}.
\]
The antipodal amplitude block (5) has the same bound.  After dividing each
contrast by its known probe-reference magnitude, the complete block
construction inherits this bound in the natural cyclic-edge coordinates.
Without that calibration rescaling, the worst antipodal contrast block has
gain ratio \((n/(n-2))^2\).  These are deterministic local-Jacobian bounds,
not finite-shot guarantees in the presence of background or probe error.

At \(m=n=4\), the new construction uses six dark outcomes, twelve scalar
contrasts, and four settings.  Its normalized Jacobian bound is \(2\), while
the unnormalized gain bound is \(4\).  It uses fewer unique selected outcomes
than the earlier ad hoc \(F_4\) cat certificate and exposes the cyclic block
structure explicitly.

Four programmed settings therefore **suffice** for every \(m\).  We do not
claim that four settings are optimal among all conceivable protocols.
Within the present design, using the dimension-minimal number of outcomes
requires two independent real rows per outcome, which the two signed probe
directions supply.

There are two important scaling qualifications:

1. For every selected occupation, the omitted common normalization factor
   obeys
   \[
   \alpha^2
   =\frac{n!}{(n-1)!}\,m^{1-n}
   =n\,m^{1-n}.
   \]
   At \(n=m\), this common factor decays as \(m^{(2-m)/2}\), while individual
   gradient entries also carry the coefficients \(n-1\) or \(1\) in
   Eq. (4).  With the unnormalized dense probe \(R\), the leading probe-only
   probability is
   \(\epsilon^2\alpha^2n^2=\epsilon^2m^{4-m}\).  If \(R\) is divided by its
   operator norm \(m-1\), that probability instead scales asymptotically as
   \(\epsilon^2m^{2-m}\).  Full rank does not imply a mode-independent count
   budget.
2. The displayed \(R\) and \(T\) are dense probes.  Their Frobenius norms
   grow as \(\sqrt{m(m-1)}\), while \(\|R\|_{\rm op}=m-1\).  If hardware
   constrains the total generator norm, they must be rescaled with \(m\).
   Any nonzero known rescaling preserves rank but reduces contrast signal
   and changes the finite-angle validity range.

Accordingly, the condition-number statement is only about the calibrated
deterministic Jacobian after known row rescaling.  It is not a physical
Fisher-information or shot-efficiency bound: count rate, background, probe
normalization, and SPAM uncertainty all affect the latter.

## Reproducibility

Run

```bash
python3 scripts/certify_general_fourier_cat_tomography.py --max-modes 9
python3 scripts/certify_general_fourier_cat_tomography.py \
  --max-modes 8 --photon-multiple 2
python3 scripts/certify_general_fourier_cat_tomography.py \
  --min-modes 2 --max-modes 2 --photon-multiple 2
```

The program constructs the full contrast matrix directly in the standard
\(X_{ab},Y_{ab}\) coordinate basis using Gaussian-integer pairs and performs
exact rational elimination.  It also asserts the charge of every selected
outcome and the closed-form probe references (6)--(7).

## What this does and does not solve

This theorem directly removes the manuscript's former \(F_4\)-only
generality ceiling for the *identification framework*.  It does not
generalize the separate sectorwise-reciprocity theorem, and it should not be
presented as doing so.

The mathematical construction assumes:

- an ideal coherent \(n\)-photon Fourier cat with a calibrated relative
  phase;
- a known nominal \(F_m\);
- calibrated signed output probes;
- coherent lossless errors restricted to off-diagonal Hermitian directions;
- local estimation near the nominal device.

Loss, partial distinguishability, source contamination, detector
backgrounds, diagonal phase estimation, and global aliases remain separate
problems.  In particular, scaling the photon number with the mode count is a
strong experimental resource requirement even though the theorem scales
algebraically.

Unknown phases in the cat preparation are especially important: they provide
the input-side phase reference and can be locally confounded with coherent
device parameters.  A practical protocol must either calibrate those phases
independently or enlarge the Jacobian and likelihood to include
state-preparation and measurement (SPAM) parameters.  The theorem proves
device identifiability only under the stated calibrated-input assumption.
