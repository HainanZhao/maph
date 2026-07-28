\\ Exact Artin and archimedean labels for the d=7 signed overlap packet.
\\
\\ This closes the ordering ambiguity left by an abstract field isomorphism:
\\ ray generators [1,0] and [0,1] are identified with explicit H/K
\\ automorphisms by local Frobenius, and every characteristic is matched to
\\ the corresponding exact real root through a rational interval.

default(parisizemax, 2000000000);
default(realprecision, 80);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

iadd(first, second) =
  [first[1] + second[1], first[2] + second[2]];
imul(first, second) =
{
  my(values = [
    first[1]*second[1], first[1]*second[2],
    first[2]*second[1], first[2]*second[2]
  ]);
  [vecmin(values), vecmax(values)];
};
ieval(polynomial, interval) =
{
  my(value = [0, 0]);
  forstep(degree = poldegree(polynomial), 0, -1,
    value = iadd(
      imul(value, interval),
      [polcoef(polynomial, degree), polcoef(polynomial, degree)]
    )
  );
  value;
};
is_subset(inner, outer) =
  inner[1] >= outer[1] && inner[2] <= outer[2];

K = bnfinit(y^2 - 2, 1);
ray14 = bnrinit(K, [[14, 0; 0, 14], [1, 0]], 1);
ray7 = bnrinit(K, [[7, 0; 0, 7], [1, 0]], 1);
full_modulus = idealhnf(K, 14);
seven_modulus = idealhnf(K, 7);
alpha_reduced = Mod(2 + y, y^2 - 2);

projection14to7 = matrix(1, 2, row, column, \
  bnrisprincipal(ray7, ray14.gen[column], 0)[row]);
assert_equal("RAY_14_TO_7_PROJECTION", projection14to7, Mat([2, 3]));

Hpol = x^24 - 8*x^23 + 6*x^22 + 100*x^21 - 336*x^20 \
  + 264*x^19 + 834*x^18 - 2980*x^17 + 5038*x^16 - 5748*x^15 \
  + 5084*x^14 - 4060*x^13 + 3611*x^12 - 4060*x^11 \
  + 5084*x^10 - 5748*x^9 + 5038*x^8 - 2980*x^7 + 834*x^6 \
  + 264*x^5 - 336*x^4 + 100*x^3 + 6*x^2 - 8*x + 1;

H = nfinit(Hpol);
H_generator = Mod(x, Hpol);
H_conjugates = nfgaloisconj(H);
generator_interval = [ \
  24298120154607662818424148631780884972067133872553900249933286935412960 \
    / 10^70, \
  24298120154607662818424148631780884972067133872553900249933286935412961 \
    / 10^70 \
];
assert_equal("DISTINGUISHED_GENERATOR_ROOT_COUNT", \
  polsturm(Hpol, generator_interval), 1);

sqrt_two_inclusions = nfisincl(x^2 - 2, Hpol, 2);
sqrt_two_H = 0;
for(index = 1, #sqrt_two_inclusions, \
  candidate_sqrt_two = Mod(sqrt_two_inclusions[index], Hpol); \
  candidate_interval = ieval(lift(candidate_sqrt_two), generator_interval); \
  if(is_subset(candidate_interval, [14/10, 15/10]), \
    sqrt_two_H = candidate_sqrt_two));
if(!sqrt_two_H, error("positive sqrt(2) inclusion was not isolated"));

\\ Certify that H is the full one-place ray-14 field over the labeled copy
\\ of K, rather than only an abstractly isomorphic degree-24 field.
\\ rnfequation(...,1) retains the image of the base generator y, allowing
\\ the isomorphisms to be tested over K exactly.
ray14_relative_polynomial = bnrclassfield(ray14, , 1);
ray14_equation = rnfequation(K, ray14_relative_polynomial, 1);
ray14_absolute_polynomial = ray14_equation[1];
sqrt_two_in_ray14 = Mod(ray14_equation[2], ray14_absolute_polynomial);
H_to_ray14_isomorphisms = nfisisom(Hpol, ray14_absolute_polynomial);
base_preserving_isomorphisms = 0;
for(index = 1, #H_to_ray14_isomorphisms, \
  candidate_isomorphism = Mod( \
    H_to_ray14_isomorphisms[index], ray14_absolute_polynomial \
  ); \
  image_sqrt_two = subst( \
    lift(sqrt_two_H), x, candidate_isomorphism \
  ); \
  if(image_sqrt_two == sqrt_two_in_ray14, \
    base_preserving_isomorphisms++));
