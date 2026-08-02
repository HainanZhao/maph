# Cycle 160: an off-diagonal pair-difference condenser

## Claim boundary

`PROVED`: for the actual Cycle-87 atom form

```text
S_k=sum_u a_u e(kz_u),
```

the fourth moment with a frozen nonnegative smooth cutoff admits an exact
diagonal/off-diagonal split whose off-diagonal term is controlled by the
largest coefficient-weighted effective pair-difference codegree. In
particular, if every `K^(-1)`-scale off-diagonal cell has effective codegree
at most `X^(1/150+o(1))`, then

```text
M4 << K (sum_u |a_u|^2)^2 X^(1/150+o(1)).          (1)
```

Under the Cycle-89 conditional excess `M4>=K(DQ)^2X^(1/75-o(1))` and the
frozen atom normalization `sum|a_u|^2 asy DQ`, some labelled cell instead has
effective codegree `X^(1/75-o(1))`, hence at least the preregistered
`X^(1/150-o(1))`. Two ordered pairs in that cell satisfy the candidate
phase relation

```text
z_u+z_v'=z_u'+z_v+O(1/K).
```

This does not prove the Cycle-89 excess, the low-codegree premise, a
phase-aligned nondegenerate colored four-cycle, a fourth-moment estimate,
density, or intervals.

## Exact split and codegree

Put `A2=sum_u|a_u|^2` and separate the ordered diagonal:

```text
|S_k|^2=A2+P_off(k),
P_off(k)=sum_(u!=v)a_u conjugate(a_v)e(k(z_u-z_v)). (2)
```

On a frozen finite-overlap `K^(-1)` circle partition, let a cell `I` contain
off-diagonal pair-difference atoms `r=(u,v)`, with

```text
b_r=a_u conjugate(a_v),
rho_I=sum_(r in I)|b_r|^2,
C_I=(sum_(r in I)|b_r|)^2/rho_I,                  (3)
```

and `C_I=0` for an empty cell. This is the coefficient-weighted effective
codegree; it includes all listed cell labels and retains coincident-vertex
rows explicitly.

## Smooth Schur estimate

For a fixed smooth cutoff,

```text
L_K(t)=sum_k U(k/K)e(kt),
|L_K(t)|<=C_U K(1+K||t||)^(-A).                   (4)
```

Finite cell overlap and Cauchy give

```text
sum_k U(k/K)|P_off(k)|^2
 <= C K(max_I C_I)sum_(u!=v)|a_u a_v|^2
 <= C K(max_I C_I)A2^2.                           (5)
```

Since `sum_k U(k/K)<<K`, (2), `(x+y)^2<=2x^2+2y^2`, and (5) prove (1).
The high-codegree consequence is the contrapositive, with `1/150<1/75`
leaving a fixed exponent reserve for the frozen smooth constants and overlap
budget.

## Gate effect

This supplies the low-codegree arm of the active E14D-H condenser and makes
the high-codegree alternative an actual labelled pair-difference cell. Its
next task is to turn that cell into a rational web or a phase-aligned
four-cycle; it is not yet a full upper-band closure.
