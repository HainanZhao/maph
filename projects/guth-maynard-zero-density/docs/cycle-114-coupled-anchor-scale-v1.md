# Cycle 114: the coupled constraints close the smooth strong branch

`PROVED`. On the original coefficient support,

```text
B=p0 n'=lambda B0<=Q,     C=q0 m=lambda C0<=Q.
```

The fixed interior stationary chart has `n',m>=aQ`; consequently
`p0,q0<=1/a`. Thus the apparent growing rational-anchor factor in Cycle 113
cannot occur on an actual supported row.

Simultaneous support of `n,n',m` and the strong near-hit makes
`K,B0,C0` comparable to one coefficient height `Zc=Q/lambda`. A fixed core
therefore has `O(Q/Zc)` supported scales. Cycle 112's full coefficient kernel
is `O(Q^(-3/2))` at each of them, so the scale sum is

```text
O(1/(sqrt(Q) Zc)).                                (1)
```

Put `Z=min(N,R)`. Compact label ratio and coefficient comparability force
`u,v~d` and `Zc~dZ/(xy)`, so summing (1) over splits reduces to

```text
1/(d Z sqrt(Q)) sum_u (u,R)(d-u,N).               (2)
```

Use `gcd(t,L)=sum_(a|t,a|L)phi(a)`. Since `(N,R)=1`, each pair
`a|R,b|N` selects at most `1+d/(ab)` values of `u`. The `d/(ab)` terms cost
`d tau(N)tau(R)`. For the `+1` terms, restrict automatically to `a,b<=d`:
if `Z<=d`, use the full totient sums to obtain `O(Z^2)`; if `Z>=d`, use
`O(d tau(R))*O(d tau(N))`. In both cases the result is

```text
sum_u (u,R)(d-u,N)<=d Z (dNR)^o(1).               (3)
```

Equations (2)--(3) give `Q^(-1/2)X^o(1)` per degree. Degrees divide `|w|`,
and strong labels inject across signed modes, hence the complete registered
smooth strong near-double contribution has arithmetic factor

```text
M Q^(-1/2) X^o(1)=X^(13/30+o(1))                 (4)
```

after the common analytic chart factor. This supersedes Cycle 112's
incorrect aggregation route and closes both rational and irrational smooth
strong cores by a coupled proof.

Weak localization, simple roots, nonsmooth payload variants, full signed-
moment assembly, density gain, and interval gain remain open.
