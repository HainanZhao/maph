# Cycle 063 — generic certified Engine-C analytic targets

**Claim tag:** `ENCLOSED_PRIMITIVE_LPRIME_TARGETS`

A generic theta/Mellin evaluator now computes primitive quartic
\(L'(0,\psi)\) from exact `lfunan` coefficients.  For analytic
conductor \(N\), it uses
\[
Q=\frac{\sqrt N}{2\pi},\qquad
\theta(t)=\sum_{n\ge1}a_n e^{-nt/Q},
\]
splits the Mellin transform at one, and derives the root-number ball
from \(\theta(1)/\overline{\theta(1)}\).  The omitted coefficients use
the explicit bound \(|a_n|\le d(n)\le n\); no PARI `lfun` or `bnrL1`
point value enters the proof chain.

The Paper-II route at conductor 2880 is reproduced.  The independent
\(\mathbb Q(\sqrt{-10})\) and \(\mathbb Q(\sqrt{-14})\) routes both
have conductor 4480 and give the identical enclosure
\[
L'(0,\psi)=
3.14906101042327538218\ldots
-10.56825360321537940335\ldots i
\]
with maximum component radius below \(1.5\times10^{-77}\).

Artifact: `artifacts/engine-c-theta-targets-v1.json`.

