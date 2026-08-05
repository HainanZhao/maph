# Cycle 51 soundness: exact finite conjugacy comparison

Let (H=K_{5,5}\setminus C_{10}) use the frozen cyclic labeling.  Its right
vertices have neighborhoods `(2,3,4)`, `(0,3,4)`, `(0,1,4)`, `(0,1,2)`, and
`(1,2,3)`, so `PROVED` it has 15 edges.

For an indicator (a=1_A) on a finite group, left translation lets one set
(x_0=e).  After the four remaining left variables are fixed, each right
variable contributes the size of an intersection of three translated copies
of (A).  Summing the five independent right contributions and then the four
left variables gives the exact numerator with denominator
(|\Gamma|^9).  `PROVED`: direct enumeration over all ten variables agrees
with this normalized calculation on the three frozen (S_3) controls.

For (a^{\rm cl}), multiply all class-average values by the least common
multiple of the conjugacy-class sizes.  The same formula then has integer
numerator, and cross multiplication by the fifteenth power of that scale
compares the two densities exactly.

`PROVED`: independent implementations agree on all 840 frozen rows:

- every indicator on (S_3,D_8,Q_8) (576 rows);
- every distinct subgroup-product indicator in (S_3) (12 rows) and (S_4)
  (252 rows).

All comparisons are nonnegative.  This is a finite corpus result only.  It
does not establish Zhao's comparison for all finite groups/functions, strong
Sidorenko, Sidorenko, or a graphon extremizer reduction.
