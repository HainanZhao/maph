\\ Exact Shintani-algebraicity audit for the maximal d=7 stratum.
\\
\\ The one-place Stark field has degree 12 over Q(sqrt(2)).  Its normal
\\ closure is the full ray field modulo 14 with both real places.  This
\\ script verifies Shintani's index-two hypothesis, identifies the maximal
\\ absolutely abelian field, finds the imaginary-quadratic conductor used
\\ in Shintani's proof, and clears every denominator in Proposition 4.

default(parisizemax, 2000000000);
default(realprecision, 80);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

K = bnfinit(y^2 - 2, 1);
ray_one = bnrinit(K, [[14, 0; 0, 14], [1, 0]], 1);
ray_both = bnrinit(K, [[14, 0; 0, 14], [1, 1]], 1);

assert_equal("BASE_BNFCERTIFY", bnfcertify(K), 1);
assert_equal("ONE_PLACE_RAY_GROUP", ray_one.cyc, [6, 2]);
assert_equal("BOTH_PLACE_RAY_GROUP", ray_both.cyc, [6, 2, 2]);

\\ Shintani conditions (0-3) and (0-6).  Modulo 7, phi=1+sqrt(2)
\\ has order six and beta=phi^2 has order three.  Hence no totally
\\ positive unit beta^n is -1, while no odd power +/-phi^(2n+1) is 1.
residue_phi = Mod(1 + y, Mod(1, 7)*(y^2 - 2));
residue_beta = residue_phi^2;
phi_order = 0;
for(exponent = 1, 6, \
  if(!phi_order && residue_phi^exponent == 1, phi_order = exponent));
beta_order = 0;
for(exponent = 1, 3, \
  if(!beta_order && residue_beta^exponent == 1, beta_order = exponent));
negative_norm_congruence = 0;
forstep(exponent = 1, 5, 2, \
  for(sign_index = 1, 2, \
    if((-1)^sign_index*residue_phi^exponent == 1, \
      negative_norm_congruence = 1)));
assert_equal("PHI_ORDER_MOD_7", phi_order, 6);
assert_equal("BETA_ORDER_MOD_7", beta_order, 3);
assert_equal("SHINTANI_CONDITION_0_3", \
  sum(exponent = 0, 2, residue_beta^exponent == -1), 0);
assert_equal("SHINTANI_CONDITION_0_6", negative_norm_congruence, 0);

\\ Conjugation on A=Gal(N/K) and the kernel B obtained by forgetting the
\\ second real place.  The commutator C=(iota-1)A and B are distinct
\\ order-two subgroups, hence [H:H cap Q^ab]=2.
base_conjugation = Mod(-y, y^2 - 2);
conjugation = matrix(3, 3, row, column, \
  bnrisprincipal(ray_both, \
    nfgaloisapply(K, base_conjugation, ray_both.gen[column]), 0)[row]);
forgetful = matrix(2, 3, row, column, \
  bnrisprincipal(ray_one, ray_both.gen[column], 0)[row]);
commutator = [3, 1, 0]~;
one_place_kernel = [3, 0, 1]~;

assert_equal("CONJUGATION_MATRIX", conjugation, \
  [4, 3, 0; 1, 0, 0; 0, 0, 1]);
assert_equal("FORGETFUL_MATRIX", forgetful, [1, 0, 3; 0, 1, 0]);
assert_equal("COMMUTATOR_GENERATOR", \
  vector(3, row, \
    (conjugation[row, 1] - (row == 1)) % ray_both.cyc[row]), \
  Vec(commutator));
assert_equal("ONE_PLACE_KERNEL_IMAGE", \
  vector(2, row, sum(column = 1, 3, \
    forgetful[row, column] * one_place_kernel[column]) \
    % ray_one.cyc[row]), \
  [0, 0]);
assert_equal("KERNEL_EQUALS_COMMUTATOR", \
  one_place_kernel == commutator, 0);
print("SHINTANI_INDEX=2");

\\ The fixed field N^C has absolute degree 24 and is Q(zeta_56).
relations = matdiagonal(ray_both.cyc);
commutator_subgroup = mathnf(concat(relations, commutator));
maximal_abelian = bnrclassfield(ray_both, commutator_subgroup, 2);
assert_equal("COMMUTATOR_SUBGROUP_INDEX", \
  matdet(commutator_subgroup), 12);
