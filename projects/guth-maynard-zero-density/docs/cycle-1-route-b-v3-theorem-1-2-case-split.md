# Cycle 1 — Route B v3 Theorem 1.2 case-split audit

Claim boundary: this is an exact, cleared-denominator exponent audit of the
case split in Guth--Maynard's proof of Theorem 1.2. `PROVED` means conditional
on the source's zero-detecting construction, Theorem 1.1, and the mean-value
theorem. It does not prove those analytic inputs or upgrade logarithmic losses
to finite-(T) power inequalities.

## Outcome

`PROVED`: every frozen branch for (s\in[7/10,4/5]) has an exact sign
certificate.

- Type II: (2(1-s)\leq B(s)).
- Small-(n) choice: (k=\lceil l(s)/n\rceil) gives
  (l(s)\leq q\leq u(s)).
- Large-(n) choice: (k=2) gives (q>l(s)) and
  (q\leq u(s)+o(1)), with the latter kept explicitly at power scale.
- In the Guth--Maynard branch (q\leq\alpha(s)), all three displayed terms
  are at most (B(s)).
- In the mean-value branch (q>\alpha(s)), the first term is at most
  (B(s)+o(1)), while the second has a strict positive margin below (B(s)).

No new density theorem or saturation theorem is claimed.

## Frozen functions and source

\[
D=6+10s,\quad l=\frac{10}{D},\quad u=\frac{15}{D},\quad
B=\frac{15(1-s)}{3+5s},
\]
\[
d=\frac{18}{5}-4s,\qquad \alpha=\frac{B}{d}.
\]

The source is `arXiv:2405.20552v2`, TeX member
`LargevaluesDirichlet17.tex`, SHA-256
`36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`.
The source tarball SHA-256 is
`9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc`.
The audited proof is at TeX lines 2307–2380; its (k)-choice is lines
2352–2358 and its strict-margin identity is lines 2375–2379.

All denominators are positive on the frozen interval:
\[
D\geq13,\qquad 3+5s\geq\frac{13}{2},\qquad 5d=18-20s\geq2.
\]
This positivity is recorded before every denominator-clearing step.

## Cleared residuals

For Type II zeros,
\[
B-2(1-s)=\frac{(1-s)(9-10s)}{3+5s}
=\frac{10s^2-19s+9}{3+5s}\geq0.
\]
The same factor gives the large-(n) endpoint gap
\[
u-1=\frac{9-10s}{D}\geq\frac1{14}>0.
\]

If (n\leq5/D=l/2), then (k=\lceil l/n\rceil) satisfies
\(q-l\geq0\) and
\[
q-u<n-(u-l)\leq0,
\]
because (D(u-l)=5\geq Dn). If (n>5/D), (k=2) gives
\(q-l=2n-10/D>0\). The source's upper endpoint is only
\(n\leq1/2+o(1)\), hence (q\leq1+o(1)\leq u+o(1)\); it is not recorded as
an unqualified finite-(T) statement.

The three Guth--Maynard residuals are
\[
B-2q(1-s)=2(1-s)(u-q),
\]
\[
B-dq=d(\alpha-q),
\]
\[
B-[1+(12/5-4s)q]=(4s-12/5)(q-l).
\]
Their signs follow from the chosen (q)-range, (d>0), and
\(4s-12/5\geq2/5>0\).

For the first residual in this branch, endpoint slack is not needed. The
cleared comparison is
\[
d(s)u(s)-B(s)=\frac{3(4-5s)}{3+5s}\geq0.
\]
Thus \(q\leq\alpha(s)\leq u(s)\) exactly; equality in the final comparison
can occur only at \(s=4/5\).

For the mean-value branch, write
\[
B-[1+(1-2s)q]=M(s)+(2s-1)(q-\alpha),
\]
where
\[
M(s)=\frac{250(s-3/4)^2+3/8}
{2(3+5s)(9-10s)}
=\frac{250s^2-375s+141}{2(3+5s)(9-10s)}>0.
\]
The numerator is at least (3/8), (2s-1>0), and (q>\alpha), giving the
strict inequality required by the source proof.

## Replay

The versioned certificate is
[cycle-1-route-b-v3-theorem-1-2-case-split.json](../artifacts/cycle-1-route-b-v3-theorem-1-2-case-split.json).

```sh
python3 projects/guth-maynard-zero-density/proof/replay_theorem_1_2_case_split_route_b_v3.py --check projects/guth-maynard-zero-density/artifacts/cycle-1-route-b-v3-theorem-1-2-case-split.json
python3 -m unittest discover -s projects/guth-maynard-zero-density/tests -p 'test_*.py'
```

The v1 baseline and v2 bottleneck artifacts are retained; this v3 test suite
checks both before passing.
