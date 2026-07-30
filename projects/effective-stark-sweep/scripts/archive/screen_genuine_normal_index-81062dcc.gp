\\ Exact genuine normal-closure index screen at a common stable modulus.
\\ Caller defines CASE_ID, D_VALUE and H11,H12,H21,H22.

default(realprecision, 80);
default(parisizemax, 4000000000);

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
  my(f = [H11, H12; H21, H22]);
  my(autos = nfgaloisconj(K), sigma = autos[1]);
  if(sigma == Mod(y, K.pol), sigma = autos[2]);
  my(fbar = idealhnf(K, nfgaloisapply(K, sigma, f)));
  my(common_f = idealintersect(K, f, fbar));
  my(ray_common = bnrinit(K, [common_f, [1, 1]], 1));
  my(ray_one = bnrinit(K, [f, [1, 0]], 1));
  my(ray_conjugate = bnrinit(K, [fbar, [0, 1]], 1));
  my(first_map = map_matrix(ray_common, ray_one));
  my(second_map = map_matrix(ray_common, ray_conjugate));
  my(normal_subgroup = joint_kernel_hnf(
    ray_common.cyc, first_map, ray_one.cyc,
    second_map, ray_conjugate.cyc
  ));
  my(normal_relative_degree = matdet(normal_subgroup));

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
  my(maximal_abelian_relative_degree =
    matdet(commutator_preimage));
  my(derived_order =
    normal_relative_degree / maximal_abelian_relative_degree);

  print("CASE_ID=", CASE_ID);
  print("PREDICATE_PROVENANCE=GENUINE");
  print("BASE_BNFCERTIFY=", bnfcertify(K));
  print("FINITE_IDEAL=", f);
  print("CONJUGATE_FINITE_IDEAL=", fbar);
  print("COMMON_STABLE_FINITE_IDEAL=", common_f);
  print("COMMON_RAY_CYC=", Vec(ray_common.cyc));
  print("ONE_PLACE_RAY_CYC=", Vec(ray_one.cyc));
  print("CONJUGATE_RAY_CYC=", Vec(ray_conjugate.cyc));
  print("FIRST_FORGETFUL_MAP=", first_map);
  print("SECOND_FORGETFUL_MAP=", second_map);
  print("NORMAL_CLOSURE_SUBGROUP_HNF=", normal_subgroup);
  print("NORMAL_CLOSURE_RELATIVE_DEGREE=",
    normal_relative_degree);
  print("GENUINE_CONJUGATION_MATRIX=", conjugation);
  print("COMMUTATOR_PREIMAGE_HNF=", commutator_preimage);
  print("MAXIMAL_ABELIAN_RELATIVE_DEGREE=",
    maximal_abelian_relative_degree);
  print("DERIVED_SUBGROUP_ORDER=", derived_order);
  print("GENUINE_NORMAL_INDEX_SCREEN_COMPLETE=1");
};

run_screen();
