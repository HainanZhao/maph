# Cycle 99: near-double roots compile to critical rational rays

## Claim boundary

`PROVED`: every sufficiently localized Cycle-97 near-double row has a unique
reduced rational critical label, and these labels are injective across mode
differences. Any excess is confined to an explicit coefficient/mode
factorization fiber.

The theorem does not bound that fiber, cover weakly localized near-double
rows, close the alias moment, or prove a density/interval gain.

## Critical label

Let `B,C<=Q`, let `a,b` be nonzero opposite-sign integers with
`max(|a|,|b|)<=M`, and put

```text
w=a-b,        r=-Cb/(Ba)=C|b|/(B|a|)>0.            (1)
```

The Cycle-97 critical equation is exactly

```text
r=exp(wt*).                                        (2)
```

After reduction, write `r=N/R`. The unreduced numerator and denominator in
(1) are at most `QM`, so

```text
N,R<=H:=QM,        1<=|w|<=2M.                    (3)
```

## Compilation error

Fix `x>0`, put `rho=|t*-x|`, and choose

```text
L>=max(|wx|,|wt*|),       E=exp(L).
```

The mean-value theorem applied to `exp(wt)` gives

```text
|r-exp(wx)|<=E|w|rho=:delta_ray.                   (4)
```

For the entropy application, `x=2pi/D`. Cycle 97 supplies
`rho<=2eta/ell`, so the right side of (4) is at most
`2E|w|eta/ell`.

## Fixed-mode uniqueness

Distinct reduced positive rationals with numerators and denominators at most
`H` differ by at least `1/H^2`. Therefore two such rationals cannot both lie
within `delta_ray` of `exp(wx)` whenever

```text
delta_ray<1/(2H^2).                                (5)
```

Thus a strongly localized row has a unique rational label for its fixed
mode difference `w`.

## Injectivity across mode differences

If `w_1!=w_2` and both `|w_jx|<=L`, then

```text
|exp(w_1x)-exp(w_2x)|
 >=exp(-L)(exp(x)-1).                              (6)
```

Consequently labels from distinct mode differences are distinct if every row
satisfies

```text
delta_ray<exp(-L)(exp(x)-1)/2.                     (7)
```

Combining (5), (7), and the Cycle-97 critical distance gives the sufficient
strong-localization condition

```text
2E|w|eta/ell
 <min(1/(2H^2), exp(-L)(exp(x)-1)/2).              (8)
```

## Surviving factorization fiber

Once `(w,N,R)` is fixed, every original row in its fiber satisfies exactly

```text
C|b|R=B|a|N,       a-b=w,                          (9)
```

with the original sign orientation retained. Thus multiplicity is no longer
an unstructured analytic error: it is a concrete four-factor convolution
fiber. This is the correct input for Möbius cancellation, divisor switching,
or the E16 alias-to-seed compiler.

## Gate effect

E14D-L advances to
`STRONG_NEAR_DOUBLE_RAYS_BANKED_SIMPLE_ROOT_AVERAGE_WEAK_CRITICAL_AND_FIBER_OPEN`.
