\\ Exact linear quadratic-reinduction audit for the first primitive
\\ dimension-eight quartic character.

default(parisizemax, 6000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

subgroup_order(subgroup) = vecprod(Vec(subgroup[2]));

subgroup_elements(subgroup, identity) =
{
  my(generators = subgroup[1]);
  my(orders = subgroup[2]);
  my(total = subgroup_order(subgroup));
  my(answer = List());
  my(quotient, value, digit);
  for(code = 0, total - 1,
    quotient = code;
    value = identity;
    for(index = 1, #generators,
      digit = quotient % orders[index];
      quotient = quotient \ orders[index];
      value = value * generators[index]^digit;
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

element_index(elements, value) =
{
  for(index = 1, #elements,
    if(elements[index] == value, return(index)));
  error("group element not found");
};

same_set(first, second) =
  #first == #second && is_subset(first, second) && is_subset(second, first);

is_quartic_character(elements, exponents) =
{
  for(first = 1, #elements,
    for(second = 1, #elements,
      product_index =
        element_index(elements, elements[first] * elements[second]);
      if((exponents[first] + exponents[second] - exponents[product_index])
          % 4,
        return(0));
    );
  );
  1;
};

character_value(elements, exponents, value) =
  I^exponents[element_index(elements, value)];

candidate_induced_character(value, subgroup, exponents, complement) =
{
  if(!contains(subgroup, value), return(0));
  character_value(subgroup, exponents, value)
    + character_value(
        subgroup, exponents, complement^(-1) * value * complement);
};

ray_character_order(character, cyclic_orders) =
{
  my(answer = 1);
  for(index = 1, #character,
    answer = lcm(answer,
      cyclic_orders[index] / gcd(character[index], cyclic_orders[index])));
  answer;
};

trivial_on_kernel(character, cyclic_orders, kernel_matrix) =
{
  for(column = 1, matsize(kernel_matrix)[2],
    value = 0;
    for(row = 1, #character,
      value += character[row] * kernel_matrix[row, column]
        / cyclic_orders[row]);
    if(denominator(value) != 1, return(0));
  );
  1;
};

kernel_characters(cyclic_orders, kernel_matrix) =
{
  my(total = vecprod(Vec(cyclic_orders)));
  my(answer = List());
  my(quotient, character);
  for(code = 0, total - 1,
    quotient = code;
    character = vector(#cyclic_orders);
    for(index = 1, #cyclic_orders,
      character[index] = quotient % cyclic_orders[index];
      quotient = quotient \ cyclic_orders[index];
    );
    if(ray_character_order(character, cyclic_orders) == 4
        && trivial_on_kernel(character, cyclic_orders, kernel_matrix),
      listput(answer, character));
  );
  Vec(answer);
};

quartic_exponent(value) =
{
  for(exponent = 0, 3,
    if(contains(kernel, value * quotient_generator^(-exponent)),
      return(exponent)));
  error("element has no quartic quotient exponent");
};

quartic_character(value) = I^quartic_exponent(value);

induced_character(value) =
{
  if(!contains(H_K, value), return(0));
  quartic_character(value)
    + quartic_character(outside^(-1) * value * outside);
};

audit_packet(packet_label, source_polynomial) =
{
  print("PACKET=", packet_label);
  splitting = nfsplitting(source_polynomial, 16, 1);
  splitting_polynomial = splitting[1];
  gal = galoisinit(splitting_polynomial);
  subgroups = galoissubgroups(gal);
  identity = gal.group[1];

  assert_equal("NORMAL_CLOSURE_DEGREE",
    poldegree(splitting_polynomial), 16);
  assert_equal("NORMAL_CLOSURE_GROUP", galoisidentify(gal), [16, 13]);

  index_two_indices = List();
  index_two_fields = List();
  K_index = 0;
  for(index = 1, #subgroups,
    if(subgroup_order(subgroups[index]) == 8,
      fixed_polynomial =
        polredbest(galoisfixedfield(gal, subgroups[index][1], 1, z));
      listput(index_two_indices, index);
      listput(index_two_fields, fixed_polynomial);
      if(fixed_polynomial == x^2 - x - 1, K_index = index);
    );
  );
  index_two_indices = Vec(index_two_indices);
  index_two_fields = Vec(index_two_fields);
  assert_equal("QUADRATIC_SUBFIELD_COUNT", #index_two_fields, 7);
  if(!K_index, error("real quadratic base subgroup not found"));

  H_K = subgroup_elements(subgroups[K_index], identity);
  assert_equal("BASE_SUBGROUP_ORDER", #H_K, 8);

  \\ The two order-two subgroups whose fixed fields are isomorphic to the
  \\ source quartic field
  \\ correspond to the quartic ray field and its base conjugate.  Either
  \\ kernel gives the same induced character; choose the first.
  kernel_index = 0;
  for(index = 1, #subgroups,
    if(subgroup_order(subgroups[index]) == 2,
      fixed_polynomial =
        polredbest(galoisfixedfield(gal, subgroups[index][1], 1, z));
      if(!kernel_index
          && #nfisisom(nfinit(fixed_polynomial), source_polynomial) > 0,
        kernel_index = index);
    );
  );
  if(!kernel_index, error("quartic-character kernel not found"));
  kernel = subgroup_elements(subgroups[kernel_index], identity);
  assert_equal("QUARTIC_CHARACTER_KERNEL_ORDER", #kernel, 2);
  assert_equal("QUARTIC_CHARACTER_KERNEL_IN_BASE",
    is_subset(kernel, H_K), 1);

  \\ Find a generator of the cyclic quotient H_K/kernel.
  quotient_generator = 0;
  for(index = 1, #H_K,
    candidate = H_K[index];
    if(!contains(kernel, candidate)
        && !contains(kernel, candidate^2)
        && contains(kernel, candidate^4),
      quotient_generator = candidate;
    );
  );
  if(type(quotient_generator) == "t_INT",
    error("cyclic quartic quotient generator not found"));

  outside = 0;
  for(index = 1, #gal.group,
    if(!contains(H_K, gal.group[index]),
      outside = gal.group[index];
      break;
    );
  );
  if(type(outside) == "t_INT",
    error("base-complement element not found"));

  print("QUADRATIC_SUBFIELDS=", index_two_fields);
  for(position = 1, #index_two_indices,
    subgroup_index = index_two_indices[position];
    subgroup = subgroup_elements(subgroups[subgroup_index], identity);
    inner_product = 0;
    for(index = 1, #subgroup,
      value = induced_character(subgroup[index]);
      inner_product += value * conj(value);
    );
    inner_product /= #subgroup;
    print("RESTRICTION_FIELD=", index_two_fields[position],
          " CHARACTER_NORM=", inner_product);

    if(inner_product == 2 && index_two_fields[position] != x^2 - x - 1,
      complement = 0;
      for(index = 1, #gal.group,
        if(!contains(subgroup, gal.group[index]),
          complement = gal.group[index];
          break;
        );
      );
      if(type(complement) == "t_INT",
        error("quadratic-complement element not found"));

      matching_characters = List();
      for(code = 0, 4^(#subgroup - 1) - 1,
        quotient = code;
        exponents = vector(#subgroup);
        for(index = 2, #subgroup,
          exponents[index] = quotient % 4;
          quotient = quotient \ 4;
        );
        if(is_quartic_character(subgroup, exponents),
          matches = 1;
          for(index = 1, #gal.group,
            if(candidate_induced_character(
                  gal.group[index], subgroup, exponents, complement)
                != induced_character(gal.group[index]),
              matches = 0;
              break;
            );
          );
          if(matches, listput(matching_characters, exponents));
        );
      );
      matching_characters = Vec(matching_characters);
      assert_equal(Str("CM_CHARACTER_COUNT_", index_two_fields[position]),
        #matching_characters, 2);

      for(character_index = 1, #matching_characters,
        exponents = matching_characters[character_index];
        character_kernel = List();
        for(index = 1, #subgroup,
          if(exponents[index] == 0,
            listput(character_kernel, subgroup[index])));
        character_kernel = Vec(character_kernel);
        kernel_subgroup_index = 0;
        for(index = 1, #subgroups,
          if(subgroup_order(subgroups[index]) == #character_kernel
              && same_set(
                subgroup_elements(subgroups[index], identity),
                character_kernel),
            kernel_subgroup_index = index;
          );
        );
        if(!kernel_subgroup_index,
          error("CM character kernel subgroup not found"));
        character_field = polredbest(galoisfixedfield(
          gal, subgroups[kernel_subgroup_index][1], 1, z));
        print("CM_BASE=", index_two_fields[position],
              " CHARACTER_EXPONENTS=", exponents,
              " KERNEL_ORDER=", #character_kernel,
              " CHARACTER_FIELD=", character_field);

        if(character_index == 1,
          base_polynomial = subst(index_two_fields[position], x, y);
          base_bnf = bnfinit(base_polynomial, 1);
          relative_factors = nffactor(base_bnf, character_field);
          relative_polynomial = relative_factors[1, 1];
          conductor_data =
            rnfconductor(base_bnf, relative_polynomial);
          conductor = conductor_data[1];
          ray = conductor_data[2];
          ray_kernel = conductor_data[3];
          dual_characters = kernel_characters(ray.cyc, ray_kernel);
          assert_equal(Str("CM_DUAL_CHARACTER_COUNT_",
            packet_label, "_", index_two_fields[position]),
            #dual_characters, 2);
          assert_equal(Str("CM_BASE_BNFCERTIFY_",
            packet_label, "_", index_two_fields[position]),
            bnfcertify(base_bnf), 1);
          print("CM_PACKET=", packet_label,
                " BASE=", index_two_fields[position],
                " RELATIVE_POLYNOMIAL=", relative_polynomial);
          print("CM_PACKET=", packet_label,
                " BASE=", index_two_fields[position],
                " CONDUCTOR=", conductor,
                " CONDUCTOR_FACTORIZATION=",
                idealfactor(base_bnf, conductor[1]));
          print("CM_PACKET=", packet_label,
                " BASE=", index_two_fields[position],
                " RAY_STRUCTURE=", ray.cyc,
                " RAY_KERNEL=", ray_kernel,
                " DUAL_CHARACTERS=", dual_characters);
        );
      );
    );
  );
};

audit_packet(0, x^8 - 6*x^6 - 30*x^4 - 18*x^2 + 9);
audit_packet(1, x^8 + 6*x^6 - 30*x^4 + 18*x^2 + 9);
quit();
