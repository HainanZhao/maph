\\ General two-route W2 screen for a frozen Engine-B candidate.
\\ The caller defines CASE_ID, D_VALUE and H11,H12,H21,H22.

default(realprecision, 80);
default(parisizemax, 4000000000);

field_polynomial(d) =
{
  if(d % 4 == 1,
    return(y^2 - y + (1-d)/4),
    return(y^2 - d)
  );
};

run_screen() =
{
  my(Kpol = field_polynomial(D_VALUE));
  my(K = bnfinit(Kpol, 1));
  my(finite_ideal = [H11, H12; H21, H22]);
  my(ray_one = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(ray_both = bnrinit(K, [finite_ideal, [1, 1]], 1));
  my(autos = nfgaloisconj(K), sigma = autos[1]);
  if(sigma == Mod(y, K.pol), sigma = autos[2]);

  my(conjugation = matrix(
    #ray_both.cyc, #ray_both.cyc, row, column,
    bnrisprincipal(
      ray_both,
      nfgaloisapply(K, sigma, ray_both.gen[column]),
      0
    )[row]
  ));
  my(commutator_columns = matrix(
    #ray_both.cyc, #ray_both.cyc, row, column,
    (
      conjugation[row, column] - (row == column)
    ) % ray_both.cyc[row]
  ));
  my(commutator_subgroup = mathnf(
    concat(matdiagonal(ray_both.cyc), commutator_columns)
  ));
  my(fixed_relative = bnrclassfield(
    ray_both, commutator_subgroup, 1
  ));
  my(fixed_absolute = rnfpolredbest(K, fixed_relative, 2));
  my(normal_relative = bnrclassfield(ray_both, , 1));
  my(normal_absolute = rnfpolredbest(K, normal_relative, 2));
  my(imaginary = List(), abelian_imaginary = List());
  my(full_ray_matches = List());

  print("CASE_ID=", CASE_ID);
  print("D=", D_VALUE);
  print("FINITE_IDEAL=", finite_ideal);
  print("FINITE_NORM=", idealnorm(K, finite_ideal));
  print("ONE_CYC=", Vec(ray_one.cyc));
  print("BOTH_CYC=", Vec(ray_both.cyc));
  print("CONJUGATION_MATRIX=", conjugation);
  print("COMMUTATOR_SUBGROUP_HNF=", commutator_subgroup);
  print("COMMUTATOR_FIXED_RELATIVE_DEGREE=",
    matdet(commutator_subgroup));
  print("COMMUTATOR_FIXED_ABSOLUTE_FIELD=", fixed_absolute);
  print("NORMAL_CLOSURE_ABSOLUTE_DEGREE=", poldegree(normal_absolute));
  print("NORMAL_CLOSURE_ABSOLUTE_FIELD=", normal_absolute);

  my(quadratics = nfsubfields(fixed_absolute, 2));
  for(index = 1, #quadratics,
    my(model = polredbest(quadratics[index][1]));
    if(poldisc(model) < 0, listput(imaginary, model));
  );
  imaginary = Set(Vec(imaginary));
  print("ROUTE1_IMAGINARY_CANDIDATES=", Vec(imaginary));
  for(index = 1, #imaginary,
    my(k = bnfinit(subst(imaginary[index], x, z), 1));
    my(factors = nffactor(k, normal_absolute));
    my(relative_normal = factors[1, 1]);
    my(is_abelian = rnfisabelian(k, relative_normal));
    print("ROUTE1_CANDIDATE_", index, "_BASE=", imaginary[index]);
    print("ROUTE1_CANDIDATE_", index, "_ABELIAN=", is_abelian);
    if(is_abelian, listput(abelian_imaginary, imaginary[index]));
  );
  abelian_imaginary = Set(Vec(abelian_imaginary));
  print("ROUTE1_ABELIAN_IMAGINARY_BASES=",
    Vec(abelian_imaginary));
  print("ROUTE1_ABELIAN_IMAGINARY_BASE_COUNT=",
    #abelian_imaginary);

  for(index = 1, #abelian_imaginary,
    my(kpol = abelian_imaginary[index]);
    my(k = bnfinit(subst(kpol, x, z), 1));
    my(relative_normal = nffactor(k, normal_absolute)[1, 1]);
    my(conductor_data = rnfconductor(k, relative_normal));
    my(conductor = conductor_data[1][1]);
    my(k_ray = conductor_data[2]);
    my(ray_subgroup = conductor_data[3]);
    my(factorization = idealfactor(k, conductor));
    my(divisor_count = prod(
      factor_index = 1, matsize(factorization)[1],
      factorization[factor_index, 2] + 1
    ));
    my(match = 0);
    my(k_subfield = bnrclassfield(k_ray, ray_subgroup, 1));
    my(k_absolute = rnfpolredbest(k, k_subfield, 2));
    match = #nfisisom(k_absolute, normal_absolute) > 0;
    print("ROUTE2_BASE_", index, "_POLYNOMIAL=", kpol);
    print("ROUTE2_BASE_", index, "_CONDUCTOR=", conductor);
    print("ROUTE2_BASE_", index, "_CONDUCTOR_FACTORIZATION=",
      factorization);
    print("ROUTE2_BASE_", index, "_DIVISOR_COUNT=", divisor_count);
    print("ROUTE2_BASE_", index, "_RAY_CYC=", Vec(k_ray.cyc));
    print("ROUTE2_BASE_", index, "_RAY_ORDER=", k_ray.no);
    print("ROUTE2_BASE_", index, "_RAY_SUBGROUP_HNF=",
      ray_subgroup);
    print("ROUTE2_BASE_", index, "_SUBFIELD_RELATIVE_DEGREE=",
      matdet(ray_subgroup));
    print("ROUTE2_BASE_", index, "_RAY_SUBFIELD_ABSOLUTE_MATCH=", match);
    if(match, listput(full_ray_matches, index));
  );
  print("ROUTE2_RAY_SUBFIELD_MATCH_INDICES=", Vec(full_ray_matches));
  print("TWO_ROUTE_RAY_SUBFIELD_MATCH_COUNT=", #full_ray_matches);
  print("ENGINE_B_TWO_ROUTE_SCREEN_COMPLETE=1");
};

run_screen();
