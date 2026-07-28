# SIC--Stark research

This project investigates the Twisted Convolution Conjecture (TCC) in the
canonical rank-one family

\[
Q_d=\langle1,1-d,1\rangle,\qquad d\ge4,
\]

as a focused route toward Zauner's SIC-existence conjecture. It is a
research ledger and executable reduction. General TCC remains open; two
companion papers prove its formal dimension-four, five, seven, and eight
instances unconditionally:

- [Paper I source](paper/sic-stark-dimensions-four-five.tex) and
  [PDF](paper/sic-stark-dimensions-four-five.pdf): dimensions four and
  five;
- [Paper II source](paper/sic-stark-dimensions-seven-eight.tex) and
  [PDF](paper/sic-stark-dimensions-seven-eight.pdf): dimensions seven
  and eight.

The dimension-six orientation problem remains open. The longer research
ledger in `docs/` records that boundary and the exploratory work behind
the proved cases.

## Publication and archival upload checklist

The recommended Zenodo deposit is a common project release with two
submission-specific reproducibility archives and the two compiled PDFs as
separate convenient downloads. Do not upload only the PDFs: both theorems
depend on exact or interval certificates that must remain available with
their generating scripts.

Build both deterministic companion archives in one command:

```bash
scripts/build_companion_archives.sh
```

This creates `dist/sic-stark-paper-I.tar.gz` and
`dist/sic-stark-paper-II.tar.gz`. Their exact contents are documented in
`publication/paper-I-README.md` and `publication/paper-II-README.md`.

### Required standalone uploads

- `paper/sic-stark-dimensions-four-five.pdf`
- `paper/sic-stark-dimensions-seven-eight.pdf`

### Required contents of the reproducibility archive

Manuscript and package guide:

- `README.md`
- `paper/sic-stark-dimensions-four-five.tex`
- `paper/sic-stark-dimensions-four-five.pdf`
- `docs/referee-package.md`
- `certificates/SHA256SUMS`
- `scripts/build_publication_archive.sh`

Dimension-four certificates:

- `certificates/dimension-four-certificate.json`
- `certificates/pari-audit.txt`
- `certificates/double-sine-audit.txt`
- `scripts/generate_referee_certificates.py`
- `scripts/verify_referee_certificate.py`
- `scripts/referee_pari_audit.gp`
- `scripts/explore_dimension_four_double_sine.py`

Dimension-five certificates:

- `certificates/dimension-five-bridge.json`
- `certificates/dimension-five-character-support.json`
- `certificates/dimension-five-finite.json`
- `certificates/dimension-five-exact-minors.txt`
- `certificates/dimension-five-pari.txt`
- `certificates/dimension-five-root-isolation.txt`
- `certificates/dimension-five-embedding-certificate.txt`
- `certificates/dimension-five-local-isolation.txt`
- `certificates/dimension-five-shintani.txt`
- `certificates/dimension-five-unit-lattice.txt`
- `certificates/dimension-five-double-sine-intervals.txt`

Dimension-five generating and verification code:

- `scripts/analyze_dimension_five_character.py`
- `scripts/analyze_dimension_five_finite.py`
- `scripts/generate_dimension_five_bridge.py`
- `scripts/dimension_five_pari_audit.gp`
- `scripts/dimension_five_root_isolation.gp`
- `scripts/dimension_five_embedding_certificate.gp`
- `scripts/dimension_five_local_isolation.gp`
- `scripts/dimension_five_shintani_audit.gp`
- `scripts/dimension_five_special_reduction_audit.gp`
- `scripts/dimension_five_unit_lattice_audit.gp`
- `scripts/certify_dimension_five_double_sine.py`
- `scripts/verify_dimension_five_conjugates.gp`

Shared implementation and regression tests:

- `src/`
- `tests/`

The dimension-eight CM-descent material is not needed to verify Paper I.
It belongs in the separate Paper II archive:

