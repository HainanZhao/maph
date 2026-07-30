\\ Audit the five selected order-six ray fields against the hypotheses
\\ of Roblot, Theorem 7.1 (arXiv:1112.2820).

allocatemem(800000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(label, ": expected ", expected, ", got ", actual));
};

audit_case(label, P, ramified_prime, base_discriminant, base_e_at_ramified_prime, expected_roblot_applies) =
{
  my(field, subfields, real_subfields = List(), plus_polynomial);
  my(plus_field, factors, relative_polynomial = 0, relative_field);
  my(decomposition, no_split = 1, local_rows = List());
  my(max_relative_e_over_base = 1, wild_above_three, roblot_applies);

  field = bnfinit(P, 1);
  assert_equal(Str(label, "_BNFCERTIFY"), bnfcertify(field), 1);
  assert_equal(Str(label, "_SIGNATURE"), field.sign, [6, 3]);

  subfields = nfsubfields(P, 6);
  for(index = 1, #subfields,
    my(candidate = nfinit(subfields[index][1]));
    if(candidate.sign == [6, 0],
      listput(real_subfields, subfields[index]));
  );
  assert_equal(Str(label, "_TOTALLY_REAL_DEGREE_SIX_SUBFIELDS"),
    #real_subfields, 1);
  plus_polynomial = real_subfields[1][1];

  \\ Give the subfield variable higher priority than the relative
  \\ generator so nffactor returns a polynomial over H^+.
  plus_field = nfinit(subst(plus_polynomial, x, y));
  factors = nffactor(plus_field, P);
  for(index = 1, matsize(factors)[1],
    if(poldegree(factors[index, 1]) == 2,
      relative_polynomial = factors[index, 1];
      break;
    );
  );
  if(relative_polynomial == 0,
    error(label, ": no quadratic H/H+ factor found"));
  relative_field = rnfinit(plus_field, relative_polynomial);

  decomposition = rnfidealprimedec(relative_field, ramified_prime);
  for(index = 1, #decomposition[1],
    my(base_prime = decomposition[1][index]);
    my(top_primes = decomposition[2][index]);
    my(row, relative_e, relative_f);
    if(#top_primes != 1, no_split = 0);
    relative_e = top_primes[1].e / base_prime.e;
    relative_f = top_primes[1].f / base_prime.f;
    max_relative_e_over_base = max(max_relative_e_over_base,
      top_primes[1].e / base_e_at_ramified_prime);
    row = [base_prime.e, base_prime.f, #top_primes,
      relative_e, relative_f];
    listput(local_rows, row);
  );
  assert_equal(Str(label, "_CLASS_NUMBER"), field.no, 1);
  assert_equal(Str(label, "_A3"), no_split, 1);
  wild_above_three =
    if(ramified_prime == 3,
      max_relative_e_over_base % 3 == 0,
      valuation(field.disc, 3)
        - 6 * valuation(base_discriminant, 3) > 0);
  roblot_applies =
    (field.no % 3 != 0) && no_split && !wild_above_three;
  assert_equal(Str(label, "_ROBLOT_APPLICABILITY"),
    roblot_applies, expected_roblot_applies);

  print(label,
    "|CLASS_NUMBER=", field.no,
    "|CLASS_NUMBER_MOD_3=", field.no % 3,
    "|BNFCERTIFY=1",
    "|SIGNATURE=", field.sign,
    "|HPLUS_POLYNOMIAL=", plus_polynomial,
    "|HPLUS_COUNT=1",
    "|A3_NO_SPLIT=", no_split,
    "|LOCAL_ROWS_[EPLUS_FPLUS_COUNT_EREL_FREL]=", Vec(local_rows),
    "|MAX_E_H_OVER_K_AT_FINITE_PRIME=", max_relative_e_over_base,
    "|WILD_ABOVE_3=", wild_above_three,
    "|ROBLOT_7_1_APPLIES=", roblot_applies,
    "|BASE_DISC_V3=", valuation(base_discriminant, 3),
    "|FIELD_DISC_V3=", valuation(field.disc, 3),
    "|RELATIVE_DISC_NORM_V3=",
      valuation(field.disc, 3) - 6 * valuation(base_discriminant, 3)
  );
};

x = 'x;

P190 = x^12-12*x^11+52*x^10-108*x^9+124*x^8-92*x^7+63*x^6-92*x^5+124*x^4-108*x^3+52*x^2-12*x+1;
P419 = x^12-26*x^11+115*x^10-24*x^9-23*x^8+6*x^7-105*x^6+6*x^5-23*x^4-24*x^3+115*x^2-26*x+1;
P021 = x^12-20*x^11+144*x^10-458*x^9+700*x^8-784*x^7+827*x^6-784*x^5+700*x^4-458*x^3+144*x^2-20*x+1;
P2057 = x^12-69*x^11+1377*x^10-6694*x^9+7590*x^8-15594*x^7+10791*x^6-15594*x^5+7590*x^4-6694*x^3+1377*x^2-69*x+1;
P2955 = x^12-33*x^11+339*x^10-1445*x^9+3442*x^8-5496*x^7+6377*x^6-5496*x^5+3442*x^4-1445*x^3+339*x^2-33*x+1;

audit_case("RQ-000190", P190, 7, 28, 2, 1);
audit_case("RQ-000419", P419, 7, 56, 2, 1);
audit_case("RQ-000021", P021, 7, 8, 1, 1);
audit_case("RQ-002057", P2057, 3, 57, 2, 0);
audit_case("RQ-002955", P2955, 7, 77, 2, 1);

print("ROBLOT_SEXTIC_OVERLAP_AUDIT=PASS");
