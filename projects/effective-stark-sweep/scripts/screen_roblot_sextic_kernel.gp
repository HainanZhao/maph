\\ Exact Roblot Theorem 7.1 screen for one frozen order-six kernel.
\\ Caller defines CASE_ID, KERNEL_INDEX, D_VALUE, H11,H12,H21,H22,
\\ SOURCE_CYC, SOURCE_SIGN_LOG, and SOURCE_CHARACTER.

default(realprecision, 80);
default(parisizemax, 1500000000);

field_polynomial(d) =
{
  if(d % 4 == 1,
    return(y^2 - y + (1-d)/4),
    return(y^2 - d)
  );
};

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

fractional(value) = value - floor(value);

character_pairing(character, element, cyc) =
{
  sum(index = 1, #cyc,
    character[index] * element[index] / cyc[index]);
};

character_kernel_hnf(character, cyc) =
{
  my(elements = List(), total = vecprod(Vec(cyc)));
  for(code = 0, total - 1,
    my(element = decode_element(code, cyc));
    if(denominator(character_pairing(character, element, cyc)) == 1,
      listput(elements, element));
  );
  elements = Vec(elements);
  my(columns = matrix(
    #cyc, #elements, row, column, elements[column][row]
  ));
  mathnf(concat(matdiagonal(cyc), columns));
};