- `docs/sic-stark-dimension-eight-cm-descent.md`
- `docs/sic-stark-dimension-eight-canonical-closure.md`
- `scripts/dimension_eight_cm_descent.gp`
- `scripts/dimension_eight_linear_cm_reinduction.gp`
- `scripts/dimension_eight_cm_unit_lattice.gp`
- `scripts/certify_dimension_eight_cm_orientation.py`
- `scripts/dimension_eight_cm_real_unit_bridge.gp`
- `scripts/dimension_eight_maximal_tuple_audit.gp`
- `scripts/dimension_eight_maximal_quadratic_units.gp`
- `scripts/certify_dimension_eight_maximal_cocycle.py`
- `scripts/dimension_eight_maximal_exact_tcc.py`
- `certificates/dimension-eight-cm-descent.txt`
- the dimension-six and dimension-eight scripts cited explicitly in
  Section 7 of the manuscript

### Release metadata

The tagged archive contains:

- `CITATION.cff`, with the author, title, and release version;
- `.zenodo.json`, with matching creator and license metadata;
- `LICENSE` (CC BY 4.0 for manuscripts/documentation) and
  `LICENSE-CODE` (MIT for code);
- a pinned Python environment or lock file recording Python 3.12.3,
  python-flint 0.9.0, FLINT 3.6.0, and the required NumPy version;
- a short `REPRODUCE.md` containing the exact commands and expected
  runtimes; and
- the final successful test transcript.

After deposition, the only remaining metadata step is to insert the
Zenodo DOI and immutable Git commit in the manuscripts, citation
metadata, and this README.

Build the complete archive in one command:

```bash
scripts/build_publication_archive.sh
```

The default output is
`dist/sic-stark-reproducibility.tar.gz`.  The builder first verifies
`certificates/SHA256SUMS`, discovers the dimension-six/eight scripts cited
by the manuscript, normalizes tar metadata for reproducible output, and
adds `ARCHIVE_CONTENTS.sha256` inside the archive.  Use
`--strict-release-metadata` for the final deposit; it will refuse to build
until the citation, Zenodo, license, environment, and reproduction files
listed above exist.  Useful alternatives are:

```bash
scripts/build_publication_archive.sh --list
scripts/build_publication_archive.sh --core-only
scripts/build_publication_archive.sh --output /path/to/release.tar.gz
```

## Current result

The canonical arithmetic, Weyl--Heisenberg diagnostics, and finite twisted
convolution are implemented exactly or to controlled floating-point
precision. Research cycles 2--15 additionally:

- proves from the source's conjugation involution that rank-one shifts
  \(0\) and \(1\) occur together;
- reduces the \(L_d^3\) Jacobi cocycle to three copies of the universal
  \(S\)-kernel;
- proves the Shintani--Faddeev values and canonical phase kernel are
  invariant under Zauner action, giving an exact threefold reduction of the
  TCC equations;
- identifies the zero-output equation as an automatic consequence of the
  cocycle inverse law;
- rewrites every remaining equation as a distinguished finite symplectic
  Fourier coefficient;
- expands the first primitive quotient into three \(S\)-kernel ratios and
  explicit finite q-Pochhammer corrections;
- gives an exact countermodel proving that covariance, reciprocal pairing,
  and cyclic telescoping alone cannot imply TCC;
- embeds every TCC special value exactly into the general modular gamma
  function and matches the dimension-four beta-integral phase;
- closes the standard pentagon/localization route by proving that every
  desired characteristic sample lies strictly inside the resulting
  two-gamma kernel's pole-free strip;
- computes the exact local ray-unit action on TCC characteristics and
  proves that it moves the output direction together with the summation
  variable;
- shows already in dimension four that the additive TCC phase does not
  descend to a fixed-direction ray-class character, so character
  resolvents decompose the full residual vector rather than force a
  primitive coefficient to vanish;
- constructs the complete dimension-four ray-unit residual packet,
  decomposes its regular \(C_2^2\) representation into all four
  characters, and finds its first degree-five and degree-six relations;
- gives a faithful, totally positive algebraic-unit countermodel in
  \(\mathbb Q(\sqrt2,\sqrt3)\) whose residual packet and every character
  projection are nonzero;
