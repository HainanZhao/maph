\\ Height-only Engine-A calibration for one Q row.
\\ Caller defines CASE_ID, D_VALUE and H11,H12,H21,H22.
\\ No packet polynomial or analytic packet target is constructed.

default(realprecision, 100);
default(parisizemax, 1000000000);
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

run_calibration() =
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
  my(scalars = List(), components = List(), denominators = List());
  my(artin_sign_rows = List(), effective_artin_image_size);

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

  for(index = 1, #supported,
    my(character = supported[index]);
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
    if(euler == 0, next);

    my(relative = bnrclassfield(ray, kernel, 1));
    my(relative_field = rnfinit(K, relative, 1));
    my(equation = rnfequation(K, relative, 1));
    my(absolute = equation[1]);
    my(base_generator = equation[2]);
    my(L = bnfinit(absolute, 1));
    my(norm_coordinates, norm_kernel, relative_vector);
    my(unit = Mod(1, absolute));
    my(base_unit, base_vector, unit_vector, relative_index);
    my(relative_value, trace_value, oriented_trace);
    my(trace_embeddings, trace_at_split, log_unit, scalar);

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
    if(rnfeltnorm(relative_field, relative_value) != 1,
      error("selected relative unit does not have norm one"));
    trace_value = rnfelttrace(relative_field, relative_value);
    oriented_trace = census_orient_trace(K, trace_value);
    trace_embeddings = nfeltembed(K, oriented_trace);
    trace_at_split =
      real(trace_embeddings[CENSUS_SPLIT_REAL_PLACE]);
    if(trace_at_split < 2, error("oriented trace is below two"));
    log_unit = acosh(trace_at_split/2);
    scalar =
      euler * (L.no/K.no) * (K.tu[1]/L.tu[1])
      * 2 / relative_index;

    listput(effective, character);
    listput(scalars, scalar);
    listput(components, abs(scalar) * log_unit);
    listput(denominators, denominator(
      2/group_order(cyc) * scalar));
  );

  effective = Vec(effective);
  if(#effective == 0,
    effective_artin_image_size = 1,
    for(code = 0, group_order(cyc) - 1,
      my(element = decode_element(code, cyc));
      listput(artin_sign_rows,
        vector(#effective, index,
          character_sign(effective[index], element, cyc)));
    );
    effective_artin_image_size = #Set(Vec(artin_sign_rows));
  );

  print("CASE_ID=", CASE_ID);
  print("GROUP_ORDER=", group_order(cyc));
  print("SUPPORTED_CHARACTER_COUNT=", #supported);
  print("EFFECTIVE_CHARACTER_COUNT=", #effective);
  print("EFFECTIVE_ARTIN_IMAGE_SIZE=", effective_artin_image_size);
  print("LPRIME_ABS_COMPONENTS=", Vec(components));
  print("PACKET_EXPONENT_DENOMINATORS=", Vec(denominators));
  print("PACKET_POLYNOMIAL_CONSTRUCTED=0");
  print("ANALYTIC_PACKET_TARGET_OPENED=0");
  print("HEIGHT_CALIBRATION=PASS");
};

run_calibration();
