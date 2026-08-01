# Cycle 12 balanced five-factor fractional-tensor theorem v1

## Claim boundary

`PROVED` conditional on an explicit balanced five-factor decomposition and
coefficient norm hypotheses: a critical length-`v^5` detector large at scale
`v^(7/2-o(1))` on a one-separated local set has at most
`v^(36/5+o(1))` rows. This beats the frozen critical local exponent `8` by
`4/5`.

`OBSERVED`: the actual Guth--Maynard zero detector has not been decomposed
into the required balanced products. The theorem therefore does not prove a
new zero-density estimate, a coefficient below `30/13`, a shorter prime
interval, Base/CRR incompatibility, or an L-function extension.

The downstream values `82/39` and `43/82` below are conditional anchor
targets only. A uniform theorem requires source factorization, a left
neighborhood of `sigma=7/10`, and the complete detector/envelope propagation.

## 1. Why the exponent is `12/5`

`PROVED` by inspection of the pinned Guth--Maynard TeX, SHA-256
`36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`:
lines 2309--2330 define the Type-I detector, lines 2332--2351 apply the
large-value theorem to integer powers, and line 2398 identifies the critical
configuration. With `T=v^13`, it is

```text
sigma=7/10,
original detector length X=v^5,
squared detector length L=v^10,
local time length H=v^12,
original threshold V_A=X^sigma=v^(7/2),
baseline local row count R=v^8.
```

The usual second moment of the squared detector corresponds to tensor power
`2` of the original detector; the next integer tensor has power `3` and is
too long. The exactly balanced power is

```text
m=log H/log X=12/5.                                    (1)
```

The engine below realizes this fractional power using only integer powers of
five balanced factors.

## 2. Balanced five-factor hypothesis

Let `W` be one-separated in an interval of length `H=v^12`. Suppose

```text
A(t)=A_1(t)A_2(t)A_3(t)A_4(t)A_5(t),                  (2)
```

where each `A_j` is a Dirichlet polynomial of nominal length `v`, with
coefficients `v^o(1)`. For each two-element subset `S` of `{1,...,5}`, define

```text
B_S(t)=product_(j in S) A_j(t)^3
       product_(j not in S) A_j(t)^2.                  (3)
```

The total length exponent in (3) is `2*5+2=12`, so `B_S` has length
`v^(12+o(1))=H v^o(1)`. Freeze the coefficient hypothesis

```text
sum_n |coeff_n(B_S)|^2 <= v^(12+o(1))                 (4)
```

uniformly in the ten choices of `S`. Divisor-bounded convolution factors
would supply (4), but that source verification is not assumed here.

## 3. `PROVED`: fractional-tensor selection identity

There are ten two-subsets `S`. Each index `j` belongs to four of them and is
absent from six. Therefore, across the product of all ten absolute values in
(3), the exponent of `|A_j|` is

```text
4*3+6*2=24.
```

Taking the tenth root gives the exact identity

```text
(product_(|S|=2)|B_S(t)|)^(1/10)
 =product_j |A_j(t)|^(12/5)
 =|A(t)|^(12/5).                                       (5)
```

Consequently, for every `t`, at least one `S` satisfies

```text
|B_S(t)|>=|A(t)|^(12/5).                               (6)
```

This is the fractional tensor: no noninteger power of a Dirichlet polynomial
is introduced.

## 4. `PROVED` conditional local large-value theorem

Assume on `W` that

```text
|A(t)|>=v^(7/2-delta).                                 (7)
```

Colour each row by one maximizing subset in (6). One of the ten colours has
at least `|W|/10` rows; call it `W_S`. On that set,

```text
|B_S(t)|>=v^(42/5-(12/5)delta).                        (8)
```

The standard discrete mean-value theorem for a length-`Y` Dirichlet
polynomial on a one-separated set in an interval of length `H`, together with
`Y=v^(12+o(1))` and (4), gives

```text
sum_(t in W_S)|B_S(t)|^2
 <=(H+Y)sum_n|coeff_n(B_S)|^2 v^o(1)
 <=v^(24+o(1)).                                        (9)
```

Combining (8)--(9),

```text
|W|/10 * v^(84/5-(24/5)delta)
 <=v^(24+o(1)),
```

and hence

```text
|W|<=v^(36/5+(24/5)delta+o(1)).                        (10)
```

At `delta=o(1)`, the local exponent is `36/5`; the gain over `8` is exactly
`4/5`.

The same proof permits a sum of `v^o(1)` balanced products in (2): a large
value selects one component at subpower cost before the ten-colour selection.
This is the precise source-decomposition target.

## 5. `PROVED`: why five equal factors are canonical for this design

Let the five factor-length exponents be nonnegative `x_1,...,x_5` with
`sum x_j=5`. The moment (3) has length exponent

```text
10+sum_(j in S)x_j.                                    (11)
```

For all ten moments to have length at most `H=v^12`, every pair sum must be
at most two. But the sum of all ten pair sums is `4 sum_j x_j=20`, so their
average is exactly two. Thus every pair sum equals two. Comparing two pairs
with a common index forces all `x_j` equal, and their total forces
`x_j=1`.

Therefore exact balance is necessary and sufficient for the uniform
ten-moment construction. The registered rational grid checked 306 sorted
fifths and found only `(1,1,1,1,1)`. The explicit unbalanced tuple

```text
(1/2,1/2,1,3/2,3/2)
```

has moment lengths from `v^11` through `v^13`, so its longest selected pair
loses a full power. This is a limitation of the uniform ten-moment design,
not of weighted or adaptive fractional tensors.

## 6. Conditional anchor map, not a promoted density theorem

If (10) held in every critical local interval, covering global height
`v^13` by `v` intervals would give global exponent

```text
1+36/5=41/5.                                           (12)
```

At `sigma=7/10`, (12) corresponds algebraically to the anchor coefficient

```text
(41/5)/(13*(1-7/10))=82/39,                            (13)
```

an anchor gain

```text
30/13-82/39=8/39.                                      (14)
```

If `82/39` were eventually made uniform in the range required by the explicit
formula, its formal interval endpoint would be

```text
1-1/(82/39)=43/82.                                     (15)
```

`OBSERVED`: equations (12)--(15) do not cross the proved fixed-splice
obstruction. They are targets that quantify the leverage of the new engine.
No propagation is authorized until the source factorization and a left
neighborhood are proved.

## 7. Exact next gate

`CONJECTURED`: decompose the normalized Type-I detector at critical length
`v^5`, or its relevant large-value component, into `v^o(1)` products of five
length-`v^(1+o(1))` Dirichlet polynomials with divisor-bounded convolution
coefficients.

The first source analysis must separate:

1. integers admitting a balanced ordered five-factorization;
2. rough or prime-dominated integers that do not;
3. smooth integers with many factorizations and the resulting coefficient
   multiplicity;
4. the Möbius-truncation and exponential/dyadic weights in the actual
   detector.

A fixed-power exceptional component is a surviving counterexample to this
factorization design and must be retained. It would motivate a weighted
fractional tensor, not erase the `36/5` theorem for balanced components.

## Replay

```sh
python3 proof/build_cycle_12_balanced_five_factor_v1.py --write
python3 proof/build_cycle_12_balanced_five_factor_v1.py --check
python3 -m unittest tests/test_cycle_12_balanced_five_factor_v1.py
```
