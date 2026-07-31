\\ Exact field-invariant gates for one deduplicated primitive sextic key.
\\ Caller defines FIELD_KEY, D_VALUE, PRIMITIVE_CONDUCTOR,
\\ and PRIMITIVE_KERNEL_HNF.

default(realprecision, 80);
default(parisizemax, 1500000000);

field_polynomial(d) =
{
  if(d % 4 == 1,
    return(y^2 - y + (1-d)/4),
    return(y^2 - d)
  );
};

stage(name, started) =
{
  print("FIELD_STAGE=", name, ":", getwalltime() - started);
};

run_field_screen() =
{
  my(started = getwalltime());
  my(base, primitive_ray, relative, relative_field, absolute, field);
  my(a1, a2, decomposition, ramification_rows = List());
  my(wild_above_three = 0, maximum_relative_e_above_three = 1);
  my(class_number_prime_to_three, quotient_certificate);
  my(full_certificate = -1, class_number_gate_provenance);

  stage("START", started);
  base = bnfinit(field_polynomial(D_VALUE), 1);
  if(bnfcertify(base) != 1, error("base bnfcertify failed"));
  stage("BASE_CERTIFIED", started);
  primitive_ray = bnrinit(base, PRIMITIVE_CONDUCTOR, 1);
  stage("PRIMITIVE_RAY", started);
  relative = bnrclassfield(primitive_ray, PRIMITIVE_KERNEL_HNF, 1);
  if(poldegree(relative) != 6,
    error("relative class field degree changed"));
  stage("RELATIVE_CLASS_FIELD", started);
  relative_field = rnfinit(base, relative, 1);
  stage("RELATIVE_NF", started);
  absolute = rnfpolredbest(base, relative, 2);
  if(poldegree(absolute) != 12 || !polisirreducible(absolute),
    error("absolute sextic-over-base polynomial failed"));
  stage("ABSOLUTE_POLYNOMIAL", started);
  field = bnfinit(absolute, 1);
  stage("ABSOLUTE_BNFINIT", started);
  quotient_certificate = bnfcertify(field, 1);
  if(quotient_certificate != 1,
    error("sextic field quotient bnfcertify failed"));
  stage("CLASS_GROUP_QUOTIENT_CERTIFIED", started);
  class_number_prime_to_three = field.no % 3 != 0;
  if(class_number_prime_to_three,
    class_number_gate_provenance =
      "QUOTIENT_OF_COMPUTED_PRIME_TO_3_GROUP",
    if(DEFER_FULL_CERTIFICATE,
      full_certificate = -2;
      class_number_gate_provenance =
        "CANDIDATE_DIVISIBLE_BY_3_NEEDS_STRONG_CERTIFICATE",
      full_certificate = bnfcertify(field);
      if(full_certificate != 1,
        error("sextic field full bnfcertify failed"));
      class_number_prime_to_three = field.no % 3 != 0;
      class_number_gate_provenance = "FULL_BNFCERTIFY"
    )
  );
  stage("CLASS_NUMBER_GATE_CERTIFIED", started);

  a1 = field.sign == [6, 3];
  a2 = a1;
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
  stage("RAMIFICATION_ABOVE_3", started);
  print("FIELD_KEY=", FIELD_KEY);
  print("RELATIVE_POLYNOMIAL=", relative);
  print("ABSOLUTE_POLYNOMIAL=", absolute);
  print("ABSOLUTE_SIGNATURE=", field.sign);
  print("CLASS_NUMBER=", field.no);
  print("QUOTIENT_BNFCERTIFY=", quotient_certificate);
  print("FULL_BNFCERTIFY_OR_MINUS_ONE=", full_certificate);
  print("CLASS_NUMBER_GATE_PROVENANCE=",
    class_number_gate_provenance);
  print("A1=", a1);
  print("A2=", a2);
  print("CLASS_NUMBER_PRIME_TO_3=", class_number_prime_to_three);
  print("RAMIFICATION_ABOVE_3_[eK,fK,eH,fH,eRel]=",
    Vec(ramification_rows));
  print("MAXIMUM_RELATIVE_E_ABOVE_3=",
    maximum_relative_e_above_three);
  print("WILD_ABOVE_3=", wild_above_three);
  print("ROBLOT_SEXTIC_FIELD_SCREEN=PASS");
};

run_field_screen();
