# SIC--Stark research cycle 95: exact weight-one modular identification

Date: 2026-07-28

## New result

The primitive dimension-six Hecke character has a completely explicit
classical modular avatar.

Let

\[
 K=\mathbf Q(\sqrt{21}),\qquad
 \mathfrak f=(6)\infty_2,\qquad
 \chi(g)=\zeta_6
\]

on
\(\operatorname{Cl}_{\mathfrak f}(K)\simeq C_6\).  PARI's exact
conductor calculation gives finite conductor \((6)\) and the stated
single infinite place.  Hence the absolute Artin conductor is

\[
 |\operatorname{disc}K|\,N(6)
 =21\cdot36
 =756.
\]

The theta series

\[
 \Theta_\chi(q)
 =
 \sum_{\substack{\mathfrak a\subset\mathcal O_K\\
                  (\mathfrak a,6)=1}}
 \chi(\mathfrak a)q^{N\mathfrak a}
\]

is the weight-one newform at level \(756\) with:

\[
\boxed{
\text{nebentypus }-7,\qquad
\text{coefficient field }\mathbf Q(\sqrt{-3}),\qquad
\text{projective type }D_{12}.
}
\]

Among all weight-one newforms at level \(756\), exactly one form after
the convention-matching coefficient-field embedding has the same
Fourier coefficients.

## Exact comparison

The Sturm index calculation is

\[
 [\operatorname{SL}_2(\mathbf Z):\Gamma_0(756)]
 =
 756\left(1+\frac12\right)
     \left(1+\frac13\right)
     \left(1+\frac17\right)
 =1728,
\]

so the weight-one Sturm bound is \(1728/12=144\).

The certificate enumerates all ideals of norm at most \(144\), computes
their exact ray logarithms, forms the coefficients in
\(\mathbf Q[t]/(t^2-t+1)\), and compares them with every PARI weight-one
eigenform through that bound.  It outputs

```text
ABSOLUTE_ARTIN_CONDUCTOR=756
STURM_BOUND=144
MATCHING_WEIGHT_ONE_NEWFORMS=1
MATCHING_NEBENTYPUS=-7
MATCHING_PROJECTIVE_GALOIS_TYPE=12
MATCHING_COEFFICIENT_FIELD=t^2-t+1
```

The executable certificate is

```text
scripts/dimension_six_weight_one_modularity.gp
```

## Meaning

The last dimension-six identity can now also be stated as a critical
value/regulator identity for one explicit real-dihedral weight-one
newform:

\[
 L(s,\Theta_\chi)=L_K(s,\chi).
\]

This is useful new structure.  It replaces a generic “order-six Stark
value” by a level-\(756\), nebentypus-\(-7\), projective-\(D_{12}\)
modular form and exposes modular-unit and Rankin--Selberg methods as
concrete possible tools.

It does not by itself prove the Stark unit formula: modularity supplies
analytic continuation and the functional equation, not the algebraic
evaluation of the oriented derivative.