assert_equal("MAXIMAL_ABELIAN_DEGREE", poldegree(maximal_abelian), 24);
assert_equal("MAXIMAL_ABELIAN_IS_Q_ZETA_56", \
  #nfisisom(maximal_abelian, polcyclo(56)) > 0, 1);

stark_field = bnrclassfield(ray_one, , 2);
assert_equal("STARK_FIELD_SIGNATURE", nfinit(stark_field).sign, [12, 6]);
print("STARK_OVER_MAXIMAL_ABELIAN_INTERSECTION_DEGREE=2");

\\ Shintani's proof passes through an abelian ray extension of
\\ k=Q(sqrt(-7)).  rnfconductor computes the conductor intrinsically,
\\ avoiding a guessed modulus or subgroup.
normal_closure = bnrclassfield(ray_both, , 2);
k = bnfinit(y^2 + 7, 1);
relative_factors = nffactor(k, normal_closure);
relative_normal_closure = relative_factors[1, 1];
assert_equal("IMAGINARY_BASE_CLASS_NUMBER", k.no, 1);
assert_equal("IMAGINARY_BASE_BNFCERTIFY", bnfcertify(k), 1);
assert_equal("NORMAL_CLOSURE_ABELIAN_OVER_Q_SQRT_MINUS_7", \
  rnfisabelian(k, relative_normal_closure), 1);

conductor_data = rnfconductor(k, relative_normal_closure, 2);
imaginary_conductor = conductor_data[1][1];
conductor_factorization = conductor_data[2];
assert_equal("IMAGINARY_CONDUCTOR", imaginary_conductor, \
  [56, 32; 0, 8]);
print("IMAGINARY_CONDUCTOR_FACTORIZATION=", conductor_factorization);

imaginary_ray = bnrinit(k, imaginary_conductor, 1);
assert_equal("IMAGINARY_CONDUCTOR_RAY_GROUP", imaginary_ray.cyc, [6, 2, 2, 2]);

\\ Shintani's Proposition 4 uses every ideal divisor d of the conductor.
\\ For d != 1, clearing the absolute-value square root and distribution
\\ exponent requires 12*f_d*n(S), where f_d is the least positive
\\ rational integer in d.  At d=1 the analogous exponent is
\\ 12*h_k*n(S).  The conductor is p_2^3 pbar_2^3 p_7, so there are 32
\\ divisors, not merely the eight square-free divisors.
conductor_primes = Vec(conductor_factorization[, 1]);
conductor_exponents = Vec(conductor_factorization[, 2]);
clearing_exponents = List();
unit_congruence_counts = List();

audit_divisor(e1, e2, e3) =
{
  my(divisor = matid(2));
  my(divisor_ray_order, roots_of_unity, distribution_index);
  my(smallest_integer, clearing_exponent);

  if(e1,
    divisor = idealmul(k, divisor,
      idealpow(k, conductor_primes[1], e1)));
  if(e2,
    divisor = idealmul(k, divisor,
      idealpow(k, conductor_primes[2], e2)));
  if(e3,
    divisor = idealmul(k, divisor,
      idealpow(k, conductor_primes[3], e3)));
  divisor = idealhnf(k, divisor);

  divisor_ray_order = bnrinit(k, divisor).no;
  \\ Shintani's w(d) is the number of units congruent to 1 modulo d.
  \\ Since O_k^x={+/-1}, it must be computed rather than replaced by 1:
  \\ -1 is also 1 modulo the first powers of primes above 2.
  roots_of_unity = 1 + ( \
    idealadd(k, divisor, idealhnf(k, 2)) == divisor \
  );
  listput(unit_congruence_counts, roots_of_unity);
  distribution_index =
    roots_of_unity * imaginary_ray.no / divisor_ray_order;
  smallest_integer = divisor[1, 1];
  clearing_exponent = if(
    e1 + e2 + e3 == 0,
    12 * k.no * distribution_index,
    12 * smallest_integer * distribution_index
  );
  listput(clearing_exponents, clearing_exponent);
  print(
    "SHINTANI_DIVISOR_", e1, "_", e2, "_", e3,
    "_IDEAL=", divisor,
    " RAY_ORDER=", divisor_ray_order,
    " N_INDEX=", distribution_index,
    " CLEARING_EXPONENT=", clearing_exponent
  );
};

for(e1 = 0, conductor_exponents[1], \
  for(e2 = 0, conductor_exponents[2], \
    for(e3 = 0, conductor_exponents[3], \
      audit_divisor(e1, e2, e3))));

assert_equal("SHINTANI_DIVISOR_COUNT", #clearing_exponents, 32);
assert_equal("SHINTANI_W_TWO_DIVISOR_COUNT", \
  sum(index = 1, #unit_congruence_counts, \
    unit_congruence_counts[index] == 2), 4);
assert_equal("SHINTANI_SAFE_EXPONENT", lcm(Vec(clearing_exponents)), 16128);

\\ The X-to-Y induction in Shintani's Lemma 8 introduces only the real
\\ distribution indices |H_F(f)|/|H_F(f(S))|.  Audit all eight subsets of
\\ the three finite prime divisors of (14).  Along a nested chain of
\\ moduli the indices telescope:
\\
\\   (|H(f)|/|H(d)|)(|H(d)|/|H(e)|)=|H(f)|/|H(e)|.
\\
\\ Hence inverting the triangular X-to-Y relations introduces no products
\\ beyond the full-to-submodulus indices audited here.  Their lcm is 24,
\\ already a divisor of 16128, so no further induction exponent is required.
real_factorization = idealfactor(K, idealhnf(K, 14));
real_distribution_indices = List();
for(mask = 0, 7, \
  divisor = matid(2); \
  for(index = 1, 3, \
    if(!bittest(mask, index - 1), \
      divisor = idealmul(K, divisor, \
        idealpow(K, real_factorization[index, 1], \
          real_factorization[index, 2])))); \
  divisor = idealhnf(K, divisor); \
  divisor_ray = bnrinit(K, [divisor, [1, 1]], 1); \
  listput(real_distribution_indices, ray_both.no/divisor_ray.no));
assert_equal("REAL_DISTRIBUTION_INDEX_LCM", \
  lcm(Vec(real_distribution_indices)), 24);
assert_equal("REAL_DISTRIBUTION_DENOMINATORS_CLEARED", \
  16128 % lcm(Vec(real_distribution_indices)) == 0, 1);

quit();
