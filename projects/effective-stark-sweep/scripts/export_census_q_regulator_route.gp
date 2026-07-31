\\ Independent regulator-route inputs for one sampled Q row.
\\ Caller defines CASE_ID, D_VALUE and H11,H12,H21,H22.
\\ No relative-unit norm kernel or packet polynomial is constructed.

default(realprecision, 100);
default(parisizemax, 1000000000);

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

run_export() =
{
  my(K = bnfinit(field_polynomial(D_VALUE), 1));
  my(finite_ideal = [H11, H12; H21, H22]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(cyc = Vec(ray.cyc));
  my(sign_generator = if(H11 <= 2, 1, H11 - 1));
  my(sign_log = Vec(
    bnrisprincipal(ray, idealhnf(K, sign_generator), 0)
  ));
  my(supported = List(), effective_count = 0);

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

  print("CASE_ID=", CASE_ID);
  print("GROUP_ORDER=", group_order(cyc));
  print("RAY_CYC=", cyc);
  print("SUPPORTED_CHARACTERS=", supported);
  print("BASE_POLYNOMIAL_COEFFICIENTS=", Vec(K.pol));
  print("BASE_UNIT_COEFFICIENTS=", Vec(lift(K.fu[1])));
  print("BASE_CLASS_NUMBER=", K.no);
  print("BASE_TORSION_ORDER=", K.tu[1]);

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
    print("CHARACTER_", index, "_CHARACTER=", character);
    print("CHARACTER_", index, "_EULER=", euler);
    if(euler == 0, next);

    my(relative = bnrclassfield(ray, kernel, 1));
    my(absolute = rnfequation(K, relative, 1)[1]);
    my(L = bnfinit(absolute, 1));
    if(bnfcertify(L) != 1, error("quartic bnfcertify failed"));
    if(L.sign != [2, 1], error("quartic signature changed"));
    effective_count++;
    print("CHARACTER_", index, "_ABSOLUTE_POLYNOMIAL_COEFFICIENTS=",
      Vec(absolute));
    print("CHARACTER_", index, "_UNIT_1_COEFFICIENTS=",
      Vec(lift(L.fu[1])));
    print("CHARACTER_", index, "_UNIT_2_COEFFICIENTS=",
      Vec(lift(L.fu[2])));
    print("CHARACTER_", index, "_CLASS_NUMBER=", L.no);
    print("CHARACTER_", index, "_TORSION_ORDER=", L.tu[1]);
    print("CHARACTER_", index, "_BNFCERTIFY=1");
  );
  print("EFFECTIVE_CHARACTER_COUNT=", effective_count);
  print("RELATIVE_UNIT_NORM_KERNEL_OPENED=0");
  print("PACKET_POLYNOMIAL_OPENED=0");
  print("REGULATOR_ROUTE_EXPORT=PASS");
};

run_export();
