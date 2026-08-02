# Cycle 82 discovery candidate: smooth q-projector

## Status

`CONJECTURED`: discovery-only candidate.  It is not proof-grade.

## Candidate

For fixed `d`, smooth Poisson summation should give

```text
Theta_Q(x)=sum_q V(q/Q)e(qx)
          =Q sum_m hat V(Q(m-x)),
|Theta_Q(x)| <<_A Q(1+Q||x||)^(-A).               (1)
```

If at most `A_k` phases

```text
x_d=kc0 exp(2pi d/D) mod 1
```

occupy any circular interval of length `1/Q`, partitioning the circle into
such intervals and summing the decaying tails in (1) suggests

```text
|S_k| << Q A_k.                                    (2)
```

Cycle 80 gives `A_k<=X^(22/45+o(1))`, so (2) has exponent `37/45`.
The dyadic `k`-block closes when

```text
xi+37/45<31/25,
xi<94/225.
```

This would extend the current cutoff `163/450` by exactly `1/18`.

## Falsifiers

1. The frozen smooth weight does not permit uniform rapid decay in (1).
2. Circular partition endpoints require more than a constant occupancy
   enlargement.
3. Summing all annuli introduces a power loss.
4. The exact cutoff or width fails rational-arithmetic verification.

