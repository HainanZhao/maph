# C99 source and engine screen: quadratic-form transfer

This is a discovery packet, not an attack preregistration. It authorizes no
executable search.

## Source status

`OBSERVED`: Grechuk--Agbanwa, arXiv:2607.06627v1 (7 July 2026), proves a
tangent-line method for equations of the form

`F(Y,Z) = R(X)`,

where `F` is a fixed non-degenerate integral binary quadratic form and `R` is
univariate. The paper explicitly lists

`z^2 + y^2 z + x^3 - 2 = 0`

among the twenty length-9 equations whose finiteness problem remains open
after its results. This is current primary-source evidence of eligibility,
not a proof that no other paper has since resolved it.

## Independent algebra screen

The residual can be completed to

`(2z + y^2)^2 = y^4 - 4x^3 + 8`.

This is a useful elliptic-surface/Mordell-fiber presentation, but it is not
the paper's direct input `F(Y,Z)=R(X)`: the right side depends on both `x` and
`y`, and `y^2 z` is not a binary-quadratic term in `(y,z)`. The factorization
`z(z+y^2)=2-x^3` is exact but tautological; it supplies no fixed norm form,
recurrence, or infinitude argument.

## Competing engines

1. **Direct quadratic-form tangent transfer.**
   Candidate state: a checked substitution into a fixed non-degenerate `F`
   and univariate `R`. Falsifier: the substitution does not preserve the
   target identity or leaves a second free variable. Exact verifier: symbolic
   expansion plus the paper's congruence and Pell-type hypotheses. Current
   screen: no such substitution is visible; the source's Table 1 explicitly
   retains this equation.
2. **Elliptic-surface/Mordell fibers.**
   Candidate state: a nonconstant section or a rigorously controlled family
   on `w^2=y^4-4x^3+8`. Falsifier: a fiber computation or height argument
   proves only finitely many integral points, or no section survives the
   integrality conditions. Exact verifier: a published theorem or a pinned
   integral-point/section computation with hypotheses checked. Current screen:
   no source-cleared section or finite first gate has been identified.
3. **Cubic norm-form engine.**
   Candidate state: an explicit cubic order and norm map turning the residual
   into a unit/congruence orbit. Falsifier: the proposed norm is merely the
   tautological divisor factorization or fails to recover all three integer
   variables. Exact verifier: ring identity, integrality, and an infinite
   orbit with distinct `x`. Current screen: no non-tautological norm form has
   been identified.
4. **Portfolio pivot.**
   A different source-cleared problem with a finite rigorous gate may dominate
   this residual if none of the three engines acquires a concrete state,
   verifier, and falsifier.

## Decision boundary

The primary recommendation is `NO_SELECTION` unless Oracle identifies a
specific fixed form/section/norm state with a bounded exact first gate. Do not
repeat C98's degree-(4,3,6) ansatz, enlarge its coefficient box, or run a raw
`|x| > 10^50` search. A surviving candidate must state its nonduplication
audit against the four equations solved in Section 3 of the source paper.

## Oracle decision

Oracle returned `NO_SELECTION`. Its adversarial check agrees that the paper's
general binary-quadratic algorithm leaves an extra square-coordinate condition
when applied to this residual; the direct transfer is therefore unauthorized.
The ranked future designs are: (A+) a square-preserving tangent lift with a
finite anchor family and exact square constraint; (B) an elliptic-surface
multisection with an integrality theorem; or (C) a cubic norm-form orbit with
an explicit unit/congruence invariant. None currently has the required finite
state, verifier, and falsifier. Do not open C99 as an attack or enlarge C98.

Source: <https://arxiv.org/abs/2607.06627>.
