# P1R-FS Route B v1 — cleared-denominator supremum obstruction

## Claim boundary

`PROVED`: conditional on the hash-pinned Huxley (1.8) published restatement
and the sealed P1R v4 architecture, the retained left coefficient

\[
I(\sigma)=\frac{3}{2-\sigma},\qquad \frac12\leq\sigma<\frac7{10},
\]

has exact strict-left supremum \(30/13\). Consequently, replacing only the
branch on \(\sigma\geq7/10\) cannot certify a uniform coefficient strictly
below \(30/13\) inside this fixed-splice architecture.

This is not a lower bound for the actual zero count, not saturation of the
Guth--Maynard method, not a zero-density theorem, and not a short-interval
theorem. It says nothing about architectures that alter or bypass the retained
left branch. P1R-FS still requires an independent Route A, reconciliation, and
hostile audit before its gate can close.

## Frozen authority and independence

`OBSERVED`: Route B pins the sealed P1R preregistration v4, its hostile `PASS`
artifact, the image-only Huxley volume scan, and the classical source ledger.
The Huxley ledger row `ING-HUX` gives the two-sided estimate with coefficient
\(3/(2-\sigma)\) on \(1/2\leq\sigma\leq3/4\), which contains the entire
retained left interval.

`OBSERVED`: this route reads or imports no Route A script, artifact, or result.
Its proof representation is the cleared-denominator parameter
\(h=7/10-\sigma\), exact rational witnesses, and supremum monotonicity under
set inclusion.

## Exact left-supremum proof

Let \(\sigma=7/10-h\), where \(0<h\leq1/5\). Direct denominator clearing gives

\[
I(7/10-h)=\frac{30}{13+10h}
\]

and

\[
\frac{30}{13}-I(7/10-h)
=\frac{300h}{169+130h}>0.
\]

Thus \(30/13\) is an upper bound, and it is not attained on the strict left
interval.

For every rational \(\eta\) with \(0<\eta<30/13\), define the explicit
rational witness

\[
h_\eta=\frac12\min\left\{\frac15,
 \frac{169\eta}{300-130\eta}\right\}.
\]

Then \(0<h_\eta\leq1/5\), and strict denominator clearing yields

\[
\frac{300h_\eta}{169+130h_\eta}<\eta.
\]

Therefore

\[
I(7/10-h_\eta)>\frac{30}{13}-\eta.
\]

`PROVED`: the upper bound and these arbitrarily close rational witnesses give
\(\sup_{1/2\leq\sigma<7/10} I(\sigma)=30/13\), both as a rational-order
supremum and, by the same inequalities, as a real supremum.

## Arbitrary right-branch obstruction

Let \(J\) be any extended-real-valued replacement on the right domain
\([7/10,1]\), and let \(F_J\) equal \(I\) on the strict left domain and \(J\)
on the right. The left image is a subset of the full image, so monotonicity of
suprema gives

\[
\sup F_J\geq\sup I=\frac{30}{13}.
\]

Equivalently, if the right supremum is denoted by \(r\) in the extended reals,
then

\[
\sup F_J=\max\left\{\frac{30}{13},r\right\}\geq\frac{30}{13}.
\]

`PROVED`: no choice of the right branch alone certifies a strict global
coefficient below \(30/13\) in this architecture. This is an obstruction to a
specific proof splice, not a statement that zeros attain this exponent.

## Falsifier and replay

The Route B result is refuted if a pinned source/range hash fails, either
cleared identity fails, the witness leaves \(0<h\leq1/5\), its strict gap
inequality fails for an admissible rational \(\eta\), or the full-splice image
does not contain the retained left image.

From the project directory:

```sh
python3 proof/p1r_fs_route_b_v1.py --check
python3 -m unittest tests/test_p1r_fs_route_b_v1.py -v
```

The replay requires non-optimized CPython 3.12.3. `--write` refuses to
overwrite the sealed artifact, and `-O` and `-OO` fail closed.
