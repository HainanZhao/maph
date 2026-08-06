# C97 fixed-ansatz selection packet

This packet proposes one finite method family after Oracle's C97
`NO_SELECTION`; it is not yet a preregistration and authorizes no execution.

## Frozen family

For `P=z^2+y^2 z+x^3-2`, use the source-motivated parity-balanced forms

```text
x(t) = a t^4 + b t^2 + c
y(t) = p t^3 + q t
z(t) = r t^6 + s t^4 + u t^2 + v.
```

All nine coefficients are integers in `[-648,648]`; the leading terms are
required to be nonzero, and duplicate maps under `t -> -t` are identified.
The bound 648 is frozen from the largest coefficient in the published
adjacent-equation family, not chosen after observing a residual solution.
The exact finite question is whether coefficient comparison makes `P` vanish
identically, and if so whether the resulting map has three distinct outputs
with `|x| > 10^50`.

## Adversarial check

This is not a claim that the degree pattern is canonical: it may simply copy
the adjacent equation's successful ansatz and fail on the constant `-2`.
Its value is a falsifiable method boundary with a finite coefficient state,
not a promise of infinitude. A failure does not constrain elliptic, norm-form,
or higher-degree maps.

## Exact gate

State: the nine bounded integer coefficients and the coefficient vector of
the substituted degree-12 polynomial. Verifier: exact integer expansion and
coefficient equality to zero, independently reconstructed from the displayed
forms. Falsifier: one nonzero coefficient or a threshold failure. Stop:
record success as a polynomial-family infinitude result; on exhaustion, seal
only this degree/bound family and pivot to a genuinely different engine.
