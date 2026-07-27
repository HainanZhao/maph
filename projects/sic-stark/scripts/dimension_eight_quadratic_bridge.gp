\\ Exact class fields and unit lattices for the four quadratic characters
\\ in the canonical dimension-eight Kopp difference.

default(realprecision, 100);
default(parisizemax, 4000000000);

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

K = bnfinit(y^2 - y - 1, 1);
ray24 = bnrinit(K, [24, [1, 0]], 1);

characters = [[0, 0, 1], [2, 1, 1], [2, 0, 1], [0, 1, 1]];

\\ Column lattices for the four index-two kernels.
kernels = [Mat([1, 0, 0; 0, 1, 0; 0, 0, 2]), \
  Mat([1, 0, 0; 1, 1, 0; 0, 1, 2]), \
  Mat([1, 0, 0; 0, 1, 0; 1, 0, 2]), \
  Mat([1, 0, 0; 0, 1, 0; 0, 1, 2])];

L_imprimitive = bnrL1(ray24, , 6);
L_primitive = bnrL1(ray24, , 4);
expected_e = [0, 1, 1, 0];
expected_t_S = [1, 0, 0, 1];
positive_embedding = [1, 2, 2, 1];

find_l_record(records, character) =
{
  for(k = 1, #records,
    if(records[k][1] == character, return(records[k][2])));
  error(Str("character not found: ", character));
};

free_unit_exponents(field_bnf, units) =
{
  my(rank = field_bnf.r1 + field_bnf.r2 - 1);
  matrix(rank, #units, row, col, bnfisunit(field_bnf, units[col])[row]);
};

print("PARI_VERSION=", version());
print("BASE_BNFCERTIFY=", bnfcertify(K));

for(j = 1, #characters, \
{
  my(character = characters[j]);
  my(relative_polynomial = bnrclassfield(ray24, kernels[j], 1));
  my(absolute_polynomial = rnfpolredbest(K, relative_polynomial, 2));
  my(field_bnf = bnfinit(absolute_polynomial, 1));
  my(relative_field = rnfinit(K, relative_polynomial, 1));
  my(norm_model_bnf = bnfinit(relative_field.polabs, 1));
  my(relative_norms = vector(#norm_model_bnf.fu, k, \
    rnfeltnorm(relative_field, \
      rnfeltabstorel(relative_field, norm_model_bnf.fu[k]))));
  my(norm_exponents = vector(#relative_norms, k, \
    bnfisunit(K, relative_norms[k])[1]));
  my(norm_index = 0);
  for(k = 1, #norm_exponents, norm_index = gcd(norm_index, norm_exponents[k]));
  my(automorphisms = nfgaloisconj(absolute_polynomial));
  my(root_variable = variable(absolute_polynomial));
  my(tau = root_variable);
  for(k = 1, #automorphisms, \
    if(Mod(automorphisms[k], absolute_polynomial) \
        != Mod(root_variable, absolute_polynomial), tau = automorphisms[k]));
  my(tau_units = vector(#field_bnf.fu, k, \
    Mod(subst(lift(field_bnf.fu[k]), variable(absolute_polynomial), tau), \
      absolute_polynomial)));
  my(tau_matrix = free_unit_exponents(field_bnf, tau_units));
  my(anti_lattice = matkerint(matid(2) + tau_matrix));
  my(anti_generator_exponents = anti_lattice[, 1]);
  my(anti_generator = Mod(1, absolute_polynomial));
  my(stark_unit);
  my(l_imprimitive = find_l_record(L_imprimitive, character));
  my(l_primitive = find_l_record(L_primitive, character));

  for(k = 1, #field_bnf.fu, \
    anti_generator *= field_bnf.fu[k]^anti_generator_exponents[k]);
  stark_unit = anti_generator^2;

  print(Str("CHARACTER_", j), "=", character);
  print(Str("CONDUCTOR_", j), "=", bnrconductor(ray24, character));
  print(Str("RELATIVE_POLYNOMIAL_", j), "=", relative_polynomial);
  print(Str("ABSOLUTE_POLYNOMIAL_", j), "=", absolute_polynomial);
  print(Str("SIGNATURE_", j), "=", field_bnf.sign);
  print(Str("CLASS_NUMBER_", j), "=", field_bnf.no);
  print(Str("BNFCERTIFY_", j), "=", bnfcertify(field_bnf));
  print(Str("TAU_", j), "=", tau);
  print(Str("TAU_UNIT_MATRIX_", j), "=", tau_matrix);
  print(Str("NORM_EXPONENTS_", j), "=", norm_exponents);
  print(Str("RELATIVE_UNIT_NORM_INDEX_", j), "=", abs(norm_index));
  print(Str("ANTI_LATTICE_", j), "=", anti_lattice);
  print(Str("ANTI_GENERATOR_", j), "=", anti_generator);
  print(Str("ANTI_GENERATOR_MINPOLY_", j), "=", minpoly(anti_generator));
  print(Str("ANTI_GENERATOR_REAL_LOGS_", j), "=", \
    vector(2, k, log(abs(nfeltembed(field_bnf, anti_generator, k)))));
  print(Str("STARK_UNIT_", j), "=", stark_unit);
  print(Str("STARK_UNIT_MINPOLY_", j), "=", minpoly(stark_unit));
  print(Str("L_IMPRIMITIVE_", j), "=", l_imprimitive);
  print(Str("L_PRIMITIVE_", j), "=", l_primitive);
  assert_equal(Str("EXPECTED_E_", j), \
    valuation(abs(norm_index), 2), expected_e[j]);
  assert_equal(Str("EXPECTED_T_S_", j), expected_t_S[j], 1-expected_e[j]);
  assert_equal(Str("ROBLOT_UNIT_INDEX_", j), 2, \
    2^(expected_e[j] + expected_t_S[j]));
  assert_small(Str("STARK_LOG_RESIDUAL_", j), \
    log(abs(nfeltembed(field_bnf, stark_unit, positive_embedding[j]))) \
      - l_imprimitive[2], 1e-80);
});

quit();
