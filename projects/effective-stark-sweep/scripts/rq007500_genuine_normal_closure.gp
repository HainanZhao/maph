\\ Genuine-reconstruction control for RQ-007500.
\\ Unlike the superseded generic W2 path, this script never represents the
\\ conjugate of an unstable modulus inside the original ray group.  It builds
\\ the one-place ray field first and obtains its actual splitting field.

default(realprecision, 100);
default(parisizemax, 8000000000);

run() =
{
  my(K = bnfinit(y^2 - y - 46, 1));
  my(f = [30, 6; 0, 3]);
  my(ray = bnrinit(K, [f, [1, 0]], 1));
  my(relative = bnrclassfield(ray, , 1));
  my(absolute = rnfpolredbest(K, relative, 2));

  print("CASE_ID=RQ-007500");
  print("PROVENANCE=GENUINE");
  print("BASE_BNFCERTIFY=", bnfcertify(K));
  print("FINITE_IDEAL=", f);
  print("FINITE_NORM=", idealnorm(K, f));
  print("ONE_PLACE_RAY_CYC=", Vec(ray.cyc));
  print("ONE_PLACE_RELATIVE_DEGREE=", ray.no);
  print("ONE_PLACE_ABSOLUTE_POLYNOMIAL=", absolute);
  print("ONE_PLACE_ABSOLUTE_DEGREE=", poldegree(absolute));

  my(splitting = nfsplitting(absolute, , 1));
  my(normal = polredbest(splitting[1]));
  print("ACTUAL_NORMAL_CLOSURE_POLYNOMIAL=", normal);
  print("ACTUAL_NORMAL_CLOSURE_DEGREE=", poldegree(normal));

  my(gal = galoisinit(normal));
  if(type(gal) == "t_INT",
    error("galoisinit failed for actual normal closure")
  );
  my(group_id = galoisidentify(gal));
  print("ACTUAL_NORMAL_CLOSURE_GROUP_ID=", group_id);

  my(quadratics = nfsubfields(normal, 2));
  my(imaginary = List(), abelian_imaginary = List());
  for(i = 1, #quadratics,
    my(model = polredbest(quadratics[i][1]));
    if(poldisc(model) < 0, listput(imaginary, model));
  );
  imaginary = Set(Vec(imaginary));
  print("ACTUAL_IMAGINARY_QUADRATIC_CANDIDATES=", Vec(imaginary));
  for(i = 1, #imaginary,
    my(k = bnfinit(subst(imaginary[i], x, z), 1));
    my(factors = nffactor(k, normal));
    my(rel = factors[1, 1]);
    my(isab = rnfisabelian(k, rel));
    print("ROUTE1_CANDIDATE_", i, "_BASE=", imaginary[i]);
    print("ROUTE1_CANDIDATE_", i, "_ABELIAN=", isab);
    if(isab, listput(abelian_imaginary, imaginary[i]));
  );
  abelian_imaginary = Set(Vec(abelian_imaginary));
  print("ROUTE1_ABELIAN_IMAGINARY_BASES=", Vec(abelian_imaginary));
  print("ROUTE1_ABELIAN_IMAGINARY_BASE_COUNT=", #abelian_imaginary);

  my(matches = List());
  for(i = 1, #abelian_imaginary,
    my(k = bnfinit(subst(abelian_imaginary[i], x, z), 1));
    my(rel = nffactor(k, normal)[1, 1]);
    my(cd = rnfconductor(k, rel));
    my(conductor = cd[1][1], kray = cd[2], subgroup = cd[3]);
    my(rebuilt_rel = bnrclassfield(kray, subgroup, 1));
    my(rebuilt_abs = rnfpolredbest(k, rebuilt_rel, 2));
    my(match = #nfisisom(rebuilt_abs, normal) > 0);
    print("ROUTE2_BASE_", i, "_POLYNOMIAL=", abelian_imaginary[i]);
    print("ROUTE2_BASE_", i, "_CONDUCTOR=", conductor);
    print("ROUTE2_BASE_", i, "_RAY_CYC=", Vec(kray.cyc));
    print("ROUTE2_BASE_", i, "_SUBGROUP_HNF=", subgroup);
    print("ROUTE2_BASE_", i, "_MATCH=", match);
    if(match, listput(matches, i));
  );
  print("TWO_ROUTE_MATCH_INDICES=", Vec(matches));
  print("GENUINE_RECONSTRUCTION_COMPLETE=1");
};

run();
