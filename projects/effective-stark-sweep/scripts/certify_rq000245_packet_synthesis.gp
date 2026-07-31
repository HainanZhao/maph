\\ Exact four-effective-character Artin-orbit synthesis anchor.
\\ No analytic L-value or packet target is read.

default(realprecision, 100);
default(parisizemax, 2000000000);
read("scripts/census_packet_conventions.gp");

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

group_order(cyc) = vecprod(Vec(cyc));

decode_element(code, cyc) =
{
  my(answer = vector(#cyc), quotient = code);
  for(index = 1, #cyc,
    answer[index] = quotient % cyc[index];
    quotient = quotient \ cyc[index];
  );
  answer;
};

character_order(character, cyc) =
{
  my(answer = 1);
  for(index = 1, #cyc,
    answer = lcm(
      answer,
      cyc[index] / gcd(cyc[index], character[index])
    ));
  answer;
};

character_pairing(character, element, cyc) =
{
  sum(index = 1, #cyc,
    character[index] * element[index] / cyc[index]);
};

character_sign(character, element, cyc) =
{
  if(denominator(character_pairing(character, element, cyc)) == 1,
    1,
    -1
  );
};

character_kernel_hnf(character, cyc) =
{
  my(columns = matdiagonal(cyc));
  for(code = 0, group_order(cyc) - 1,
    my(element = decode_element(code, cyc));
    if(denominator(character_pairing(character, element, cyc)) == 1,
      columns = concat(columns, element~));
  );
  mathnf(columns);
};

primitive_character(cyc, kernel) =
{
  for(code = 1, group_order(cyc) - 1,
    my(character = decode_element(code, cyc));
    if(character_order(character, cyc) == 2
       && character_kernel_hnf(character, cyc) == mathnf(kernel),
      return(character));
  );
  error("primitive quadratic character not recovered");
};

census_trace_step(polynomial, trace_value) =
{
  my(result = polresultant(
    subst(polynomial, x, z),
    x^2 - trace_value*x*z + z^2,
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

evaluate_K_polynomial_in_H(polynomial, base_generator, value, Hpol) =
{
  my(answer = Mod(0, Hpol));
  for(exponent = 0, poldegree(polynomial),
    my(embedded_coefficient = Mod(
      subst(
        lift(polcoef(polynomial, exponent)),
        y,
        lift(base_generator)
      ),
      Hpol
    ));
    answer += embedded_coefficient * value^exponent;
  );
  answer;
};

run_anchor() =
{
  my(K = bnfinit(y^2 - 7, 1));
  my(finite_ideal = [24, 4; 0, 4]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(cyc = Vec(ray.cyc));
  my(sign_log = Vec(
    bnrisprincipal(ray, idealhnf(K, 23), 0)
  ));
  my(supported = List());
  my(characters, character_sum, artin_sign_rows = List());
  my(relative_polynomials, relative_fields, absolute_fields);
  my(base_generators, field_bnfs, relative_units, relative_norms);
  my(relative_indices, euler_factors, scalars);
  my(common_denominator = 1, powered_exponents);
  my(powered_traces, ambient);
  my(full_relative, full_equation, H, Hpol, H_base_generator);
  my(H_base_signs, H_split_embedding = 0, embedded_units);
  my(identity_power = Mod(1, 1), identity_packet);
  my(packet_power_coordinates, packet_root_base, torsion_roots);
  my(lift_factorization, matching_factors = List(), packet_factor);

  for(code = 1, group_order(cyc) - 1,
    my(character = decode_element(code, cyc));
    if(character_order(character, cyc) == 2
       && denominator(
         character_pairing(character, sign_log, cyc)
       ) != 1,
      listput(supported, character));
  );
  characters = Vec(supported);
  assert_equal("CASE_ID", "RQ-000245", "RQ-000245");
  assert_equal("PARI_VERSION", version(), [2, 15, 4]);
  assert_equal("BASE_BNFCERTIFY", bnfcertify(K), 1);
  assert_equal("FINITE_IDEAL", finite_ideal, [24, 4; 0, 4]);
  assert_equal("FINITE_NORM", idealnorm(K, finite_ideal), 96);
  assert_equal("RAY_CYC", cyc, [2, 2, 2]);
  assert_equal("SIGN_LOG", sign_log, [1, 0, 1]);
  assert_equal("SUPPORTED_CHARACTER_COUNT", #characters, 4);
  print("SUPPORTED_CHARACTERS=", characters);

  character_sum = vector(#cyc, coordinate,
    sum(index = 1, #characters, characters[index][coordinate])
      % cyc[coordinate]);
  assert_equal("FOUR_CHARACTER_PRODUCT_RELATION", character_sum,
    [0, 0, 0]);
  for(code = 0, group_order(cyc) - 1,
    my(element = decode_element(code, cyc));
    my(signs = vector(#characters, index,
      character_sign(characters[index], element, cyc)));
    listput(artin_sign_rows, signs);
  );
  artin_sign_rows = Set(Vec(artin_sign_rows));
  assert_equal("ARTIN_SIGN_IMAGE_CARDINALITY", #artin_sign_rows, 8);
  for(index = 1, #artin_sign_rows,
    assert_equal(
      Str("ARTIN_SIGN_RELATION_", index),
      vecprod(artin_sign_rows[index]),
      1
    ));
  print("ARTIN_SIGN_IMAGE=", artin_sign_rows);

  relative_polynomials = vector(#characters);
  relative_fields = vector(#characters);
  absolute_fields = vector(#characters);
  base_generators = vector(#characters);
  field_bnfs = vector(#characters);
  relative_units = vector(#characters);
  relative_norms = vector(#characters);
  relative_indices = vector(#characters);
  euler_factors = vector(#characters);
  scalars = vector(#characters);

  for(index = 1, #characters,
    my(character = characters[index]);
    my(kernel = character_kernel_hnf(character, cyc));
    my(conductor_data = bnrconductor(ray, kernel, , 2));
    my(primitive_modulus = conductor_data[1]);
    my(primitive_ray = conductor_data[2]);
    my(primitive_kernel = conductor_data[3]);
    my(primitive_cyc = Vec(primitive_ray.cyc));
    my(primitive_chi =
      primitive_character(primitive_cyc, primitive_kernel));
    my(factors = idealfactor(K, finite_ideal));
    my(euler = 1);
    my(relative = bnrclassfield(ray, kernel, 1));
    my(relative_field = rnfinit(K, relative, 1));
    my(equation = rnfequation(K, relative, 1));
    my(absolute = equation[1]);
    my(base_generator = equation[2]);
    my(L = bnfinit(absolute, 1));
    my(norm_coordinates, norm_kernel, relative_vector);
    my(unit = Mod(1, absolute));
    my(base_unit, base_vector, unit_vector, relative_index);

    for(row = 1, matsize(factors)[1],
      my(prime_ideal = factors[row, 1]);
      if(idealval(K, primitive_modulus[1], prime_ideal) == 0,
        my(prime_log = Vec(
          bnrisprincipal(primitive_ray, prime_ideal, 0)
        ));
        if(denominator(character_pairing(
             primitive_chi, prime_log, primitive_cyc)) == 1,
          euler = 0,
          euler *= 2);
      );
    );
    assert_equal(Str("CHARACTER_", index, "_EULER_NONZERO"),
      euler != 0, 1);
    assert_equal(Str("CHARACTER_", index, "_FIELD_BNFCERTIFY"),
      bnfcertify(L), 1);
    assert_equal(Str("CHARACTER_", index, "_FIELD_SIGNATURE"),
      L.sign, [2, 1]);

    norm_coordinates = vector(#L.fu, unit_index,
      bnfisunit(
        K,
        rnfeltnorm(
          relative_field,
          rnfeltabstorel(relative_field, L.fu[unit_index])
        )
      )[1]);
    norm_kernel = matkerint(Mat(norm_coordinates));
    assert_equal(Str("CHARACTER_", index, "_NORM_KERNEL_RANK"),
      matsize(norm_kernel)[2], 1);
    relative_vector = norm_kernel[, 1];
    if(relative_vector[1] < 0, relative_vector = -relative_vector);
    for(unit_index = 1, #L.fu,
      unit *= L.fu[unit_index]^relative_vector[unit_index]);
    base_unit = Mod(
      subst(lift(K.fu[1]), y, lift(base_generator)),
      absolute
    );
    base_vector = bnfisunit(L, base_unit)[1..#L.fu];
    unit_vector = bnfisunit(L, unit)[1..#L.fu];
    relative_index =
      abs(matdet(Mat([base_vector, unit_vector])));

    relative_polynomials[index] = relative;
    relative_fields[index] = relative_field;
    absolute_fields[index] = absolute;
    base_generators[index] = base_generator;
    field_bnfs[index] = L;
    relative_units[index] = unit;
    relative_norms[index] = rnfeltnorm(
      relative_field, rnfeltabstorel(relative_field, unit));
    relative_indices[index] = relative_index;
    euler_factors[index] = euler;
    scalars[index] =
      4/group_order(cyc) * euler
      * (L.no/K.no) * (K.tu[1]/L.tu[1])
      / relative_index;
    common_denominator =
      lcm(common_denominator, denominator(scalars[index]));

    print("CHARACTER_", index, "_CHARACTER=", character);
    print("CHARACTER_", index, "_CONDUCTOR=", primitive_modulus);
    print("CHARACTER_", index, "_ABSOLUTE_FIELD=", absolute);
    print("CHARACTER_", index, "_NORM_MAP=", norm_coordinates);
    print("CHARACTER_", index, "_PRIMITIVE_NORM_KERNEL=",
      relative_vector);
    print("CHARACTER_", index, "_RELATIVE_NORM=",
      relative_norms[index]);
    print("CHARACTER_", index, "_RELATIVE_INDEX=", relative_index);
    print("CHARACTER_", index, "_EULER_FACTOR=", euler);
    print("CHARACTER_", index, "_PACKET_SCALAR=", scalars[index]);
  );

  powered_exponents = vector(#characters, index,
    common_denominator * scalars[index]);
  for(index = 1, #characters,
    if(relative_norms[index] == -1
       && powered_exponents[index] % 2,
      common_denominator *= 2;
      powered_exponents *= 2;
      break);
  );
  assert_equal("COMMON_DENOMINATOR", common_denominator,
    common_denominator);
  print("POWERED_EXPONENTS=", powered_exponents);
  for(index = 1, #characters,
    assert_equal(Str("POWERED_EXPONENT_", index, "_INTEGRAL"),
      denominator(powered_exponents[index]), 1));

  powered_traces = vector(#characters, index,
    my(relative_value = rnfeltabstorel(
      relative_fields[index],
      relative_units[index]^powered_exponents[index]
    ));
    assert_equal(Str("POWERED_UNIT_", index, "_RELATIVE_NORM"),
      rnfeltnorm(relative_fields[index], relative_value), 1);
    census_orient_trace(
      K,
      rnfelttrace(relative_fields[index], relative_value)
    );
  );
  print("POWERED_TRACES=", powered_traces);
  ambient = census_trace_synthesis(powered_traces);
  assert_equal("AMBIENT_FORMAL_SIGN_DEGREE", poldegree(ambient), 16);
  assert_equal("AMBIENT_FORMAL_SIGN_RECIPROCAL",
    census_is_reciprocal(ambient), 1);
  print("AMBIENT_FORMAL_SIGN_POLYNOMIAL=", ambient);

  full_relative =
    bnrclassfield(ray, matdiagonal(cyc), 1);
  assert_equal("FULL_RAY_RELATIVE_DEGREE",
    poldegree(full_relative), 8);
  full_equation = rnfequation(K, full_relative, 1);
  Hpol = full_equation[1];
  H_base_generator = Mod(full_equation[2], Hpol);
  H = bnfinit(Hpol, 1);
  assert_equal("FULL_RAY_ABSOLUTE_DEGREE", poldegree(Hpol), 16);
  assert_equal("FULL_RAY_BNFCERTIFY", bnfcertify(H), 1);
  H_base_signs = nfeltsign(H, H_base_generator);
  for(index = 1, H.r1,
    if(!H_split_embedding && H_base_signs[index] == 1,
      H_split_embedding = index));
  if(!H_split_embedding,
    error("no real embedding above the selected split base place"));
  print("FULL_RAY_SIGNATURE=", H.sign);
  print("FULL_RAY_SPLIT_EMBEDDING=", H_split_embedding);

  embedded_units = vector(#characters);
  identity_power = Mod(1, Hpol);
  for(index = 1, #characters,
    my(inclusions = nfisincl(
      absolute_fields[index], Hpol, 2));
    my(compatible = List());
    for(inclusion_index = 1, #inclusions,
      my(inclusion = inclusions[inclusion_index]);
      my(image_base = Mod(
        subst(
          lift(base_generators[index]),
          x,
          lift(inclusion)
        ),
        Hpol
      ));
      if(image_base == H_base_generator,
        listput(compatible, inclusion));
    );
    compatible = Vec(compatible);
    assert_equal(Str("CHARACTER_", index, "_K_COMPATIBLE_INCLUSIONS"),
      #compatible, 2);
    my(image = Mod(
      subst(
        lift(relative_units[index]),
        x,
        lift(compatible[1])
      ),
      Hpol
    ));
    if(nfeltsign(H, image, [H_split_embedding])[1] < 0,
      image = -image);
    if(nfeltsign(H, image - 1, [H_split_embedding])[1] < 0,
      image = 1/image);
    assert_equal(Str("CHARACTER_", index, "_ORIENTED_ABOVE_ONE"),
      nfeltsign(H, image - 1, [H_split_embedding])[1], 1);
    assert_equal(Str("CHARACTER_", index, "_EMBEDDED_TRACE"),
      image^powered_exponents[index]
        + image^(-powered_exponents[index]),
      Mod(
        subst(
          lift(powered_traces[index]),
          y,
          lift(H_base_generator)
        ),
        Hpol
      ));
    embedded_units[index] = image;
    identity_power *= image^powered_exponents[index];
  );
  assert_equal("IDENTITY_POWER_POSITIVE",
    nfeltsign(H, identity_power, [H_split_embedding])[1], 1);
  assert_equal("IDENTITY_POWER_ON_AMBIENT_POLYNOMIAL",
    evaluate_K_polynomial_in_H(
      ambient, H_base_generator, identity_power, Hpol), 0);

  packet_power_coordinates = bnfisunit(H, identity_power);
  assert_equal("IDENTITY_POWER_IS_FULL_RAY_UNIT",
    #packet_power_coordinates > 0, 1);
  packet_root_base = Mod(1, Hpol);
  for(index = 1, #H.fu,
    assert_equal(Str("PACKET_ROOT_FREE_COORDINATE_", index,
      "_DIVISIBLE"),
      packet_power_coordinates[index] % common_denominator,
      0);
    packet_root_base *=
      H.fu[index]^(
        packet_power_coordinates[index]/common_denominator);
  );
  torsion_roots = List();
  for(torsion_exponent = 0, H.tu[1] - 1,
    my(candidate =
      packet_root_base * H.tu[2]^torsion_exponent);
    if(candidate^common_denominator == identity_power,
      listput(torsion_roots, candidate));
  );
  torsion_roots = Vec(torsion_roots);
  assert_equal("PACKET_ROOT_TORSION_CANDIDATES_NONEMPTY",
    #torsion_roots > 0, 1);
  identity_packet = 0;
  for(index = 1, #torsion_roots,
    if(nfeltsign(
         H, torsion_roots[index], [H_split_embedding])[1] == 1,
      if(identity_packet,
        error("multiple positive packet roots in torsion orbit"));
      identity_packet = torsion_roots[index];
    );
  );
  if(!identity_packet, error("positive packet root not found"));
  assert_equal("IDENTITY_PACKET_POWER_IDENTITY",
    identity_packet^common_denominator, identity_power);

  lift_factorization =
    nffactor(K, subst(lift(ambient), x, x^common_denominator));
  print("PACKET_LIFT_FACTORIZATION=", lift_factorization);
  for(index = 1, matsize(lift_factorization)[1],
    if(evaluate_K_polynomial_in_H(
         lift_factorization[index, 1],
         H_base_generator,
         identity_packet,
         Hpol
       ) == 0,
      listput(matching_factors, lift_factorization[index, 1]));
  );
  matching_factors = Vec(matching_factors);
  assert_equal("IDENTITY_PACKET_MATCHING_FACTOR_COUNT",
    #matching_factors, 1);
  packet_factor = matching_factors[1];
  assert_equal("PACKET_FACTOR_RELATIVE_DEGREE",
    poldegree(packet_factor), 8);
  assert_equal("PACKET_FACTOR_RECIPROCAL",
    census_is_reciprocal(packet_factor), 1);
  assert_equal("PACKET_FACTOR_POSITIVE_ROOT_SIGN_PATTERN",
    census_polynomial_has_positive_root_sign_pattern(
      K, packet_factor), 1);
  assert_equal("PACKET_FACTOR_IRREDUCIBLE_OVER_K",
    matsize(nffactor(K, lift(packet_factor)))[1], 1);
  assert_equal("PACKET_ABSOLUTE_DEGREE",
    poldegree(minpoly(identity_packet)), 16);
  print("PACKET_FACTOR_OVER_K=", packet_factor);
  print("PACKET_ABSOLUTE_POLYNOMIAL=", minpoly(identity_packet));
  print("RQ000245_ARTIN_ORBIT_SYNTHESIS=PASS");
  print("CENSUS_ANALYTIC_TARGET_OPENED=0");
};

run_anchor();
