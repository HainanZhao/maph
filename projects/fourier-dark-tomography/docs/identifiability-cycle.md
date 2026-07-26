# Research cycle: identifiability from multiphoton dark events

Date: 2026-07-26

## Motivation and revised thesis

The original manuscript studied directional response jets of selected
suppressed events in \(F_4\).  That establishes exact event-level structure,
but it does not by itself supply a broadly useful inference task.  The
revised thesis is:

> A calibrated signed displacement turns a multiphoton dark event into a
> phase-sensitive local measurement of coherent interferometer error.  The
> accessible rank is controlled jointly by the dark-event amplitude
> derivatives and the phase reference in the input.  Number-state inputs
> have an exact gauge obstruction; a coherent Fourier-cat input removes it.

The theory of the measurement and the propagation of internal coherent
errors is valid for arbitrary passive multiports.  \(F_4\) is used for exact,
finite, information-minimal certificates.

## Claim ledger

Claims below are separated into proved statements, exact finite
certificates, and open experimental questions.

### Proved statements

1. **Unprobed null-count no-go.**  If a target amplitude is dark at the
   nominal device, its probability has zero first derivative.  Its quadratic
   jet cannot recover the sign of a small coherent error.  This rules out a
   regular \(C^1\) or locally Lipschitz inverse at the null, but zero Jacobian
   alone does not rule out a nonregular higher-order inverse.

2. **Signed-probe differential.**  Let
   \[
   p_{e,h}^{\pm}(\theta,\epsilon)=
   |\langle s_e|e^{\pm i\epsilon\widehat H_h}
   e^{i\widehat H(\theta)}U_0|r_e\rangle|^2
   \]
   for an event dark at \(\theta=0\).  After subtracting the calibrated
   probe-only baseline,
   \[
   D_\theta C_{e,h}(0,\epsilon)[\delta]
   =\operatorname{Re}\!\left[
   (\ell_e h)^*(\ell_e\delta)\right]+O(\epsilon^2),
   \]
   where \(\ell_e\delta=\langle s_e|\widehat H(\delta)U_0|r_e\rangle\).
   Full column rank of these limiting rows implies full column rank, and
   hence a local differentiable left inverse on the chosen parameter slice,
   for every sufficiently small nonzero probe angle.

   This conclusion uses the standard local inverse-function theorem, not the
   algebraic-geometric Jacobian conjecture.  The latter asks whether a
   polynomial self-map with constant nonzero Jacobian determinant has a
   global polynomial inverse.  Our contrast map need not be polynomial, its
   determinant is checked at one operating point, and the conclusion is only
   local.  Global injectivity is neither assumed nor claimed.

3. **Two-real-row event bound.**  For one dark event, every limiting
   signed-probe row lies in
   \(\operatorname{span}_{\mathbb R}\{\operatorname{Re}\ell_e,
   \operatorname{Im}\ell_e\}\).  One event therefore supplies at most two
   independent real first-order measurements.

4. **Exact Fock-input gauge.**  Number-state preparation and counting are
   invariant under input and output diagonal phases.  At \(F_4\), the
   transported traceless input-diagonal generators
   \(F_4DF_4^\dagger\) form a three-dimensional subspace inside the twelve
   off-diagonal \(X/Y\) coordinates.  They remain invisible after any known
   output analyzer.  Therefore no such Fock-input protocol identifies all
   twelve coordinates.

5. **Internal-error propagation.**  If \(U_0=U_LU_R\), then
   \[
   U_Le^{i\epsilon H}U_R
   =e^{i\epsilon U_LHU_L^\dagger}U_0.
   \]
   For several small component errors, the first-order effective output
   generator is
   \[
   H_{\rm eff}=\sum_\ell U_{>\ell}H_\ell U_{>\ell}^\dagger.
   \]
   Thus output-generator identification applies to arbitrary internal
   coherent lossless errors.  Locating faulty components additionally
   requires the circuit Jacobian and need not be unique.

