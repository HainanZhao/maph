\\ Unconditional Shintani algebraicity audit for the lower d=8 stratum.

default(realprecision, 80);
default(parisize, 128000000);
default(parisizemax, 3000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

K = bnfinit(y^2 - y - 1, 1);
ray_one = bnrinit(K, [12, [1, 0]], 1);
ray_both = bnrinit(K, [12, [1, 1]], 1);
lower_polynomial = \
  x^8 - 8*x^7 + 12*x^6 + 8*x^5 - 22*x^4 \
    + 8*x^3 + 12*x^2 - 8*x + 1;

assert_equal("BASE_BNFCERTIFY", bnfcertify(K), 1);
assert_equal("ONE_PLACE_RAY_GROUP", ray_one.cyc, [2, 2]);
assert_equal("BOTH_PLACE_RAY_GROUP", ray_both.cyc, [2, 2, 2]);
lower_ray_field = bnrclassfield(ray_one, , 2);
assert_equal("LOWER_POLYNOMIAL_MATCHES_RAY_12", \
  #nfisisom(lower_polynomial, lower_ray_field) > 0, 1);

\\ Shintani's two unit congruence hypotheses.  The fundamental unit phi
\\ has order 24 modulo 12, no power is -1, and no signed odd power
\\ (the negative-norm units) is 1.
residue_phi = Mod(y, Mod(1, 12)*(y^2 - y - 1));
phi_order = 0;
for(exponent = 1, 24, \
  if(!phi_order && residue_phi^exponent == 1, phi_order = exponent));
positive_minus_one = sum(exponent = 0, 11, \
  residue_phi^(2*exponent) == -1);
negative_norm_one = 0;
forstep(exponent = 1, 23, 2, \
  for(sign_index = 0, 1, \
    if((-1)^sign_index*residue_phi^exponent == 1, \
      negative_norm_one++)));
assert_equal("PHI_ORDER_MOD_12", phi_order, 24);
assert_equal("SHINTANI_CONDITION_POSITIVE_NOT_MINUS_ONE", \
  positive_minus_one, 0);
assert_equal("SHINTANI_CONDITION_NEGATIVE_NORM_NOT_ONE", \
  negative_norm_one, 0);

\\ The commutator subgroup and the kernel of forgetting infinity_2 are
\\ distinct order-two subgroups.  Hence [H:H cap Q^ab]=2.
base_conjugation = Mod(1 - y, y^2 - y - 1);
conjugation = matrix(3, 3, row, column, \
  bnrisprincipal(ray_both, \
    nfgaloisapply(K, base_conjugation, ray_both.gen[column]), 0)[row]);
forgetful = matrix(2, 3, row, column, \
  bnrisprincipal(ray_one, ray_both.gen[column], 0)[row]);
commutator = [0, 1, 0]~;
one_place_kernel = [1, 0, 1]~;
assert_equal("CONJUGATION_MATRIX", conjugation, \
  [1, 0, 0; 0, 1, 1; 0, 0, 1]);
assert_equal("FORGETFUL_MATRIX", forgetful, [1, 0, 1; 0, 1, 0]);
assert_equal("COMMUTATOR_GENERATOR", \
  vector(3, row, \
    (conjugation[row, 3] - (row == 3)) % 2), Vec(commutator));
assert_equal("ONE_PLACE_KERNEL_IMAGE", \
  vector(2, row, sum(column = 1, 3, \
    forgetful[row, column]*one_place_kernel[column]) % 2), [0, 0]);
assert_equal("KERNEL_EQUALS_COMMUTATOR", \
  one_place_kernel == commutator, 0);
print("SHINTANI_INDEX=2");

\\ The normal closure is abelian over Q(sqrt(-5)).  Its conductor there
\\ is (6)=p_2^2 p_3 pbar_3.
normal_closure = bnrclassfield(ray_both, , 2);
imaginary_base = bnfinit(y^2 + 5, 1);
relative_normal_closure = nffactor( \
  imaginary_base, normal_closure)[1, 1];
assert_equal("IMAGINARY_BASE_CLASS_NUMBER", imaginary_base.no, 2);
assert_equal("IMAGINARY_BASE_BNFCERTIFY", \
  bnfcertify(imaginary_base), 1);
assert_equal("NORMAL_CLOSURE_ABELIAN_OVER_Q_SQRT_MINUS_5", \
  rnfisabelian(imaginary_base, relative_normal_closure), 1);
conductor_data = rnfconductor( \
  imaginary_base, relative_normal_closure, 2);
imaginary_conductor = conductor_data[1][1];
conductor_factorization = conductor_data[2];
assert_equal("IMAGINARY_CONDUCTOR", imaginary_conductor, \
  [6, 0; 0, 6]);
print("IMAGINARY_CONDUCTOR_FACTORIZATION=", conductor_factorization);

imaginary_ray = bnrinit(imaginary_base, imaginary_conductor, 1);
assert_equal("IMAGINARY_RAY_GROUP", imaginary_ray.cyc, [4, 2]);
clearing_exponents = List();
root_counts = List();

audit_divisor(e2, e3a, e3b) =
{
  my(divisor = matid(2), divisor_ray_order, roots_of_unity);
  my(distribution_index, smallest_integer, clearing_exponent);
  if(e2, divisor = idealmul(imaginary_base, divisor, \
    idealpow(imaginary_base, conductor_factorization[1, 1], e2)));
  if(e3a, divisor = idealmul(imaginary_base, divisor, \
    conductor_factorization[2, 1]));
  if(e3b, divisor = idealmul(imaginary_base, divisor, \
    conductor_factorization[3, 1]));
  divisor = idealhnf(imaginary_base, divisor);
  divisor_ray_order = bnrinit(imaginary_base, divisor).no;
  roots_of_unity = 1 + ( \
    idealadd(imaginary_base, divisor, idealhnf(imaginary_base, 2)) \
      == divisor);
  distribution_index = \
    roots_of_unity*imaginary_ray.no/divisor_ray_order;
  smallest_integer = divisor[1, 1];
  clearing_exponent = if(e2 + e3a + e3b == 0, \
    12*imaginary_base.no*distribution_index, \
    12*smallest_integer*distribution_index);
  listput(clearing_exponents, clearing_exponent);
  listput(root_counts, roots_of_unity);
  print("DIVISOR_", e2, "_", e3a, "_", e3b, \
    "_CLEARING_EXPONENT=", clearing_exponent);
};

for(e2 = 0, 2, \
  for(e3a = 0, 1, \
    for(e3b = 0, 1, audit_divisor(e2, e3a, e3b))));
assert_equal("SHINTANI_DIVISOR_COUNT", #clearing_exponents, 12);
assert_equal("ROOT_COUNT_TWO_DIVISORS", \
  sum(index = 1, #root_counts, root_counts[index] == 2), 3);
assert_equal("SHINTANI_SAFE_EXPONENT", \
  lcm(Vec(clearing_exponents)), 576);

\\ The real distribution indices along every divisor of (12) have lcm 8,
\\ already dividing 576.
real_factorization = idealfactor(K, idealhnf(K, 12));
real_indices = List();
for(e2 = 0, real_factorization[1, 2], \
  for(e3 = 0, real_factorization[2, 2], \
    divisor = matid(2); \
    if(e2, divisor = idealmul(K, divisor, \
      idealpow(K, real_factorization[1, 1], e2))); \
    if(e3, divisor = idealmul(K, divisor, \
      idealpow(K, real_factorization[2, 1], e3))); \
    divisor = idealhnf(K, divisor); \
    divisor_ray = bnrinit(K, [divisor, [1, 1]], 1); \
    listput(real_indices, ray_both.no/divisor_ray.no)));
assert_equal("REAL_DISTRIBUTION_INDEX_LCM", \
  lcm(Vec(real_indices)), 8);
assert_equal("REAL_DENOMINATORS_CLEARED", 576 % 8 == 0, 1);

print("LOWER_DIMENSION_EIGHT_SHINTANI_ALGEBRAICITY_CERTIFIED=1");
quit();
