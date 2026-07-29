# SIC--Stark program status as of 2026-07-29

Date: 2026-07-29

## Proved dimensions

Unconditional formal TCC identities are proved in four dimensions,
with the following exact scope:

- **Dimension 4** (Paper I): boundary value \(\log u\) via the class
  number formula, fused packet at \(-q\), exact two-base calibration.
- **Dimension 5** (Paper I): fused at \(+q\) at the closed locus, lens
  level 15, alias sign bit 0, independently proved algebraic packet.
- **Dimension 7, discriminant 32** (Paper II): exact packet
  certificate, phase audit, symbolic reduction, and both TCC shifts.
  The distinct admissible discriminant-8 stratum remains open.
- **Dimension 8** (Paper II): CM orientation certified, maximal cocycle
  certified, lower conductor certified, primitive windows certified,
  unconditional closure.

Companion papers compiled:

- Paper I: `paper/sic-stark-dimensions-four-five.{tex,pdf}`
- Paper II: `paper/sic-stark-dimensions-seven-eight.{tex,pdf}`

## Dimension six: stopped at a formulation gap

The remaining open case. The exact downstream argument had been
presented as conditional on one analytic lemma:

> **MFC\(_6\).** The primitive order-six logarithmic spectral resolvent,
> defined by any admissible tilted contour in the pole-free strip and
> with its branch continued from the two-base chamber, has a finite
> limit along the attracting \(A_6\)-axis, and spectral periodization
> commutes in that component with trace-five base fusion, preserving
> the norm-37 Frobenius/lens label.

Everything after a correctly identified MFC\(_6\) input is exact and
verified: the multiplier ledger (all 36 comparisons), the conditional
implication to both TCC shifts and form transport, the Grade-2
equivalence at the rigid endpoint, and the analytic-to-Stark bridge.
Cycle 157 found, however, that the current text never defines the map
from the 36 additive spectral coefficients to the three logarithmic
ray-class values \(\mathscr P_j\). MFC\(_6\) is therefore not
operationally testable from the present definition of “spectral
periodization.”

The standalone boundary estimate BF\(_6(\eta)\) is written without SIC,
TCC, ray-class, or Stark notation in
`docs/dimension-six-standalone-estimate.md`. It states
\[
 |\mathscr S_{a,b,r}(s)-\mathscr S^{\rm fus}_{a,b,r}|
 \le C|t(\gamma(s))|^\eta
\]
uniformly over the thirty growing modes. A Dini modulus would suffice.
The formerly claimed implication BF\(_6(\eta)\Rightarrow\)MFC\(_6\) is
withdrawn. Cycle 156 found adverse numerical behavior for the raw
componentwise packets. Cycle 157 then showed that those packets omit
the ordinary Fourier gauge, while the correctly gauged additive
coefficient also grows strongly on the tested ladder. BF\(_6\), as
written, is retired.

Paper III remains a research draft and requires this formulation gap to
be repaired before it is publication-ready:
`paper/sic-stark-dimension-six-boundary-fusion.{tex,pdf}`.

## Latest completed cycles

### Cycle 160: dimension-seven scope correction

The Cycle-158 replay correctly verified the discriminant-32 packet but
incorrectly promoted covariance within that discriminant to all
dimension-seven admissible forms. Admissibility permits conductors one
and two, hence discriminants 8 and 32. Paper II is rescoped to the
proved discriminant-32 stratum; discriminant 8 is an explicit open
target. The Cycle-158 universal scope verdict is withdrawn.

### Cycle 154: factorized conditioning

### Conditioning measurement

The factorized q-Pochhammer continuation exhibits essential exponential
conditioning in \(1/s\) in both dimensions:
\[
 \log_{10}C_6(s)=2.8040\,s^{-1}-14.900,\quad R^2=0.999996,
\]
\[
 \log_{10}C_4(s)=0.6436\,s^{-1}-17.028,\quad R^2=0.999933.
\]
The dimension-six slope is \(4.35669\) times the dimension-four slope.
Since dimension four is proved and exhibits the same pathology, the
conditioning is an artifact of the factorized-continuation
implementation, not an intrinsic exponent of the open estimate.

### Cycle 154: Fresnel versus arithmetic strata

The 36 alias packets split into 6 Fresnel/oscillatory modes
(\(4b-5a\equiv0\pmod6\)) and 30 one-sided-growing modes. The six
Fresnel modes coincide exactly with the six q-gamma singular-cancellation
patterns. They do not coincide with the conductor-lowered arithmetic
stratum: only one of the three proved modulus-three orbit points is
Fresnel. The analytic wall is organized by Fourier direction, not by
conductor.

### Cycle 154: Grade-2 conservation

At the rigid endpoint, fusion is Grade-2 reduction-equivalent to the
oriented regulator equality
\[
 L'_S(0,\chi_1)=r_0+\zeta_6 r_1+\zeta_6^2 r_2,
\]
using the proved quadratic component, reciprocity, exact \(C_6\) Fourier
inversion, shift/reflection/duplication, conductor lowering, and the
multiplier ledger. The full MFC\(_6\) remains strictly stronger.

### Cycle 155: central tilted integral

The sinh-integral representation of each central lens kernel is
uniformly conditioned in both dimensions four and six.  It loses zero
digits down the tested geodesic ladders and converges essentially
linearly to its directly evaluated boundary value.  This removes the
cycle-154 q-Pochhammer conditioning artifact from the central integral.

