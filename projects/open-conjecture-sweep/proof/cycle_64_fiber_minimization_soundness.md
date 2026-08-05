# C64 invariant-fiber minimization theorem and boundary

## Exact fiber

Use C63's coordinates and fix `(e,t,c,r2)`.  The outer projection of the
normalized nonnegative S3 simplex is

\[
 e+3t+2c=1,\qquad e,t,c,r_2\geq0,\qquad r_2\leq6t^2.
\]

Indeed, if the transposition coordinates are `q_i=t+x_i`, then
`r2=sum(q_i^2)-3t^2`.  At fixed nonnegative sum `sum(q_i)=3t`, the sum of
squares lies between `3t^2` and `9t^2`, proving the stated range.  Conversely,
C63's cubic criterion gives the exact remaining fiber

\[
 0\leq s_2\leq c^2,
\]

and

\[
 \max\left(\frac{tr_2}{2}-t^3,-\sqrt{\frac{r_2^3}{54}}\right)
 \leq u\leq \sqrt{\frac{r_2^3}{54}}.
\]

The interval is nonempty throughout the outer projection.  For `t>0`, put
`R=r2/t^2`.  If `R<=2`, the root-product lower bound is nonpositive.  For
`2<=R<=6`, its comparison with the positive discriminant endpoint follows
after squaring from

\[
 2R^3-27(R-2)^2=2(R-\tfrac32)(R-6)^2\geq0.
\]

The case `t=0` has `r2=u=0` directly.

For sufficiency, the discriminant inequality gives three real roots
`x,y,z` of `X^3-r2*X/2-u` with sum zero.  The shifted roots `q_i=t+x_i`
have elementary symmetric functions

\[
 3t,\qquad 3t^2-\frac{r_2}{2},\qquad
 t^3-\frac{tr_2}{2}+u.
\]

They are all nonnegative on the displayed outer domain and fiber.  If one
real root were negative, the product would be negative; if two were negative,
nonnegative sum would force their pair sum negative.  Thus all `q_i` are
nonnegative.  Independently, `0<=s2<=c^2` permits real `s` with
`c-s,c+s>=0`.  This proves sufficiency of the projected description rather
than only necessity.

## Uniform resultant reduction

On every fiber the deficit `P` has the frozen Newton support recorded by the
packet: `deg_u(P)=5` and `deg_s2(P)=7`.  An interior fiber minimum satisfies

\[
 P_u=P_{s_2}=0.
\]

Treat these as polynomials in `s2`, with coefficients in
`Q[e,t,c,r2,u]`.  The exact post-differentiation supports give
`deg_s2(P_u)=6` and `deg_s2(P_s2)=6`, so their bounded-degree Sylvester
matrix is `12 x 12`.  Exact maximum-weight matching on its support
gives the upper bound 26 for the degree in `u` of its determinant.  There are
27 maximum-weight determinant terms.  Expanding only those terms, with the
exact outer coefficient polynomials, gives

\[
 [u^{26}]\operatorname{Res}_{s_2}(P_u,P_{s_2})
 =-152066696928339427279920998154715326750000000000.
\]

This is a nonzero rational constant, independent of all outer parameters.
The universal proof is the fully expanded fixed-size determinant and its
constant leading coefficient.  A degree-preserving specialization checks its
conventions.  At a second specialization where the `s2` degree drops, the
bounded-degree and freshly recomputed lower-degree resultants differ by the
expected nonzero factor 270; this is only a convention check and carries no
part of the universal argument.

Therefore the degree-bounded resultant is nonzero of exact `u` degree 26 on
**every** outer fiber.  Every isolated interior critical point projects to one
of at most 26 algebraic `u` values, and for each such value to at most six
`s2` values.  If both derivatives vanish identically as polynomials in `s2`
at one exceptional projected `u`, then `P_s2=0` there and `P` is constant in
`s2`; its value is already attained on `s2=0` and `s2=c^2`.  Thus such a
vertical critical component introduces no new minimum value.

It follows that every fiber minimum is attained in the explicit list:

1. `s2=0` or `s2=c^2`;
2. `54*u^2=r2^3` or `u=t*r2/2-t^3` when that root-zero constraint is active;
3. one of at most 156 isolated algebraic pairs selected by the degree-26
   resultant and one derivative.

This is a uniform finite fiber-minimum reduction, with no genericity exception.
It is finite **per fixed fiber**.  The algebraic candidates still vary over
the three-dimensional continuum of normalized outer parameters, so 156 is
not a global candidate count.

## Exact anchor checks and unresolved sign

At each of the three preregistered rational outer anchors, exact Sturm
isolation of the specialized degree-26 resultant finds no root in the
corresponding feasible `u` interval.  Hence all three frozen fibers attain
their minima on the named boundaries.  The anchors are convention and fiber
checks only.  The two equal-mass anchors lose the top `s2` degree, while the
third preserves it; none carries a uniform sign claim.

The boundary specializations themselves have mixed coefficients and no
promoted positivity certificate.  C64 therefore does **not** prove that the
listed boundary or isolated values are nonnegative.  It proves neither S3
Zhao comparison, Zhao's universal comparison, nor Sidorenko for the target
graph.  A feasible algebraic branch with negative `P` remains the decisive
falsifier.
