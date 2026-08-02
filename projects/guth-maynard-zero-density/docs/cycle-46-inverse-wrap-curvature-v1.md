# Cycle 46: wrap de-aliasing is a near-lattice logarithmic-curve theorem

## Claim boundary

`PROVED`: local multiplicity of the Cycle 45 frequency set at the natural
large-sieve resolution `1/X` is equivalent, up to absolute constant changes
in the window, to counting integer points in a thin tube around an inverse
logarithmic curve. At the critical Fourier scale the required multiplicity
bound equals the reciprocal-curvature scale.

`CONJECTURED`: the near-lattice curve count satisfies this bound uniformly.
No de-aliasing theorem, `LCAM_s`, density, or interval gain is proved.

## 1. Invert a wrap

Fix a circular arc centered at `beta mod 1` with radius `1/X`. An index `k`
lies in that arc precisely when some integer `j=O(h)` satisfies

```text
|h(exp(2pi k/Delta)-1)-j-beta| <=1/X.                (1)
```

On a fixed-proportion range `k<=c_0 Delta`, the inverse derivative is
comparable to `Delta/h`. The mean-value theorem turns (1), in both
directions up to absolute constants, into

```text
|| y_(h,beta)(j) || <= C Delta/(hX),                  (2)

y_(h,beta)(j)
 =(Delta/(2pi)) log(1+(j+beta)/h),                    (3)
```

where `||.||` denotes distance to the nearest integer. Therefore the maximum
number of curved frequencies in a `1/X` arc is the maximum near-integer count
for (3), over `beta` and intervals `j=O(h)`.

## 2. Geometry of the inverse curve

For `j=O(h)` away from the harmless endpoint,

```text
y'(j)  asymp Delta/h,
|y''(j)| asymp Delta/h^2.                             (4)
```

Writing `h=X^nu`, the interval length, curve height, slope, curvature, and
tube-width exponents are

```text
nu,   3/5,   3/5-nu,   3/5-2nu,   -2/5-nu.           (5)
```

## 3. Critical reciprocal-curvature transition

At the required Fourier resolution `nu=11/25`, (5) becomes

```text
j length:       X^(11/25),
curve height:   X^(15/25),
slope:          X^(4/25),
curvature:      X^(-7/25),
tube width:     X^(-21/25).                          (6)
```

Cycle 45 requires effective wrap multiplicity at most

```text
h^(7/11+o(1))=X^(7/25+o(1)).                         (7)
```

The exponent in (7) is exactly the reciprocal of the curvature exponent in
(6). This is a genuine transition: a bound that merely counts one point per
unit of vertical travel gives `X^(15/25)`, while one point per curvature
length gives the precise target.

## 4. Sufficient theorem

The lattice branch would close its Cycle 45 de-aliasing gate if, uniformly
for `h<=X^(11/25)`, real `beta`, and the registered `j` intervals,

```text
# {j=O(h): ||(Delta/(2pi))log(1+(j+beta)/h)||
                 <=C Delta/(hX)}
 <=h^(7/11+o(1)).                                    (ILC)
```

`(ILC)` is now the principal arithmetic-geometric statement. Candidate
methods are determinant bounds for lattice points near curved arcs,
Bombieri--Iwaniec-style first/second spacing, or averaging the curve family
over the prime variable before taking a maximum in `beta`.

## Gate effect

`PROVED` exact reduction: E7 is
`INVERSE_LOG_CURVE_7_11_OR_NONLATTICE_ROW_OPEN`. The wrap loss is no longer
an unspecified alias phenomenon; it is the uniform near-lattice count
`(ILC)` at a reciprocal-curvature transition.
