\\ Exact CM unit-lattice audit for the two primitive dimension-eight
\\ quartic packets.  The imaginary quadratic base is Q(sqrt(-6)).

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
  my(rank = #bnf.fu);
  my(answer = matrix(rank, rank));
  my(exponents);
  for(column = 1, rank,
    exponents = unit_exponents(
      bnf,
      Mod(subst(lift(bnf.fu[column]), x, automorphism), polynomial)
    );
    for(row = 1, rank, answer[row, column] = exponents[row]);
  );
  answer;
};

coordinate_matrix(bnf, units) =
{
  my(answer = matrix(#bnf.fu, #units));
  my(exponents);
  for(column = 1, #units,
    exponents = unit_exponents(bnf, units[column]);
    for(row = 1, #bnf.fu, answer[row, column] = exponents[row]);
  );
  answer;
};

audit_packet(packet, polynomial, expected_action) =
{
  my(field = bnfinit(polynomial, 1));
  my(automorphisms = nfgaloisconj(polynomial));
  my(sigma = automorphisms[2]);
  my(action = unit_action_matrix(field, polynomial, sigma));
  my(anti_lattice = matkerint(matid(#field.fu) + action^2));
  my(stark_unit = field.fu[3]^2);
  my(stark_conjugate =
    Mod(subst(lift(stark_unit), x, sigma), polynomial));
  my(stark_coordinates = matinverseimage(
    anti_lattice,
    coordinate_matrix(field, [stark_unit, stark_conjugate])
  ));

  assert_equal(Str("PACKET_", packet, "_SIGNATURE"),
    field.sign, [0, 4]);
  assert_equal(Str("PACKET_", packet, "_CLASS_NUMBER"), field.no, 4);
  assert_equal(Str("PACKET_", packet, "_BNFCERTIFY"),
    bnfcertify(field), 1);
  assert_equal(Str("PACKET_", packet, "_ROOTS_OF_UNITY"),
    field.tu[1], 2);
  assert_equal(Str("PACKET_", packet, "_AUTOMORPHISM_COUNT"),
    #automorphisms, 4);
  assert_equal(Str("PACKET_", packet, "_UNIT_ACTION"),
    action, expected_action);
  assert_equal(Str("PACKET_", packet, "_ANTI_UNIT_LATTICE"),
    anti_lattice, [0, 0; 1, 0; 0, 1]);
  assert_equal(Str("PACKET_", packet, "_STARK_COORDINATE_INDEX"),
    abs(matdet(stark_coordinates)), 4);

  print("PACKET_", packet, "_POLYNOMIAL=", polynomial);
  print("PACKET_", packet, "_SIGMA=", sigma);
  print("PACKET_", packet, "_FUNDAMENTAL_UNIT_2=", field.fu[2]);
  print("PACKET_", packet, "_FUNDAMENTAL_UNIT_3=", field.fu[3]);
  print("PACKET_", packet, "_STARK_UNIT=", stark_unit);
  print("PACKET_", packet, "_STARK_UNIT_MINPOLY=", minpoly(stark_unit));
  print("PACKET_", packet, "_STARK_COORDINATES=", stark_coordinates);
};

packet_0_polynomial =
  x^8 - 4*x^6 - 12*x^5 + 18*x^4 + 48*x^3 \
    - 16*x^2 - 168*x + 166;
packet_1_polynomial =
  x^8 - 4*x^7 + 8*x^5 + 28*x^4 + 96*x^3 \
    + 144*x^2 + 96*x + 24;

\\ Orient the two Q(sqrt(-6)) ray characters against the original
\\ real-quadratic characters.  The exact ray kernels leave precisely two
\\ inverse faithful characters.  The exact coefficient at n=5 separates
\\ them, so no finite-coefficient recognition or Chebotarev bound is used.
real_base = bnfinit(y^2 - y - 1, 1);
real_ray = bnrinit(real_base, [24, [1, 0]], 1);
cm_base = bnfinit(y^2 + 6, 1);

\\ Fix the relative factors explicitly: nffactor's row order can change
\\ with precision and is not a mathematical label.
cm_relative_0 = \
  x^4 + Mod(-y - 2, y^2 + 6)*x^2 \
    + Mod(-2*y - 6, y^2 + 6)*x + Mod(5*y + 4, y^2 + 6);
cm_relative_1 = \
  x^4 - 2*x^3 + Mod(-2*y - 2, y^2 + 6)*x^2 \
    + Mod(-4*y, y^2 + 6)*x + Mod(-2*y, y^2 + 6);
cm_conductor_0 = rnfconductor(cm_base, cm_relative_0);
cm_conductor_1 = rnfconductor(cm_base, cm_relative_1);
cm_ray_0 = cm_conductor_0[2];
cm_ray_1 = cm_conductor_1[2];
print("CM_CONDUCTOR_0=", cm_conductor_0[1]);
print("CM_CONDUCTOR_0_FACTORIZATION=", \
  idealfactor(cm_base, cm_conductor_0[1][1]));
print("CM_CONDUCTOR_1=", cm_conductor_1[1]);
print("CM_CONDUCTOR_1_FACTORIZATION=", \
  idealfactor(cm_base, cm_conductor_1[1][1]));

\\ Construct the ray groups before the absolute unit audits so their
\\ displayed cyclic coordinates are reproducible within this transcript.
audit_packet(0, packet_0_polynomial, \
  [-1, 0, 0; 0, 0, 1; 0, -1, 0]);
audit_packet(1, packet_1_polynomial, \
  [-1, 0, 0; 0, 0, -1; 0, 1, 0]);

assert_equal("CM_RAY_0_STRUCTURE", cm_ray_0.cyc, [8, 4]);
assert_equal("CM_RAY_1_STRUCTURE", cm_ray_1.cyc, [8, 4]);
assert_equal("REAL_CHARACTER_0_FULL_CONDUCTOR", \
  bnrconductor(real_ray, [1, 0, 0]), [[24, 0; 0, 24], [1, 0]]);
assert_equal("REAL_CHARACTER_1_FULL_CONDUCTOR", \
  bnrconductor(real_ray, [1, 1, 0]), [[24, 0; 0, 24], [1, 0]]);

coefficient_count = 5;
real_coefficients_0 = lfunan( \
  lfuncreate([real_ray, [1, 0, 0]]), coefficient_count);
real_coefficients_1 = lfunan( \
  lfuncreate([real_ray, [1, 1, 0]]), coefficient_count);
cm_candidates_0 = [[6, 1], [2, 3]];
cm_candidates_1 = [[2, 1], [6, 3]];
cm_match_0 = List();
cm_match_1 = List();
for(index = 1, #cm_candidates_0, \
  cm_coefficients = lfunan( \
    lfuncreate([cm_ray_0, cm_candidates_0[index]]), coefficient_count); \
  if(cm_coefficients == real_coefficients_0, \
    listput(cm_match_0, cm_candidates_0[index])));
for(index = 1, #cm_candidates_1, \
  cm_coefficients = lfunan( \
    lfuncreate([cm_ray_1, cm_candidates_1[index]]), coefficient_count); \
  if(cm_coefficients == real_coefficients_1, \
    listput(cm_match_1, cm_candidates_1[index])));

assert_equal("PACKET_0_DIRICHLET_CHARACTER_MATCH_COUNT", \
  #cm_match_0, 1);
assert_equal("PACKET_1_DIRICHLET_CHARACTER_MATCH_COUNT", \
  #cm_match_1, 1);
assert_equal("PACKET_0_SELECTED_RAY_CHARACTER", \
  Vec(cm_match_0)[1], [6, 1]);
assert_equal("PACKET_1_SELECTED_RAY_CHARACTER", \
  Vec(cm_match_1)[1], [2, 1]);
print("PACKET_0_MATCHING_CM_CHARACTER=", Vec(cm_match_0)[1]);
print("PACKET_1_MATCHING_CM_CHARACTER=", Vec(cm_match_1)[1]);
print("PACKET_0_SOURCE_COEFFICIENT_N_5=", real_coefficients_0[5]);
print("PACKET_0_SELECTED_COEFFICIENT_N_5=", \
  lfunan(lfuncreate([cm_ray_0, Vec(cm_match_0)[1]]), 5)[5]);
print("PACKET_0_INVERSE_COEFFICIENT_N_5=", \
  lfunan(lfuncreate([cm_ray_0, [2, 3]]), 5)[5]);
print("PACKET_1_SOURCE_COEFFICIENT_N_5=", real_coefficients_1[5]);
print("PACKET_1_SELECTED_COEFFICIENT_N_5=", \
  lfunan(lfuncreate([cm_ray_1, Vec(cm_match_1)[1]]), 5)[5]);
print("PACKET_1_INVERSE_COEFFICIENT_N_5=", \
  lfunan(lfuncreate([cm_ray_1, [6, 3]]), 5)[5]);
assert_equal("PACKET_0_EXACT_SEPARATOR_N_5", \
  real_coefficients_0[5] != \
    lfunan(lfuncreate([cm_ray_0, [2, 3]]), 5)[5], 1);
assert_equal("PACKET_1_EXACT_SEPARATOR_N_5", \
  real_coefficients_1[5] != \
    lfunan(lfuncreate([cm_ray_1, [6, 3]]), 5)[5], 1);
print("FINITE_CANDIDATE_RAY_LABEL_SELECTION=1");
print("CM_UNIT_LATTICE_AUDIT_COMPLETE=1");

quit();
