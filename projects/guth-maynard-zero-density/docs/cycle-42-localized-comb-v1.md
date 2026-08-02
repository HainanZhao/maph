# Cycle 42: retain the sampling comb and the row Fourier transform

## Claim boundary

`PROVED`: the smooth sampling proof naturally produces a localized comb
whose total mass is proportional to the number of rows. Replacing it by the
full annulus loses `X^(9/10)`, exceeding both Cycle 39 closure margins. The
comb has an exact Fourier factorization coupling prime-monomial collisions to
the Fourier transform of the same separated row set.

`CONJECTURED`: this row-aware signed resonance form is bounded at its
diagonal scale. No kernel-count, density, or interval gain is proved.

## 1. The comb should not be flattened

Fix a real even Schwartz reproducing kernel `phi` and put

```text
omega_(B,C)(u)=sum_(t in C)|phi_B(t-u)|,
phi_B(x)=B phi(Bx).                                   (1)
```

Cycle 41 actually proves

```text
sum_(t in C)|f(t)|^2
 <=||phi||_1 integral_R omega_(B,C)(u)|f(u)|^2du.      (2)
```

The exact mass and separated overlap scales are

```text
integral_R omega_(B,C)=|C| ||phi||_1,
sup_u omega_(B,C)(u)<<_phi B                         (3)
```

when `B Delta>=1`. Cycle 41 replaced the comb by its supremum on an annulus
of length `H`. At maximal separated occupancy `|C|=X^(H-Delta)`, the ratio
between the relaxed mass `BH` and the true mass `|C|` is

```text
B H / |C| = B Delta = X^(3/10+3/5)=X^(9/10).          (4)
```

This loss is larger than the `17/50` and `7/50` closure margins. Hence
`ASAM_s` remains a valid sufficient theorem but is superseded as the lead
allocation target: it discards precisely the sparse row geometry the project
needs to exploit.

## 2. Exact Fourier factorization

Let `g_B=|phi_B|`, let

```text
R_C(xi)=sum_(t in C)exp(-it xi),                      (5)
```

and write `F_(m,s)(u)=sum_n c_m(n)n^(-iu)`. Expanding (1) gives the exact
identity, up to the fixed Fourier-transform convention,

```text
integral_R omega_(B,C)(u)|F_(m,s)(u)|^2du
 =sum_(n,n') c_m(n)c_m(n')
    hat(g_B)(log(n/n')) R_C(log(n/n')).               (6)
```

Because `g_B(x)=B|phi(Bx)|`,

```text
hat(g_B)(xi)=hat(|phi|)(xi/B).                        (7)
```

Thus the new object keeps three pieces simultaneously:

1. sparse prime-monomial coefficient labels;
2. a smooth frequency window at scale `B_m=O(s+m)`;
3. the signed row resonance sum `R_C`.

Taking `|R_C|<=|C|` or replacing the comb by `B 1_W` erases the only source
of a spacing gain.

## 3. The diagonal is exactly sharp

Define the localized-comb target

```text
LCAM_s:
sum_(2<=m<=A) integral omega_(B_m,C)(u)|F_(m,s)(u)|^2du
 <=X^(s+31/10+o(1)).                                  (8)
```

By (2), `LCAM_s` implies `AMPR_s`. For diagonal pairs `n=n'`, (6) has scale

```text
|C| sum_m sum_n c_m(n)^2.
```

Using the maximal row exponent `9/5`, harmonic exponent `3/10`, and
coefficient-square exponent `s+1`, the diagonal exponent is

```text
9/5+3/10+s+1=s+31/10.                                 (9)
```

It exactly matches (8). Consequently the remaining theorem is not an
extra-saving mean value: it is a diagonal-sharp assertion that the total
off-diagonal row resonance does not exceed the diagonal by a fixed power.

## 4. New gate

The principal statement is now:

```text
sum_m sum_(n!=n') c_m(n)c_m(n')
 hat(|phi|)(log(n/n')/B_m) R_C(log(n/n'))
 <=X^(s+31/10+o(1)),                                  (10)
```

with the complete real value understood after pairing `(n,n')` and
`(n',n)`. This is a row-aware prime-monomial resonance theorem. It can be
attacked through a dual large sieve in the row variable, differencing of
`R_C`, or shifted-prime curvature after one coefficient variable is opened.

`PROVED` route correction: E7 is
`LOCALIZED_COMB_ROW_RESONANCE_OPEN`. `ASAM_s` is retained as a sufficient
but overstrong branch; the localized diagonal-sharp form (10) is the lead.
