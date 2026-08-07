# Oracle C113 selection: balanced paired-fiber obstruction

**`CONJECTURED` planning decision; F001 only.** Oracle first rejects another
character-kernel variation as duplicating C109/C112, then notes that C110's
failure was its spectral reduction, not the paired-fiber state. The selected
question is whether the endpoint-fiber terms make the fully balanced
paired-fiber state itself impossible.

On \([q]\times\{\pm1\}\), with \(q=2n-1\), each fiber has its internal
edge colour \(r_x\), and every cross-fiber pair is the matching determined by
a symmetric sign \(h_{xy}\): \((x,\epsilon)(y,\delta)\) is red exactly when
\(\epsilon\delta=h_{xy}\). The Seidel row-sum condition is part of the
state and should force the balanced choice of all internal edges red.

For a cross pair, derive exact red/blue common-neighbour counts, including the
two endpoint-fiber contributions C110 omitted. The proposed invariant is the
signed triangle split \(N_\pm(x,y)\), where
\(h_{xy}h_{xz}h_{yz}=\pm1\), and \(N_++N_-=2n-3\). A direct q=7 normalized
bitset reconstruction is the smallest independent verifier.

**Falsifier:** a direct-cap survivor, a formula/reconstruction disagreement,
or a non-balanced state satisfying the required Seidel row sum. **Cap:** one
CPU, 120 seconds, 512 MiB RAM, 16 MiB temporary output; exactly
\(2^{15}2^7\) normalized q=7 logical states, with degree filtering allowed.
**Stop:** a proved obstruction closes only this balanced paired-fiber family;
it does not close F001 or select another problem.

**Exclusion map:** C103--C107 and C109 are reflection/Cayley/kernel states;
C111--C112 are fixed-Paley or norm cross-kernel states; C108 has no seed; and
C110's invalid spectral equation is not used here.