6. **Known Fourier-cat dark sectors (recalled for the construction).**  For
   \(F_m(k,j)=m^{-1/2}\omega^{kj}\) and
   \[
   |\Psi_\ell^{(m,n)}\rangle
   =m^{-1/2}\sum_{j=0}^{m-1}\omega^{-\ell j}|n e_j\rangle,
   \]
   the amplitude for output occupation \(s\) is
   \[
   \sqrt{\frac{n!}{\prod_k s_k!}}\,
   m^{(1-n)/2}\,
   \delta_{\sum_kks_k\,({\rm mod}\ m),\,\ell}.
   \]
   Every output outside one modular sector is exactly dark.  This statement
   holds for all \(m,n\geq1\); it is not an \(F_4\)-specific reciprocity
   claim.  The identity is not new: it is essentially Eqs. (18)--(20) of
   Vourdas and Dunningham, Phys. Rev. A 71, 013809 (2005), and is also
   contained in the later general symmetry framework of Dittel et al.

### Exact finite certificates

1. **Optimal Fock design.**  For input \((1,1,1,1)\), five dark outputs and
   nine signed contrasts attain rank nine.  Their common nullspace is exactly
   \[
   \begin{aligned}
   K_A&=X_{01}+X_{03}+X_{12}+X_{23},\\
   K_B&=Y_{01}-Y_{03}+Y_{12}+Y_{23},\\
   K_C&=X_{02}+X_{13}.
   \end{aligned}
   \]
   Five events and nine scalar contrasts are both minimal.

2. **Full-rank coherent design.**  The input
   \[
   |\Psi_{\rm cat}\rangle=
   (|4000\rangle+|0400\rangle+|0040\rangle+|0004\rangle)/2
   \]
   with signed probes
   \(H_X=X_{01}-X_{02}\) and \(H_Y=Y_{01}-Y_{02}\) gives a block-diagonal
   \(12\times12\) Jacobian from twelve selected dark outcomes.  Exact block
   determinants are
   \[
   \det J_X=-243/8,\qquad
   \det J_Y=729/32,
   \]
   so the full determinant is \(-177147/256\).  These are the
   \(\epsilon\to0\) Jacobian blocks of \(\Delta P/\epsilon\), not exact
   finite-angle Jacobians.  Continuity gives full rank for every sufficiently
   small nonzero calibrated probe angle after the probe-only baseline is
   subtracted.  Twelve scalar measurements attain the dimension lower bound.
   Since all selected outcomes are recorded in parallel, the construction
   uses four programmed settings: \(\pm H_X,\pm H_Y\).

3. **Conditioning.**  The presently selected physical Jacobian has raw
   spectral condition number approximately \(7.05\), row-normalized
   condition number \(4.86\), and ideal background-free Poisson-weighted
   condition number \(4.79\).  These are reproducible design diagnostics,
   not hardware-independent sample-complexity guarantees.

### Assumptions and boundaries

- The result is local around a calibrated nominal interferometer; it is not
  global unitary tomography.  The cat state can retain discrete global input
  phase aliases even though it removes the three continuous blind directions
  in the chosen local model.
- The identified parameter space contains the twelve off-diagonal
  \(X_{pq},Y_{pq}\) mode-mixing coordinates.  It does not include the three
  traceless output-diagonal generators, whose first-order dark-event
  amplitude is zero in the unshifted counting basis.
- The signed probes and the coherent input phase must themselves be
  calibrated.  Unknown state-preparation and probe errors enlarge the
  parameter model.
- The exact theorems concern coherent, lossless evolution.  Loss, partial
  distinguishability, source contamination, and detector backgrounds require
  a joint likelihood model.
- The four-photon cat input is a stronger and experimentally harder resource
  than \(|1,1,1,1\rangle\).  The rank-nine Fock protocol is the conservative
  near-term design; the cat protocol is the complete-identifiability
  benchmark.
