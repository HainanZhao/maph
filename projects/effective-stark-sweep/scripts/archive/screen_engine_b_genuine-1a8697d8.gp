\\ Genuine Engine-B structural battery.
\\ Caller defines CASE_ID, D_VALUE and H11,H12,H21,H22.
\\ The actual normal closure is realized inside the ray field of the common
\\ conjugation-stable modulus. No conjugation action is represented in an
\\ unstable ray group, and every deciding predicate is therefore GENUINE.

default(realprecision, 100);
default(parisizemax, 8000000000);

field_polynomial(d) =
{
  if(d % 4 == 1,
    return(y^2 - y + (1-d)/4),
    return(y^2 - d)
  );
};

vertical(A, B) =
{
  mattranspose(concat(mattranspose(A), mattranspose(B)));
};

map_matrix(source_ray, target_ray) =
{
  matrix(
    #target_ray.cyc, #source_ray.cyc, row, column,
    bnrisprincipal(
      target_ray, source_ray.gen[column], 0
    )[row]
  );
};

joint_kernel_hnf(source_cyc, first_map, first_cyc, second_map, second_cyc) =
{
  my(mapping = vertical(first_map, second_map));
  my(target_cyc = concat(Vec(first_cyc), Vec(second_cyc)));
  my(target_relations = matdiagonal(target_cyc));
  my(kernel = matkerint(concat(mapping, -target_relations)));
  my(rank = #source_cyc);
  my(projected = kernel[1..rank,]);
  mathnf(concat(matdiagonal(source_cyc), projected));
};

run_screen() =
{
  my(K = bnfinit(field_polynomial(D_VALUE), 1));
  my(finite_ideal = [H11, H12; H21, H22]);
  my(autos = nfgaloisconj(K), sigma = autos[1]);
  if(sigma == Mod(y, K.pol), sigma = autos[2]);
  my(conjugate_ideal = idealhnf(
    K, nfgaloisapply(K, sigma, finite_ideal)
  ));
  my(common_ideal = idealintersect(
    K, finite_ideal, conjugate_ideal
  ));
  my(ray_common = bnrinit(K, [common_ideal, [1, 1]], 1));
  my(ray_one = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(ray_conjugate = bnrinit(
    K, [conjugate_ideal, [0, 1]], 1
  ));
  my(first_map = map_matrix(ray_common, ray_one));
  my(second_map = map_matrix(ray_common, ray_conjugate));
  my(normal_subgroup = joint_kernel_hnf(
    ray_common.cyc, first_map, ray_one.cyc,
    second_map, ray_conjugate.cyc
  ));
  my(conjugation = matrix(
    #ray_common.cyc, #ray_common.cyc, row, column,
    bnrisprincipal(
      ray_common,
      nfgaloisapply(K, sigma, ray_common.gen[column]),
      0
    )[row]
  ));
  my(commutator_columns = matrix(
    #ray_common.cyc, #ray_common.cyc, row, column,
    (
      conjugation[row, column] - (row == column)
    ) % ray_common.cyc[row]
  ));
  my(commutator_preimage = mathnf(
    concat(normal_subgroup, commutator_columns)
  ));
  my(normal_relative_degree = matdet(normal_subgroup));
  my(max_ab_relative_degree = matdet(commutator_preimage));
  my(derived_order =
    normal_relative_degree / max_ab_relative_degree);
  if(derived_order != 2,
    error(Str("Engine-B index is ", derived_order, ", not 2"))
  );
  my(normal_relative = bnrclassfield(
    ray_common, normal_subgroup, 1
  ));
  my(normal = rnfpolredbest(K, normal_relative, 2));
  my(max_ab_relative = bnrclassfield(
    ray_common, commutator_preimage, 1
  ));
  my(max_ab = rnfpolredbest(K, max_ab_relative, 2));
  my(quadratics = nfsubfields(max_ab, 2));
  my(imaginary = List(), abelian_imaginary = List(), matches = List());

  for(i = 1, #quadratics,
    my(model = polredbest(quadratics[i][1]));
    if(poldisc(model) < 0, listput(imaginary, model));
  );
  imaginary = Set(Vec(imaginary));
  for(i = 1, #imaginary,
    my(k = bnfinit(subst(imaginary[i], x, z), 1));
    my(rel = nffactor(k, normal)[1, 1]);
    if(rnfisabelian(k, rel), listput(abelian_imaginary, imaginary[i]));
  );
  abelian_imaginary = Set(Vec(abelian_imaginary));
  for(i = 1, #abelian_imaginary,
    my(k = bnfinit(subst(abelian_imaginary[i], x, z), 1));
    my(rel = nffactor(k, normal)[1, 1]);
    my(cd = rnfconductor(k, rel));
    my(rebuilt = rnfpolredbest(
      k, bnrclassfield(cd[2], cd[3], 1), 2
    ));
    my(match = #nfisisom(rebuilt, normal) > 0);
    print("ROUTE2_BASE_", i, "_POLYNOMIAL=", abelian_imaginary[i]);
    print("ROUTE2_BASE_", i, "_CONDUCTOR=", cd[1][1]);
    print("ROUTE2_BASE_", i, "_MATCH=", match);
    if(match, listput(matches, i));
  );

  print("CASE_ID=", CASE_ID);
  print("PREDICATE_PROVENANCE=GENUINE");
  print("BASE_BNFCERTIFY=", bnfcertify(K));
  print("FINITE_IDEAL=", finite_ideal);
  print("FINITE_NORM=", idealnorm(K, finite_ideal));
  print("CONJUGATE_FINITE_IDEAL=", conjugate_ideal);
  print("COMMON_STABLE_FINITE_IDEAL=", common_ideal);
  print("ONE_PLACE_RAY_CYC=", Vec(ray_one.cyc));
  print("NORMAL_CLOSURE_CONSTRUCTION=COMMON_STABLE_RAY_QUOTIENT");
  print("NORMAL_CLOSURE_SUBGROUP_HNF=", normal_subgroup);
  print("ACTUAL_NORMAL_CLOSURE_DEGREE=", poldegree(normal));
  print("DERIVED_SUBGROUP_ORDER=", derived_order);
  print("MAXIMAL_ABELIAN_SUBFIELD_DEGREE=", poldegree(max_ab));
  print("ABELIAN_IMAGINARY_BASES=", Vec(abelian_imaginary));
  print("ABELIAN_IMAGINARY_BASE_COUNT=", #abelian_imaginary);
  print("TWO_ROUTE_MATCH_INDICES=", Vec(matches));
  print("TWO_ROUTE_MATCH_COUNT=", #matches);
  print("ENGINE_B_GENUINE_SCREEN_COMPLETE=1");
};

run_screen();
