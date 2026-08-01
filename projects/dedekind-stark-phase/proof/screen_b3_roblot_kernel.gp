\\ Exact Roblot (A1)--(A3) screen for one frozen quartic kernel.
\\ Caller defines CASE_ID, KERNEL_INDEX, D_VALUE, H11,H12,H21,H22,
\\ SOURCE_CYC, SOURCE_SIGN_LOG, and SOURCE_CHARACTER.

default(realprecision, 80);
default(parisizemax, 1073741824);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(label, ": expected ", expected, ", got ", actual));
};

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
    answer = lcm(answer,
      cyc[index] / gcd(cyc[index], character[index])));
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

unique_totally_real_quartic(polynomial) =
{
  my(subfields = nfsubfields(polynomial, 4), answers = List());
  for(index = 1, #subfields,
    if(nfinit(subfields[index][1]).sign == [4, 0],
      listput(answers, subfields[index][1])));
  assert_equal("unique totally real quartic", #answers, 1);
  answers[1];
};

run_screen() =
{
  my(base_polynomial = field_polynomial(D_VALUE));
  my(base = bnfinit(base_polynomial, 1));
  my(finite_ideal = [H11, H12; H21, H22]);
  my(ray = bnrinit(base, [finite_ideal, [1, 0]], 1));
  my(cyc = Vec(ray.cyc));
  my(sign_generator = if(H11 <= 2, 1, H11 - 1));
  my(sign_log = Vec(bnrisprincipal(
    ray, idealhnf(base, sign_generator), 0
  )));
  my(conductor, primitive_ray, primitive_cyc, transport);
  my(matches = List(), primitive_character, kernel);
  my(relative, absolute, absolute_nf, plus_polynomial);
  my(plus_nf);
  my(finite_factorization, local_rows = List(), a3 = 1);

  assert_equal("base bnfcertify", bnfcertify(base), 1);
  assert_equal("base signature", base.sign, [2, 0]);
  assert_equal("source ray cyc", cyc, SOURCE_CYC);
  assert_equal("source sign log", sign_log, SOURCE_SIGN_LOG);
  assert_equal("source character order",
    character_order(SOURCE_CHARACTER, cyc), 4);
  if(denominator(character_pairing(
      SOURCE_CHARACTER, sign_log, cyc)) == 1,
    error("source character is not supported"));

  conductor = bnrconductor(ray, SOURCE_CHARACTER);
  primitive_ray = bnrinit(base, conductor, 1);
  primitive_cyc = Vec(primitive_ray.cyc);
  transport = matrix(
    #primitive_cyc, #cyc, row, column,
    bnrisprincipal(primitive_ray, ray.gen[column], 0)[row]
  );
  for(code = 0, vecprod(primitive_cyc) - 1,
    my(candidate = decode_element(code, primitive_cyc));
    if(character_order(candidate, primitive_cyc) == 4,
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
  assert_equal("primitive character match count", #matches, 1);
  primitive_character = matches[1];
  kernel = character_kernel_hnf(primitive_character, primitive_cyc);

  relative = bnrclassfield(primitive_ray, kernel, 1);
  absolute = rnfpolredbest(base, relative, 2);
  assert_equal("absolute irreducible", polisirreducible(absolute), 1);
  absolute_nf = nfinit(absolute);
  assert_equal("absolute degree", poldegree(absolute), 8);

  my(a1 =
    absolute_nf.sign == [4, 2]
    && #nfgaloisconj(absolute_nf) == 4);
  plus_polynomial = unique_totally_real_quartic(absolute);
  plus_nf = nfinit(plus_polynomial);
  my(a2 =
    polisirreducible(plus_polynomial) == 1
    && poldegree(plus_polynomial) == 4
    && plus_nf.sign == [4, 0]);

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
      if(frobenius_order == 1,
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

  print("CASE_ID=", CASE_ID);
  print("KERNEL_INDEX=", KERNEL_INDEX);
  print("SOURCE_CHARACTER=", SOURCE_CHARACTER);
  print("PRIMITIVE_CONDUCTOR=", conductor);
  print("PRIMITIVE_RAY_CYC=", primitive_cyc);
  print("PRIMITIVE_CHARACTER=", primitive_character);
  print("PRIMITIVE_KERNEL_HNF=", kernel);
  print("RELATIVE_POLYNOMIAL=", relative);
  print("ABSOLUTE_POLYNOMIAL=", absolute);
  print("ABSOLUTE_SIGNATURE=", absolute_nf.sign);
  print("ABSOLUTE_AUTOMORPHISM_COUNT=",
    #nfgaloisconj(absolute_nf));
  print("KPLUS_POLYNOMIAL=", plus_polynomial);
  print("A3_LOCAL_ROWS_[Nq,vS,vcond,frob_order_or_0,pass]=",
    Vec(local_rows));
  print("A1=", a1);
  print("A2=", a2);
  print("A3=", a3);
  print("ROBLOT_ELIGIBLE=", a1 && a2 && a3);
  print("B3_ROBLOT_KERNEL_SCREEN=PASS");
};

run_screen();
