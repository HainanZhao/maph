# Cycle 2 — Stream C Route B v2 correction and dependency closure

Claim boundary: `PROVED` within this document means the named source theorem,
its exact hypotheses needed here, and the displayed transfer have been checked.
The resulting `PROVED` narrow PASS closes the external dependencies in the
Guth--Maynard section 13.2 replay. It is not an independent proof of their
short-interval corollaries and does not improve an exponent.

## Versioned correction

`PROVED`: v1 incorrectly described the Huxley alternative as unread. The
existing direct inspection recorded in
[literature-ledger-classical-inputs.md](literature-ledger-classical-inputs.md)
locates Huxley's (1.9) at printed p. 164 / PDF p. 173. It states, for
(3/4leq sleq1),

\[
 N(s,T)\ll T^{3(1-s)/(3s-1)}(\log T)^{44},
 \qquad -T\leq\gamma\leq T.
\]

`PROVED`: on (4/5leq sleq1),

\[
 \frac{30}{13}-\frac3{3s-1}
 =\frac{3(30s-23)}{13(3s-1)}\geq\frac {15}{91}>0.
\]

Thus this is stronger than the (30/13) coefficient needed by the near-one
branch, while retaining the explicitly stated ((\log T)^{44}). The
Guth--Maynard density result supplies the adjacent (7/10leq sleq4/5)
branch. V1 is deliberately retained unchanged as an `OBSERVED` historical
record; v2 records the correction rather than silently changing it.

## Local count and finite-height closure

`PROVED`: Hasanalizade--Shen--Wong, Corollary 1.1, gives for (Tgeq e)

\[
 \left|N(T)-\frac{T}{2\pi}\log\frac{T}{2\pi e}\right|
 \leq0.1038\log T+0.2573\log\log T+9.3675.
\]

Their argument-principle derivation is also inspected. Bui--Heath-Brown
explicitly pins the standard (N(T)) convention required here: every zero is
counted with its multiplicity. Subtract the upper and lower displayed bounds
at (u+1) and (u-1). The main-term increment and the two errors are
(O(\log(u+2))); the bounded range is absorbed into (N(e+2)). Therefore a
unit-height strip contains (O(\log(T+2))) zeros with multiplicity when its
centre has absolute value at most (T). Partitioning ordinates by distance
from (operatorname{Im}z) gives

\[
 \sum_{|\gamma|\leq T}\frac1{|1+z+\bar\rho|}
 \ll(\log(T+2))^2,
\]

because (operatorname{Re}zgeq0), (0<operatorname{Re}ho<1), and hence
(|1+z+\bar\rho|geqsqrt{1+(\operatorname{Im}z-\gamma)^2}).

`PROVED`: Ford's Theorem 5 gives the required Vinogradov--Korobov region for
(|t|geq3). Platt--Trudgian Theorem 1, rigorously computed with interval
arithmetic, places all non-trivial zeros through height
(3{,}000{,}175{,}332{,}800) on (Re s=1/2); conjugation handles negative
ordinates. Together these close the low-height scope gap in v1. In
particular, for all sufficiently large (T), the weaker cutoff
(1-c(\log T)^{-5/7}) contains no zero, since (5/7-2/3=1/21>0).

## Replayed transfer

`PROVED`: the exact arithmetic replay retains

\[
 1/b=13/30,qquad 2/b=13/15,qquad
 \theta_{\rm unif}=17/30,qquad \theta_{\rm aa}=2/15.
\]

For the uniform branch, after absorbing the subpower factor,
(Tleq x^{1/b-epsilon/2}), and

\[
 (b+\eta)(1/b-\epsilon/2)-1\leq-b\epsilon/4
 \quad(\eta\leq b^2\epsilon/4).
\]

For the almost-all branch,
(Tleq X^{2/b-epsilon/3}), and

\[
 (b+\eta)(2/b-\epsilon/3)-2\leq-b\epsilon/6
 \quad(\eta\leq b^2\epsilon/12).
\]

`PROVED`: the cutoff contributes
(exp(-c(\log X)^{2/7})), absorbing every logarithmic factor, including
Huxley's ((\log T)^{44}), and the fixed (E(X)^{-1}) losses. The just-pinned
reciprocal-distance sum supplies the only formerly unpinned local input in
the almost-all second-moment reduction.

## Narrow PASS

`PROVED`: the source route now passes the four preregistered external nodes:
near-one density with its log factor, the high-height zero-free region,
finite-height completion, and the multiplicity-inclusive local pair bound.

`CONJECTURED` / deliberately not claimed: this audit does not establish a
new prime-in-short-interval theorem, alter Guth--Maynard's proof, or show
that their exponent can be improved. Its conclusion is only that the frozen
section 13.2 transfer has no remaining external-source blocker of the kind
listed in the v1 ledger.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/replay_short_intervals_stream_c_route_b_v2.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-route-b-v2.json
python3 -m unittest discover -s projects/guth-maynard-zero-density/tests -p 'test_*.py'
```

The v2 source locations, source hashes, exact rational checks, and claim
boundary are in
[cycle-2-stream-c-route-b-v2.json](../artifacts/cycle-2-stream-c-route-b-v2.json)
and
[cycle-2-stream-c-source-ledger-v2.json](../artifacts/cycle-2-stream-c-source-ledger-v2.json).
