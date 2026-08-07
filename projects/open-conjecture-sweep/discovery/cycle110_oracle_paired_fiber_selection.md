# Oracle C110 selection: paired-fiber signed-triangle lift

**`CONJECTURED` selection.** For odd \(q=2n-1\ge7\), take
\(V=[q]\times\{\pm1\}\).  Choose symmetric signs \(h_{xy}\) for
\(x\ne y\); between fibers, red is the matching \(\epsilon\delta=h_{xy}\),
blue its complement, and within-fiber edges are free colours.  Set
\[t_{xy}=h_{xy}\sum_{z\ne x,y}h_{xz}h_{yz}.\]
The asymmetric cross-edge caps force \(t_{xy}=-1\), equivalently
\(H^2+H=(q-1)I\).  Its eigenvalue discriminant \(4q-3\) yields a uniform
obstruction for odd \(q\ge7\).

Verify symbolically and independently exhaust the \(2^{15}=32768\)
q=7 signings after switching normalization.  Cap: one CPU, 60 seconds,
256 MiB, 16 MiB output.  A contradiction closes only this paired-fiber lift;
a direct-cap/sign-triangle mismatch falsifies it.  It changes every prior
state: no character blocks (C103), dihedral law (C104--C106), Paley kernel
(C107), unavailable seed (C108), or finite-field nonlinear kernel (C109).
