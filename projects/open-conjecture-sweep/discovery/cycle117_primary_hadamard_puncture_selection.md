# C117/B115 primary selection: Sylvester-Hadamard puncture orbit

**`CONJECTURED` primary planning decision; F001 only.** Question the
inheritance: C113 and C114 constrain two incompatible coordinate models, not
the possibility that a near-Hadamard two-graph becomes asymmetric-book-feasible
after a codimension-one puncture. Question that critique: an unrestricted
14-vertex switching search would be a graph census, so the parent state and
the deletion operation must both be fixed algebraically.

Candidates considered: (1) revive the q=13 conference switching orbit,
rejected because its unsealed, discarded design is not a fresh pre-result
question; (2) a Hadamard puncture, selected because the fixed Sylvester
Walsh matrix supplies a functorial 16-to-14 transition and complete orbit;
and (3) a skew-tournament lift, rejected because C115's stated balance input
is unavailable and its preflight is quarantined.

Selected state: index the Sylvester matrix by \(\mathbb F_2^4\),
\(H_{xy}=(-1)^{x\cdot y}\). Form the zero-diagonal signed matrix \(K\) by
retaining its off-diagonal entries, delete an unordered pair of vertices, and
apply all remaining diagonal switchings modulo global sign. Red means signed
entry \(-1\). The complete state has \({16\choose2}2^{13}=983{,}040\)
members. Direct common-neighbour counts and an independent bitset replay are
the smallest verifiers.

**Falsifier:** a survivor or route disagreement. **Stop:** a no-hit closes
only this fixed Hadamard-puncture orbit; a hit is an exact n=4 candidate, not
an all-n result. One CPU, 120 s, 512 MiB RAM, 16 MiB temporary disk.
