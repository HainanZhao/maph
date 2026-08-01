# P6 primitive-to-all character transfer v1

## Outcome and boundary

`PROVED`: every character \(\chi\) modulo \(q\) has a unique primitive
inducer \(\chi^*\) of conductor \(d\mid q\), and

\[
 L(s,\chi)=L(s,\chi^*)
 \prod_{\substack{p\mid q\\p\nmid d}}(1-\chi^*(p)p^{-s}).
\]

Each finite Euler factor has zeros only on \(\operatorname{Re}s=0\). Hence
the zero multisets of \(L(s,\chi)\) and \(L(s,\chi^*)\), including
multiplicities, are equal in \(\operatorname{Re}s>0\). This gives the exact
identity

\[
 \sum_{\chi\bmod q}N(\sigma,T,\chi)
 =\sum_{d\mid q}\sum_{\chi^*\bmod d}^{*}N(\sigma,T,\chi^*)
 \qquad(\sigma>0).
\]

The result is a narrow repair of the mathematics behind P6 Z05/Z06. It is
not a validation or repair of Chen--Gupta--Li v2, nor a zero-density or
short-interval theorem. The replay pins the CGL-v2 source tar and verifies
the relevant source locations: TeX 2109, 2136--2138, and 2148--2152.

## Proof and uniform transfer

The conductor statement follows from Chinese remaindering and the least local
power \(p^{b_p}\) through which each local group character factors. Their
product is primitive; leastness proves uniqueness. Dividing Euler products in
\(\operatorname{Re}s>1\), then using meromorphic continuation, gives the
displayed finite factorization. If \(1-\chi^*(p)p^{-s}=0\), absolute values
give \(p^{-\operatorname{Re}s}=1\), so \(\operatorname{Re}s=0\).

`PROVED`: if a primitive envelope is uniform for \(dT\) sufficiently large,

\[
 N^*(\sigma,T;d)\ll_\delta(dT)^{A(1-\sigma)+\delta},
\]

for \(d,T\geq1\) and \(\sigma_0\leq\sigma<1\), then the all-character
envelope is

\[
 \sum_{\chi\bmod q}N(\sigma,T,\chi)
 \ll_\epsilon(qT)^{A(1-\sigma)+\epsilon}.
\]

Indeed, the large-\(dT\) divisors contribute at most
\(\tau(q)(qT)^{A(1-\sigma)+\delta}\), and
\(\tau(q)\ll_\delta q^\delta\leq(qT)^\delta\). The finitely many divisors
with \(dT<K_\delta\) have \(d,T<K_\delta\); their zero counts are bounded by
a finite compact-range constant and are absorbed. Thus the argument never
applies an asymptotic primitive estimate in its unlicensed small-\(dT\)
range.

Conditionally, the CGL-style monotone primitive envelope

\[
 (dT)^{o(1)}\{(d^{7/3}T^2)^{1-\sigma}
 +(dT)^{(30/13)(1-\sigma)}\}
\]

transfers termwise with only the divisor loss. Since both bases are monotone
in \(d\), it yields the corresponding \(q\)-envelope and then the uniform
\(7/3\) envelope. This is the appropriate Z05/Z06 application.

## Scope retained

`OBSERVED`: this does not automatically transfer every intermediate
\(q_1\)-sensitive expression. Once a character has conductor \(d\), a fixed
\(q_1\mid q\) need not divide \(d\), and its original source range may not
survive. It also leaves `Z03_TAIL_X_RANGE`, `S06_EXTERNAL_INPUTS`,
`F08_T_SMOOTH_UNDEFINED`, and `S03_MULTIPLICITY_NOT_STATED` open. The exact
transfer works for either zero-count multiplicity convention if it is applied
on both sides, but it does not resolve the source's unstated convention.

`OBSERVED` display correction: the first generated copy of this note lost
several Markdown backslashes in inline mathematics. The replay artifact and
proof script were unaffected; this paragraph records the presentation-only
repair.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/p6_primitive_to_all_transfer_v1.py --check
python3 -m unittest tests/test_p6_primitive_to_all_transfer_v1.py -v
```
