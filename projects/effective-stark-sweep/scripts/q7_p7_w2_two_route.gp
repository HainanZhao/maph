\\ W2 two-route reconstruction for Q(sqrt(7)), p_7 infinity_2.
\\ No imaginary quadratic base is specified in the input.  Route 1
\\ derives it from the sigma-commutator fixed field.  Route 2 rebuilds
\\ the normal closure from the derived k-side conductor.

default(realprecision, 100);
default(parisizemax, 1000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

run_audit() =
{
  my(K = bnfinit(y^2 - 7, 1));
  my(finite_ideal = [7, 0; 0, 1]);
  my(ray_one = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(ray_both = bnrinit(K, [finite_ideal, [1, 1]], 1));
  my(autos = nfgaloisconj(K), sigma = autos[1]);
  my(conjugation, forgetful, commutator_columns, commutator_subgroup);
  my(fixed_relative, fixed_absolute, fixed_quadratics);
  my(imaginary_models = List(), abelian_imaginary_models = List());
  my(full_ray_matches = List(), divisor_counts = vector(2));
  my(normal_relative, normal_absolute, relative_factors);

  if(sigma == Mod(y, K.pol), sigma = autos[2]);
  assert_equal("BASE_BNFCERTIFY", bnfcertify(K), 1);
  assert_equal("ONE_PLACE_RAY_GROUP", Vec(ray_one.cyc), [6]);
  assert_equal("BOTH_PLACE_RAY_GROUP", Vec(ray_both.cyc), [6, 2]);

  conjugation = matrix(
    #ray_both.cyc, #ray_both.cyc, row, column,
    bnrisprincipal(
      ray_both,
      nfgaloisapply(K, sigma, ray_both.gen[column]),
      0
    )[row]
  );
  forgetful = matrix(
    #ray_one.cyc, #ray_both.cyc, row, column,
    bnrisprincipal(ray_one, ray_both.gen[column], 0)[row]
  );
  print("CONJUGATION_MATRIX=", conjugation);
  print("FORGETFUL_MATRIX=", forgetful);

  commutator_columns = matrix(
    #ray_both.cyc, #ray_both.cyc, row, column,
    (
      conjugation[row, column] - (row == column)
    ) % ray_both.cyc[row]
  );
  commutator_subgroup = mathnf(
    concat(matdiagonal(ray_both.cyc), commutator_columns)
  );
  print("COMMUTATOR_SUBGROUP_HNF=", commutator_subgroup);
  print("COMMUTATOR_FIXED_RELATIVE_DEGREE=",
    matdet(commutator_subgroup));

  fixed_relative = bnrclassfield(ray_both, commutator_subgroup, 1);
  fixed_absolute = rnfpolredbest(K, fixed_relative, 2);
  print("COMMUTATOR_FIXED_RELATIVE_FIELD=", fixed_relative);
  print("COMMUTATOR_FIXED_ABSOLUTE_FIELD=", fixed_absolute);

  fixed_quadratics = nfsubfields(fixed_absolute, 2);
  for(index = 1, #fixed_quadratics,
    my(model = polredbest(fixed_quadratics[index][1]));
    print("ROUTE1_FIXED_QUADRATIC_", index, "=", model);
    if(poldisc(model) < 0, listput(imaginary_models, model));
  );
  imaginary_models = Set(Vec(imaginary_models));
  normal_relative = bnrclassfield(ray_both, , 1);
  normal_absolute = rnfpolredbest(K, normal_relative, 2);
  print("NORMAL_CLOSURE_ABSOLUTE_FIELD=", normal_absolute);
  print("ROUTE1_IMAGINARY_CANDIDATE_COUNT=", #imaginary_models);
  for(index = 1, #imaginary_models,
    my(candidate_k = bnfinit(
      subst(imaginary_models[index], x, z), 1
    ));
    my(candidate_factors = nffactor(candidate_k, normal_absolute));
    my(candidate_relative = candidate_factors[1, 1]);
    my(candidate_abelian = rnfisabelian(
      candidate_k, candidate_relative
    ));
    print("ROUTE1_CANDIDATE_", imaginary_models[index],
      "_NORMAL_CLOSURE_ABELIAN=", candidate_abelian);
    if(candidate_abelian,
      listput(abelian_imaginary_models, imaginary_models[index])
    );
  );
  abelian_imaginary_models = Set(Vec(abelian_imaginary_models));
  print("ROUTE1_ABELIAN_IMAGINARY_BASE_COUNT=",
    #abelian_imaginary_models);

  \\ Route 2 begins separately from every base surviving Route 1.
  \\ It derives the conductor intrinsically and attempts a full ray
  \\ reconstruction.  No base is selected in advance.
  for(index = 1, #abelian_imaginary_models,
    my(imaginary_polynomial = abelian_imaginary_models[index]);
    my(k = bnfinit(subst(imaginary_polynomial, x, z), 1));
    my(relative_factors = nffactor(k, normal_absolute));
    my(relative_normal = relative_factors[1, 1]);
    my(conductor_data, imaginary_conductor, k_ray);
    my(k_full_relative, k_full_absolute, isomorphic = 0);
    assert_equal(Str("ROUTE2_BASE_", index, "_BNFCERTIFY"),
      bnfcertify(k), 1);
    conductor_data = rnfconductor(k, relative_normal, 2);
    imaginary_conductor = conductor_data[1][1];
    print("ROUTE2_BASE_", index, "_POLYNOMIAL=",
      imaginary_polynomial);
    print("ROUTE2_BASE_", index, "_CONDUCTOR=",
      imaginary_conductor);
    print("ROUTE2_BASE_", index, "_CONDUCTOR_FACTORIZATION=",
      conductor_data[2]);
    divisor_counts[index] = prod(
      factor_index = 1, matsize(conductor_data[2])[1],
      conductor_data[2][factor_index, 2] + 1
    );
    print("ROUTE2_BASE_", index, "_DIVISOR_COUNT=",
      divisor_counts[index]);
    k_ray = bnrinit(k, imaginary_conductor, 1);
    print("ROUTE2_BASE_", index, "_RAY_GROUP=", Vec(k_ray.cyc));
    print("ROUTE2_BASE_", index, "_RAY_ORDER=", k_ray.no);
    if(2*k_ray.no == poldegree(normal_absolute),
      k_full_relative = bnrclassfield(k_ray, , 1);
      k_full_absolute = rnfpolredbest(k, k_full_relative, 2);
      isomorphic = #nfisisom(k_full_absolute, normal_absolute) > 0;
      print("ROUTE2_BASE_", index, "_FULL_RAY_ABSOLUTE_FIELD=",
        k_full_absolute);
      print("ROUTE2_BASE_", index, "_FULL_RAY_ISOMORPHIC=",
        isomorphic);
      if(isomorphic, listput(full_ray_matches, index));
    ,
      print("ROUTE2_BASE_", index,
        "_FULL_RAY_ISOMORPHIC=NOT_SAME_DEGREE")
    );
  );
  print("ROUTE2_FULL_RAY_MATCH_INDICES=", Vec(full_ray_matches));
  assert_equal("TWO_ROUTE_FULL_RAY_MATCH_COUNT",
    #full_ray_matches, 2);
  assert_equal("BASE_1_HAS_STRICTLY_SMALLER_DIVISOR_TABLE",
    divisor_counts[1] < divisor_counts[2], 1);
  print("SELECTED_PRINTED_TABLE_BASE_INDEX=1");
  print("HALT_TWO_ROUTE_MISMATCH=0");
  print("Q7_P7_W2_TWO_ROUTE_CERTIFIED=1");
};

run_audit();
