# _005 / F001 selection: dihedral reflection completion

**`CONJECTURED` planning decision:** F001 adds inversion
\(R_{s,t}=1\iff s\equiv-t\pmod m\) to D001's six-block character state.
Each of six inter-block entries \(C\in\{X,Y\}\) becomes \(CR^\epsilon\),
with the original 19 signs retained and the reverse block transposed.

At most \(2^{25}\) assignments are tested after D001 row-sum pruning, first
at \(q=7\), then at \(q=23\). The cap is one worker, 1,800 seconds, 1 GiB
RAM, and 128 MiB disk. No SAT, graph census, free blocks, or more reflection
layers. A no-hit closes only this one-reflection extension.
