# SIC--Stark research cycle 75: character and Euler-factor audit

The exact induced-character equality proves equality of the complete
Artin Euler products.  As an independent implementation and convention
check, the first 500 Dirichlet coefficients of the original
\(\mathbf Q(\sqrt5)\) characters and the reinduced
\(\mathbf Q(\sqrt{-6})\) characters agree exactly.

The original quartic characters \([1,0,0]\) and \([1,1,0]\) have full
conductor \((24)\infty_2\).  Therefore the \(S\)-imprimitive values used
in the dimension-eight calculation introduce no missing nontrivial
Euler multiplier.  Earlier cross-base phase discrepancies in raw
`bnrL1` output are PARI root/character-label choices; they are not used
as mathematical evidence.

Reproduction:

```bash
gp -q scripts/dimension_eight_cm_unit_lattice.gp
```
