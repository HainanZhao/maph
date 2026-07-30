\\ Exact algebraic W3 certificate for RQ-002057.

default(realprecision, 150);
default(parisizemax, 2000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

run_exact_candidate() =
{
  my(Kpol = y^2 - y - 14, K = bnfinit(Kpol, 1));
  my(finite_ideal = [9, 3; 0, 3]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(P = x^6 - (30 + 9*y)*x^5 + (582 + 177*y)*x^4
    - (2529 + 772*y)*x^3 + (582 + 177*y)*x^2
    - (30 + 9*y)*x + 1);
  my(Q = polresultant(Kpol, P, y));
  my(expected_Q =
    x^12 - 69*x^11 + 1377*x^10 - 6694*x^9
      + 7590*x^8 - 15594*x^7 + 10791*x^6
      - 15594*x^5 + 7590*x^4 - 6694*x^3
      + 1377*x^2 - 69*x + 1);
  my(ray_relative = bnrclassfield(ray, , 1));
  my(candidate_data = rnfequation(Kpol, P, 1));
  my(ray_data = rnfequation(Kpol, ray_relative, 1));
  my(candidate_absolute = candidate_data[1]);
  my(ray_absolute = ray_data[1]);
  my(candidate_base = Mod(candidate_data[2], candidate_absolute));
  my(ray_base = Mod(ray_data[2], ray_absolute));
  my(isomorphisms = nfisisom(candidate_absolute, ray_absolute));
  my(k_compatible = 0, field, windows);

  assert_equal("PACKET_ABSOLUTE_POLYNOMIAL", Q, expected_Q);
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
  assert_equal("PACKET_REAL_ROOT_COUNT", polsturm(Q), 6);
  windows = [
    [28/1000, 29/1000],
    [35/1000, 36/1000],
    [175/1000, 176/1000],
    [5709/1000, 5710/1000],
    [27792/1000, 27793/1000],
    [34732/1000, 34733/1000]
  ];
  for(index = 1, #windows,
    assert_equal(Str("STURM_WINDOW_", index),
      polsturm(Q, windows[index][1], windows[index][2]), 1)
  );

  my(prime7 = idealprimedec(K, 7)[1]);
  my(prime41 = idealprimedec(K, 41)[1]);
  assert_equal("FROBENIUS_PRIME_7_NORM",
    idealnorm(K, prime7), 7);
  assert_equal("FROBENIUS_PRIME_41_NORM",
    idealnorm(K, prime41), 41);
  assert_equal("FROBENIUS_PRIME_7_RAY_LOG",
    lift(bnrisprincipal(ray, prime7, 0)[1]), 5);
  assert_equal("FROBENIUS_PRIME_41_RAY_LOG",
    lift(bnrisprincipal(ray, prime41, 0)[1]), 1);

  print("RELATIVE_PACKET_POLYNOMIAL=", P);
  print("ABSOLUTE_PACKET_POLYNOMIAL=", Q);
  print("RQ57_NORM27_W3_EXACT_ALGEBRAIC_CANDIDATE_VERIFIED=1");
  print("RQ57_NORM27_W3_ANALYTIC_ARB_GATE=PENDING");
};

run_exact_candidate();
