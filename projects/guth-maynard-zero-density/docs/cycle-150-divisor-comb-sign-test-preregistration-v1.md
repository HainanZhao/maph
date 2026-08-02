# Cycle 150 preregistration: divisor-comb sign test

Date frozen: 2026-08-02 UTC.

Take the denominator witness `h` from Cycle 149 and use the real correlation
against

```text
w_h(k)=Q 1_(h|k),       K<=k<=2K.
```

Split the exact complement into `P+H`, where `P` consists of every other mode
that satisfies the Cycle-148 strict positive endpoint hypotheses with
denominator at most `QX^(-delta)`, and `H` is the remaining escape class.

Substitute `k=h ell` into `P`.  Apply the exact Cycle-148 Poisson dichotomy
mode by mode: resonant denominators dividing `h ell` must contribute in the
positive phase wedge, and nondivisors must be power-negligible.  Combine this
sign test with the Cycle-149 negative witness and Cauchy--Schwarz to obtain a
norm lower bound for `H`.

Success is a proof that strict positive endpoint combs cannot anti-align with
one another, plus an exhaustive scoped list of escape mechanisms and a
quantified negative-correlation/norm obligation for them.  Do not claim that
the escape class is absent or that the full moment is closed.
