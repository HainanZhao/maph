# C74 problem-selection scratch

## Question

Which eligible open target now has the best short-horizon chance of a complete
proof or a durable scoped theorem, given the new C72 defect-six boundary?

## Question the questioning

The new Ryser theorem creates sunk-cost and vocabulary bias: a nearby (D=6)
model is easy to name but may merely start a defect ladder.  Conversely, a
small SAT verifier such as the (Q_7) square problem can look tractable while
hiding a hard symmetry-rich UNSAT certificate.  A very elementary statement
such as the regular-graph independent-domination inequality can also look easy
because its definitions are familiar, even when the missing exchange map is
the whole conjecture.  The real selection question is therefore not “which
instance is smallest?” or “which theorem is nearest?” but “which next exact
decision most sharply distinguishes a credible closing mechanism from a dead
end?”

## Initial brainstorm

1. **Regular-graph independent domination versus minimum maximal matching.**
   Seek an alternating-forest or charging map taking a minimum maximal matching
   to an independent dominating set of no larger size.  Falsifier: an exact
   regular graph with (i(G)>\mu^*(G)), or a local configuration defeating
   every proposed exchange rule.
2. **Ryser (r=6) after (D\ge6).**  Replace a defect ladder with a global
   dual certificate: distribute excess intersections over a minimum cover and
   prove either a five-blocker or a rigid (D=6) countermodel.  Falsifier: an
   exact (D=6) core surviving the new invariant.
3. **(\operatorname{ex}(Q_7,C_4)=304).**  Use symmetry-aware proof logging or
   a combinatorial compression, not bare ILP.  Falsifier: a verified 305-edge
   construction; failure gate: no compact upper-bound certificate after the
   calibrated first tranche.
4. **The (1/3\)–(2/3) poset conjecture.**  Search for a new injection or
   entropy argument on a structurally closed class rather than another finite
   census.  Falsifier: a poset outside the claimed class or an exact extension
   ratio outside the proposed interval.
5. **Fresh finite/extremal target from the current literature screen.**  Admit
   it only if its status is primary-source checked, it is outside OpenAI's
   official unit-distance and ten-Astra-result set, and its first rigorous gate
   tests a real proof mechanism.

Main rejected default: immediate (D=6) enumeration.  It is retained as a
candidate but not selected merely because C72 made it available.

Selection falsifier: if the chosen target lacks a precise current source, an
exact/rigorous first gate, or a credible bridge from that gate to a theorem,
the selection itself fails and Oracle must choose another candidate before
attack code is written.

## Eligibility and selection outcome

**Eligibility correction — OBSERVED.** The C74 screen missed Haonan Zhang,
*Proof of the Holevo-Utkin conjecture on sharp \(\ell_p\) norms for
zero-sum vectors*, arXiv:2605.05243v1 (4 May 2026). Its Theorem 2 proves the
Holevo--Utkin conjecture for every \(d\ge4\). The selected target was
therefore ineligible when chosen; C75 is an overlapping reconstruction, not
a result of this program. This correction supersedes the eligibility and
selection text below. The practical repair is to search exact statement
phrases and both citing/cited primary records, not only titles and authors,
before a future attack is authorized.

**Eligibility — OBSERVED.**  The primary source is Holevo--Utkin,
*A conjecture on a tight norm inequality in the finite-dimensional*
\(l_p\), arXiv:2603.24017v2 (9 April 2026; subsequently listed as
*Lobachevskii Journal of Mathematics* 47 (2026), 3300--3310).  Its stated
scope proves \(d=3\) and reports numerical checks through \(d=200\); it
does not claim the \(d=4\) theorem.  A title/author search on 5 August 2026
found no primary-source claim closing \(d=4\).  This is a bounded status
check, not proof of universal novelty.  It is not among the official
OpenAI/Astra or unit-distance exclusions recorded in the C74 preflight.

**Oracle selection — CONJECTURED planning decision.**  Select the
Holevo--Utkin conjecture in \(d=4\), with an exact KKT and
boundary-stratification engine.  For
\[
 L_4=\{x\in\mathbb R^4:\sum_i x_i=0\},\qquad \|x\|_2=1,
\]
the target is the asserted extremal value of
\(F_\alpha(x)=\sum_i|x_i|^{2\alpha}\): a maximum for \(\alpha\ge1\)
and a minimum for \(0<\alpha<1\), equal to the appropriate one of
\[
 A_\alpha=2^{1-\alpha},\qquad
 B_\alpha=4^{-\alpha}(3^\alpha+3^{1-\alpha}).
\]
The proposed equality families are, up to permutation and total sign,
\((2^{-1/2},-2^{-1/2},0,0)\) and
\((\sqrt{3/4},-1/\sqrt{12},-1/\sqrt{12},-1/\sqrt{12})\).

The source's multiplier equation has at most three coordinate values at an
interior critical point.  In dimension four that promises a finite list of
multiplicity/sign families, each reducible to a one-variable comparison.
The indispensable correction to that attractive story is that it does not
cover zero-coordinate strata, nonsmooth regimes, or the exact switch of
\(A_\alpha\) and \(B_\alpha\).  C75 must cover all of them.

**Alternatives rejected after independent comparison.**  Gupta's LEM
cycle-spectrum question is the strongest fallback: a rerouting lemma could
be decisive, but its bridge is less constrained.  Post-C72 Ryser has real
leverage but an immediate \(D=6\) ladder has no credible global closure
mechanism.  Q7, regular independent domination, and the 1/3--2/3 poset
problem have clean finite falsifiers but weaker proof bridges.

**First rigorous gate for the next cycle.**  Prove a complete \(d=4\)
KKT/boundary reduction: enumerate every support size and every
multiplicity/sign type; reduce every surviving family to a normalized
one-variable inequality; then prove the requisite signs on the full
\(\alpha\)-range, including the candidate-switch point.  A rigorous
zero-sum unit vector and parameter whose objective is strictly beyond both
candidate values falsifies the conjecture.  If a complete classification
leaves a residual family without a global one-variable sign proof at the
frozen cap, bank only the classification theorem if it is durable and pivot
to the LEM cycle-spectrum question—do not compensate with numerical sweeps.
