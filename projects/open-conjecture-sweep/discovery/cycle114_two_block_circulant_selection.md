# C114 creative selection: full two-block-circulant q=7 gate

**`CONJECTURED` routine cycle decision; F001 only.** Question the inherited
framing: C107 fixed the cross operator to a Paley choice and therefore could
not test the complete two-block construction native to Wesley's proof. Question
that critique: replacing it with a small orbit-restricted kernel would merely
move the arbitrary restriction and would be less discriminating than the full
source state at q=7.

Serious alternatives considered: (1) a cubic-coset cross kernel, rejected
because it is a strict subfamily of the source state; (2) a three-fiber voltage
state, rejected because its order does not equal \(4n-2\); and (3) local
switching of C107, rejected as an unbounded variant without a direct verifier.

Selected state: Wesley's two-block circulant graph
\(\Gamma_{\mathbb Z_q}(D_{11},D_{12},D_{22})\), with symmetric
\(D_{11},D_{22}\subseteq\mathbb Z_q\setminus\{0\}\), arbitrary
\(D_{12}\subseteq\mathbb Z_q\), and the required red degree \(q\). At
q=7 this entails \(|D_{11}|=|D_{22}|=a\) and \(|D_{12}|=7-a\), giving
exactly 512 labelled translation states. This changes C107's fixed Paley
cross block while retaining only the source-native block architecture.

**Falsifier:** a q=7 direct-cap survivor or route disagreement. **Stop:** a
q=7 no-hit closes only this full two-block-circulant q=7 state; a hit is a
candidate and does not prove the all-n target. **Resources:** one CPU, 60 s,
256 MiB RAM, 8 MiB temporary disk.
