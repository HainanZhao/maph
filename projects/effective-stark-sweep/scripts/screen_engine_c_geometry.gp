\\ Complete geometric pre-screen for an Engine-C route candidate.
\\ The caller defines CASE_ID, D_VALUE and H11,H12,H21,H22.
\\ Each distinct supported quartic kernel is constructed exactly.

default(realprecision, 80);
default(parisizemax, 4000000000);

fractional(value) = value - floor(value);

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

polynomial_key(polynomial) = Str(polredbest(polynomial));
normalized_polynomial(polynomial) =
  subst(polynomial, variable(polynomial), t);

subgroup_order(subgroup) = vecprod(Vec(subgroup[2]));

subgroup_elements(subgroup, identity) =
{
  my(generators = subgroup[1], orders = subgroup[2]);
  my(total = subgroup_order(subgroup), answer = List());
  for(code = 0, total - 1,
    my(quotient = code, value = identity);
    for(index = 1, #generators,
      my(digit = quotient % orders[index]);
      quotient = quotient \ orders[index];
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

element_index(elements, value) =
{
  for(index = 1, #elements,
    if(elements[index] == value, return(index)));
  error("group element not found");
};

quartic_exponent(value) =
{
  for(exponent = 0, 3,
    if(contains(source_kernel,
        value * quotient_generator^(-exponent)),
      return(exponent)));
  error("element has no quartic quotient exponent");
};

quartic_character(value) = I^quartic_exponent(value);

induced_character(value) =
{
  if(!contains(base_subgroup, value), return(0));
  quartic_character(value)
    + quartic_character(outside^(-1) * value * outside);
};

run_screen() =
{
  my(Kpol = field_polynomial(D_VALUE));
  my(K = bnfinit(Kpol, 1));
  my(finite_ideal = [H11, H12; H21, H22]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(cyc = Vec(ray.cyc), total = vecprod(cyc));
  my(sign_generator = if(H11 <= 2, 1, H11 - 1));
  my(sign_log = Vec(bnrisprincipal(
    ray, idealhnf(K, sign_generator), 0
  )));
  my(kernel_keys = List(), kernels = List());
  my(packet_count = 0, pass_count = 0);

  for(code = 0, total - 1,
    my(character = decode_element(code, cyc));
    if(character_order(character, cyc) == 4
       && denominator(character_pairing(character, sign_log, cyc)) != 1,
      my(kernel = character_kernel_hnf(character, cyc));
      my(key = Str(kernel));
      if(!setsearch(Set(Vec(kernel_keys)), key),
        listput(kernel_keys, key);
        listput(kernels, [character, kernel]);
      );
    );
  );

  print("CASE_ID=", CASE_ID);
  print("D=", D_VALUE);
  print("FINITE_IDEAL=", finite_ideal);
  print("FINITE_NORM=", idealnorm(K, finite_ideal));
  print("ONE_CYC=", cyc);
  print("DISTINCT_QUARTIC_KERNELS=", #kernels);

  for(packet = 1, #kernels,
    if(PACKET_FILTER && packet != PACKET_FILTER, next);
    packet_count++;
    my(character = kernels[packet][1]);
    my(source_kernel_hnf = kernels[packet][2]);
    my(conductor = bnrconductor(ray, character));
    my(primitive_ray = bnrinit(K, conductor, 1));
    my(primitive_cyc = Vec(primitive_ray.cyc));
    my(transport = matrix(
      #primitive_cyc, #cyc, row, column,
      bnrisprincipal(primitive_ray, ray.gen[column], 0)[row]
    ));
    my(matches = List());
    for(primitive_code = 0, vecprod(primitive_cyc) - 1,
      my(candidate = decode_element(primitive_code, primitive_cyc));
      if(character_order(candidate, primitive_cyc) == 4,
        my(ok = 1);
        for(column = 1, #cyc,
          my(source_phase = fractional(character[column] / cyc[column]));
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
    if(#matches != 1,
      error(Str("primitive character match count ", #matches)));
    my(primitive_character = matches[1]);
    my(kernel = character_kernel_hnf(
      primitive_character, primitive_cyc
    ));
    print("PACKET_", packet, "_SOURCE_CHARACTER=", character);
    print("PACKET_", packet, "_SOURCE_KERNEL_HNF=", source_kernel_hnf);
    print("PACKET_", packet, "_PRIMITIVE_CONDUCTOR=", conductor);
    print("PACKET_", packet, "_PRIMITIVE_RAY_CYC=", primitive_cyc);
    print("PACKET_", packet, "_PRIMITIVE_CHARACTER=",
      primitive_character);
    print("PACKET_", packet, "_PRIMITIVE_KERNEL_HNF=", kernel);
    my(relative = bnrclassfield(primitive_ray, kernel, 1));
    my(absolute = rnfpolredbest(K, relative, 2));
    my(galois_descriptor = polgalois(absolute));
    my(galois_order = galois_descriptor[1], splitting = 0);
    my(splitting_polynomial, group_id = 0);
    my(quadratics = List(), imaginary = List(), cm_bases = List());
    my(base_present = 0);
    my(geometry_pass = 0);

    print("PACKET_", packet, "_RELATIVE_POLYNOMIAL=", relative);
    print("PACKET_", packet, "_ABSOLUTE_POLYNOMIAL=", absolute);
    print("PACKET_", packet, "_ABSOLUTE_SIGNATURE=",
      nfinit(absolute).sign);
    print("PACKET_", packet, "_POLGALOIS=", galois_descriptor);
    if(galois_order != 16,
      print("PACKET_", packet, "_NORMAL_CLOSURE_DEGREE=",
        galois_order);
      print("PACKET_", packet,
        "_NORMAL_CLOSURE_GROUP=SKIPPED_ORDER_NOT_16");
      print("PACKET_", packet,
        "_LINEAR_REINDUCTION_BASES=NOT_APPLICABLE");
    ,
      splitting = nfsplitting(absolute, 16, 1);
      splitting_polynomial = splitting[1];
      print("PACKET_", packet, "_NORMAL_CLOSURE_DEGREE=",
        poldegree(splitting_polynomial));
      if(poldegree(splitting_polynomial) <= 32,
        my(gal = galoisinit(splitting_polynomial));
        if(type(gal) != "t_INT",
          group_id = galoisidentify(gal);
          my(subgroups = galoissubgroups(gal));
          my(identity = gal.group[1], base_index = 0);
          my(source_kernel_index = 0);
          my(source_model =
            normalized_polynomial(polredbest(absolute)));
          for(index = 1, #subgroups,
            my(order_value = subgroup_order(subgroups[index]));
            if(order_value == 8,
              my(fixed = polredbest(galoisfixedfield(
                gal, subgroups[index][1], 1, z
              )));
              if(poldisc(fixed) == K.disc,
                base_index = index);
            );
            if(order_value == 2,
              my(fixed = polredbest(galoisfixedfield(
                gal, subgroups[index][1], 1, z
              )));
              if(!source_kernel_index
                 && normalized_polynomial(fixed) == source_model,
                source_kernel_index = index);
            );
          );
          if(base_index && source_kernel_index,
            base_subgroup = subgroup_elements(
              subgroups[base_index], identity
            );
            source_kernel = subgroup_elements(
              subgroups[source_kernel_index], identity
            );
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
                outside = gal.group[index];
                break);
            );
            if(type(quotient_generator) != "t_INT"
               && type(outside) != "t_INT",
              for(index = 1, #subgroups,
                if(subgroup_order(subgroups[index]) == 8,
                  my(fixed = polredbest(galoisfixedfield(
                    gal, subgroups[index][1], 1, z
                  )));
                  my(elements = subgroup_elements(
                    subgroups[index], identity
                  ));
                  my(inner_product = sum(
                    item = 1, #elements,
                    induced_character(elements[item])
                      * conj(induced_character(elements[item]))
                  ) / #elements);
                  if(inner_product == 2 && poldisc(fixed) < 0,
                    listput(cm_bases, fixed));
                );
              );
            );
          );
        );
      );
      print("PACKET_", packet, "_NORMAL_CLOSURE_GROUP=", group_id);
      my(raw_quadratics = nfsubfields(splitting_polynomial, 2));
      for(index = 1, #raw_quadratics,
        my(model = polredbest(raw_quadratics[index][1]));
        listput(quadratics, model);
        if(poldisc(model) == K.disc, base_present = 1);
        if(poldisc(model) < 0, listput(imaginary, model));
      );
      quadratics = Set(Vec(quadratics));
      imaginary = Set(Vec(imaginary));
      print("PACKET_", packet, "_QUADRATIC_SUBFIELDS=",
        Vec(quadratics));
      print("PACKET_", packet, "_IMAGINARY_QUADRATIC_BASES=",
        Vec(imaginary));
      cm_bases = Set(Vec(cm_bases));
      print("PACKET_", packet, "_LINEAR_REINDUCTION_BASES=",
        Vec(cm_bases));
      print("PACKET_", packet, "_REAL_BASE_PRESENT=", base_present);
      geometry_pass =
        poldegree(splitting_polynomial) == 16
        && group_id == [16, 13]
        && base_present
        && #cm_bases == 2;
    );
    print("PACKET_", packet, "_C_GEOMETRY_PASS=", geometry_pass);
    if(geometry_pass, pass_count++);
  );
  print("PACKET_COUNT=", packet_count);
  print("GEOMETRY_PASS_COUNT=", pass_count);
  print("ENGINE_C_GEOMETRY_SCREEN_COMPLETE=1");
};

run_screen();
