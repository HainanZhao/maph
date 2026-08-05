# Cycle 16: canonical gcd-witness partition

For an admissible first lift, at most eleven of the thirteen selected speeds
are divisible by 2 and at most eleven are divisible by 7.  Hence at least two
coordinate indices are nondivisible by each prime.  The first two such indices
are a unique pair `(i,j)` for 2 and a unique pair `(u,v)` for 7.  Conversely,
the canonical conditions for any two pairs force at least two nondivisible
coordinates for each prime.  The `78^2 = 6084` pair states are therefore
disjoint and cover exactly the gcd-admissible assignments.

A canonical condition is encoded only by forbidding choice variables.  Before
`i`, every selected residue must be divisible by 2; at `i` it must not be;
between `i` and `j` it must be divisible; at `j` it must not be; later choices
are unrestricted.  The same rule is conjoined for 7.  A negative unit is added
for each base-dependent digit whose lifted residue violates either required
condition.  Since the Cycle-11 CNF already chooses exactly one digit in every
coordinate, the residual CNF is satisfiable exactly when that canonical leaf
contains an improper first lift.

Thus checked UNSAT certificates for all 6084 residuals independently imply
that the named base has no improper first lift.  A partial tree proves only its
certified leaves.  Proof size, solver speed, and learned structural patterns
are not proof; any transferred leaf core must remain an exact clause subset
under a fully checked literal map.