- Two combined probes suffice for the displayed cat design.  No theorem yet
  proves that one arbitrary combined probe is impossible, so two-probe
  minimality must not be claimed.
- The general calibrated-displacement principle has prior art in
  displaced-null estimation, and the Fourier-cat modular selection rule is
  also known.  The defensible contribution is the exact Fock-input gauge
  theorem, explicit optimal \(F_4\) certificates, and the
  coherent-resource separation.

## Next verification steps

1. Replace all floating complex arithmetic and rounding in the search code
   with Gaussian-integer pairs and rational arithmetic.
2. Assert every displayed Jacobian entry and determinant in automated tests.
3. Give complete human-readable proofs of every unbounded theorem in the main
   paper or its appendices; use code only for finite certificates.
4. Derive finite-angle bias bounds and a multinomial/Fisher-information
   analysis including a background floor.
5. Run an adversarial proof audit and a targeted prior-art audit.
6. Reframe the paper around identifiability; retain \(F_4\) reciprocity as a
   secondary structural result rather than the main generality claim.

## Candidate scalable theorem under independent audit

The following extension was derived after the original \(F_4\) certificate
and is being independently checked before promotion to a theorem in the
paper.

Let \(m\mid n\), \(n>2\), and use the known charge-zero Fourier cat
\(|\Psi_0^{(m,n)}\rangle\).  Write an off-diagonal Hermitian generator as
\(G=(g_{pq})\).  For a dark output of charge \(c\),

\[
\langle s|\widehat G F_m|\Psi_0^{(m,n)}\rangle
=\alpha_s\sum_p s_p g_{p,p-c},
\qquad
\alpha_s=m^{(1-n)/2}\sqrt{\frac{n!}{\prod_ps_p!}}.
\]

Choose
\[
s_{p,c}=(n-1)e_p+e_{p+c}.
\]
It is dark because \(Q(s_{p,c})=np+c\equiv c\ne0\pmod m\), and its
gradient obeys
\[
L_{p,c}=(n-1)z_p+z_{p+c},
\qquad z_p=g_{p,p-c}.
\]
For a non-opposite cyclic distance, this is
\(((n-1)I+P_c)z\).  The matrix is invertible because
\(\|(n-1)z\|>\|P_cz\|\) for every nonzero \(z\), and its singular values
lie between \(n-2\) and \(n\).  Hermiticity makes the negative charge
redundant.

When \(m\) is even and \(c=m/2\), take one \(p\) from each opposite pair.
Then \(z_{p+c}=z_p^*\) and
\[
L_{p,c}=n\,\operatorname{Re}z_p
 i(n-2)\,\operatorname{Im}z_p,
\]
which is invertible because \(n>2\).  Signed \(X\)- and \(Y\)-probes on
the minority pair \((p,p+c)\) provide noncollinear reference amplitudes
and hence both real quadratures.

Taking one representative of every distance pair \(\{c,-c\}\) uses
exactly \(m(m-1)/2\) dark events and \(m(m-1)\) scalar differentials,
matching the dimension lower bounds for the full off-diagonal error
space and for a scheme in which one dark event supplies at most two
rows.  After calibration rescaling, the cyclic systems have condition
number at most \(n/(n-2)\).

If verified and absent from prior work, this theorem removes the
mathematical \(F_4\) limitation.  It does **not** by itself give an
efficient large-\(m\) experiment: for the displayed sparse outputs the
common gradient normalization is
\(\alpha_s^2=n\,m^{1-n}\).  The unnormalized dense probe supplies an
additional \(n^2\) factor, whereas operator-norm normalization removes a
factor asymptotic to \(m^2\).  Either convention gives a rapidly decaying
large-\(m\) count scale at the minimal choice \(n=m\).  Algebraic
scalability and shot efficiency must therefore be stated separately.
