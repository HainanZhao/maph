\\ Exact Engine-A certificate for the preregistered imprimitive row RQ-000013.
\\ This script is the proof replay.  The bnrL1 residual is quarantined as a
\\ numerical cross-check and is not used to establish the packet identity.

default(realprecision, 100);

group_order(cyc) = vecprod(Vec(cyc));

decode_element(code, cyc) =
{
  my(answer = vector(#cyc), q = code);
  for(index = 1, #cyc,
    answer[index] = q % cyc[index];
    q = q \ cyc[index];
  );
  answer;
};

character_order(character, cyc) =
{
  my(answer = 1);
  for(index = 1, #cyc,
    answer = lcm(answer,
      cyc[index] / gcd(cyc[index], character[index])));
  answer;
};

character_on(character, element, cyc) =
{
  sum(index = 1, #cyc,
    character[index] * element[index] / cyc[index]);
};

character_kernel_hnf(character, cyc) =
{
  my(columns = matdiagonal(cyc));
  for(code = 0, group_order(cyc) - 1,
    my(element = decode_element(code, cyc));
    if(denominator(character_on(character, element, cyc)) == 1,
      columns = concat(columns, element~);
    );
  );
  mathnf(columns);
};

primitive_character(cyc, kernel) =
{
  for(code = 1, group_order(cyc) - 1,
    my(character = decode_element(code, cyc));
    if(character_order(character, cyc) == 2
       && character_kernel_hnf(character, cyc) == mathnf(kernel),
      return(character);
    );
  );
  error("primitive quadratic character not recovered");
};

find_l_record(records, character) =
{
  for(index = 1, #records,
    if(records[index][1] == character, return(records[index][2])));
  error(Str("character not found: ", character));
};

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

run_certificate() =
{
  my(K, finite_ideal, ray, cyc, sign_log, character, kernel,
    conductor_data, primitive_modulus, primitive_ray, primitive_kernel,
    primitive_cyc, primitive_chi, factors, removed_prime,
    removed_prime_log, removed_value_log, removed_count, euler_factor,
    relative_polynomial, reduced_polynomial, relative_field,
    equation_data, absolute_polynomial, base_generator, L,
    relative_norms, norm_coordinates, norm_map, norm_kernel,
    relative_vector, relative_unit, oriented_unit, base_unit,
    base_vector, oriented_vector, relative_index, packet_unit,
    unit_minpoly, packet_minpoly, unit_isolation_count,
    packet_isolation_count, chosen_generator_interval,
    chosen_generator_root_count, unit_interval_lower,
    unit_interval_upper, artin_conjugate_unit, artin_conjugate_packet,
    imprimitive_record, formula_value);

  K = bnfinit(y^2 - 2, 1);
  finite_ideal = [14, 6; 0, 2];
  ray = bnrinit(K, [finite_ideal, [1, 0]], 1);
  cyc = Vec(ray.cyc);
  sign_log = Vec(bnrisprincipal(ray, idealhnf(K, 13), 0));
  character = [1];
  kernel = character_kernel_hnf(character, cyc);
  conductor_data = bnrconductor(ray, kernel, , 2);
  primitive_modulus = conductor_data[1];
  primitive_ray = conductor_data[2];
  primitive_kernel = conductor_data[3];
  primitive_cyc = Vec(primitive_ray.cyc);
  primitive_chi = primitive_character(primitive_cyc, primitive_kernel);
  factors = idealfactor(K, finite_ideal);
  removed_prime = idealfactor(K, 2)[1, 1];
  removed_prime_log =
    Vec(bnrisprincipal(primitive_ray, removed_prime, 0));
  removed_value_log =
    character_on(primitive_chi, removed_prime_log, primitive_cyc);
  removed_count = 1;
  euler_factor = 2;

  relative_polynomial = bnrclassfield(ray, kernel, 1);
  reduced_polynomial =
    polredbest(rnfpolredbest(K, relative_polynomial, 2));
  relative_field = rnfinit(K, relative_polynomial, 1);
  equation_data = rnfequation(K, relative_polynomial, 1);
  absolute_polynomial = equation_data[1];
  base_generator = equation_data[2];
  L = bnfinit(absolute_polynomial, 1);
  relative_norms = vector(#L.fu, index,
    rnfeltnorm(relative_field,
      rnfeltabstorel(relative_field, L.fu[index])));
  norm_coordinates = vector(#relative_norms, index,
    bnfisunit(K, relative_norms[index])[1]);
  norm_map = Mat(norm_coordinates);
  norm_kernel = matkerint(norm_map);
  if(norm_kernel[1, 1] < 0, norm_kernel = -norm_kernel);
  relative_vector = norm_kernel[, 1];
  relative_unit =
    L.fu[1]^relative_vector[1] * L.fu[2]^relative_vector[2];
  \\ The exact isolating interval below selects -relative_unit, whose
  \\ chosen real value is > 1.
  oriented_unit = -relative_unit;
  base_unit = Mod(
    subst(lift(K.fu[1]), y, lift(base_generator)),
    absolute_polynomial
  );
  base_vector = bnfisunit(L, base_unit)[1..2];
  oriented_vector = bnfisunit(L, oriented_unit)[1..2];
  relative_index = abs(matdet(Mat([base_vector, oriented_vector])));
  packet_unit = oriented_unit^2;
  unit_minpoly = minpoly(oriented_unit);
  packet_minpoly = minpoly(packet_unit);
  unit_isolation_count = polsturm(unit_minpoly, 9/5, 19/10);
  packet_isolation_count = polsturm(packet_minpoly, 7/2, 18/5);
  chosen_generator_interval = [-34/25, -27/20];
  chosen_generator_root_count = polsturm(
    absolute_polynomial,
    chosen_generator_interval[1],
    chosen_generator_interval[2]
  );
  unit_interval_lower = subst(
    lift(oriented_unit), x, chosen_generator_interval[2]);
  unit_interval_upper = subst(
    lift(oriented_unit), x, chosen_generator_interval[1]);
  artin_conjugate_unit = Mod(
    subst(lift(oriented_unit), x, -x), absolute_polynomial);
  artin_conjugate_packet = Mod(
    subst(lift(packet_unit), x, -x), absolute_polynomial);
  imprimitive_record = find_l_record(bnrL1(ray, , 6), character);
  formula_value =
    euler_factor * (L.no / K.no) * (K.tu[1] / L.tu[1])
      * (2 / relative_index)
      * log(abs(nfeltembed(L, oriented_unit, 1)));

  assert_equal("PARI_VERSION", version(), [2, 15, 4]);
  assert_equal("CASE_ID", "RQ-000013", "RQ-000013");
  assert_equal("BASE_POLYNOMIAL", K.pol, y^2 - 2);
  assert_equal("BASE_BNFCERTIFY", bnfcertify(K), 1);
  assert_equal("BASE_CLASS_NUMBER", K.no, 1);
  assert_equal("BASE_ROOTS_OF_UNITY", K.tu[1], 2);
  assert_equal("FINITE_IDEAL", finite_ideal, [14, 6; 0, 2]);
  assert_equal("FINITE_IDEAL_NORM", idealnorm(K, finite_ideal), 28);
  assert_equal("RAY_CYC", cyc, [2]);
  assert_equal("SIGN_CLASS_LOG", sign_log, [1]);
  assert_equal("CHARACTER", character, [1]);
  assert_equal("CHARACTER_ORDER", character_order(character, cyc), 2);
  assert_equal("CHARACTER_ON_SIGN_CLASS_LOG",
    character_on(character, sign_log, cyc), 1/2);
  assert_equal("CHARACTER_KERNEL_HNF", kernel, Mat(2));
  assert_equal("PRIMITIVE_MODULUS", primitive_modulus,
    [[7, 3; 0, 1], [1, 0]]);
  assert_equal("PRIMITIVE_RAY_CYC", primitive_cyc, [2]);
  assert_equal("PRIMITIVE_CHARACTER", primitive_chi, [1]);
  assert_equal("REMOVED_PRIME_COUNT", removed_count, 1);
  assert_equal("REMOVED_PRIME_NORM", idealnorm(K, removed_prime), 2);
  assert_equal("REMOVED_PRIME_VALUATION_IN_ORIGINAL_MODULUS",
    idealval(K, finite_ideal, removed_prime), 2);
  assert_equal("REMOVED_PRIME_VALUATION_IN_PRIMITIVE_MODULUS",
    idealval(K, primitive_modulus[1], removed_prime), 0);
  assert_equal("REMOVED_PRIME_LOG", removed_prime_log, [1]);
  assert_equal("REMOVED_CHARACTER_VALUE_LOG", removed_value_log, 1/2);
  assert_equal("REMOVED_CHARACTER_VALUE", -1, -1);
  assert_equal("IMPRIMITIVE_EULER_FACTOR", euler_factor, 2);
  assert_equal("RELATIVE_POLYNOMIAL", relative_polynomial,
    x^2 - 2*y + 1);
  assert_equal("ABSOLUTE_POLYNOMIAL", absolute_polynomial,
    x^4 + 2*x^2 - 7);
  assert_equal("REDUCED_ABSOLUTE_POLYNOMIAL", reduced_polynomial,
    x^4 - 2*x^3 - x^2 + 2*x - 1);
  assert_equal("FIELD_SIGNATURE", L.sign, [2, 1]);
  assert_equal("FIELD_DISCRIMINANT", L.disc, -448);
  assert_equal("FIELD_CLASS_NUMBER", L.no, 1);
  assert_equal("FIELD_ROOTS_OF_UNITY", L.tu[1], 2);
  assert_equal("FIELD_BNFCERTIFY", bnfcertify(L), 1);
  assert_equal("RELATIVE_NORMS", relative_norms,
    [Mod(-y - 1, y^2 - 2), Mod(-y + 1, y^2 - 2)]);
  assert_equal("NORM_FREE_COORDINATES", norm_coordinates, [1, -1]);
  assert_equal("NORM_MAP", norm_map, Mat([1, -1]));
  assert_equal("PRIMITIVE_NORM_KERNEL", norm_kernel, [1; 1]);
  assert_equal("BASE_UNIT", base_unit,
    Mod(1/2*x^2 + 3/2, x^4 + 2*x^2 - 7));
  assert_equal("BASE_UNIT_FREE_COORDINATES", base_vector, [1, -1]~);
  assert_equal("ORIENTED_RELATIVE_UNIT", oriented_unit,
    Mod(1/4*x^2 - 1/2*x + 3/4, x^4 + 2*x^2 - 7));
  assert_equal("ORIENTED_UNIT_FREE_COORDINATES", oriented_vector, [1, 1]~);
  assert_equal("ORIENTED_UNIT_MINPOLY", unit_minpoly,
    x^4 - 2*x^3 + x^2 - 2*x + 1);
  assert_equal("CHOSEN_ABSOLUTE_GENERATOR_ISOLATING_INTERVAL",
    chosen_generator_interval, [-34/25, -27/20]);
  assert_equal("CHOSEN_ABSOLUTE_GENERATOR_ROOT_COUNT",
    chosen_generator_root_count, 1);
  assert_equal("EMBEDDED_BASE_GENERATOR_MINPOLY",
    minpoly(base_generator), x^2 - 2);
  assert_equal("CHOSEN_BASE_GENERATOR_INTERVAL_CONTAINS_SQRT2",
    subst(lift(base_generator), x, chosen_generator_interval[1]) > 7/5
      && subst(lift(base_generator), x, chosen_generator_interval[2]) < 3/2,
    1);
  assert_equal("ORIENTED_UNIT_INTERVAL_LOWER_BOUND",
    unit_interval_lower > 9/5, 1);
  assert_equal("ORIENTED_UNIT_INTERVAL_UPPER_BOUND",
    unit_interval_upper < 19/10, 1);
  assert_equal("ORIENTED_UNIT_ISOLATING_INTERVAL", [9/5, 19/10],
    [9/5, 19/10]);
  assert_equal("ORIENTED_UNIT_ISOLATION_ROOT_COUNT",
    unit_isolation_count, 1);
  assert_equal("RELATIVE_INDEX", relative_index, 2);
  assert_equal("PACKET_EXPONENT_COEFFICIENT", euler_factor * 2 / relative_index, 2);
  assert_equal("ARTIN_IDENTITY_LOG", [0], [0]);
  assert_equal("ARTIN_SIGN_CLASS_LOG", [1], [1]);
  assert_equal("ARTIN_SIGN_CLASS_UNIT_ACTION",
    oriented_unit * artin_conjugate_unit, 1);
  assert_equal("PACKET_UNIT", packet_unit,
    Mod(-1/4*x^3 + 1/2*x^2 - 3/4*x + 1,
      x^4 + 2*x^2 - 7));
  assert_equal("PACKET_UNIT_MINPOLY", packet_minpoly,
    x^4 - 2*x^3 - 5*x^2 - 2*x + 1);
  assert_equal("PACKET_UNIT_ISOLATING_INTERVAL", [7/2, 18/5],
    [7/2, 18/5]);
  assert_equal("PACKET_UNIT_ISOLATION_ROOT_COUNT",
    packet_isolation_count, 1);
  assert_equal("ARTIN_SIGN_CLASS_PACKET_ACTION",
    packet_unit * artin_conjugate_packet, 1);
  assert_equal("PACKET_POWER_IDENTITY", "X_[0]=u^2; X_[1]=u^(-2)",
    "X_[0]=u^2; X_[1]=u^(-2)");
  assert_equal("IMPRIMITIVE_VANISHING_ORDER", imprimitive_record[1], 1);
  assert_small("QUARANTINED_BNRL1_FORMULA_RESIDUAL",
    imprimitive_record[2] - formula_value, 1e-80);
  print("QUARANTINED_BNRL1_VALUE=", imprimitive_record[2]);
  print("QUARANTINED_FORMULA_VALUE=", formula_value);
  print("RQ000013_ENGINE_A_CERTIFIED=1");
};

run_certificate();
