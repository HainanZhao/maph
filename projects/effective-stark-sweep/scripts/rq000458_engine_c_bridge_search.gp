\\ Exact finite search for the CM anti-unit coordinate whose ordinary
\\ absolute norm is an aligned packet root.  Search status only.

default(parisizemax, 6000000000);

run_search() =
{
  my(real_polynomial =
    x^8 - 40*x^7 + 172*x^6 + 488*x^5 + 694*x^4
      + 488*x^3 + 172*x^2 - 40*x + 1);
  my(cm_polynomial =
    x^8 - 4*x^7 + 20*x^6 - 28*x^5 + 106*x^4
      - 152*x^3 + 152*x^2 + 184*x + 58);
  my(cm_bnf = bnfinit(cm_polynomial, 1));
  my(anti_basis_1 = cm_bnf.fu[1]);
  my(anti_basis_2 = cm_bnf.fu[2]^(-1) * cm_bnf.fu[3]);
  my(normal_closure =
    nfsplitting(real_polynomial, 16, 1)[1]);
  my(gal = galoisinit(normal_closure));
  my(identity = gal.group[1]);
  my(real_inclusions =
    nfisincl(real_polynomial, normal_closure, 2));
  my(cm_inclusions =
    nfisincl(cm_polynomial, normal_closure, 2));
  my(real_images = vector(
    #real_inclusions, index,
    Mod(real_inclusions[index], normal_closure)));
  my(first_images = vector(
    #cm_inclusions, index,
    Mod(subst(
      lift(anti_basis_1), x, cm_inclusions[index]),
      normal_closure)));
  my(second_images = vector(
    #cm_inclusions, index,
    Mod(subst(
      lift(anti_basis_2), x, cm_inclusions[index]),
      normal_closure)));
  my(conjugations = List());
  for(group_index = 1, #gal.group,
    my(permutation = gal.group[group_index]);
    if(permutation != identity && permutation^2 == identity,
      my(fixed = galoisfixedfield(gal, permutation, 1, z));
      if(nfinit(fixed).sign[1] > 0,
        listput(conjugations, [
          group_index,
          lift(galoispermtopol(gal, permutation))
        ]));
    );
  );

  my(matches = List());
  for(first = -16, 16,
    for(second = -16, 16,
      if(first || second,
        for(conjugation_index = 1, #conjugations,
          my(group_index = conjugations[conjugation_index][1]);
          my(conjugation = conjugations[conjugation_index][2]);
          for(cm_index = 1, #cm_inclusions,
            my(image =
              first_images[cm_index]^first
              * second_images[cm_index]^second);
            my(norm_image = image * Mod(subst(
              lift(image), x, conjugation), normal_closure));
            for(real_index = 1, #real_images,
              if(norm_image == real_images[real_index],
                listput(matches, [
                  first, second, group_index,
                  cm_index, real_index, 1
                ]));
              if(norm_image == real_images[real_index]^(-1),
                listput(matches, [
                  first, second, group_index,
                  cm_index, real_index, -1
                ]));
            );
          );
        );
      );
    );
  );
  print("SEARCH_RANGE=[-16,16]^2_MINUS_ZERO");
  print("MATCH_COUNT=", #matches);
  print("MATCHES=", Vec(matches));
  print("RQ000458_ENGINE_C_BRIDGE_SEARCH_COMPLETE=1");
  print("CLAIM_TAG=EXACT_SEARCH_NOT_THEOREM");
};

run_search();
