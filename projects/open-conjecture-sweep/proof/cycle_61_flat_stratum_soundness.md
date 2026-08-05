# C61 flat-stratum soundness

`check_cycle_61_flat_stratum.py` evaluates the translation-fixed numerator
for (K_{5,5}\setminus C_{10}) on (S_3), using integer polynomials in a
single perturbation parameter.  A class-zero direction leaves the
centralization fixed, so every positive-degree coefficient is the
corresponding coefficient of (N(a)-N(P_{\rm cl}a)).

At a central base, the class-zero tangent space is the direct sum of the
two-dimensional standard representation (V) (the three transposition
coordinates summing to zero) and the one-dimensional sign representation
(S) (the oriented difference of the two 3-cycles).  At the four frozen
Hessian-flat bases `111`, `121`, `212`, and `222`, an invariant cubic can only
be a multiple of the standard cubic.  The generic direction
((-1,-2,3)\in V) has nonzero standard cubic, and the exact calculation gives
zero cubic coefficient; hence the full restricted cubic vanishes.

More explicitly, the degree-three invariant space of `V ⊕ S` is
one-dimensional: the usual invariant cubic on `V`. A term involving one `S`
would require a sign summand in `Sym²(V)`, which is absent, and odd pure powers
of `S` are sign-valued. Thus the generic standard calculation tests the whole
allowed cubic tensor, not merely one ray of a larger cubic space.

Writing (r^2=x^2+y^2+z^2), (x+y+z=0), and
\(\Delta=(x-y)(y-z)(z-x)\), every invariant restricted quartic has the form

\[
A r^4+B r^2s^2+C s^4+D s\Delta.
\]

The exact evaluator determines `A` from a standard axis, `C` from the sign
axis, and `B,D` from the two generic mixed directions.  It obtains `D=0` and
`A>0`, `B>=0`, `C>0` at every frozen base.  Therefore the quartic is strictly
positive away from the origin.  This is a finite local Taylor statement only;
it neither proves Zhao's comparison for all groups nor Sidorenko for the
target graph.

## Central-transverse check

The preceding restriction alone would be insufficient if a central direction
could create an (x^2y) or (x^3y) fourth-order destabilization.  The second
exact symbolic replay computes the central parameter dependence.  For a
standard axis and for the sign line, its quadratic coefficient factors as
\((c-e)^2R(e,t,c)\), where the quotient has strictly positive integer
coefficients.  The standard generic cubic is
\((c-e)^4S(e,t,c)\), again with a strictly positive coefficientwise quotient;
the other cubic coefficients vanish by representation type.  Exact sparse
division, rather than numerical factor recognition, is checked in
`check_cycle_61_transverse.py`.

Consequently the complete fourth homogeneous transverse form around each
frozen base is the positive raw kernel quartic plus nonnegative
\((c-e)^2\)-times-Hessian terms.  It is nonnegative, and strictly positive
off the central equality manifold to fourth order.

## Finite-polynomial remainder dominance

Write a nearby function as a positive central parameter `c'=(e',t',c')` plus
a class-zero vector `x=(v,s)`. The exact factorization gives a nonnegative
quadratic term, with a positive-definite coefficient when `c' != e'`, and a
cubic coefficient of order `(c'-e')^4`. At `c'=e'`, the exact quartic above is
positive definite on every nonzero `x`. Positivity of this finite coefficient
list is open, so it remains uniformly positive for central parameters in a
sufficiently small rational neighborhood of each frozen base. The remaining
finite polynomial terms have degree at least five in `x` and are bounded by a
constant times `||x||^5`; after shrinking the neighborhood they are dominated
by that uniform quartic margin. The cubic term is dominated by the quadratic
factor when `c' != e'`, and by the quartic margin when `c'=e'`.

Therefore `N(a)-N(P_cl a) > 0` for all sufficiently close noncentral `a`,
with equality on the central subspace. This proves strict local endpoint
comparison near the four specified positive central `S3` bases only. It does
not prove the assertion for arbitrary `S3` functions, finite groups, Zhao's
comparison, or Sidorenko.
