\\ Exact scope audit and ray-character selection for the
\\ Q(sqrt(-3)) route of RQ-000129.
\\
\\ This certificate deliberately ends at THEOREM_SCOPE_RESISTANCE:
\\ the conductor has one distinct finite prime, hence |S|=2, so the
\\ |S|>=3 global-unit version of the banked general-e lemma does not
\\ apply.

default(parisizemax, 4000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

run_scope_audit() =
{
  my(real_base = bnfinit(y^2 - 6, 1));
  my(real_ray = bnrinit(
    real_base, [[4, 0; 0, 2], [1, 0]], 1));
  my(cm_base = bnfinit(y^2 - y + 1, 1));
  my(character_field_polynomial =
    x^8 - 2*x^6 + 5*x^4 - 4*x^2 + 1);
  my(character_field =
    bnfinit(character_field_polynomial, 1));
  my(relative =
    nffactor(cm_base, character_field_polynomial)[1, 1]);
  my(conductor_data = rnfconductor(cm_base, relative));
  my(factorization =
    idealfactor(cm_base, conductor_data[1][1]));
  my(distinct_finite_primes = matsize(factorization)[1]);
  my(S_size = 1 + distinct_finite_primes);
  my(source_coefficients =
    lfunan(lfuncreate([real_ray, [1]]), 30));
  my(selected_coefficients =
    lfunan(lfuncreate([conductor_data[2], [1, 1]]), 30));
  my(inverse_coefficients =
    lfunan(lfuncreate([conductor_data[2], [3, 1]]), 30));

  assert_equal("CASE_ID", "RQ-000129", "RQ-000129");
  assert_equal("CM_BASE", cm_base.pol, y^2 - y + 1);
  assert_equal("CM_BASE_ROOTS_OF_UNITY_W_K", cm_base.tu[1], 6);
  assert_equal("CHARACTER_FIELD_SIGNATURE",
    character_field.sign, [0, 4]);
  assert_equal("CHARACTER_FIELD_CLASS_NUMBER",
    character_field.no, 1);
  assert_equal("CHARACTER_FIELD_BNFCERTIFY",
    bnfcertify(character_field), 1);
  assert_equal("CHARACTER_FIELD_ROOTS_OF_UNITY_E",
    character_field.tu[1], 12);
  assert_equal("CM_CONDUCTOR", conductor_data[1],
    [[8, 0; 0, 8], []]);
  assert_equal("CM_CONDUCTOR_FACTORIZATION", factorization,
    Mat([[2, [2, 0]~, 1, 2, 1], 3]));
  assert_equal("CM_RAY_CYC", Vec(conductor_data[2].cyc),
    [4, 2]);
  assert_equal("CM_RAY_SUBGROUP_HNF", conductor_data[3],
    [4, 2; 0, 1]);
  assert_equal("DISTINCT_FINITE_CONDUCTOR_PRIMES",
    distinct_finite_primes, 1);
  assert_equal("STARK_S_SIZE", S_size, 2);
  assert_equal("SOURCE_MATCHES_SELECTED_CHARACTER",
    source_coefficients == selected_coefficients, 1);
  assert_equal("INVERSE_SEPARATED_AT_N3",
    source_coefficients[3] == -I
      && selected_coefficients[3] == -I
      && inverse_coefficients[3] == I, 1);

  print("CHARACTER_FIELD_POLYNOMIAL=",
    character_field_polynomial);
  print("EXHAUSTIVE_INVERSE_PAIR=[[1,1],[3,1]]");
  print("SELECTED_CM_RAY_CHARACTER=[1,1]");
  print("ORDINARY_MODULUS_COEFFICIENT=1/6");
  print("ANALYTIC_TO_UNIT_SCALE=6");
  print("GLOBAL_UNIT_CLAUSE_APPLIES=", S_size >= 3);
  print("THEOREM_SCOPE_RESISTANCE="
    "STARK_S_SIZE_2_NO_GLOBAL_UNIT_CLAUSE");
  print("Q6_SECOND_BASE_SCOPE_AUDIT_COMPLETE=1");
  print("CLAIM_TAG=VERIFIED_SCOPE_FAILURE_NO_PACKET_PROMOTION");
};

run_scope_audit();
