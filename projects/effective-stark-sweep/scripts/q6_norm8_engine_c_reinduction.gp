\\ Exact linear reinduction certificate for RQ-000129:
\\ K=Q(sqrt(6)), finite ideal [[4,0],[0,2]], one real place.

default(parisizemax, 4000000000);

subgroup_order(subgroup) = vecprod(Vec(subgroup[2]));

subgroup_elements(subgroup, identity) =
{
  my(answer = List(), generators = subgroup[1], orders = subgroup[2]);
  for(code = 0, subgroup_order(subgroup) - 1,
    my(q = code, value = identity);
    for(index = 1, #generators,
      my(digit = q % orders[index]);
      q = q \ orders[index];
      value *= generators[index]^digit;
    );
    listput(answer, value);
  );
  Vec(answer);
};

contains(elements, value) =
{
  for(index = 1, #elements,
    if(elements[index] == value, return(1)));
  0;
};

is_subset(first, second) =
{
  for(index = 1, #first,
    if(!contains(second, first[index]), return(0)));
  1;
};

same_set(first, second) =
  #first == #second && is_subset(first, second) && is_subset(second, first);

element_index(elements, value) =
{
  for(index = 1, #elements,
    if(elements[index] == value, return(index)));
  error("group element not found");
};

is_quartic_character(elements, exponents) =
{
  for(first = 1, #elements,
    for(second = 1, #elements,
      my(product_index = element_index(
        elements, elements[first] * elements[second]
      ));
      if((exponents[first] + exponents[second]
          - exponents[product_index]) % 4,
        return(0));
    );
  );
  1;
};

character_value(elements, exponents, value) =
  I^exponents[element_index(elements, value)];

candidate_induced(value, subgroup, exponents, complement) =
{
  if(!contains(subgroup, value), return(0));
  character_value(subgroup, exponents, value)
    + character_value(
        subgroup, exponents, complement^(-1) * value * complement
      );
};

quartic_exponent(value) =
{
  for(exponent = 0, 3,
    if(contains(source_kernel, value * quotient_generator^(-exponent)),
      return(exponent)));
  error("quartic quotient exponent missing");
};

quartic_character(value) = I^quartic_exponent(value);

source_induced(value) =
{
  if(!contains(base_subgroup, value), return(0));
  quartic_character(value)
    + quartic_character(outside^(-1) * value * outside);
};

ray_character_order(character, cyc) =
{
  my(answer = 1);
  for(index = 1, #character,
    answer = lcm(answer,
      cyc[index] / gcd(character[index], cyc[index])));
  answer;
};

trivial_on_kernel(character, cyc, kernel) =
{
  for(column = 1, matsize(kernel)[2],
    my(value = sum(row = 1, #character,
      character[row] * kernel[row, column] / cyc[row]));
    if(denominator(value) != 1, return(0));
  );
  1;
};

