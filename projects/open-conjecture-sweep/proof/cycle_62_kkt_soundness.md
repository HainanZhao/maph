# C62 KKT packet soundness and boundary

For an integer vector `a` on `S3`, let `B=6 P_cl(a)`. Homogeneity gives the
integer deficit `6^15 N(a)-N(B)`, so its sign is exactly the sign of
`N(a)-N(P_cl(a))`. The complete height-24 composition loop contains
`C(29,5)=118755` rows.

The simplex KKT check uses the full boundary conditions. All positive
coordinates have one common gradient value; every zero coordinate has
gradient at least that value. The earlier active-support-only diagnostic was
corrected before promotion. With complementary slackness included, all 61
grid-KKT rows are central.

Within either nontrivial conjugacy class, the centralization term has equal
coordinate derivatives and cancels from an exchange difference. Exact sparse
algebra factors the two remaining derivatives by the corresponding coordinate
difference. Their 7,082-term quotients have mixed signs, and multiplication by
the full coordinate sum through degree 24 never becomes coefficientwise
nonnegative. These are certificate-family no-gos, not exchange reversals.

The denominator-1000 probe is `OBSERVED` only. An initial signed-128-bit run
overflowed and is quarantined as invalid. The promoted replay uses
`boost::multiprecision::cpp_int`; three deterministic PCG64 streams totaling
300,000 rows then contain no negative deficit. The invalid outputs support no
claim and are not frozen evidence.

Nothing here classifies the continuous KKT system. A noncentral stationary
point or negative basin may lie between grid points. C62 therefore proves only
the frozen finite packet and exact algebraic certificate no-gos; it does not
prove continuous S3 comparison, Zhao's universal comparison, or Sidorenko.
