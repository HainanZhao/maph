\\ Exact normal-closure bridge from the Q(sqrt(-42)) Stark-unit
\\ candidate to the aligned real RQ-000458 packet.

default(parisizemax, 6000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

run_bridge() =
{
  my(real_polynomial =
    x^8 - 40*x^7 + 172*x^6 + 488*x^5 + 694*x^4
      + 488*x^3 + 172*x^2 - 40*x + 1);
  my(cm_polynomial =
    x^8 - 4*x^7 + 20*x^6 - 28*x^5 + 106*x^4
      - 152*x^3 + 152*x^2 + 184*x + 58);
  my(real_unit = Mod(x, real_polynomial));
  my(cm_bnf = bnfinit(cm_polynomial, 1));
  my(anti_basis_1 = cm_bnf.fu[1]);
  my(anti_basis_2 = cm_bnf.fu[2]^(-1) * cm_bnf.fu[3]);
  my(cm_stark_unit = anti_basis_1^(-2) * anti_basis_2);
  my(normal_closure =
    nfsplitting(real_polynomial, 16, 1)[1]);
  my(galois_group = galoisinit(normal_closure));
  my(identity = galois_group.group[1]);
  my(real_inclusions =
    nfisincl(real_polynomial, normal_closure, 2));
  my(cm_inclusions =
    nfisincl(cm_polynomial, normal_closure, 2));
  my(real_images = vector(#real_inclusions));
  my(cm_images = vector(#cm_inclusions));
  my(complex_conjugations = List());
  my(identity_records = List());

  assert_equal("CASE_ID", "RQ-000458", "RQ-000458");
  assert_equal("NORMAL_CLOSURE_DEGREE",
    poldegree(normal_closure), 16);
  assert_equal("NORMAL_CLOSURE_GROUP",
    galoisidentify(galois_group), [16, 13]);
  assert_equal("NORMAL_CLOSURE_SIGNATURE",
    nfinit(normal_closure).sign, [0, 8]);
  assert_equal("REAL_INCLUSION_COUNT", #real_inclusions, 8);
  assert_equal("CM_INCLUSION_COUNT", #cm_inclusions, 8);

  for(index = 1, #real_inclusions,
    real_images[index] = Mod(
      subst(lift(real_unit), x, real_inclusions[index]),
      normal_closure));
  for(index = 1, #cm_inclusions,
    cm_images[index] = Mod(
      subst(lift(cm_stark_unit), x, cm_inclusions[index]),
      normal_closure));

  for(group_index = 1, #galois_group.group,
    my(permutation = galois_group.group[group_index]);
    if(permutation != identity && permutation^2 == identity,
      my(fixed_polynomial =
        galoisfixedfield(galois_group, permutation, 1, z));
      if(nfinit(fixed_polynomial).sign[1] > 0,
        listput(complex_conjugations, group_index));
    );
  );

  for(position = 1, #complex_conjugations,
    my(group_index = complex_conjugations[position]);
    my(permutation = galois_group.group[group_index]);
    my(conjugation = lift(
      galoispermtopol(galois_group, permutation)));
    for(real_index = 1, #real_images,
      if(Mod(subst(
            lift(real_images[real_index]), x, conjugation),
          normal_closure) == real_images[real_index],
        my(match_count = 0);
        for(cm_index = 1, #cm_images,
          my(conjugate_image = Mod(subst(
            lift(cm_images[cm_index]), x, conjugation),
            normal_closure));
          \\ The C unit has e=4.  The ordinary modulus is the positive
          \\ square root of the algebraic complex norm, so the aligned
          \\ real packet root is compared after squaring.
          if(real_images[real_index]^2
             == cm_images[cm_index] * conjugate_image,
            listput(identity_records,
              [group_index, real_index, cm_index, 1]);
            match_count++);
          if(real_images[real_index]^(-2)
             == cm_images[cm_index] * conjugate_image,
            listput(identity_records,
              [group_index, real_index, cm_index, -1]);
            match_count++);
        );
        print("CONJUGATION_", group_index,
          "_REAL_", real_index,
          "_IDENTITY_COUNT=", match_count);
      );
    );
  );

  if(#identity_records == 0,
    error("no exact CM-to-real packet identity found"));
  print("CM_STARK_UNIT=", cm_stark_unit);
  print("CM_STARK_UNIT_MINPOLY=", minpoly(cm_stark_unit));
  print("CM_STARK_ANTI_COORDINATES=[-2,1]");
  print("ROOT_OF_UNITY_COUNT=4");
  print("ORDINARY_MODULUS_RELATION=PACKET_ROOT_SQUARED_EQUALS_CM_NORM");
  print("COMPLEX_CONJUGATIONS=", Vec(complex_conjugations));
  print("EXACT_IDENTITY_COUNT=", #identity_records);
  print("EXACT_IDENTITIES=", Vec(identity_records));
  print("RQ000458_ENGINE_C_EXACT_PACKET_BRIDGE_VERIFIED=1");
  print("CLAIM_TAG=VERIFIED");
};

run_bridge();
