# Cycle 148 preregistration: endpoint major-arc comb

Date frozen: 2026-08-02 UTC.

Fix `delta>0`, a nonnegative smooth coefficient cutoff `V(n/Q)`, a bounded
reduced rational anchor `c0=A/B`, and one strict Cycle-132 endpoint class.
For each occupied mode, reduce `c0 p_a/q_a=r_a/h_a`, with `h_a~N`, and
require

```text
|c0 g^a-r_a/h_a|<=c_*/(KQ),
N<=Q X^(-delta).
```

Use exact Poisson summation in the length-`Q` coefficient variable in

```text
T_C(k)=sum_(a in C)u_a sum_n V(n/Q)e(k n c0 g^a),
```

with fixed interior-chart weights `0<u_0<=u_a<=u_1`.  Prove that nonmultiples
`h_a` not dividing `k` are power-negligible, while multiples form a common
positive phase wedge.  Compare the resulting second moment with the cell's
diagonal energy.

Success is either a strict saving or a proved resonant-comb lower bound of
size `(Q/N)` times diagonal.  The adverse result is scoped to an isolated
endpoint operator: do not claim that it survives cancellation against other
endpoint cells, that the cell carries target mass, or that it refutes the
full fixed polynomial.