assert_equal("RAY_14_RELATIVE_DEGREE", \
  poldegree(ray14_relative_polynomial), 12);
assert_equal("RAY_14_ABSOLUTE_DEGREE", \
  poldegree(ray14_absolute_polynomial), 24);
assert_equal("H_TO_RAY_14_ISOMORPHISM_COUNT", \
  #H_to_ray14_isomorphisms, 12);
assert_equal("H_TO_RAY_14_BASE_PRESERVING_COUNT", \
  base_preserving_isomorphisms, 12);

\\ Identify arithmetic Frobenius at the split prime above 17 with ray log
\\ [1,0], and at the split prime above 41 with ray log [0,1].
identify_frobenius(rational_prime, base_prime_index) =
{
  my(base_primes = idealprimedec(K, rational_prime));
  my(base_prime = base_primes[base_prime_index]);
  my(base_log = Vec(bnrisprincipal(ray14, base_prime, 0)));
  my(alpha = base_prime[2][1] + base_prime[2][2]*sqrt_two_H);
  my(H_primes = idealprimedec(H, rational_prime));
  my(answer = 0, modulus, target, matches);

  for(prime_index = 1, #H_primes,
    modulus = nfmodprinit(H, H_primes[prime_index]);
    if(nfmodpr(H, alpha, modulus) == 0,
      target = nfmodpr(H, H_generator, modulus)^rational_prime;
      matches = List();
      for(index = 1, #H_conjugates,
        if(
          nfmodpr(H, Mod(H_conjugates[index], Hpol), modulus) == target,
          listput(matches, index)
        )
      );
      if(#matches != 1,
        error(Str("Frobenius match count ", #matches)));
      if(answer && answer != matches[1],
        error("inconsistent Frobenius over primes above the same K-prime"));
      answer = matches[1]
    )
  );
  [base_log, answer];
};

frobenius17 = identify_frobenius(17, 2);
frobenius41 = identify_frobenius(41, 2);
assert_equal("PRIME_17_RAY_LOG", frobenius17[1], [1, 0]);
assert_equal("PRIME_17_AUTOMORPHISM_INDEX", frobenius17[2], 5);
assert_equal("PRIME_41_RAY_LOG", frobenius41[1], [0, 1]);
assert_equal("PRIME_41_AUTOMORPHISM_INDEX", frobenius41[2], 10);

ray_generator_six = Mod(H_conjugates[frobenius17[2]], Hpol);
ray_generator_two = Mod(H_conjugates[frobenius41[2]], Hpol);

act(automorphism, element) =
{
  subst(lift(automorphism), x, element);
};

artin_image(log_vector) =
{
  my(element = H_generator);
  for(index = 1, log_vector[1],
    element = act(ray_generator_six, element));
  if(log_vector[2], element = act(ray_generator_two, element));
  element;
};

positive_representative(gamma) =
{
  my(answer = gamma);
  while(subst(lift(answer), y, -sqrt(2)) <= 0, answer += 14);
  answer;
};

factor_class(first, second, lift_index) =
{
  my(gamma = 2*second*alpha_reduced - first - second - 7*lift_index);
  my(positive_gamma = positive_representative(gamma));
  my(gamma_ideal = idealhnf(K, positive_gamma));
  my(common = idealadd(K, full_modulus, gamma_ideal));
  my(reduced_modulus = idealdiv(K, full_modulus, common));
  my(reduced_ideal = idealdiv(K, gamma_ideal, common));
  my(ray = bnrinit(K, [reduced_modulus, [1, 0]], 1));
  [reduced_modulus, Vec(bnrisprincipal(ray, reduced_ideal, 0))];
};

\\ [a,b,left,right] for the twelve representatives in the full ray orbit.
full_packet() =
{
  [
    0, 1, 2429/1000, 2430/1000;
    0, 2, 1781/1000, 1782/1000;
    0, 3, 1220/1000, 1221/1000;
    0, 4,  819/1000,  820/1000;
    0, 5,  561/1000,  562/1000;
    0, 6,  411/1000,  412/1000;
    1, 1, -383/1000, -382/1000;
    1, 3, -284/1000, -283/1000;
    2, 2,  208/1000,  209/1000;
    2, 6, -2614/1000, -2613/1000;
    4, 4, -3533/1000, -3532/1000;
    4, 5, 4793/1000, 4794/1000
  ];
};

packet = full_packet();
base_ray7_log = 4;

audit_full_characteristic(row) =
{
  my(first = packet[row, 1], second = packet[row, 2]);
  my(factors = vector(2, index,
    factor_class(first, second, index - 1)));
  my(full_index = 0, seven_index = 0);
  my(full_log, seven_log, projected_log, candidate, image_interval);

  for(index = 1, 2,
    if(factors[index][1] == full_modulus, full_index = index);
    if(factors[index][1] == seven_modulus, seven_index = index)
  );
  if(!full_index || !seven_index,
    error(Str("missing full/seven factors for ", [first, second])));

  full_log = factors[full_index][2];
  seven_log = factors[seven_index][2][1];
  projected_log =
    (base_ray7_log + (projection14to7*Col(full_log))[1]) % 6;
  assert_equal(
    Str("CHAR_", first, "_", second, "_RAY7_COMPATIBLE"),
    seven_log,
    projected_log
  );

  candidate = artin_image(full_log);
  image_interval = ieval(lift(candidate), generator_interval);
  assert_equal(
    Str("CHAR_", first, "_", second, "_TARGET_ROOT_COUNT"),
    polsturm(Hpol, [packet[row, 3], packet[row, 4]]),
    1
  );
  assert_equal(
    Str("CHAR_", first, "_", second, "_ROOT_INTERVAL"),
    is_subset(
      image_interval,
      [packet[row, 3], packet[row, 4]]
    ),
    1
  );
  print(
    "CHAR_", first, "_", second,
    "_FULL_RAY_LOG=", full_log,
    " ROOT_INTERVAL_CERTIFIED=1"
  );
};

for(row = 1, matsize(packet)[1], audit_full_characteristic(row));

\\ The two quadratic strata each have a nontrivial ray involution.  Exact
\\ class logs distinguish the large root (class 0) from its reciprocal
\\ small root (class 1).
plus_polynomial = x^4 - 2*x^3 - 5*x^2 - 2*x + 1;
minus_polynomial = x^4 - 4*x^3 + 4*x^2 - 4*x + 1;
plus_inclusions = nfisincl(plus_polynomial, Hpol, 2);
minus_inclusions = nfisincl(minus_polynomial, Hpol, 2);

subfield_root(polynomial, inclusions, left, right) =
{
  my(matches = 0, answer, image_interval);
  if(polsturm(polynomial, [left, right]) != 1,
    error(Str("target subfield-root count is not one: ", [left, right])));
  for(index = 1, #inclusions,
    answer = Mod(inclusions[index], Hpol);
    image_interval = ieval(lift(answer), generator_interval);
    if(is_subset(image_interval, [left, right]),
      matches++;
      result = answer)
  );
  if(matches != 1, error(Str("subfield root matches=", matches)));
  result;
};

audit_quadratic_pair(label, polynomial, large_characteristic, \
    small_characteristic, inclusions, large_left, large_right, \
    small_left, small_right) =
{
  my(large_factors = vector(2, index,
    factor_class(
      large_characteristic[1],
      large_characteristic[2],
      index - 1
    )
  ));
  my(small_factors = vector(2, index,
    factor_class(
      small_characteristic[1],
      small_characteristic[2],
      index - 1
    )
  ));
  my(large_nontrivial = List(), small_nontrivial = List());
  my(large_root, small_root);

  for(index = 1, 2,
    if(#large_factors[index][2],
      listput(large_nontrivial, large_factors[index][2][1]));
    if(#small_factors[index][2],
      listput(small_nontrivial, small_factors[index][2][1]))
  );
  assert_equal(Str(label, "_LARGE_CLASS_LOGS"), \
    Vec(large_nontrivial), vector(#large_nontrivial));
  assert_equal(Str(label, "_SMALL_CLASS_LOGS"), \
    Vec(small_nontrivial), vector(#small_nontrivial, index, 1));

  large_root = subfield_root(
    polynomial, inclusions, large_left, large_right
  );
  small_root = subfield_root(
    polynomial, inclusions, small_left, small_right
  );
  assert_equal(Str(label, "_RECIPROCAL_ROOTS"), large_root*small_root, 1);
};

audit_quadratic_pair("PLUS_STRATUM", plus_polynomial, [3, 5], [1, 4], \
  plus_inclusions, 3546/1000, 3547/1000, 281/1000, 282/1000);
audit_quadratic_pair("MINUS_STRATUM", minus_polynomial, [3, 6], [1, 2], \
  minus_inclusions, 3090/1000, 3091/1000, 323/1000, 324/1000);

print("ALL_ARTIN_AND_ROOT_LABELS_CERTIFIED=1");

quit();
