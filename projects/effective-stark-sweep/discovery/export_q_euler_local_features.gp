\\ Exact local feature export for one quadratic-support census row.
\\ Caller defines CASE_ID, D_VALUE and H11,H12,H21,H22.

default(realprecision, 80);
default(parisizemax, 2000000000);

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
    answer = lcm(
      answer,
      cyc[index] / gcd(cyc[index], character[index])
    );
  );
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
  my(supported = List());

  for(code = 1, group_order(cyc) - 1,
    my(character = decode_element(code, cyc));
    if(character_order(character, cyc) == 2
       && denominator(character_on(character, sign_log, cyc)) != 1,
      listput(supported, character);
    );
  );
  supported = Vec(supported);

  my(total_zero = 0, total_removed = 0);
  print("CASE_ID=", CASE_ID);
  print("RAY_CYC=", cyc);
  print("SIGN_LOG=", sign_log);
  print("SUPPORTED_CHARACTER_COUNT=", #supported);

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
    my(this_zero = 0, this_removed = 0);

    print("CHARACTER_", index, "_COORDS=", character);
    print("CHARACTER_", index, "_PRIMITIVE_CYC=", primitive_cyc);
    print("CHARACTER_", index, "_PRIMITIVE_COORDS=", primitive_chi);
    print("CHARACTER_", index, "_PRIMITIVE_CONDUCTOR_HNF=",
          idealhnf(K, primitive_modulus[1]));

    for(row = 1, matsize(factors)[1],
      my(prime_ideal = factors[row, 1]);
      if(idealval(K, primitive_modulus[1], prime_ideal) == 0,
        my(prime_log = Vec(
          bnrisprincipal(primitive_ray, prime_ideal, 0)
        ));
        my(value_log =
          character_on(primitive_chi, prime_log, primitive_cyc));
        my(value_denominator = denominator(value_log));
        my(value_sign);
        if(value_denominator != 1 && value_denominator != 2,
          error("nonquadratic local character value encountered"));
        value_sign = if(value_denominator == 1, 1, -1);
        this_removed++;
        if(value_sign == 1, this_zero = 1);
        print("CHARACTER_", index, "_REMOVED_", this_removed,
              "_RATIONAL_PRIME=", prime_ideal[1]);
        print("CHARACTER_", index, "_REMOVED_", this_removed,
              "_RAMIFICATION_INDEX=", prime_ideal[3]);
        print("CHARACTER_", index, "_REMOVED_", this_removed,
              "_RESIDUE_DEGREE=", prime_ideal[4]);
        print("CHARACTER_", index, "_REMOVED_", this_removed,
              "_ABSOLUTE_NORM=", idealnorm(K, prime_ideal));
        print("CHARACTER_", index, "_REMOVED_", this_removed,
              "_MODULUS_EXPONENT=", factors[row, 2]);
        print("CHARACTER_", index, "_REMOVED_", this_removed,
              "_PRIMITIVE_VALUE=", value_sign);
        print("CHARACTER_", index, "_REMOVED_", this_removed,
              "_PRIME_HNF=", idealhnf(K, prime_ideal));
      );
    );
    print("CHARACTER_", index, "_REMOVED_COUNT=", this_removed);
    print("CHARACTER_", index, "_ZERO_EULER=", this_zero);
    total_removed += this_removed;
    total_zero += this_zero;
  );
  print("ZERO_EULER_CHARACTER_COUNT=", total_zero);
  print("REMOVED_PRIME_COUNT=", total_removed);
  print("Q_EULER_LOCAL_FEATURE_EXPORT_VERIFIED=1");
};

run_export();