- specializes the published conductor-lowering theorem to exact
  same-grid distribution products and shows that prime dimensions have
  no proper scalar relation;
- constructs a two-parameter multiplicative perturbation preserving all
  published within-level multiplicative identities while forcing a
  nonzero primitive Laurent coefficient;
- proves that fractional \(q\)-Pochhammer cell elimination gives only
  pure-gauge flatness, while the natural bilinear Hirota determinant
  already fails in its first formal coefficient;
- classifies the RM Floquet evolution as diagonal or
  weighted-permutation, proves that the formal deformation lifts to it,
  and rewrites TCC as a twisted trace of the multiplicative commutator
  between RM monodromy and characteristic translation;
- constructs an explicit all-parity finite Zak/Weyl representation of
  the TCC cocycle and converts the conjecture into a
  deformation-sensitive \(d\times d\) RM matrix-inverse identity.
- uses fixed-point reflection, with its exceptional zero characteristic,
  to reduce that inverse identity to a single normalized involution
  \(H^2=I\), proves \(\operatorname{Tr}H=2-d\), and identifies this
  remaining target with ghost-projector idempotency;
- proves that Zauner block diagonalization gives no reduction beyond the
  existing orbit count, and isolates the off-grid
  \(1-\widetilde q^nq^m\) factor that a boundary-limit proof must retain.
- aligns the new cyclic-quantum-dilogarithm approximants with the
  canonical threefold level step and proves that their safe
  subsequences retain the off-grid factor;
- proves that reciprocity already forces the first two trace moments
  and constructs an ordinary-Hermitian, Zauner-invariant exact
  countermodel having those moments but failing idempotency;
- matches a new quotient--Fourier quantum-dilogarithm identity to the
  TCC sum and isolates its zero-characteristic and \(3\mid d\)
  obstructions.
- converts TCC into the rank-one determinantal equations for one
  scalar-shifted RM Zak matrix and writes every \(2\times2\) minor as
  an explicit sheared partial-Fourier exchange identity.
- compresses the complete minor system to one nonnegative
  exterior-square scalar, gives its exact partial-Fourier
  sum-of-squares form, and separates this fourth positive moment from
  the already-forced algebraic trace moments.
- uses parity-Hermiticity to turn that certificate into the polynomial
  saturation \(\operatorname{Tr}(PG)^4=(\operatorname{Tr}(PG)^2)^2\),
  proves the sharp reciprocal lower bound on the quadratic norm, and
  shows the constant-overlap countermodel attains the bound without
  satisfying the fourth moment.
- separates the published Bos--Waldron holomorphic quartic from the
  positive RM quartic and gives an exact parity-Hermitian, full-rank
  dimension-four countermodel satisfying the first, second, and
  fourth algebraic power-trace equations.
- finds that all 36 dimension-four ghost minors share the single
  double-sine factor
  \(x^2-\sqrt{3+\sqrt5}\,x+1\), reducing dimension-four TCC to one
  explicit quarter-period special-value identity.
- identifies that special value with a modulus-four Shintani ray-class
  invariant, gives its exact reciprocal degree-eight target polynomial,
  and isolates the remaining algebraicity/class-polynomial step.
- computes the modulus-four ray group as order two and matches it to
  the quadratic polynomial of the Stark invariant \(x^2\), explaining
  the quartic for the cocycle square root \(x\).
- identifies the full ray field as
  \(\mathbb Q(\sqrt5,\sqrt\phi)\) and the target Stark unit as
  \(\phi+\sqrt\phi\), leaving only its analytic partial-zeta evaluation.
- replaces that direct special-function evaluation by a relative
  class-number calculation: \(D_L=400\), \(h_L=1\), and the visible
  regulator gives the required logarithm once two finite checks pass.
- closes those checks, proves the fundamental-unit and normalization
  statements, and obtains an exact dimension-four TCC theorem.

