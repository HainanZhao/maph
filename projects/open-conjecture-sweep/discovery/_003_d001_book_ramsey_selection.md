# _003 / D001 selection: book-Ramsey character-block completion

This is Oracle's non-credit selection decision. D001 is legacy Cycle 101 / B101;
executable work requires its own preregistration.

## Selection

**`CONJECTURED` planning decision:** D001 is the all-\(n\) book-Ramsey
construction problem. Its first bounded design gate asks whether a fixed
signed six-block completion of the public \(n=70\) character construction
extends to prime powers \(q\equiv7\pmod8\), with \(n=(q+1)/2\).

The current Epoch problem page calls for an algorithm producing a graph on
\(4n-2\) vertices for every \(n\), still labels the problem unsolved, and
reports the public \(n=70\) example. The latter supplies explicit block
algebra rather than merely an adjacency-string target.

Sources: <https://epoch.ai/frontiermath/open-problems/ramsey-book-graphs>;
<https://epoch.ai/files/open-problems/ramsey-book-graphs-70.pdf>.

## Decision question and first gate

Let \(H=(\mathbb F_q^\times)^2=\langle g\rangle\), \(\chi\) be the
quadratic character, and define circulants of order \((q-1)/2\) from
\(a_0=1\), \(a_t=\chi(g^t-1)\) for \(t\ne0\), and
\(b_t=\chi(g^t+1)\). For \(q\equiv7\pmod8\), the proposed symbolic state is
\[
 XJ=J,\quad YJ=-J,\quad Y^T=Y,\quad X+X^T=2I,\quad
 XX^T+Y^2=(q+1)I-2J.
\]

**Question:** do the public six block-type placements admit one of the
\(2^{19}\) allowed sign assignments such that the resulting symmetric Seidel
template has \(S\mathbf1=-\mathbf1\) and every off-diagonal entry of
\(S^2\) is in \(\{0,-4\}\), identically under these relations?

The state is \((I,J,X,X^T,Y)\), six block classes
\(u,v,H_0,H_1,H_2,H_3\), and a 19-bit sign vector. The map is the signed
block assembly. The invariant is constant Seidel row sum and nonpositive
off-diagonal signed two-walk counts. The smallest verifier is exact symbolic
block multiplication, followed by independent finite-field and graph checks
at \(q=7\) and \(q=23\). Limit the sign enumeration to \(2^{19}\), one CPU,
30 minutes, and 1 GiB; do not use SAT over graph edges, graph local search,
or a parameter census.

## Adversarial comparison

The direct question risks treating a finite sign search as a family
construction. Its meaningful negative outcome is instead restricted to the
fixed six-block/sign mechanism. The critique itself could overreact to earlier
census failures and miss a symbolic finite search whose outcome applies to a
uniform relation algebra.

| Candidate | Prior decision and outcome | Delta or exclusion |
| --- | --- | --- |
| Book-Ramsey (selected) | `cycle96_book_ramsey_candidate_screen.md` required a current parameter and new family, then stopped with only an isolated graph verifier. | The public \(n=70\) derivation now fixes a uniform block architecture; D001 tests its symbolic transition, not an \(n=71\) graph search. |
| Hadamard 668 | `_002_hadamard_near_williamson_screen.md` has an exact state but no lift or informative cap. | No transition preserving complementary autocorrelation is specified; a no-hit would be only a census. |
| Size-22 Diophantine surface | `cycle-98-b098-diophantine-fixed-ansatz-boundary-v1.json`, `cycle99_quadratic_form_screen.md`, and `_001_portfolio_no_selection.md` close the fixed ansatz and evident tangent planes. | No new integrality-preserving map exists; enlarging bounds duplicates C98--C99. |
| ES(7) | `cycle100_control_outcome.md` closes the C001 criterion after a valid SAT control. | No newly proved polarity or realizability map licenses a retry. |

## Falsifier and continuation

**`OBSERVED` source status:** the public \(n=70\) derivation works at
\(q=139\equiv3\pmod8\); the \(q\equiv7\pmod8\) sign change is the exact
interface D001 probes. **`CONJECTURED` strongest flaw:** sign changes may be
too rigid to repair the row-sum switch; public/under-review overlap must be
audited before any novelty claim.

A symbolic solution advances to independent finite-field, graph, eligibility,
and overlap checks. Exhaustion seals only the 19-sign rigidity boundary; it
does not license free blocks or a graph search. Continue D001 only when the
residual algebra names one bounded new block type, otherwise close it and
return to an Oracle selection.
