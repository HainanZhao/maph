# C53 idea selection: analytic local stability at the constant graphon

## Candidates

1. **Quadratic-form / kernel route (chosen).** Expand the homomorphism density
   at \(W\equiv1/2\) for an arbitrary bounded symmetric zero-mean kernel
   \(U\).  Classify edge pairs in the 3-regular Möbius graph.  The only
   nonzero quadratic terms should be adjacent edge pairs, giving a positive
   multiple of \(\|x\mapsto\int U(x,y)dy\|_2^2\).  On the zero-degree
   kernel, enumerate the first surviving edge subsets; if they are precisely
   four-cycles, their contribution is a positive multiple of
   \(\operatorname{tr}(T_U^4)\).  A rigorous remainder bound would turn that
   lexicographic positivity into a local theorem for each bounded nonzero
   perturbation.

2. **Larger step-graphon census.** It could find a candidate at q=4 or with
   unequal parts, but C52 already shows that finite direction enumeration
   becomes a weak proxy for the analytic local question.  It is rejected as a
   continuation of the same census rather than a discriminating new engine.

3. **Finite extremizer/entropy search.** It might identify a global
   competitor, but without first locating Hessian-flat directions it is an
   undirected nonconvex search.  It is deferred until the local structure
   tells us what a plausible competitor must avoid.

## Question the question

Why is a positive quadratic form not already a Sidorenko proof?  It controls
only a neighborhood of the constant graphon; a global minimizer may be far
away.  Why might the quadratic framing mislead?  The zero-degree kernel is
infinite-dimensional, so coercivity can fail there.  The discriminating
alternative is to compute—not assume—the first nonzero kernel form and to
derive a uniform enough finite-degree remainder estimate.  If a selected
edge-subset term outside the claimed adjacent-pair/four-cycle classes
survives under the relevant zero-mean constraints, or if its coefficient can
be negative, the proposed theorem is falsified.

## Choice and falsifier

Choose the analytic quadratic/kernel route.  Its advance is an exact identity
and a checked remainder theorem for every bounded symmetric kernel in the
stated class, not merely a finite sample.  The primary falsifier is an exact
edge-subset classification showing a nonzero term incompatible with the
claimed positive form; a secondary falsifier is an explicit bounded rational
kernel with a negative first surviving coefficient.
