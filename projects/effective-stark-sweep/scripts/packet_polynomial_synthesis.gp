\\ Compositum-free trace-descent synthesis for Engine-A packet powers.
\\ The recurrence is exact.  Numerical values below are quarantined
\\ validation of the dimension-eight anchor, never selection inputs.

default(realprecision, 120);
read("scripts/census_packet_conventions.gp");

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

assert_small(label, actual, tolerance) =
{
  if(abs(actual) > tolerance,
    error(Str(label, ": residual ", actual, " exceeds ", tolerance)));
  print(label, "=", actual);
};

census_trace_power(trace_value, exponent) =
{
  if(exponent < 0,
    error("trace-power exponent must be nonnegative"));
  if(exponent == 0, return(2));
  if(exponent == 1, return(trace_value));
  my(previous = 2, current = trace_value);
  for(index = 2, exponent,
    my(next = trace_value * current - previous);
    previous = current;
    current = next;
  );
  current;
};

census_trace_step(polynomial, trace_value) =
{
  my(result = polresultant(
    subst(polynomial, x, z),
    x^2 - trace_value * x * z + z^2,
    z
  ));
  result / pollead(result);
};

census_trace_synthesis(traces) =
{
  my(polynomial = x - 1);
  for(index = 1, #traces,
    polynomial = census_trace_step(polynomial, traces[index]));
  polynomial;
};

census_is_reciprocal(polynomial) =
{
  my(degree = poldegree(polynomial));
  x^degree * subst(polynomial, x, 1/x) == polynomial;
};

census_positive_square_lift(base_nf, powered_polynomial) =
{
  my(factorization =
    nffactor(base_nf, subst(lift(powered_polynomial), x, x^2)));
  my(matches = List());
  for(index = 1, matsize(factorization)[1],
    my(factor = factorization[index, 1]);
    if(factorization[index, 2] == 1
       && census_polynomial_has_positive_root_sign_pattern(
            base_nf, factor),
      listput(matches, factor));
  );
  if(#matches != 1,
    error(Str(
      "positive square-lift factor count: expected 1, got ",
      #matches
    )));
  [Vec(matches)[1], factorization];
};

