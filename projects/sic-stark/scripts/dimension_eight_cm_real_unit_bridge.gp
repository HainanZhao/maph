\\ Exact bridge between the real-quadratic Roblot units and the
\\ imaginary-quadratic Stark-unit candidates in dimension eight.

default(parisizemax, 6000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

audit_packet(packet, real_polynomial, cm_polynomial) =
{
  my(normal_closure =
    nfsplitting(real_polynomial, 16, 1)[1]);
  my(galois_group = galoisinit(normal_closure));
  my(identity = galois_group.group[1]);
  my(real_bnf = bnfinit(real_polynomial, 1));
  my(cm_bnf = bnfinit(cm_polynomial, 1));
  my(real_unit = (real_bnf.fu[4] * real_bnf.fu[5])^2);
  my(cm_stark_unit = cm_bnf.fu[3]^2);
  my(real_inclusions =
    nfisincl(real_polynomial, normal_closure, 2));
  my(cm_inclusions =
    nfisincl(cm_polynomial, normal_closure, 2));
  my(real_images = vector(#real_inclusions));
  my(cm_images = vector(#cm_inclusions));
  my(complex_conjugations = List());
  my(identity_records = List());
  my(permutation, fixed_polynomial, conjugation);
  my(conjugate_image, match_count);

  assert_equal(Str("PACKET_", packet, "_NORMAL_CLOSURE_DEGREE"),
    poldegree(normal_closure), 16);
  assert_equal(Str("PACKET_", packet, "_NORMAL_CLOSURE_SIGNATURE"),
    nfinit(normal_closure).sign, [0, 8]);
  assert_equal(Str("PACKET_", packet, "_REAL_INCLUSION_COUNT"),
    #real_inclusions, 8);
  assert_equal(Str("PACKET_", packet, "_CM_INCLUSION_COUNT"),
    #cm_inclusions, 8);

  for(index = 1, #real_inclusions,
    real_images[index] = Mod(
      subst(lift(real_unit), x, real_inclusions[index]),
      normal_closure
    );
  );
  for(index = 1, #cm_inclusions,
    cm_images[index] = Mod(
      subst(lift(cm_stark_unit), x, cm_inclusions[index]),
      normal_closure
    );
  );

  \\ In a totally imaginary Galois field, an involution is a complex
  \\ conjugation for some embedding exactly when its fixed field has a
  \\ real place.  This detects the conjugations algebraically, without
  \\ using floating-point root labels.
  for(group_index = 1, #galois_group.group,
    permutation = galois_group.group[group_index];
    if(permutation != identity && permutation^2 == identity,
      fixed_polynomial =
        galoisfixedfield(galois_group, permutation, 1, z);
      if(nfinit(fixed_polynomial).sign[1] > 0,
        listput(complex_conjugations, group_index)
      );
    );
  );

  assert_equal(Str("PACKET_", packet, "_COMPLEX_CONJUGATION_COUNT"),
    #complex_conjugations, 2);

  for(conjugation_position = 1, #complex_conjugations,
    group_index = complex_conjugations[conjugation_position];
    permutation = galois_group.group[group_index];
    conjugation = lift(galoispermtopol(galois_group, permutation));
    for(real_index = 1, #real_images,
      \\ Only the real-field images fixed by this conjugation represent
      \\ real places for the associated embedding.
      if(Mod(subst(
            lift(real_images[real_index]), x, conjugation),
          normal_closure) == real_images[real_index],
        match_count = 0;
        for(cm_index = 1, #cm_images,
          conjugate_image = Mod(subst(
              lift(cm_images[cm_index]), x, conjugation),
            normal_closure);
          if(real_images[real_index]
              == cm_images[cm_index] * conjugate_image,
            listput(identity_records,
              [group_index, real_index, cm_index, 1]);
            match_count++;
          );
          if(real_images[real_index]^(-1)
              == cm_images[cm_index] * conjugate_image,
            listput(identity_records,
              [group_index, real_index, cm_index, -1]);
            match_count++;
          );
        );
        assert_equal(
          Str("PACKET_", packet, "_CONJUGATION_", group_index,
              "_REAL_", real_index, "_IDENTITY_COUNT"),
          match_count, 4
        );
      );
    );
  );

  assert_equal(Str("PACKET_", packet, "_EXACT_IDENTITY_COUNT"),
    #identity_records, 32);
  print("PACKET_", packet, "_COMPLEX_CONJUGATIONS=",
    Vec(complex_conjugations));
  print("PACKET_", packet, "_EXACT_IDENTITIES=",
    Vec(identity_records));
};

audit_packet(0, \
  x^8 - 6*x^6 - 30*x^4 - 18*x^2 + 9, \
  x^8 - 4*x^6 - 12*x^5 + 18*x^4 + 48*x^3 \
    - 16*x^2 - 168*x + 166);
audit_packet(1, \
  x^8 + 6*x^6 - 30*x^4 + 18*x^2 + 9, \
  x^8 - 4*x^7 + 8*x^5 + 28*x^4 + 96*x^3 \
    + 144*x^2 + 96*x + 24);

print("CM_TO_REAL_UNIT_BRIDGE_CERTIFIED=1");
quit();
