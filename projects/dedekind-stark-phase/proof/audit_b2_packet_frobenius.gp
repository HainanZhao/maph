\\ Exact target-blind packet-field Frobenius audit for B2.
\\ No L-function value, logarithmic coefficient, phase, or old
\\ direct/inverse selection is read.

default(parisizemax, 4000000000);

automorphism_order(nf, automorphism) =
{
  my(alpha = Mod(variable(nf.pol), nf.pol), value = alpha);
  for(order = 1, 8,
    value = nfgaloisapply(nf, automorphism, value);
    if(value == alpha, return(order));
  );
  error("automorphism order exceeds eight");
};

first_order_four_automorphism(nf) =
{
  my(automorphisms = nfgaloisconj(nf));
  for(index = 1, #automorphisms,
    if(automorphism_order(nf, automorphisms[index]) == 4,
      return(automorphisms[index])));
  error("no order-four automorphism");
};

automorphism_power(nf, automorphism, exponent) =
{
  my(alpha = Mod(variable(nf.pol), nf.pol), value = alpha);
  for(index = 1, exponent,
    value = nfgaloisapply(nf, automorphism, value));
  value;
};

run_case(case_id, polynomial, real_base_polynomial, real_finite_hnf, source_character, separator_prime) =
{
  my(nf = nfinit(polynomial));
  my(alpha = Mod(variable(polynomial), polynomial));
  my(gamma = first_order_four_automorphism(nf));
  my(automorphisms = nfgaloisconj(nf));
  my(primes = idealprimedec(nf, separator_prime));
  my(matches = List());

  for(automorphism_index = 1, #automorphisms,
    if(automorphism_order(nf, automorphisms[automorphism_index]) == 4,
      for(prime_index = 1, #primes,
        if(primes[prime_index].f == 4,
          my(modpr = nfmodprinit(nf, primes[prime_index]));
          my(frobenius_on_integral_basis = 1);
          for(basis_index = 1, #nf.zk,
            my(basis_element = Mod(nf.zk[basis_index], polynomial));
            if(nfmodpr(
                 nf,
                 nfgaloisapply(
                   nf,
                   automorphisms[automorphism_index],
                   basis_element
                 ),
                 modpr)
               != nfmodpr(nf, basis_element, modpr)^separator_prime,
              frobenius_on_integral_basis = 0;
              break;
            );
          );
          if(frobenius_on_integral_basis,
            listput(matches, [
              automorphism_index,
              prime_index,
              automorphisms[automorphism_index]
            ]);
          );
        );
      );
    );
  );
  matches = Vec(matches);
  my(frobenius_automorphisms =
    Set(vector(#matches, index, Str(matches[index][3]))));
  if(#frobenius_automorphisms != 1,
    error(case_id, ": integral-basis Frobenius is not unique"));
  my(sigma = matches[1][3]);
  my(gamma_frobenius_power = 0);
  for(exponent = 1, 3,
    if(automorphism_power(nf, sigma, exponent) == Mod(gamma, polynomial),
      gamma_frobenius_power = exponent));
  if(gamma_frobenius_power != 1 && gamma_frobenius_power != 3,
    error(case_id, ": gamma is not a primitive Frobenius power"));

  my(real_base = bnfinit(real_base_polynomial, 1));
  my(real_ray = bnrinit(
    real_base, [real_finite_hnf, [1, 0]], 1));
  my(cyc = Vec(real_ray.cyc));
  my(base_primes = idealfactor(real_base, separator_prime)[, 1]);
  my(character_exponents = vector(#base_primes));
  for(index = 1, #base_primes,
    my(class_log = Vec(bnrisprincipal(
      real_ray, base_primes[index], 0)));
    my(value = 4 * sum(
      coordinate = 1, #cyc,
      source_character[coordinate]
        * class_log[coordinate] / cyc[coordinate]));
    if(denominator(value) != 1,
      error(case_id, ": source character is not quartic"));
    character_exponents[index] = lift(value) % 4;
  );
  if(#Set(character_exponents) != 1,
    error(case_id, ": separator primes have different character values"));
  my(gamma_character_exponent =
    (character_exponents[1] * gamma_frobenius_power) % 4);
  if(gamma_character_exponent != 1
     && gamma_character_exponent != 3,
    error(case_id, ": separator does not have primitive quartic value"));
  my(orientation = if(
    gamma_character_exponent == 1, "direct", "inverse"));

  print("CASE_ID=", case_id);
  print("SEPARATOR_PRIME=", separator_prime);
  print("USABLE_PRIME_COUNT=", #matches);
  print("FROBENIUS_AUTOMORPHISM=", sigma);
  print("GAMMA_EQUALS_FROBENIUS_POWER=", gamma_frobenius_power);
  print("CONSTRUCTOR_GAMMA=", gamma);
  print("SOURCE_RAY_CYC=", cyc);
  print("SOURCE_CHARACTER=", source_character);
  print("BASE_PRIME_COUNT=", #base_primes);
  print("BASE_PRIME_CHARACTER_EXPONENTS=", character_exponents);
  print("CHI_OF_GAMMA_EXPONENT=", gamma_character_exponent);
  print("DEDEKIND_TO_ANALYTIC_ORIENTATION=", orientation);
  print("PACKET_FROBENIUS_GATE=PASS");
};

x = 'x;

main() =
{
run_case(
  "RQ-000129",
  x^8 - 4*x^5 - 2*x^4 - 8*x^2 - 8*x - 2,
  y^2 - 6,
  [4, 0; 0, 2],
  [1],
  3
);
run_case(
  "RQ-001280",
  x^8 + 10*x^6 + 14*x^4 - 20*x^2 + 4,
  y^2 - 35,
  [8, 4; 0, 4],
  [1, 0],
  5
);
run_case(
  "RQ-001569",
  x^8 + 10*x^6 - 12*x^5 + 9*x^4 + 24*x^3
    - 44*x^2 + 12*x + 1,
  y^2 - 42,
  [6, 0; 0, 2],
  [1, 1],
  11
);
run_case(
  "RQ-001894",
  x^8 + 10*x^6 - 120*x^5 - 1050*x^4 + 1950*x^3
    + 5875*x^2 - 14550*x + 8725,
  y^2 - 51,
  [15, 0; 0, 5],
  [1, 0, 1],
  2
);
run_case(
  "RQ-007519",
  x^8 + 10*x^6 - 12*x^5 - 99*x^4 + 312*x^3
    - 584*x^2 + 372*x + 217,
  y^2 - 186,
  [6, 0; 0, 2],
  [1, 1],
  5
);

print("B2_PACKET_FROBENIUS_AUDIT=PASS");
};

main();
