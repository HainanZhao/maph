# _004 / E001 selection: quartic-character Hadamard-668 completion

**`CONJECTURED` planning decision:** Oracle selects Hadamard order 668. The
first gate is a reciprocal-even quartic-character constructor for a
near-Williamson quadruple of order 167, not arbitrary sequence generation.

For the quadratic character \(\chi\) of \(\mathbb F_{167}\), take
\(A(0)=1\), \(A(i)=\chi(i)\) otherwise, and for every admissible parameter
\(b\), take \(B_b(i)=\chi(i^4+bi^2+1)\). The decision asks whether an
unordered triple \(b\le c\le d\) satisfies the complete PAF condition with
\(A,B_b,B_c,B_d\). Evenness \(B_b(-i)=B_b(i)\) is immediate from the formula;
the direct PAF and Williamson block tests remain exact checks.

The source state and target invariant are from
Kharaghani--Mohammadian--Tayfeh-Rezaie, arXiv:2605.08661, and Epoch's
Hadamard-668 page. The exact quartic map and pair-sum completion are the new
E001 mechanism, not source claims.

## Exclusion map

| Candidate | Prior outcome | E001 delta or exclusion |
| --- | --- | --- |
| Book-Ramsey | `cycle-101-b101-book-ramsey-character-sign-rigidity-v1.json` exactly rejects every frozen six-block sign completion at \(q=7\). | No named new block type remains. E001 changes state and invariant to PAF completion. |
| Size-22 Diophantine | C98, C99, and `_001` close the bounded ansatz and evident tangent maps. | No integrality-preserving section is specified. |
| Ryser \(r=6\) | C72, C88, and C91 close the current local/trace mechanisms. | No reconstructing component quotient exists. |
| Hadamard `_002` | Exact near-Williamson state but no non-enumerative transition. | The map \(b\mapsto B_b\) and 84-coordinate exact completion supply that transition. |

## Gate and boundary

Enumerate at most 167 admissible parameters, their complete PAF/row-sum
vectors, and 14,028 unordered pair sums; use exact third-parameter lookup.
Use one CPU, ten minutes, 512 MiB RAM, and 128 MiB temporary disk. No SAT,
local search, heuristic sequence generation, or arbitrary near-Williamson
census is allowed. A no-hit is an exact boundary for this quartic family. A
hit is only a candidate until direct all-shift autocorrelation, a 668-by-668
block product, current eligibility, and overlap checks pass.