run_dimension_eight_anchor() =
{
  my(base = bnfinit(y^2 - y - 1, 1));
  my(raw_trace_0 = Mod(2*y, base.pol));
  my(raw_trace_1 = Mod(8*y + 6, base.pol));
  my(trace_0 = census_orient_trace(base, raw_trace_0));
  my(trace_1 = census_orient_trace(base, raw_trace_1));
  my(first, powered, lift_data, packet, lift_factorization);
  my(expected_powered, expected_packet, signed_powered);
  my(absolute_packet, split_y, split_packet, packet_roots);
  my(unit_roots_0, unit_roots_1, brute_roots, analytic_anchor);

  assert_equal("PARI_VERSION", version(), [2, 15, 4]);
  assert_equal("BASE_BNFCERTIFY", bnfcertify(base), 1);
  assert_equal(
    "SOURCE_INFINITY_VECTOR",
    CENSUS_SOURCE_INFINITY_VECTOR,
    [1, 0]
  );
  assert_equal("RAMIFIED_REAL_PLACE", CENSUS_RAMIFIED_REAL_PLACE, 1);
  assert_equal("SPLIT_REAL_PLACE", CENSUS_SPLIT_REAL_PLACE, 2);
  assert_equal("BASE_REAL_ROOT_SIGNS", nfeltsign(base, Mod(y, base.pol)),
    [-1, 1]);
  assert_equal("ORIENTED_TRACE_0", trace_0, raw_trace_0);
  assert_equal("ORIENTED_TRACE_1", trace_1, raw_trace_1);
  assert_equal(
    "NEGATED_TRACE_0_REORIENTS",
    census_orient_trace(base, -raw_trace_0),
    raw_trace_0
  );
  assert_equal("TRACE_POWER_0", census_trace_power(trace_0, 0), 2);
  assert_equal("TRACE_POWER_2",
    census_trace_power(trace_0, 2), trace_0^2 - 2);

  first = census_trace_synthesis([trace_0]);
  assert_equal(
    "ONE_TRACE_POLYNOMIAL",
    first,
    x^2 - trace_0*x + 1
  );
  assert_equal("ONE_TRACE_RECIPROCAL", census_is_reciprocal(first), 1);

  powered = census_trace_synthesis([trace_0, trace_1]);
  expected_powered =
    x^4 + Mod(-28*y - 16, base.pol)*x^3
      + Mod(164*y + 102, base.pol)*x^2
      + Mod(-28*y - 16, base.pol)*x + 1;
  assert_equal("POWERED_ORBIT_POLYNOMIAL", powered, expected_powered);
  assert_equal("POWERED_ORBIT_DEGREE", poldegree(powered), 4);
  assert_equal(
    "POWERED_ORBIT_RECIPROCAL",
    census_is_reciprocal(powered),
    1
  );

  lift_data = census_positive_square_lift(base, powered);
  packet = lift_data[1];
  lift_factorization = lift_data[2];
  expected_packet =
    x^4 + Mod(-4*y - 4, base.pol)*x^3
      + Mod(10*y + 8, base.pol)*x^2
      + Mod(-4*y - 4, base.pol)*x + 1;
  assert_equal("SQUARE_LIFT_FACTOR_COUNT",
    matsize(lift_factorization)[1], 2);
  assert_equal("POSITIVE_PACKET_FACTOR", packet, expected_packet);
  assert_equal("PACKET_FACTOR_DEGREE", poldegree(packet), 4);
  assert_equal("PACKET_FACTOR_RECIPROCAL",
    census_is_reciprocal(packet), 1);
  assert_equal(
    "PACKET_FACTOR_IRREDUCIBLE_OVER_K",
    matsize(nffactor(base, lift(packet)))[1],
    1
  );
  signed_powered = packet * subst(packet, x, -x);
  assert_equal(
    "EXACT_DENOMINATOR_TWO_LIFT_IDENTITY",
    signed_powered,
    subst(powered, x, x^2)
  );

  absolute_packet = polresultant(base.pol, lift(packet), y);
  assert_equal(
    "ABSOLUTE_PACKET_POLYNOMIAL",
    absolute_packet,
    x^8 - 12*x^7 + 42*x^6 - 68*x^5 + 78*x^4
      - 68*x^3 + 42*x^2 - 12*x + 1
  );
  assert_equal(
    "ABSOLUTE_PACKET_IRREDUCIBLE",
    polisirreducible(absolute_packet),
    1
  );

  \\ Quarantined numerical validation: neither the factor nor its
  \\ orientation was selected from these values.
  split_y = (1 + sqrt(5))/2;
  split_packet = subst(lift(packet), y, split_y);
  packet_roots = polrootsreal(split_packet);
  assert_equal("SPLIT_PACKET_REAL_ROOT_COUNT", #packet_roots, 4);
  analytic_anchor = 7.3889768540986208519104304947855586515268267739437;
  assert_small(
    "QUARANTINED_ANALYTIC_ANCHOR_RESIDUAL",
    packet_roots[4] - analytic_anchor,
    1e-48
  );

  unit_roots_0 = polrootsreal(x^2 - subst(lift(trace_0), y, split_y)*x + 1);
  unit_roots_1 = polrootsreal(x^2 - subst(lift(trace_1), y, split_y)*x + 1);
  brute_roots = vecsort([
    sqrt(unit_roots_0[1] * unit_roots_1[1]),
    sqrt(unit_roots_0[1] * unit_roots_1[2]),
    sqrt(unit_roots_0[2] * unit_roots_1[1]),
    sqrt(unit_roots_0[2] * unit_roots_1[2])
  ]);
  for(index = 1, 4,
    assert_small(
      Str("QUARANTINED_BRUTE_FORCE_ROOT_RESIDUAL_", index),
      packet_roots[index] - brute_roots[index],
      1e-100
    ));

  print("TRACE_DESCENT_SYNTHESIS=PASS");
  print("CLAIM_TAG_ALGEBRAIC_RECURRENCE=PROVED");
  print("CLAIM_TAG_NUMERICAL_ANCHOR=OBSERVED");
  print("CENSUS_TARGET_ARTIFACT_OPENED=0");
};

run_dimension_eight_anchor();
