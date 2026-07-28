\\ Exact Artin labels for the sixteen primitive squared d=8 overlaps.

default(realprecision, 100);
default(parisizemax, 3000000000);

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

K = bnfinit(y^2 - y - 1, 1);
ray24 = bnrinit(K, [24, [1, 0]], 1);

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
H = nfinit(Hpol);
H_generator = Mod(x, Hpol);
H_conjugates = nfgaloisconj(H);
assert_equal("RAY_GROUP", ray24.cyc, [4, 2, 2]);
assert_equal("H_AUTOMORPHISM_COUNT", #H_conjugates, 16);

generator_interval = [ \
  69109374262288169846434600299567179964040849270327183006592698019167902 \
    / 10^70, \
  69109374262288169846434600299567179964040849270327183006592698019167903 \
    / 10^70 \
];
assert_equal("DISTINGUISHED_ROOT_COUNT", \
  polsturm(Hpol, generator_interval), 1);

base_inclusions = nfisincl(y^2 - y - 1, Hpol, 2);
phi_H = 0;
for(index = 1, #base_inclusions, \
  candidate_phi = Mod(base_inclusions[index], Hpol); \
  candidate_interval = ieval(lift(candidate_phi), generator_interval); \
  if(is_subset(candidate_interval, [16/10, 17/10]), \
    phi_H = candidate_phi));
if(!phi_H, error("positive base-field inclusion was not isolated"));
assert_equal("POSITIVE_PHI_MINPOLY", phi_H^2 - phi_H - 1, 0);

identify_frobenius(rational_prime, base_prime_index) =
{
  my(base_primes = idealprimedec(K, rational_prime));
  my(base_prime = base_primes[base_prime_index]);
  my(base_log = Vec(bnrisprincipal(ray24, base_prime, 0)));
  my(residue_field_size = idealnorm(K, base_prime));
  my(alpha = base_prime[2][1] + base_prime[2][2]*phi_H);
  my(H_primes = idealprimedec(H, rational_prime));
  my(answer = 0, modulus, target, matches);

  for(prime_index = 1, #H_primes,
    modulus = nfmodprinit(H, H_primes[prime_index]);
    if(nfmodpr(H, alpha, modulus) == 0,
      target = nfmodpr(H, H_generator, modulus)^residue_field_size;
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
        error("inconsistent Frobenius above the same base prime"));
      answer = matches[1]
    )
  );
  [base_log, answer];
};

frobenius_four = identify_frobenius(31, 2);
frobenius_two_a = identify_frobenius(59, 1);
frobenius_two_b = identify_frobenius(71, 2);
assert_equal("PRIME_31_RAY_LOG", frobenius_four[1], [1, 0, 0]);
assert_equal("PRIME_59_RAY_LOG", frobenius_two_a[1], [0, 1, 0]);
assert_equal("PRIME_71_RAY_LOG", frobenius_two_b[1], [0, 0, 1]);

generator_four = Mod(H_conjugates[frobenius_four[2]], Hpol);
generator_two_a = Mod(H_conjugates[frobenius_two_a[2]], Hpol);
generator_two_b = Mod(H_conjugates[frobenius_two_b[2]], Hpol);

act(automorphism, element) =
  subst(lift(automorphism), x, element);

artin_image(log_vector) =
{
  my(element = H_generator);
  for(index = 1, log_vector[1],
    element = act(generator_four, element));
  if(log_vector[2], element = act(generator_two_a, element));
  if(log_vector[3], element = act(generator_two_b, element));
  element;
};

\\ [a,b,left numerator,right numerator,denominator]
windows = [ \
  0,1, 6910937, 6910938, 1000000; \
  0,3, 2061122, 2061123, 1000000; \
  0,5,  485172,  485173, 1000000; \
  0,7,  144698,  144699, 1000000; \
  1,1,  125112,  125113, 1000000; \
  1,2,   90044,   90045, 1000000; \
  1,3,   65762,   65763, 1000000; \
  1,4,   54831,   54832, 1000000; \
  1,5,   60665,   60666, 1000000; \
  2,3,   22955,   22956, 1000000; \
  2,7, 7992821, 7992822, 1000000; \
  3,6,16483891,16483892, 1000000; \
  3,7,11105600,11105601, 1000000; \
  4,5,18237810,18237811, 1000000; \
  4,7,15206346,15206347, 1000000; \
  5,5,43562131,43562132, 1000000 \
];

matched_windows = vector(matsize(windows)[1]);
for(first_log = 0, 3, \
  for(second_log = 0, 1, \
    for(third_log = 0, 1, \
      log_vector = [first_log, second_log, third_log]; \
      candidate = artin_image(log_vector); \
      image_interval = ieval(lift(candidate), generator_interval); \
      match = 0; \
      for(row = 1, matsize(windows)[1], \
        target = [ \
          windows[row, 3]/windows[row, 5], \
          windows[row, 4]/windows[row, 5] \
        ]; \
        if(is_subset(image_interval, target), match = row) \
      ); \
      if(!match, error(Str("no root interval for ray log ", log_vector))); \
      if(matched_windows[match], \
        error(Str("duplicate root interval for ray log ", log_vector))); \
      matched_windows[match] = 1; \
      print( \
        "CHAR_", windows[match, 1], "_", windows[match, 2], \
        "_RAY_LOG=", log_vector, " ROOT_INTERVAL_CERTIFIED=1" \
      ) \
    ) \
  ) \
);

assert_equal("MATCHED_ROOT_COUNT", vecsum(matched_windows), 16);
print("ALL_DIMENSION_EIGHT_ARTIN_LABELS_CERTIFIED=1");

quit();
