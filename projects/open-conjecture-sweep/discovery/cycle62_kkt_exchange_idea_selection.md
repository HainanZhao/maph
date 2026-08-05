# C62 idea selection: endpoint exchange rather than another local certificate

## Candidates

1. **Conjugacy-orbit KKT/exchange lemma (chosen).** On a normalized finite
   group function, assume a negative minimizer of the Zhao deficit and derive
   the exact Karush--Kuhn--Tucker equalities on its support. Test whether an
   unequal pair in one conjugacy class has an exchange direction with a
   forced descent, which would make every minimizer central.
2. **Higher-order local expansion.** Extend C61 to higher jets or more
   groups. This is rejected: C61 already excludes the relevant local pattern,
   and more local data does not constrain an endpoint minimizer.
3. **A larger Pólya/Gram certificate.** This is rejected for now because C57
   and C59 already delimit two coefficientwise certificate families; a larger
   resource tranche would preserve the same non-endpoint framing.
4. **Random finite-group countermodel search.** This remains a useful
   falsifier, but without a minimizer invariant it risks becoming another
   unconstrained census. It is retained only as C62's decisive negative test.

## Questioning the question

Why should a KKT condition help? Homogeneity and centralization make the
central subspace an equality manifold; a negative endpoint could lie on a
face, where naive interior gradients are inapplicable. The first task must
therefore classify support faces and derive complementary-slackness equations
before proposing a smooth exchange. A misleading framing would assume full
support or infer universal descent from the C61 local theorem. The simpler
discriminating alternative is to find one rational nonnegative countermodel;
that falsifies Zhao directly and is checked alongside every proposed exchange
identity.

## Chosen question and falsifier

For the frozen S3 probability simplex, can exact KKT/support equations plus
classwise exchange directions force every negative local minimizer to be
central? A rational nonnegative S3 function with negative deficit falsifies
the target comparison. Failure of a particular exchange identity only rejects
that identity family, not the comparison.