kernel_characters(cyc, kernel) =
{
  my(answer = List(), total = vecprod(Vec(cyc)));
  for(code = 0, total - 1,
    my(q = code, character = vector(#cyc));
    for(index = 1, #cyc,
      character[index] = q % cyc[index];
      q = q \ cyc[index];
    );
    if(ray_character_order(character, cyc) == 4
       && trivial_on_kernel(character, cyc, kernel),
      listput(answer, character));
  );
  Vec(answer);
};

run_certificate() =
{
  my(Kpol = y^2 - 6);
  my(source = x^8 - 4*x^5 - 2*x^4 - 8*x^2 - 8*x - 2);
  my(splitting = nfsplitting(source, 16, 1));
  my(P = splitting[1], gal = galoisinit(P));
  my(subgroups = galoissubgroups(gal), identity = gal.group[1]);
  my(base_index = 0, kernel_index = 0);

  if(galoisidentify(gal) != [16, 13], error("normal group changed"));
  for(index = 1, #subgroups,
    my(order_value = subgroup_order(subgroups[index]));
    my(fixed = polredbest(galoisfixedfield(
      gal, subgroups[index][1], 1, z
    )));
    if(order_value == 8 && poldisc(fixed) == 24, base_index = index);
    if(order_value == 2
       && subst(fixed, variable(fixed), t)
          == subst(polredbest(source), x, t),
      kernel_index = index);
  );
  if(!base_index || !kernel_index, error("source subgroups missing"));
  base_subgroup = subgroup_elements(subgroups[base_index], identity);
  source_kernel = subgroup_elements(subgroups[kernel_index], identity);
  quotient_generator = 0;
  for(index = 1, #base_subgroup,
    my(candidate = base_subgroup[index]);
    if(!contains(source_kernel, candidate)
       && !contains(source_kernel, candidate^2)
       && contains(source_kernel, candidate^4),
      quotient_generator = candidate);
  );
  outside = 0;
  for(index = 1, #gal.group,
    if(!contains(base_subgroup, gal.group[index]),
      outside = gal.group[index]; break));
  if(type(quotient_generator) == "t_INT" || type(outside) == "t_INT",
    error("source induced character not constructed"));

  my(cm_base_count = 0, total_matching_characters = 0);
  for(index = 1, #subgroups,
    if(subgroup_order(subgroups[index]) == 8,
      my(fixed = polredbest(galoisfixedfield(
        gal, subgroups[index][1], 1, z
      )));
      my(elements = subgroup_elements(subgroups[index], identity));
      my(norm = sum(item = 1, #elements,
        source_induced(elements[item])
          * conj(source_induced(elements[item]))) / #elements);
      if(norm == 2 && poldisc(fixed) < 0,
        cm_base_count++;
        my(complement = 0);
        for(item = 1, #gal.group,
          if(!contains(elements, gal.group[item]),
            complement = gal.group[item]; break));
        my(matches = List());
        for(code = 0, 4^(#elements - 1) - 1,
          my(q = code, exponents = vector(#elements), ok = 1);
          for(item = 2, #elements,
            exponents[item] = q % 4; q = q \ 4);
          if(is_quartic_character(elements, exponents),
            for(item = 1, #gal.group,
              if(candidate_induced(
                    gal.group[item], elements, exponents, complement
                  ) != source_induced(gal.group[item]),
                ok = 0; break));
            if(ok, listput(matches, exponents));
          );
        );
        matches = Vec(matches);
        if(#matches != 2, error("matching character count changed"));
        total_matching_characters += #matches;
        print("CM_BASE_", cm_base_count, "=", fixed);
        print("CM_BASE_", cm_base_count,
          "_MATCHING_CHARACTER_COUNT=", #matches);

        my(character_kernel = List());
        for(item = 1, #elements,
          if(matches[1][item] == 0,
            listput(character_kernel, elements[item])));
        character_kernel = Vec(character_kernel);
        my(character_kernel_index = 0);
        for(item = 1, #subgroups,
          if(subgroup_order(subgroups[item]) == #character_kernel
             && same_set(
               subgroup_elements(subgroups[item], identity),
               character_kernel
             ),
            character_kernel_index = item);
        );
        if(!character_kernel_index, error("CM kernel missing"));
        my(character_field = polredbest(galoisfixedfield(
          gal, subgroups[character_kernel_index][1], 1, z
        )));
        my(k = bnfinit(subst(fixed, variable(fixed), y), 1));
        my(character_model = subst(
          character_field, variable(character_field), x
        ));
        my(relative = nffactor(k, character_model)[1, 1]);
        my(conductor_data = rnfconductor(k, relative));
        my(dual = kernel_characters(
          Vec(conductor_data[2].cyc), conductor_data[3]
        ));
        print("CM_BASE_", cm_base_count,
          "_CHARACTER_FIELD=", character_field);
        print("CM_BASE_", cm_base_count,
          "_CONDUCTOR=", conductor_data[1]);
        print("CM_BASE_", cm_base_count,
          "_CONDUCTOR_FACTORIZATION=",
          idealfactor(k, conductor_data[1][1]));
        print("CM_BASE_", cm_base_count,
          "_RAY_CYC=", Vec(conductor_data[2].cyc));
        print("CM_BASE_", cm_base_count,
          "_RAY_SUBGROUP_HNF=", conductor_data[3]);
        print("CM_BASE_", cm_base_count,
          "_DUAL_INVERSE_PAIR=", dual);
        print("CM_BASE_", cm_base_count,
          "_BNFCERTIFY=", bnfcertify(k));
      );
    );
  );
  print("CM_BASE_COUNT=", cm_base_count);
  print("TOTAL_MATCHING_CHARACTERS=", total_matching_characters);
  print("Q6_NORM8_LINEAR_REINDUCTION_VERIFIED=",
    cm_base_count == 2 && total_matching_characters == 4);
};

run_certificate();