run_screen() =
{
  my(base = bnfinit(field_polynomial(D_VALUE), 1));
  my(finite_ideal = [H11, H12; H21, H22]);
  my(ray = bnrinit(base, [finite_ideal, [1, 0]], 1));
  my(cyc = Vec(ray.cyc));
  my(sign_generator = if(H11 <= 2, 1, H11 - 1));
  my(sign_log = Vec(bnrisprincipal(
    ray, idealhnf(base, sign_generator), 0
  )));
  my(conductor = bnrconductor(ray, SOURCE_CHARACTER));
  my(primitive_ray = bnrinit(base, conductor, 1));
  my(primitive_cyc = Vec(primitive_ray.cyc));
  my(transport = matrix(
    #primitive_cyc, #cyc, row, column,
    bnrisprincipal(primitive_ray, ray.gen[column], 0)[row]
  ));
  my(matches = List(), primitive_character, kernel);
  my(relative, relative_field, absolute, field);
  my(finite_factorization, local_rows = List());
  my(a1, a2, a3 = 1, extra_prime_count = 0);
  my(decomposition, ramification_rows = List());
  my(wild_above_three = 0, maximum_relative_e_above_three = 1);
  my(primitive_S, class_number_prime_to_three, applies);

  if(bnfcertify(base) != 1, error("base bnfcertify failed"));
  if(cyc != SOURCE_CYC, error("source ray cyc changed"));
  if(sign_log != SOURCE_SIGN_LOG, error("source sign log changed"));
  if(character_order(SOURCE_CHARACTER, cyc) != 6,
    error("source character is not order six"));
  if(denominator(character_pairing(
       SOURCE_CHARACTER, sign_log, cyc)) == 1,
    error("source character is not supported"));

  for(code = 0, vecprod(primitive_cyc) - 1,
    my(candidate = decode_element(code, primitive_cyc));
    if(character_order(candidate, primitive_cyc) == 6,
      my(ok = 1);
      for(column = 1, #cyc,
        my(source_phase =
          fractional(SOURCE_CHARACTER[column] / cyc[column]));
        my(candidate_phase = fractional(sum(
          row = 1, #primitive_cyc,
          candidate[row] * transport[row, column]
            / primitive_cyc[row]
        )));
        if(source_phase != candidate_phase, ok = 0);
      );
      if(ok, listput(matches, candidate));
    );
  );
  matches = Vec(matches);
  if(#matches != 1, error("primitive character match count changed"));
  primitive_character = matches[1];
  kernel = character_kernel_hnf(primitive_character, primitive_cyc);

  relative = bnrclassfield(primitive_ray, kernel, 1);
  if(poldegree(relative) != 6,
    error("relative class field degree changed"));
  relative_field = rnfinit(base, relative, 1);
  absolute = rnfpolredbest(base, relative, 2);
  if(poldegree(absolute) != 12 || !polisirreducible(absolute),
    error("absolute sextic-over-base polynomial failed"));
  field = bnfinit(absolute, 1);
  if(bnfcertify(field) != 1, error("sextic field bnfcertify failed"));

  a1 = field.sign == [6, 3];
  \\ For a cyclic degree-six extension, the checked A1 signature makes
  \\ complex conjugation the unique order-two subgroup and its fixed
  \\ field the maximal totally real degree-six subfield.
  a2 = a1;

  finite_factorization = idealfactor(base, finite_ideal);
  for(row = 1, matsize(finite_factorization)[1],
    my(base_prime = finite_factorization[row, 1]);
    my(original_exponent = finite_factorization[row, 2]);
    my(conductor_exponent = idealval(base, conductor[1], base_prime));
    my(frobenius_order = 0, local_verdict = 1);
    if(conductor_exponent == 0,
      my(prime_log =
        Vec(bnrisprincipal(primitive_ray, base_prime, 0)));
      frobenius_order = denominator(fractional(
        character_pairing(
          primitive_character, prime_log, primitive_cyc
        )
      ));
      extra_prime_count++;
      if(frobenius_order % 2,
        local_verdict = 0;
        a3 = 0);
    );
    listput(local_rows, [
      idealnorm(base, base_prime),
      original_exponent,
      conductor_exponent,
      frobenius_order,
      local_verdict
    ]);
  );
  primitive_S = extra_prime_count == 0;

  decomposition = rnfidealprimedec(relative_field, 3);
  for(index = 1, #decomposition[1],
    my(base_prime = decomposition[1][index]);
    my(top_primes = decomposition[2][index]);
    for(top_index = 1, #top_primes,
      my(relative_e = top_primes[top_index].e / base_prime.e);
      maximum_relative_e_above_three = max(
        maximum_relative_e_above_three, relative_e);
      if(relative_e % 3 == 0, wild_above_three = 1);
      listput(ramification_rows, [
        base_prime.e,
        base_prime.f,
        top_primes[top_index].e,
        top_primes[top_index].f,
        relative_e
      ]);
    );
  );
  class_number_prime_to_three = field.no % 3 != 0;
  applies =
    a1 && a2 && a3 && primitive_S
    && class_number_prime_to_three && !wild_above_three;

  print("CASE_ID=", CASE_ID);
  print("KERNEL_INDEX=", KERNEL_INDEX);
  print("SOURCE_CHARACTER=", SOURCE_CHARACTER);
  print("PRIMITIVE_CONDUCTOR=", conductor);
  print("PRIMITIVE_CHARACTER=", primitive_character);
  print("PRIMITIVE_KERNEL_HNF=", kernel);
  print("RELATIVE_POLYNOMIAL=", relative);
  print("ABSOLUTE_POLYNOMIAL=", absolute);
  print("ABSOLUTE_SIGNATURE=", field.sign);
  print("CLASS_NUMBER=", field.no);
  print("BNFCERTIFY=1");
  print("A1=", a1);
  print("A2=", a2);
  print("A3=", a3);
  print("A3_LOCAL_ROWS_[Nq,vS,vcond,frob_order_or_0,pass]=",
    Vec(local_rows));
  print("EXTRA_FINITE_S_PRIME_COUNT=", extra_prime_count);
  print("S_EQUALS_S_EXTENSION=", primitive_S);
  print("CLASS_NUMBER_PRIME_TO_3=", class_number_prime_to_three);
  print("RAMIFICATION_ABOVE_3_[eK,fK,eH,fH,eRel]=",
    Vec(ramification_rows));
  print("MAXIMUM_RELATIVE_E_ABOVE_3=",
    maximum_relative_e_above_three);
  print("WILD_ABOVE_3=", wild_above_three);
  print("ROBLOT_THEOREM_7_1_APPLIES=", applies);
  print("ROBLOT_SEXTIC_KERNEL_SCREEN=PASS");
};

run_screen();