This result does not include spectral periodization.

### Cycle 156: proved growing-component dissection

The cycle-156 repair separated the central kernel from its bilateral
helical alias packet and corrected the scope of
\(\psi^2(A_6)=-1\).  The exact multiplier belongs to the transported
Kopp/AFK cocycle, not to a raw fixed-label kernel ratio.

For the conductor-lowered growing mode \((a,b)=(0,2)\):

- the raw kernel reaches its direct boundary value with error
  \(1.14\times10^{-7}\) at \(s=8.54\times10^{-10}\);
- the telescoped alias ratio agrees with a direct neighboring-kernel
  quotient to \(48.16\) digits;
- every two-precision packet evaluation loses zero digits;
- nevertheless
  \(|\mathscr S_{0,2,0}|\) grows from \(4.783\) at \(1/s=64\) to
  \(9.962\) at \(1/s=4096\);
- the unweighted three-residue sum grows from \(3.630\) to \(185.415\)
  on the same endpoints.

Thus central-integral continuity does not control periodization.
Componentwise BF\(_6(\eta)\), in its current raw-packet form, is not
numerically supported.  Finite numerical growth is not a nonexistence
proof, and the weaker primitive-component MFC\(_6\) remains open.

### Cycle 157: Fourier normalization and stop decision

Equation (66) had extracted the constant phase
\[
 \exp(-\pi i\alpha Q/(24\omega_1)).
\]
The ordinary Fourier coefficient restores the inverse phase. At the
fused boundary this changes the alias scalar from \(-q\) to \(q^2\).
The weighted direct/telescoped ratios agree beyond 53 digits.

All aliases descend to one finite frequency \((a,b)\); the three
\(r\bmod3\) packets merely partition that coefficient and are not
three ray classes. The complete ordinary transformed values grow
\[
 |\widehat K_{0,2}|: 8.508\longrightarrow2053.313,\qquad
 |\widehat K_{0,1}|: 66.124\longrightarrow1248.365
\]
from \(1/s=64\) to \(4096\), with at least 31.34 digits of
two-precision agreement.

No repository artifact supplies the subsequent nonlinear map from the
36 additive coefficients to the three ray-class logarithms, including
branch and finite-part choices. The proved dimension-four and
dimension-five controls compute their alias sums and boundary overlaps
independently and do not supply that map. The present dimension-six
boundary-packet route is therefore stopped. This does not disprove the
dimension-six SIC claim; it retires an unsupported analytic
formulation.

## Verified facts inventory

Key verified results (full list in `docs/dimension-six-state-notes-v3.md`):

- \(A_6\beta_6=\beta_6\), \(\beta_6+\beta_6^{-1}=5\),
  \(\beta_6=[4;\overline{1,3}]\).
- \(A_6\equiv I\pmod6\), \(\psi^2(A_6)=-1\), all 36 multiplier
  comparisons.
- Small divisor: \(\|n\beta_6\|\ge(\sqrt{21}n+\tfrac12)^{-1}\).
- Zero-mode normalization: reciprocal roots \(-2\sqrt7\pm3\sqrt3\),
  trace \(-4\sqrt7\).
- Component split: 6 Fresnel + 30 growing modes.
- Admissible tilted contours agree by Cauchy in the pole-free strip.
- Interior identity verified as a meromorphic spectral identity.
- No finite pole pinch at \(g=Q\); endpoint failure is loss of decay at
  imaginary infinity.

## Excluded shortcuts

- Equal-base \({}_2\psi_2\) as interior representation (retired).
- Slater's strict bilateral annulus at the RM boundary.
- Absolute convergence of the undeformed vertical endpoint contour.
- Garoufalidis--Kashaev Theorem 1.1 for the general-\(A_6\),
  \(\mathbb Z/24\)-labeled kernel.
- Rational-root Nahm-sum boundary theorems at the quadratic irrational
  endpoint.

## Artifact inventory

- 139 Python/GP/shell scripts in `scripts/`.
- 40 Python test files in `tests/`.
- 172 Markdown research notes in `docs` (cycles 1--157 plus dimension-specific
  notes).
- 37 files in `certificates/` (JSON, TXT, SHA256SUMS).
- 4 compiled papers (4 tex + 4 pdf) in `paper/`.
- Deterministic companion archives buildable via
  `scripts/build_companion_archives.sh`.

## Next research plan

Stop direct work on the current dimension-six boundary-packet route.
Do not spend another cycle fitting or extending its numerical ladder.
Resume it only if an independent derivation supplies an explicit map
\[
 \{C_{a,b}\}_{(a,b)\in(\mathbb Z/6)^2}
 \longrightarrow
 (\mathscr P_0,\mathscr P_1,\mathscr P_2)
\]
with normalization, logarithm branches, finite-part prescription, and
identification with the AFK cocycle.

The next active work should divert to a bounded independent item:

1. the owed dimension-7 conductor-2 stratum; or
2. a new project/problem chosen independently of this failed analytic
   route.

The \(d=16\) Shintani hypothesis check remains excluded because
condition (0--9) fails.

## Tooling

- Python 3 with mpmath, sympy, numpy.
- PARI/GP available as `gp`.
- No sage, flint, or magma on this machine.
- Local `codex` CLI (codex-cli 0.145.0, model gpt-5.6-sol) for heavy
  derivation support.
