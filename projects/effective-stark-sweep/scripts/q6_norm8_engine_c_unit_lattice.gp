\\ Exact anti-unit lattice and ray-character orientation for RQ-000129.
\\ The final analytic identification of the displayed candidate is a
\\ separate Arb gate; no floating-point L-value is used here.

default(realprecision, 100);
default(parisizemax, 4000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

unit_exponents(bnf, unit) =
{
  my(raw = bnfisunit(bnf, unit));
  vector(#bnf.fu, index, raw[index]);
};

unit_action_matrix(bnf, polynomial, automorphism) =
{
  my(rank = #bnf.fu, answer = matrix(rank, rank));
  for(column = 1, rank,
    my(exponents = unit_exponents(
      bnf,
      Mod(subst(lift(bnf.fu[column]), x, automorphism), polynomial)
    ));
    for(row = 1, rank,
      answer[row, column] = exponents[row]);
  );
  answer;
};

coordinate_matrix(bnf, units) =
{
  my(answer = matrix(#bnf.fu, #units));
  for(column = 1, #units,
    my(exponents = unit_exponents(bnf, units[column]));
    for(row = 1, #bnf.fu,
      answer[row, column] = exponents[row]);
  );
  answer;
};

run_certificate() =
{
  my(polynomial =
    x^8 - 4*x^6 - 4*x^5 + 6*x^4 + 16*x^3 + 16*x^2 + 8*x + 2);
  my(field = bnfinit(polynomial, 1));
  my(automorphisms = nfgaloisconj(polynomial));
  my(sigma = automorphisms[2]);
  my(action = unit_action_matrix(field, polynomial, sigma));
  my(anti_lattice = matkerint(matid(#field.fu) + action^2));
  my(anti_generators = [
    field.fu[1] * field.fu[2],
    field.fu[1] * field.fu[3]
  ]);
  my(candidate = anti_generators[1]^4);
  my(candidate_conjugate =
    Mod(subst(lift(candidate), x, sigma), polynomial));
  my(candidate_coordinates = matinverseimage(
    anti_lattice,
    coordinate_matrix(field, [candidate, candidate_conjugate])
  ));

  assert_equal("CHARACTER_FIELD_SIGNATURE", field.sign, [0, 4]);
  assert_equal("CHARACTER_FIELD_CLASS_NUMBER", field.no, 1);
  assert_equal("CHARACTER_FIELD_BNFCERTIFY", bnfcertify(field), 1);
  assert_equal("CHARACTER_FIELD_ROOTS_OF_UNITY", field.tu[1], 8);
  assert_equal("CHARACTER_FIELD_AUTOMORPHISM_COUNT",
    #automorphisms, 4);
  assert_equal("C4_UNIT_ACTION", action,
    [0, 1, -1; 0, 0, -1; 1, 0, -1]);
  assert_equal("ANTI_UNIT_LATTICE", anti_lattice,
    [1, 1; 1, 0; 0, 1]);
  assert_equal("CANDIDATE_ORBIT_COORDINATES",
    candidate_coordinates, [4, 0; 0, 4]);

  \\ Exact finite coefficients choose [1] rather than its inverse.
  my(real_base = bnfinit(y^2 - 6, 1));
  my(real_ray = bnrinit(
    real_base, [[4, 0; 0, 2], [1, 0]], 1
  ));
  my(cm_base = bnfinit(y^2 + 2, 1));
  my(relative = nffactor(cm_base, polynomial)[1, 1]);
  my(conductor_data = rnfconductor(cm_base, relative));
  my(cm_ray = conductor_data[2]);
  my(source_coefficients =
    lfunan(lfuncreate([real_ray, [1]]), 20));
  my(selected_coefficients =
    lfunan(lfuncreate([cm_ray, [1]]), 20));
  my(inverse_coefficients =
    lfunan(lfuncreate([cm_ray, [3]]), 20));
  assert_equal("SOURCE_CM_CHARACTER_FIRST_20",
    selected_coefficients, source_coefficients);
  assert_equal("INVERSE_SEPARATED_AT_N3",
    inverse_coefficients[3] != source_coefficients[3], 1);

  print("CHARACTER_FIELD_POLYNOMIAL=", polynomial);
  print("C4_GENERATOR_AUTOMORPHISM=", sigma);
  print("ANTI_UNIT_GENERATOR_1=", anti_generators[1]);
  print("ANTI_UNIT_GENERATOR_2=", anti_generators[2]);
  print("ORIENTED_CM_RAY_CHARACTER=[1]");
  print("CANDIDATE_STARK_UNIT=", candidate);
  print("CANDIDATE_STARK_UNIT_MINPOLY=", minpoly(candidate));
  print("CANDIDATE_STARK_UNIT_NORM=", norm(candidate));
  print("Q6_NORM8_EXACT_UNIT_LATTICE_VERIFIED=1");
  print("Q6_NORM8_ANALYTIC_ARB_ORIENTATION_GATE=PENDING");
};

run_certificate();
