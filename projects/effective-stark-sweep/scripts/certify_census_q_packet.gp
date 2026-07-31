\\ Exact Engine-A packet polynomial for one Q row.
\\ Caller defines CASE_ID, D_VALUE and H11,H12,H21,H22.

default(realprecision, 100);
default(parisizemax, 1500000000);
read("scripts/census_packet_conventions.gp");

field_polynomial(d) =
{
  if(d % 4 == 1,
    return(y^2 - y + (1-d)/4),
    return(y^2 - d)
  );
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
  x^degree * subst(polynomial, x, 1/x)
    == polcoef(polynomial, 0) * polynomial;
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

integer_decimal_digits(value) =
{
  if(value == 0, 1, #Str(abs(value)));
};

coefficient_coordinate_digit_height(polynomial) =
{
  my(answer = 1);
  for(exponent = 0, poldegree(polynomial),
    my(coefficient = lift(polcoef(polynomial, exponent)));
    for(base_exponent = 0, 1,
      my(coordinate = polcoef(coefficient, base_exponent, y));
      answer = max(
        answer,
        max(
          integer_decimal_digits(numerator(coordinate)),
          integer_decimal_digits(denominator(coordinate))
        )
      );
    );
  );
  answer;
};

run_packet() =
{
  my(K = bnfinit(field_polynomial(D_VALUE), 1));
  my(finite_ideal = [H11, H12; H21, H22]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(cyc = Vec(ray.cyc));
  my(sign_generator = if(H11 <= 2, 1, H11 - 1));
  my(sign_log = Vec(
    bnrisprincipal(ray, idealhnf(K, sign_generator), 0)
  ));
  my(supported = List(), effective = List());
  my(relative_fields = List(), absolute_fields = List());
  my(base_generators = List(), relative_units = List());
  my(scalars = List(), powered_exponents, powered_traces);
  my(character_records = List(), common_denominator = 1);
  my(artin_sign_rows = List(), artin_image_size);
  my(ambient, packet_factor, absolute_packet);
  my(full_relative, full_equation, Hpol, H_base_generator, H);
  my(H_base_signs, H_split_embedding = 0, identity_power);
  my(identity_packet, lift_factorization, matching_factors = List());
  my(coordinate_digit_height);

  if(bnfcertify(K) != 1, error("base bnfcertify failed"));
  for(code = 1, group_order(cyc) - 1,
    my(character = decode_element(code, cyc));
    if(character_order(character, cyc) == 2
       && denominator(
         character_pairing(character, sign_log, cyc)
       ) != 1,
      listput(supported, character));
  );
  supported = Vec(supported);

  for(supported_index = 1, #supported,
    my(character = supported[supported_index]);
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
    if(euler == 0,
      listput(character_records,
        [character, 0, primitive_modulus, 0, 0]);
      next);

    my(relative = bnrclassfield(ray, kernel, 1));
    my(relative_field = rnfinit(K, relative, 1));
    my(equation = rnfequation(K, relative, 1));
    my(absolute = equation[1]);
    my(base_generator = equation[2]);
    my(L = bnfinit(absolute, 1));
    my(norm_coordinates, norm_kernel, relative_vector);
    my(unit = Mod(1, absolute));
    my(base_unit, base_vector, unit_vector, relative_index);
    my(relative_value, relative_norm, scalar);

    if(bnfcertify(L) != 1, error("quartic bnfcertify failed"));
    norm_coordinates = vector(#L.fu, unit_index,
      bnfisunit(
        K,
        rnfeltnorm(
          relative_field,
          rnfeltabstorel(relative_field, L.fu[unit_index])
        )
      )[1]);
    norm_kernel = matkerint(Mat(norm_coordinates));
    if(matsize(norm_kernel)[2] != 1,
      error("relative norm kernel rank changed"));
    relative_vector = norm_kernel[, 1];
    if(relative_vector[1] < 0,
      relative_vector = -relative_vector);
    for(unit_index = 1, #L.fu,
      unit *= L.fu[unit_index]^relative_vector[unit_index]);
    base_unit = Mod(
      subst(lift(K.fu[1]), y, lift(base_generator)),
      absolute
    );
    base_vector = bnfisunit(L, base_unit)[1..#L.fu];
    unit_vector = bnfisunit(L, unit)[1..#L.fu];
    relative_index = abs(matdet(Mat([base_vector, unit_vector])));
    if(relative_index == 0, error("relative unit index vanished"));
    relative_value = rnfeltabstorel(relative_field, unit);
    relative_norm = rnfeltnorm(relative_field, relative_value);
    scalar =
      4/group_order(cyc) * euler
      * (L.no/K.no) * (K.tu[1]/L.tu[1])
      / relative_index;

    listput(effective, character);
    listput(relative_fields, relative_field);
    listput(absolute_fields, absolute);
    listput(base_generators, base_generator);
    listput(relative_units, unit);
    listput(scalars, scalar);
    listput(character_records,
      [character, euler, primitive_modulus, relative_index, scalar]);
    common_denominator =
      lcm(common_denominator, denominator(scalar));
  );

  effective = Vec(effective);
  relative_fields = Vec(relative_fields);
  absolute_fields = Vec(absolute_fields);
  base_generators = Vec(base_generators);
  relative_units = Vec(relative_units);
  scalars = Vec(scalars);

  if(#effective == 0,
    artin_image_size = 1;
    ambient = x - 1;
    packet_factor = x - 1,
    for(code = 0, group_order(cyc) - 1,
      my(element = decode_element(code, cyc));
      listput(artin_sign_rows,
        vector(#effective, index,
          character_sign(effective[index], element, cyc)));
    );
    artin_sign_rows = Set(Vec(artin_sign_rows));
    artin_image_size = #artin_sign_rows;

    powered_exponents = vector(#effective, index,
      common_denominator * scalars[index]);
    for(index = 1, #effective,
      if(denominator(powered_exponents[index]) != 1,
        error("powered exponent is not integral")));
    powered_traces = vector(#effective, index,
      my(relative_value = rnfeltabstorel(
        relative_fields[index],
        relative_units[index]^powered_exponents[index]
      ));
      if(rnfeltnorm(relative_fields[index], relative_value) != 1,
        error("powered relative unit does not have norm one"));
      census_orient_trace(
        K,
        rnfelttrace(relative_fields[index], relative_value)
      )
    );
    ambient = census_trace_synthesis(powered_traces);
    if(!census_is_reciprocal(ambient),
      error("ambient polynomial is not reciprocal"));

    full_relative =
      bnrclassfield(ray, matdiagonal(cyc), 1);
    full_equation = rnfequation(K, full_relative, 1);
    Hpol = full_equation[1];
    H_base_generator = Mod(full_equation[2], Hpol);
    H = nfinit(Hpol);
    H_base_signs = nfeltsign(H, H_base_generator);
    for(index = 1, H.r1,
      if(!H_split_embedding && H_base_signs[index] == 1,
        H_split_embedding = index));
    if(!H_split_embedding,
      error("no full-field embedding above selected split place"));

    identity_power = Mod(1, Hpol);
    for(index = 1, #effective,
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
      if(#compatible != 2,
        error("K-compatible inclusion count changed"));
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
      if(nfeltsign(H, image - 1, [H_split_embedding])[1] != 1,
        error("embedded relative unit is not above one"));
      identity_power *= image^powered_exponents[index];
    );
    if(evaluate_K_polynomial_in_H(
         ambient, H_base_generator, identity_power, Hpol) != 0,
      error("identity power is not on ambient polynomial"));

    if(common_denominator == 1,
      identity_packet = identity_power,
      my(packet_root_base);
      if(common_denominator != 2,
        error("unregistered packet denominator"));
      if(!nfeltissquare(H, identity_power, &packet_root_base),
        error("identity power is not an exact square"));
      identity_packet = nfbasistoalg(H, packet_root_base);
      if(nfeltsign(
           H, identity_packet, [H_split_embedding])[1] < 0,
        identity_packet = -identity_packet);
      if(nfeltsign(
           H, identity_packet, [H_split_embedding])[1] != 1,
        error("positive packet root not found"));
      if(identity_packet^2 != identity_power,
        error("exact packet square identity failed"));
    );

    lift_factorization =
      nffactor(K, subst(lift(ambient), x,
        x^common_denominator));
    for(index = 1, matsize(lift_factorization)[1],
      if(evaluate_K_polynomial_in_H(
           lift_factorization[index, 1],
           H_base_generator,
           identity_packet,
           Hpol
         ) == 0,
        listput(matching_factors,
          lift_factorization[index, 1]));
    );
    matching_factors = Vec(matching_factors);
    if(#matching_factors != 1,
      error("identity packet factor is not unique"));
    packet_factor = matching_factors[1];
  );

  if(poldegree(packet_factor) != artin_image_size,
    error("packet factor degree differs from Artin image"));
  if(!census_is_reciprocal(packet_factor),
    error("packet factor is not reciprocal"));
  if(!census_polynomial_has_positive_root_sign_pattern(
       K, packet_factor),
    error(Str(
      "packet factor fails positive-root coefficient signs: ",
      packet_factor
    )));
  if(poldegree(gcd(packet_factor, deriv(packet_factor))) != 0,
    error("packet factor is not squarefree"));
  if(matsize(nffactor(K, lift(packet_factor)))[1] != 1,
    error("packet factor is reducible over K"));
  coordinate_digit_height =
    coefficient_coordinate_digit_height(packet_factor);
  if(coordinate_digit_height > 256,
    error("packet factor exceeds frozen coefficient digit cap"));
  absolute_packet =
    polresultant(K.pol, lift(packet_factor), y);

  print("CASE_ID=", CASE_ID);
  print("PARI_VERSION=", version());
  print("BASE_BNFCERTIFY=1");
  print("RAY_CYC=", cyc);
  print("SIGN_LOG=", sign_log);
  print("SUPPORTED_CHARACTERS=", supported);
  print("EFFECTIVE_CHARACTERS=", effective);
  print("CHARACTER_RECORDS=", Vec(character_records));
  print("COMMON_DENOMINATOR=", common_denominator);
  print("POWERED_EXPONENTS=",
    if(#effective, powered_exponents, []));
  print("POWERED_TRACES=",
    if(#effective, powered_traces, []));
  print("FORMAL_SIGN_ORBIT_DEGREE=", poldegree(ambient));
  print("EFFECTIVE_ARTIN_IMAGE_SIZE=", artin_image_size);
  print("PACKET_FACTOR_OVER_K=", packet_factor);
  print("PACKET_FACTOR_DEGREE=", poldegree(packet_factor));
  print("PACKET_FACTOR_RECIPROCAL=1");
  print("PACKET_FACTOR_SQUAREFREE=1");
  print("PACKET_FACTOR_IRREDUCIBLE_OVER_K=1");
  print("PACKET_FACTOR_POSITIVE_ROOT_SIGN_PATTERN=1");
  print("COEFFICIENT_COORDINATE_DECIMAL_DIGITS=",
    coordinate_digit_height);
  print("ABSOLUTE_PACKET_RESULTANT=", absolute_packet);
  print("PACKET_POLYNOMIAL_SYNTHESIS=PASS");
  print("ANALYTIC_PACKET_TARGET_OPENED=0");
};

run_packet();
