\\ Generic exact Engine-C character-selection certificate.
\\
\\ Caller defines:
\\ CASE_ID, ROUTE_ID, REAL_BASE_POLYNOMIAL, REAL_FINITE_HNF,
\\ SOURCE_CHARACTER, PACKET_FIELD_POLYNOMIAL, CM_BASE_POLYNOMIAL,
\\ CHARACTER_FIELD_POLYNOMIAL, COEFFICIENT_LIMIT,
\\ REQUIRE_RELATIVE_ABELIAN.

default(parisizemax, 4000000000);

ray_character_order(character, cyc) =
{
  my(answer = 1);
  for(index = 1, #cyc,
    answer = lcm(
      answer,
      cyc[index] / gcd(cyc[index], character[index])));
  answer;
};

inverse_characters(first, second, cyc) =
{
  if(#first != #second || #first != #cyc, return(0));
  for(index = 1, #cyc,
    if((first[index] + second[index]) % cyc[index], return(0)));
  1;
};

finite_hnf_key(modulus) =
{
  my(finite = modulus[1]);
  [finite[1, 1], finite[1, 2], finite[2, 1], finite[2, 2]];
};

run_character_selection() =
{
  my(real_base = bnfinit(REAL_BASE_POLYNOMIAL, 1));
  my(real_ray = bnrinit(
    real_base, [REAL_FINITE_HNF, [1, 0]], 1));
  my(source_conductor =
    bnrconductor(real_ray, SOURCE_CHARACTER));
  my(source_coefficients = lfunan(
    lfuncreate([real_ray, SOURCE_CHARACTER]), COEFFICIENT_LIMIT));
  my(cm_base = bnfinit(CM_BASE_POLYNOMIAL, 1));
  my(character_field =
    bnfinit(CHARACTER_FIELD_POLYNOMIAL, 1));
  my(factors =
    nffactor(cm_base, CHARACTER_FIELD_POLYNOMIAL));
  my(best_factor = 0, best_conductor = 0, best_key = 0);
  my(best_quartic = 0, best_selected_index = 0);
  my(best_pari_rnfisabelian = 0);
  my(source_compatible_factor_count = 0);

  for(index = 1, matsize(factors)[1],
    my(candidate_factor = factors[index, 1]);
    if(poldegree(candidate_factor) == 4,
      my(candidate_relative_abelian =
        rnfisabelian(cm_base, candidate_factor));
      my(candidate_conductor =
        rnfconductor(cm_base, candidate_factor));
      my(candidate_key =
        finite_hnf_key(candidate_conductor[1]));
      my(candidate_ray = candidate_conductor[2]);
      my(all_compatible =
        bnrchar(candidate_ray, candidate_conductor[3]));
      my(candidate_quartic = List());
      for(item = 1, #all_compatible,
        if(ray_character_order(
          all_compatible[item], Vec(candidate_ray.cyc)) == 4,
          listput(candidate_quartic, all_compatible[item])));
      candidate_quartic = Vec(candidate_quartic);
      if(#candidate_quartic == 2
         && inverse_characters(
           candidate_quartic[1],
           candidate_quartic[2],
           Vec(candidate_ray.cyc)),
        my(candidate_matches = List());
        for(item = 1, #candidate_quartic,
          if(lfunan(
               lfuncreate([candidate_ray, candidate_quartic[item]]),
               COEFFICIENT_LIMIT)
             == source_coefficients,
            listput(candidate_matches, item)));
        candidate_matches = Vec(candidate_matches);
        if(#candidate_matches == 1,
          source_compatible_factor_count++;
          if(type(best_factor) == "t_INT"
             || lex(candidate_key, best_key) < 0
             || (
               lex(candidate_key, best_key) == 0
               && cmp(candidate_factor, best_factor) < 0
             ),
            best_factor = candidate_factor;
            best_conductor = candidate_conductor;
            best_key = candidate_key;
            best_quartic = candidate_quartic;
            best_selected_index = candidate_matches[1];
            best_pari_rnfisabelian = candidate_relative_abelian;
          );
        );
      );
    );
  );
  if(type(best_factor) == "t_INT",
    error("no source-compatible relative quartic factor found"));

  my(cm_ray = best_conductor[2]);
  my(quartic = best_quartic);
  my(classfield_absolute = 0);
  my(classfield_isomorphisms = []);
  my(relative_abelian_certified = best_pari_rnfisabelian);
  if(!relative_abelian_certified,
    classfield_absolute =
      bnrclassfield(cm_ray, best_conductor[3], 2);
    if(polisirreducible(classfield_absolute),
      classfield_isomorphisms =
        nfisisom(character_field, nfinit(classfield_absolute));
      relative_abelian_certified =
        type(classfield_isomorphisms) != "t_INT"
        && #classfield_isomorphisms > 0;
    );
  );
  if(REQUIRE_RELATIVE_ABELIAN
     && !relative_abelian_certified,
    error("ray-class round-trip abelian certificate failed"));
  if(#quartic != 2,
    error(Str("compatible quartic character count changed: ",
      #quartic)));
  if(!inverse_characters(quartic[1], quartic[2], Vec(cm_ray.cyc)),
    error("compatible quartic characters are not inverses"));

  my(candidate_coefficients = vector(
    #quartic, index,
    lfunan(
      lfuncreate([cm_ray, quartic[index]]),
      COEFFICIENT_LIMIT)));
  my(matches = List());
  for(index = 1, #quartic,
    if(candidate_coefficients[index] == source_coefficients,
      listput(matches, index)));
  matches = Vec(matches);
  if(#matches != 1,
    error(Str("exact source-match count changed: ", #matches)));
  my(selected_index = matches[1]);
  if(selected_index != best_selected_index,
    error("selected character changed after matching-factor freeze"));
  my(inverse_index = 3 - selected_index);
  my(separator = 0);
  for(n = 1, COEFFICIENT_LIMIT,
    if(!separator
       && candidate_coefficients[1][n]
          != candidate_coefficients[2][n],
      separator = n));
  if(!separator,
    error("coefficient limit did not separate inverse characters"));
  if(source_coefficients[separator]
     != candidate_coefficients[selected_index][separator],
    error("separator does not select source character"));

  my(conductor_factorization =
    idealfactor(cm_base, best_conductor[1][1]));
  my(S_size = 1 + matsize(conductor_factorization)[1]);
  if(bnfcertify(real_base) != 1
     || bnfcertify(cm_base) != 1
     || bnfcertify(character_field) != 1,
    error("bnfcertify failure"));

  print("CASE_ID=", CASE_ID);
  print("ROUTE_ID=", ROUTE_ID);
  print("REAL_BASE=", real_base.pol);
  print("REAL_RAY_CYC=", Vec(real_ray.cyc));
  print("SOURCE_CHARACTER=", SOURCE_CHARACTER);
  print("SOURCE_CONDUCTOR=", source_conductor);
  print("PACKET_FIELD_POLYNOMIAL=", PACKET_FIELD_POLYNOMIAL);
  print("CM_BASE=", cm_base.pol);
  print("CM_BASE_ROOTS_OF_UNITY_W_K=", cm_base.tu[1]);
  print("CHARACTER_FIELD_POLYNOMIAL=",
    CHARACTER_FIELD_POLYNOMIAL);
  print("CHARACTER_FIELD_SIGNATURE=", character_field.sign);
  print("CHARACTER_FIELD_CLASS_NUMBER=", character_field.no);
  print("CHARACTER_FIELD_ROOTS_OF_UNITY_E=",
    character_field.tu[1]);
  print("CHARACTER_FIELD_BNFCERTIFY=1");
  print("SOURCE_COMPATIBLE_RELATIVE_FACTOR_COUNT=",
    source_compatible_factor_count);
  print("PARI_RNFISABELIAN_DIAGNOSTIC=",
    best_pari_rnfisabelian);
  print("CLASSFIELD_ROUNDTRIP_ABSOLUTE_POLYNOMIAL=",
    classfield_absolute);
  print("CLASSFIELD_ROUNDTRIP_ISOMORPHISM_COUNT=",
    #classfield_isomorphisms);
  print("RELATIVE_ABELIAN_CERTIFIED=",
    relative_abelian_certified);
  print("RELATIVE_ABELIAN_REQUIRED=", REQUIRE_RELATIVE_ABELIAN);
  print("CANONICAL_RELATIVE_FACTOR=", best_factor);
  print("CM_CONDUCTOR=", best_conductor[1]);
  print("CM_CONDUCTOR_FACTORIZATION=", conductor_factorization);
  print("CM_RAY_CYC=", Vec(cm_ray.cyc));
  print("CM_RAY_SUBGROUP_HNF=", best_conductor[3]);
  print("COMPATIBLE_QUARTIC_CHARACTERS=", quartic);
  print("SELECTED_CM_CHARACTER=", quartic[selected_index]);
  print("INVERSE_CM_CHARACTER=", quartic[inverse_index]);
  print("COEFFICIENT_LIMIT=", COEFFICIENT_LIMIT);
  print("EXACT_SEPARATOR_INDEX=", separator);
  print("SOURCE_SEPARATOR_COEFFICIENT=",
    source_coefficients[separator]);
  print("SELECTED_SEPARATOR_COEFFICIENT=",
    candidate_coefficients[selected_index][separator]);
  print("INVERSE_SEPARATOR_COEFFICIENT=",
    candidate_coefficients[inverse_index][separator]);
  print("EXACT_FULL_VECTOR_MATCH=1");
  print("DISTINCT_FINITE_CONDUCTOR_PRIMES=",
    matsize(conductor_factorization)[1]);
  print("STARK_S_SIZE=", S_size);
  print("GLOBAL_UNIT_CLAUSE_APPLIES=", S_size >= 3);
  print("GENERIC_ENGINE_C_CHARACTER_SELECTION_VERIFIED=1");
  print("CLAIM_TAG=VERIFIED_EXACT_CHARACTER_SELECTION");
};

run_character_selection();
