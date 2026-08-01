# P1R-FS fixed-splice obstruction: Route A v1

## Claim boundary

`PROVED`, conditional on the pinned published Ingham estimate as restated and
range-checked through Huxley: in the frozen envelope class that retains

\[
I(\sigma)=\frac{3}{2-\sigma}\quad(1/2\leq\sigma<7/10)
\]

and permits changes only for \(\sigma\geq7/10\), no right-only change can
certify a strict global coefficient below \(30/13\).

This is not a lower bound for the actual zero count, not saturation of the
Guth--Maynard method, not a new density estimate, and not a short-interval
theorem. A changed left branch or splice is outside this theorem.

## Direct exact proof

For every point of the strict left branch,

\[
\frac{30}{13}-I(\sigma)
=\frac{30(7/10-\sigma)}{13(2-\sigma)}>0.
\]

The endpoint value of the same rational function is \(30/13\). More
explicitly, for every \(0<\eta<30/13\), put

\[
H_\eta=\frac{169\eta}{300-130\eta},\qquad
h=\min\{1/10,H_\eta/2\},\qquad \sigma=7/10-h.
\]

Then \(1/2\leq\sigma<7/10\), \(h<H_\eta\), and exact cross-multiplication
gives \(I(\sigma)>30/13-\eta\). Hence the left supremum is exactly
\(30/13\). Any global uniform coefficient must dominate this retained left
branch, regardless of the replacement made on the right.

## Replay

```sh
python3 proof/p1r_fs_route_a_v1.py --check
python3 -m unittest tests/test_p1r_fs_route_a_v1.py -v
```
