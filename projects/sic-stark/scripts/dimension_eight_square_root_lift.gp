\\ Test whether the distinguished primitive squared overlap has a square
\\ root inside its exact degree-32 ray field.

default(realprecision, 100);
default(parisizemax, 6000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

relative_polynomial = \
  x^16 + (-56*y - 32)*x^15 + (2696*y + 1668)*x^14 \
  + (-70632*y - 43656)*x^13 + (1085616*y + 670940)*x^12 \
  + (-10068808*y - 6222872)*x^11 \
  + (55400584*y + 34239444)*x^10 \
  + (-169674744*y - 104864752)*x^9 \
  + (255738816*y + 158055290)*x^8 \
  + (-169674744*y - 104864752)*x^7 \
  + (55400584*y + 34239444)*x^6 \
  + (-10068808*y - 6222872)*x^5 \
  + (1085616*y + 670940)*x^4 \
  + (-70632*y - 43656)*x^3 + (2696*y + 1668)*x^2 \
  + (-56*y - 32)*x + 1;
Hpol = rnfequation(y^2 - y - 1, relative_polynomial);
H = bnfinit(Hpol, 1);
H_generator = Mod(x, Hpol);
generator_exponents = bnfisunit(H, H_generator);
H_conjugates = nfgaloisconj(H);

print("PARI_VERSION=", version());
print("FIELD_SIGNATURE=", H.sign);
print("GENERATOR_UNIT_EXPONENTS=", generator_exponents);
assert_equal("GENERATOR_IS_A_UNIT", #generator_exponents > 0, 1);

free_rank = H.r1 + H.r2 - 1;
generator_parity = \
  vecsum(vector(#generator_exponents, index, \
    generator_exponents[index] % 2));
print("GENERATOR_SQUARE_PARITY_WEIGHT=", generator_parity);

square_ratio_count = 0;
verified_ratio_root_count = 0;
for(conjugate_index = 1, #H_conjugates, \
{
  my(conjugate = Mod(H_conjugates[conjugate_index], Hpol));
  my(ratio = conjugate / H_generator);
  my(exponents = bnfisunit(H, ratio));
  my(parity = vecsum(vector(#exponents, index, exponents[index] % 2)));
  my(ratio_root = Mod(1, Hpol));
  print(Str("CONJUGATE_", conjugate_index, "_RATIO_PARITY_WEIGHT="), \
    parity);
  if(parity == 0, \
    square_ratio_count++; \
    for(index = 1, free_rank, \
      ratio_root *= H.fu[index]^(exponents[index]/2)); \
    ratio_root *= H.tu[2]^(exponents[free_rank + 1]/2); \
    if(ratio_root^2 == ratio, verified_ratio_root_count++));
});
print("SQUARE_CONJUGATE_RATIO_COUNT=", square_ratio_count);
assert_equal("ALL_CONJUGATE_RATIOS_ARE_SQUARES", \
  square_ratio_count, #H_conjugates);
assert_equal("ALL_CONJUGATE_RATIO_ROOTS_VERIFIED", \
  verified_ratio_root_count, #H_conjugates);

signed_relative_polynomial = subst(relative_polynomial, x, x^2);
signed_absolute_polynomial = \
  rnfequation(y^2 - y - 1, signed_relative_polynomial);
print("SIGNED_OVERLAP_RELATIVE_DEGREE=", \
  poldegree(signed_relative_polynomial));
print("SIGNED_OVERLAP_ABSOLUTE_DEGREE=", \
  poldegree(signed_absolute_polynomial));
assert_equal("SIGNED_OVERLAP_POLYNOMIAL_IS_IRREDUCIBLE", \
  polisirreducible(signed_absolute_polynomial), 1);
print("DISTINGUISHED_ROOT_IS_NOT_A_SQUARE_IN_RAY_FIELD=1");
print("ONE_QUADRATIC_EXTENSION_CONTAINS_ALL_PRIMITIVE_SIGNED_ROOTS=1");

\\ The four nontrivial lower-conductor absolute values are the real roots
\\ of this reciprocal degree-eight polynomial.  The analytic identification
\\ is a separate root-isolation step; here we certify the exact field
\\ containment needed by the finite calculation.
lower_conductor_polynomial = \
  x^8 - 8*x^7 + 12*x^6 + 8*x^5 - 22*x^4 \
    + 8*x^3 + 12*x^2 - 8*x + 1;
assert_equal("LOWER_CONDUCTOR_POLYNOMIAL_IS_IRREDUCIBLE", \
  polisirreducible(lower_conductor_polynomial), 1);
assert_equal("LOWER_CONDUCTOR_REAL_ROOT_COUNT", \
  polsturm(lower_conductor_polynomial), 4);
lower_inclusions = nfisincl( \
  lower_conductor_polynomial, signed_absolute_polynomial, 2);
print("LOWER_CONDUCTOR_FIELD_INCLUSION_COUNT=", #lower_inclusions);
assert_equal("LOWER_CONDUCTOR_FIELD_LIES_IN_SIGNED_FIELD", \
  #lower_inclusions > 0, 1);

quit();
