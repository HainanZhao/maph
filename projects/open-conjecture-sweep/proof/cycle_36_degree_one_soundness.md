# Cycle 36: degree-one signed product functional

## Claim boundary

`PROVED`: for p199 base 4 / leaf 78, the constant function is not in the
rational span of the 1,394 direct uncovered predicates \(F_t\) and their
221,646 coordinate-option multiples \(x_{i,a}F_t\). This is a no-go for the
frozen degree-\(\le1\) direct-predicate calculus. It does not exclude the leaf,
classify nonproduct duals, address degree two or ownership auxiliaries, or
prove LRC(13).

The functional is signed and is not a positive pseudoexpectation in the
sums-of-squares sense.

## Product functional and degree-one compression

For local integer vectors \(u_i\) of mass one, define

\[
L(g)=\sum_d\left(\prod_i u_i(d_i)\right)g(d).
\]

Let \(z_{t,i}=\langle u_i,b_{t,i}\rangle\). Then

\[
L(F_t)=\prod_i z_{t,i},\qquad
L(x_{i,a}F_t)=u_i(a)b_{t,i}(a)\prod_{j\ne i}z_{t,j}.
\]

For a fixed predicate, all degree-zero and degree-one expressions vanish if
and only if one of the following exact conditions holds:

1. at least two coordinates have \(z_{t,i}=0\); or
2. exactly one coordinate \(k\) has \(z_{t,k}=0\), and it is strong:
   \(u_k(a)b_{t,k}(a)=0\) for every option \(a\).

With two zeros, deleting any one local contraction leaves another zero. With a
unique zero at \(k\), multipliers outside \(k\) retain that zero, while the
multipliers at \(k\) vanish exactly under the pointwise strong condition. With
no zero contractions, vanishing all multipliers would force a zero contraction
and is contradictory. This proves the compression from 221,646 labeled
multiplier constraints to 1,394 ordinary-or-strong predicate conditions.

## Exact result and independent replay

The first raw-signature implementation crossed its frozen memory boundary
after 397.43 seconds and was interrupted without a terminal result; it makes no
algebraic claim. The equivalent predicate-compressed engine found thirteen
integer local normals after 224 states. Every local mass is one, every
predicate has either two ordinary killers or a strong killer, and the maximum
absolute coefficient is six.

`PROVED`: direct evaluation gives zero for all 1,394 \(F_t\) and all 221,646
raw \(x_{i,a}F_t\), including 31,768 automatic zero local entries. An
independent implementation rebuilt the allowed digits and every direct mask
as sets, reevaluated every raw labeled generator, and reproduced the ordinary
and strong kill histograms. It found no nonzero contraction and global mass
one.

Therefore applying \(L\) to any hypothetical degree-\(\le1\) identity gives
zero on its left side and one on its constant right side, a contradiction.

## Falsifiers

Any local mass different from one, any raw predicate or multiplier with
nonzero contraction, any mismatch between the ordinary-or-strong rule and raw
evaluation, or any one-hot option-order mismatch invalidates the claim.
Negative coefficients falsify any positivity interpretation.
