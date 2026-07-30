\\ Exact algebraic W3 certificate for Q(sqrt(14)), p_7 infinity_2.
\\ The independent analytic Arb enclosure is a separate gate.

default(realprecision, 140);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

run_exact_candidate() =
{
  my(Kpol = y^2 - 14, K = bnfinit(Kpol, 1));
  my(finite_ideal = [7, 0; 0, 1]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(P = x^6 - (13 + 4*y)*x^5 + (85 + 22*y)*x^4
    - (139 + 38*y)*x^3 + (85 + 22*y)*x^2
    - (13 + 4*y)*x + 1);
  my(Q = polresultant(Kpol, P, y));
  my(expected_Q =
    x^12 - 26*x^11 + 115*x^10 - 24*x^9 - 23*x^8
      + 6*x^7 - 105*x^6 + 6*x^5 - 23*x^4 - 24*x^3
      + 115*x^2 - 26*x + 1);
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
    [48/1000, 49/1000],
    [189/1000, 190/1000],
    [916/1000, 917/1000],
    [1090/1000, 1091/1000],
    [5289/1000, 5290/1000],
    [20431/1000, 20432/1000]
  ];
  for(index = 1, #windows,
    assert_equal(Str("STURM_WINDOW_", index),
      polsturm(Q, windows[index][1], windows[index][2]), 1)
  );

  my(prime11 = idealprimedec(K, 11)[1]);
  my(prime103 = idealprimedec(K, 103)[1]);
  assert_equal("FROBENIUS_PRIME_11_NORM",
    idealnorm(K, prime11), 11);
  assert_equal("FROBENIUS_PRIME_103_NORM",
    idealnorm(K, prime103), 103);
  assert_equal("FROBENIUS_PRIME_11_RAY_LOG",
    lift(bnrisprincipal(ray, prime11, 0)[1]), 5);
  assert_equal("FROBENIUS_PRIME_103_RAY_LOG",
    lift(bnrisprincipal(ray, prime103, 0)[1]), 1);

  print("RELATIVE_PACKET_POLYNOMIAL=", P);
  print("ABSOLUTE_PACKET_POLYNOMIAL=", Q);
  print("Q14_P7_W3_EXACT_ALGEBRAIC_CANDIDATE_VERIFIED=1");
  print("Q14_P7_W3_ANALYTIC_ARB_GATE=PENDING");
};

run_exact_candidate();
