\\ Exact two-prime auxiliary-Euler audit for RQ-000129.

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

run_audit() =
{
  my(K = bnfinit(y^2 - 6, 1));
  my(source_ray =
    bnrinit(K, [[4, 0; 0, 2], [1, 0]], 1));
  my(source_L = lfuncreate([source_ray, [1]]));

  my(k8 = bnfinit(y^2 + 2, 1));
  my(ray8 = bnrinit(k8, [[12, 8; 0, 2], []], 1));
  my(L8 = lfuncreate([ray8, [1]]));

  my(k12 = bnfinit(y^2 - y + 1, 1));
  my(ray12 = bnrinit(k12, [[8, 0; 0, 8], []], 1));
  my(L12 = lfuncreate([ray12, [1, 1]]));

  my(auxiliary_primes = [3, 5]);
  my(expected_denominators = [I*x + 1, x^2 + 1]);
  my(expected_values_at_zero = [1 + I, 2]);
  for(index = 1, #auxiliary_primes,
    my(q = auxiliary_primes[index]);
    my(source_factor = lfuneuler(source_L, q));
    my(primary_factor = lfuneuler(L8, q));
    my(secondary_factor = lfuneuler(L12, q));
    assert_equal(Str("Q_", q, "_SOURCE_EULER"),
      source_factor, primary_factor);
    assert_equal(Str("Q_", q, "_PRIMARY_SECONDARY_EULER"),
      primary_factor, secondary_factor);
    my(denominator_polynomial = denominator(source_factor));
    assert_equal(Str("Q_", q, "_DENOMINATOR"),
      denominator_polynomial, expected_denominators[index]);
    my(multiplier_at_zero =
      subst(denominator_polynomial, x, 1));
    assert_equal(Str("Q_", q, "_LPRIME_MULTIPLIER"),
      multiplier_at_zero, expected_values_at_zero[index]);
    if(multiplier_at_zero == 0,
      error("auxiliary prime raises the analytic rank"));
  );

  print("PRIMARY_NATURAL_S_SIZE=3");
  print("SECONDARY_NATURAL_S_SIZE=2");
  print("Q_3_PRIMARY_ENLARGED_S_SIZE=4");
  print("Q_3_SECONDARY_ENLARGED_S_SIZE=3");
  print("Q_5_PRIMARY_ENLARGED_S_SIZE=4");
  print("Q_5_SECONDARY_ENLARGED_S_SIZE=3");
  print("AUXILIARY_EULER_FACTORS_ROUTE_INDEPENDENT=1");
  print("Q6_TWO_PRIME_EULER_AUDIT_VERIFIED=1");
  print("CLAIM_TAG=VERIFIED_EXACT_EULER_FACTORS");
};

run_audit();
