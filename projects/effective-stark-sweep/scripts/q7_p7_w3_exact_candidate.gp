\\ Exact algebraic half of W3 for Q(sqrt(7)), p7 infinity_2.
\\ The analytic Arb enclosure remains a separate gate.

default(realprecision, 120);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

run_exact_candidate() =
{
  my(Kpol = y^2 - 7, K = bnfinit(Kpol, 1));
  my(finite_ideal = [7, 0; 0, 1]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(P = x^6 - (6 + 2*y)*x^5 + (22 + 8*y)*x^4
    - (34 + 13*y)*x^3 + (22 + 8*y)*x^2
    - (6 + 2*y)*x + 1);
  my(Q = polresultant(Kpol, P, y));
  my(ray_relative = bnrclassfield(ray, , 1));
  my(candidate_data = rnfequation(Kpol, P, 1));
  my(ray_data = rnfequation(Kpol, ray_relative, 1));
  my(candidate_absolute = candidate_data[1]);
  my(ray_absolute = ray_data[1]);
  my(candidate_base = Mod(candidate_data[2], candidate_absolute));
  my(ray_base = Mod(ray_data[2], ray_absolute));
  my(isomorphisms = nfisisom(candidate_absolute, ray_absolute));
  my(k_compatible = 0, field, windows);

  assert_equal("PACKET_ABSOLUTE_POLYNOMIAL", Q,
    x^12 - 12*x^11 + 52*x^10 - 108*x^9 + 124*x^8
      - 92*x^7 + 63*x^6 - 92*x^5 + 124*x^4
      - 108*x^3 + 52*x^2 - 12*x + 1);
  assert_equal("PACKET_ABSOLUTE_IRREDUCIBLE",
    polisirreducible(Q), 1);
  assert_equal("PACKET_RECIPROCAL",
    x^12 * subst(Q, x, 1/x) == Q, 1);
  assert_equal("PACKET_UNIT_NORM", polcoef(Q, 0), 1);

  for(index = 1, #isomorphisms,
    my(mapped_base = subst(
      lift(candidate_base), x,
      Mod(isomorphisms[index], ray_absolute)
    ));
    if(mapped_base == ray_base, k_compatible++);
  );
  assert_equal("CANDIDATE_RAY_ISOMORPHISM_COUNT",
    #isomorphisms, 6);
  assert_equal("K_COMPATIBLE_RAY_ISOMORPHISM_COUNT",
    k_compatible, 6);

  field = bnfinit(Q, 1);
  assert_equal("PACKET_FIELD_BNFCERTIFY", bnfcertify(field), 1);
  assert_equal("PACKET_FIELD_SIGNATURE", field.sign, [6, 3]);
  assert_equal("PACKET_FIELD_CLASS_NUMBER", field.no, 1);
  assert_equal("PACKET_REAL_ROOT_COUNT", polsturm(Q), 6);

  windows = [
    [187/1000, 188/1000],
    [368/1000, 369/1000],
    [444/1000, 445/1000],
    [2251/1000, 2252/1000],
    [2713/1000, 2714/1000],
    [5325/1000, 5326/1000]
  ];
  for(index = 1, #windows,
    assert_equal(Str("STURM_WINDOW_", index),
      polsturm(Q, windows[index][1], windows[index][2]), 1)
  );

  \\ Two distinct split rational primes give inverse ray generators.
  my(prime19 = idealprimedec(K, 19)[2]);
  my(prime31 = idealprimedec(K, 31)[2]);
  assert_equal("FROBENIUS_PRIME_19_NORM",
    idealnorm(K, prime19), 19);
  assert_equal("FROBENIUS_PRIME_31_NORM",
    idealnorm(K, prime31), 31);
  print("FROBENIUS_PRIME_19_RAY_LOG=",
    bnrisprincipal(ray, prime19, 0));
  print("FROBENIUS_PRIME_31_RAY_LOG=",
    bnrisprincipal(ray, prime31, 0));
  assert_equal("FROBENIUS_PRIME_19_GENERATES",
    gcd(lift(bnrisprincipal(ray, prime19, 0)[1]), 6), 1);
  assert_equal("FROBENIUS_PRIME_31_GENERATES",
    gcd(lift(bnrisprincipal(ray, prime31, 0)[1]), 6), 1);

  print("RELATIVE_PACKET_POLYNOMIAL=", P);
  print("ABSOLUTE_PACKET_POLYNOMIAL=", Q);
  print("Q7_P7_W3_EXACT_ALGEBRAIC_CANDIDATE_VERIFIED=1");
  print("Q7_P7_W3_ANALYTIC_ARB_GATE=PENDING");
};

run_exact_candidate();
