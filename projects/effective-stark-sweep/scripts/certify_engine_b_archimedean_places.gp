\\ Exact all-archimedean-place audit for the seven Engine-B packets.
\\ For a reciprocal polynomial Q of degree 2n, construct the unique
\\ trace polynomial R with Q(X)=X^n R(X+X^-1).  Roots of R in (-2,2)
\\ give conjugate pairs of Q on the unit circle.  The remaining roots
\\ of R give the positive real packet roots.

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

trace_polynomial(Q) =
{
  my(n = poldegree(Q) / 2);
  my(S0 = 2, S1 = t, S = S1);
  my(R = polcoef(Q, n));
  for(k = 1, n,
    if(k == 1,
      S = S1,
      my(S2 = t * S1 - S0);
      S0 = S1;
      S1 = S2;
      S = S2
    );
    R += polcoef(Q, n + k) * S;
  );
  R;
};

audit_case(case_id, Q, expected_real, expected_unit_pairs) =
{
  my(n = poldegree(Q) / 2);
  my(R = trace_polynomial(Q));
  my(total_trace_real = polsturm(R));
  my(unit_pairs = polsturm(R, -2, 2));
  my(real_roots = polsturm(Q));
  my(positive_roots = polsturm(Q, 0));

  assert_equal(Str(case_id, "_RECIPROCAL"),
    x^(2*n) * subst(Q, x, 1/x) == Q, 1);
  assert_equal(Str(case_id, "_TRACE_IDENTITY"),
    x^n * subst(R, t, x + 1/x) == Q, 1);
  assert_equal(Str(case_id, "_TRACE_ENDPOINT_MINUS_2_NONZERO"),
    subst(R, t, -2) != 0, 1);
  assert_equal(Str(case_id, "_TRACE_ENDPOINT_PLUS_2_NONZERO"),
    subst(R, t, 2) != 0, 1);
  assert_equal(Str(case_id, "_TRACE_ALL_ROOTS_REAL"),
    total_trace_real, n);
  assert_equal(Str(case_id, "_UNIT_CIRCLE_CONJUGATE_PAIRS"),
    unit_pairs, expected_unit_pairs);
  assert_equal(Str(case_id, "_REAL_ROOTS"),
    real_roots, expected_real);
  assert_equal(Str(case_id, "_POSITIVE_REAL_ROOTS"),
    positive_roots, expected_real);
  assert_equal(Str(case_id, "_ROOT_ACCOUNTING"),
    expected_real + 2 * expected_unit_pairs, 2*n);
  print(case_id, "_TRACE_POLYNOMIAL=", R);
};

run_audit() =
{
  audit_case("RQ_000190",
    x^12-12*x^11+52*x^10-108*x^9+124*x^8-92*x^7+63*x^6
      -92*x^5+124*x^4-108*x^3+52*x^2-12*x+1,
    6, 3);
  audit_case("RQ_000419",
    x^12-26*x^11+115*x^10-24*x^9-23*x^8+6*x^7-105*x^6
      +6*x^5-23*x^4-24*x^3+115*x^2-26*x+1,
    6, 3);
  audit_case("RQ_000108",
    x^8-8*x^7-2*x^6+19*x^5+25*x^4+19*x^3-2*x^2-8*x+1,
    4, 2);
  audit_case("RQ_000021",
    x^12-20*x^11+144*x^10-458*x^9+700*x^8-784*x^7+827*x^6
      -784*x^5+700*x^4-458*x^3+144*x^2-20*x+1,
    6, 3);
  audit_case("RQ_002057",
    x^12-69*x^11+1377*x^10-6694*x^9+7590*x^8-15594*x^7
      +10791*x^6-15594*x^5+7590*x^4-6694*x^3+1377*x^2-69*x+1,
    6, 3);
  audit_case("RQ_002955",
    x^12-33*x^11+339*x^10-1445*x^9+3442*x^8-5496*x^7+6377*x^6
      -5496*x^5+3442*x^4-1445*x^3+339*x^2-33*x+1,
    6, 3);
  audit_case("RQ_001107",
    x^20-20*x^19+146*x^18-513*x^17+995*x^16-1336*x^15
      +1613*x^14-1598*x^13+1131*x^12-826*x^11+803*x^10
      -826*x^9+1131*x^8-1598*x^7+1613*x^6-1336*x^5
      +995*x^4-513*x^3+146*x^2-20*x+1,
    10, 5);
  print("ENGINE_B_ARCHIMEDEAN_PLACE_AUDIT=VERIFIED");
};

run_audit();