See [`docs/sic-stark-sprint1.md`](docs/sic-stark-sprint1.md) and
[`docs/sic-stark-cycle2.md`](docs/sic-stark-cycle2.md), followed by
[`docs/sic-stark-cycle3.md`](docs/sic-stark-cycle3.md) and
[`docs/sic-stark-cycle4.md`](docs/sic-stark-cycle4.md), then
[`docs/sic-stark-cycle5.md`](docs/sic-stark-cycle5.md) and
[`docs/sic-stark-cycle6.md`](docs/sic-stark-cycle6.md), and finally
[`docs/sic-stark-cycle7.md`](docs/sic-stark-cycle7.md) and
[`docs/sic-stark-cycle8.md`](docs/sic-stark-cycle8.md), followed by
[`docs/sic-stark-cycle9.md`](docs/sic-stark-cycle9.md) and
[`docs/sic-stark-cycle10.md`](docs/sic-stark-cycle10.md), and finally
[`docs/sic-stark-cycle11.md`](docs/sic-stark-cycle11.md) and
[`docs/sic-stark-cycle12.md`](docs/sic-stark-cycle12.md), followed by
[`docs/sic-stark-cycle13.md`](docs/sic-stark-cycle13.md) and
[`docs/sic-stark-cycle14.md`](docs/sic-stark-cycle14.md), and finally
[`docs/sic-stark-cycle15.md`](docs/sic-stark-cycle15.md) and
[`docs/sic-stark-cycle16.md`](docs/sic-stark-cycle16.md), followed by
[`docs/sic-stark-cycle17.md`](docs/sic-stark-cycle17.md) and
[`docs/sic-stark-cycle18.md`](docs/sic-stark-cycle18.md), and finally
[`docs/sic-stark-cycle19.md`](docs/sic-stark-cycle19.md), followed by
[`docs/sic-stark-cycle20.md`](docs/sic-stark-cycle20.md) and
[`docs/sic-stark-cycle21.md`](docs/sic-stark-cycle21.md), followed by
[`docs/sic-stark-cycle22.md`](docs/sic-stark-cycle22.md) and
[`docs/sic-stark-cycle23.md`](docs/sic-stark-cycle23.md), followed by
[`docs/sic-stark-cycle24.md`](docs/sic-stark-cycle24.md), for the claim ledger.

## Higher-dimensional status

The later research ledger now separates the first dimensions beyond
the closed \(d=4\) case:

- dimension five has an unconditional algebraic closure package;
- dimension six has a genuine primitive-character obstruction to the
  currently available conductor-lowering argument; and
- dimension seven has a complete unconditional analytic and exact
  finite closure; while
- dimension eight is now closed unconditionally in both admissible
  strata: the conductor-three/discriminant-45 packet by linear CM
  reinduction, and the maximal-order/discriminant-five packet by
  quadratic ray units and an exact six-factor phase audit.

The dimension-seven derivation, including the exact \(\Upsilon\) labels,
six lowered moduli, stabilizer, Kopp exponents, and the \(3.5\cdot10^{-9}\)
full-packet audit, is in
[`docs/sic-stark-cycle46.md`](docs/sic-stark-cycle46.md).  Cycles
[`47`](docs/sic-stark-cycle47.md) through
[`56`](docs/sic-stark-cycle56.md) subsequently derive the exact phase
\(\phi_p=\zeta_{56}^{7-32Q(p)}\), construct the complete complex
characteristic packet, identify all six exact ray fields, recognize small
reciprocal unit polynomials, reduce the packet to eight variables, and audit
both formal shifts.  [Cycle 57](docs/sic-stark-cycle57.md) then isolates all
sixteen squared-overlap roots, finds the safe Shintani exponent \(16128\),
certifies the Artin labels, collapses the signed overlap algebra and
\(\zeta_{56}\) into one degree-\(48\) field, selects that compositum by an
exact real-cyclotomic intersection identity, verifies the labeled
ray-field isomorphism over \(\mathbf Q(\sqrt2)\), and proves exactly all
\(441\) rank-two minors for each of the two formal shifts.  The
adversarial source and field-gluing audit, including the corrected
Shintani unit-congruence factors, is recorded in
[Cycle 58](docs/sic-stark-cycle58.md).

