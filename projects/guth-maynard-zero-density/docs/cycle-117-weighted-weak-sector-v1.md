# Cycle 117: the weighted weak sector closes with margin `1/25`

Cycle 114 gives bounded `p0,q0`; stationary support then forces `B,C~Q`.
For each coefficient pair, Cycle 116 confines weak modes to

```text
B a^2+C b^2 <<D^2/K.
```

The elementary ellipse count is

```text
O(1+D^2/(K sqrt(BC)))=O(1+D^2/(KQ)).              (1)
```

For fixed `(B,C,a,b)`, the Laurent window has radius `O(1/K)<1/2`, so it
contains at most one integer `A`. There are `O(Q^2)` coefficient pairs, and
Cycle 112's corrected full coefficient kernel is `O(Q^(-3/2))`. Therefore
the entire smooth weak sector has arithmetic factor

```text
Q^(1/2)+D^2/(K Q^(1/2)).                          (2)
```

Writing `K=X^xi`, the exponent in (2) is

```text
max(1/6,31/30-xi).
```

It decreases across the lower band and at `xi=16/25` equals `59/150`.
Cycle 114's strong benchmark is `13/30=65/150`, leaving uniform margin
`1/25`.

Thus the registered smooth weak-turnover sector is closed. Simple-root
averages, nonsmooth payload variants, complete signed-moment assembly,
density gain, and interval gain remain open.
