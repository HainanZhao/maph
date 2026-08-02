# Cycle 163 preregistration v1 correction: common-wrap mass condition

The original preregistration correctly freezes the factorization and the two
complexity scales, but its common-wrap mass sentence omitted the complementary
condition. `R_fiber>=H` alone does not imply `sum_mD_m^2>=D^2/H`.

The corrected dichotomy is:

1. `R_wrap>=H=X^(1/600-o(1))`: preserve weighted integer-wrap complexity.
2. `R_wrap<H`: then factorization and `R>=H^2` imply `R_fiber>=H`, while
   `sum_mD_m^2=D^2/R_wrap>D^2/H`. This is the common-wrap web arm.

Only the second arm retains common-wrap squared edge mass
`>>A2^2X^(1/200-o(1))`. This correction changes no frozen labels, threshold,
or claimed endpoint. It prevents a false mass implication.