[Cycle 59](docs/sic-stark-cycle59.md) applies the resulting theorem schema
to dimension eight.  The finite TCC equations select one of the \(64\)
natural quartic orientation pairs.  The \(16\) primitive squared overlaps
collapse to the degree-\(32\) one-place ray field and acquire exact Artin
labels; adjoining one square root contains every signed primitive overlap
and the lower-conductor field.  In a compatible degree-\(128\) Weyl-phase
compositum, exact arithmetic proves idempotency and all \(784\) rank-two
minors for each formal shift.  This closes the finite algebraic gate but
does not promote Roblot's quartic absolute-value theorem to the two
oriented analytic identities.

[Cycle 60](docs/sic-stark-cycle60.md) closes the entire lower-conductor
dimension-eight stratum unconditionally.  Its degree-eight field is the
one-place ray-\(12\) field, has Shintani index two and safe exponent \(576\),
and Arb/height rigidity proves all fifteen lower entries.  Rigorous Arb
windows also isolate the primitive values, leaving precisely two oriented
cyclic-quartic identities—or an index-four powered-algebraicity
refinement—as the remaining analytic theorem.

[Cycle 61](docs/sic-stark-cycle61.md) performs the direct Shintani-cone
fail-fast test on those two identities.  Kopp's exact telescoping formula
does preserve the analytic orientation, but its quartic Fourier transform
does not identify the result with the explicit unit resolvent.  The two
phase quotients are numerically \(1\) to roughly \(10^{-114}\), while the
proved input gives only unit modulus.  This isolates an oriented
cyclic-quartic Stark identity—not an unfinished cone calculation—as the
precise remaining theorem.

[Cycles 72–81](docs/sic-stark-cycle72.md) revisit the proposed CM descent
without assuming that projective equivalence is enough.  Exact
degree-sixteen character calculations prove genuine linear reinduction
from both \(\mathbf Q(\sqrt{-6})\) and
\(\mathbf Q(\sqrt{-30})\).  Over the former base, Stark's proved
imaginary-quadratic rank-one theorem supplies an oriented unit
resolvent; Arb balls isolate its integral unit coordinates, and exact
normal-closure identities identify its absolute norms with the original
real-quadratic Roblot units.  This closes both formerly missing quartic
orientations and hence the canonical conductor-three dimension-eight
packet unconditionally.  The consolidated statement and reproduction
commands are in
[`docs/sic-stark-dimension-eight-canonical-closure.md`](docs/sic-stark-dimension-eight-canonical-closure.md).

[Cycles 82–92](docs/sic-stark-cycle82.md) resolve the separate
maximal-order discriminant-five stratum.  They identify the
\(C_2^2\) ray group and its two supported quadratic characters, prove
both associated regulator/unit formulas unconditionally, transcribe
the six-factor AFK continued-fraction cocycle, and compress the signed
packet to a degree-\(32\) quotient ring shared with
\(\mathbb Q(\zeta_{16})\).  Exact arithmetic proves all \(784\) minors
for each shift.  [Cycle 92](docs/sic-stark-cycle92.md) removes the
last numerical sign choice: every finite \(q\)-Pochhammer and
double-sine recurrence phase is reduced exactly in
\(\mathbb Q(\sqrt5)\), and all \(63\) resulting integral
\(\pi\)-phases reproduce the radical table.  Together with the
conductor-three result and form-class transport, this proves the
complete formal TCC in dimension eight.  The consolidated theorem and
reproduction commands are in
[`docs/sic-stark-dimension-eight-unconditional-closure.md`](docs/sic-stark-dimension-eight-unconditional-closure.md).

[Cycle 62](docs/sic-stark-cycle62.md) returns to dimension six and
classifies every quadratic induction base of its faithful dihedral
quotient.  The only abelian base is the original
\(\mathbf Q(\sqrt{21})\); the \(\mathbf Q(\sqrt{-3})\) and
\(\mathbf Q(\sqrt{-7})\) relative groups are nonabelian, ruling out a
hidden elliptic-unit transfer.  It identifies a uniform \(q\)-gamma
regularization at vanishing cyclic factors as the next concrete route to
a direct finite-level TCC identity.

