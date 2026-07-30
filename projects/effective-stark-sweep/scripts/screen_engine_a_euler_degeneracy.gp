\\ Exact imprimitive-Euler-factor audit for one Engine-A row.
\\ Caller defines CASE_ID, D_VALUE and H11,H12,H21,H22.

default(realprecision, 80);
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

run_audit() =
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

  my(zero_count = 0, removed_prime_count = 0);
  print("CASE_ID=", CASE_ID);
  print("SUPPORTED_QUADRATIC_CHARACTER_COUNT=", #supported);
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

    for(row = 1, matsize(factors)[1],
      my(prime_ideal = factors[row, 1]);
      if(idealval(K, primitive_modulus[1], prime_ideal) == 0,
        my(prime_log = Vec(
          bnrisprincipal(primitive_ray, prime_ideal, 0)
        ));
        my(value_log =
          character_on(primitive_chi, prime_log, primitive_cyc));
        this_removed++;
        if(denominator(value_log) == 1, this_zero = 1);
      );
    );
    zero_count += this_zero;
    removed_prime_count += this_removed;
    print("CHARACTER_", index, "_ZERO_EULER=", this_zero);
    print("CHARACTER_", index, "_REMOVED_PRIMES=", this_removed);
  );
  print("ZERO_EULER_CHARACTER_COUNT=", zero_count);
  print("REMOVED_PRIME_COUNT=", removed_prime_count);
  print("ENGINE_A_EULER_AUDIT_VERIFIED=1");
};

run_audit();