[Cycle 63](docs/sic-stark-cycle63.md) derives that \(q\)-gamma correction.
For all nonzero singular characteristics, the numerator and denominator
parameters agree, so every fractional boundary order and gamma factor
cancels.  Including the residual modular-scale factor and the
Möbius-curvature dilogarithmic phase gives complete rational-boundary
tables.  Their imaginary parts, idempotency defects, and rank-two minors
all decrease along the modular geodesic, validly reopening a direct
cyclic-limit proof of dimension-six TCC.

[Cycles 64--68](docs/sic-stark-cycle68.md) correct and sharpen the
dimension-six boundary analysis.  Even-dimensional wrap signs leave
thirteen signed Zauner defect representatives, and the moving
characteristic contributes an Euler--Maclaurin half-power that was
invisible in the first symmetric validation.  With it restored, the
idempotency defect decays as the square of the convergent denominator
and the normalized first-derivative packet stabilizes.  The remaining
target is a local fixed-point divisibility lemma for
\(K_6(\tau)^2-K_6(\tau)\).

[Cycles 69--71](docs/sic-stark-cycle71.md) prove that this local
fixed-point lemma is equivalent to the missing constant-term identity
and state the final unconditional boundary.  All \(225\) finite minors,
the lower analytic stratum, the ray labels, and the orientation sign are
certified; the full theorem is equivalent to one positive modulus-six
Shintani--Stark value.

[Cycles 93--96](docs/sic-stark-cycle93.md) test four new routes against
that boundary.  CM cyclic-sextic Brumer--Stark is excluded by the
ray-field signature \((6,3)\), and the published
\(\mathbb Q(\sqrt{21})\) algebraic double-sine formula is the already-used
level-three stratum.  Exact rational-character linear algebra proves
that rational Artin induction sees only the inversion-even primitive
packet.  The final cycle identifies the primitive Hecke \(L\)-function
exactly with the level-\(756\), nebentypus-\(-7\), projective-\(D_{12}\)
weight-one newform through the Sturm bound \(144\).  This is a new
modular formulation of the remaining oriented regulator identity, not
yet an unconditional evaluation of it.

[Cycle 97](docs/sic-stark-cycle97.md) checks the closest modern modular
Stark theorems.  The proved real-dihedral derived-Hecke formula concerns
the adjoint representation and a totally odd quotient character; the
dimension-six target is the original mixed-signature representation.
Harmonic-Maass results likewise do not provide the required
composite-level mixed-signature algebraicity theorem.  This isolates a
new mixed-signature, non-adjoint regulator formula as the precise modular
extension that would finish the proof.

## Verification

The default tests use Python, NumPy, and PARI/GP.  The rigorous
double-sine enclosure additionally uses `python-flint`.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/analyze_sic_canonical_family.py --stop 20
python3 scripts/verify_sic_fiducials.py --dimension 4 --show-residuals
python3 scripts/explore_dimension_four_double_sine.py
python3 scripts/verify_dimension_seven_conductor_lowering.py
gp -q scripts/dimension_seven_shintani_audit.gp
gp -q scripts/dimension_seven_artin_labels.gp
gp -q scripts/dimension_seven_exact_tcc.gp
gp -q scripts/dimension_eight_artin_labels.gp
gp -q scripts/dimension_eight_lower_shintani_audit.gp
gp -q scripts/dimension_eight_exact_tcc.gp
gp -q scripts/dimension_eight_maximal_tuple_audit.gp
gp -q scripts/dimension_eight_maximal_quadratic_units.gp
PYTHONPATH=scripts python3 scripts/certify_dimension_eight_maximal_cocycle.py
python3 scripts/dimension_eight_maximal_sign_audit.py
python3 scripts/dimension_eight_maximal_exact_tcc.py
python3 scripts/dimension_six_rational_induction_gate.py
gp -q scripts/dimension_six_weight_one_modularity.gp
```
