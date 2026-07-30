\\ Exact search for the independently normalized Q(sqrt(-3)) route
\\ of RQ-000129.  This is a search artifact, not a W3 promotion.
\\
\\ If epsilon_8 and epsilon_12 encode the same ordinary-modulus
\\ Stark packet, the general-e theorem gives
\\
\\   log |epsilon_8| / 8 = log |epsilon_12| / 12.
\\
\\ For algebraic complex norms q_e=epsilon_e*conj(epsilon_e), this is
\\ the root-free exact identity q_8^3=q_12^2.

default(parisizemax, 6000000000);

unit_exponents(bnf, unit) =
{
  my(raw = bnfisunit(bnf, unit));
  vector(#bnf.fu, index, raw[index]);
};

unit_action_matrix(bnf, polynomial, automorphism) =
{
  my(rank = #bnf.fu, answer = matrix(rank, rank));
  for(column = 1, rank,
    my(image = Mod(subst(
      lift(bnf.fu[column]), x, automorphism), polynomial));
    my(exponents = unit_exponents(bnf, image));
    for(row = 1, rank,
      answer[row, column] = exponents[row]);
  );
  answer;
};

contains_pair(pairs, first, second) =
{
  for(index = 1, #pairs,
    if(pairs[index] == [first, second], return(1)));
  0;
};

run_search() =
{
  my(source =
    x^8 - 4*x^5 - 2*x^4 - 8*x^2 - 8*x - 2);
  my(primary_polynomial =
    x^8 - 4*x^6 - 4*x^5 + 6*x^4
      + 16*x^3 + 16*x^2 + 8*x + 2);
  my(secondary_polynomial =
    x^8 - 2*x^6 + 5*x^4 - 4*x^2 + 1);
  my(primary = bnfinit(primary_polynomial, 1));
  my(secondary = bnfinit(secondary_polynomial, 1));
  my(primary_unit =
    (primary.fu[1] * primary.fu[2])^4);
  my(secondary_automorphisms =
    nfgaloisconj(secondary_polynomial));
  my(secondary_sigma = secondary_automorphisms[3]);
  my(secondary_action = unit_action_matrix(
    secondary, secondary_polynomial, secondary_sigma));
  my(secondary_anti_lattice =
    matkerint(matid(#secondary.fu) + secondary_action^2));
  my(normal_closure = nfsplitting(source, 16, 1)[1]);
  my(galois_group = galoisinit(normal_closure));
  my(identity = galois_group.group[1]);
  my(primary_inclusions =
    nfisincl(primary_polynomial, normal_closure, 2));
  my(secondary_inclusions =
    nfisincl(secondary_polynomial, normal_closure, 2));
  my(primary_images = vector(#primary_inclusions));
  my(complex_conjugations = List());
  my(matches = List());
  my(match_exponent_pairs = List());

  if(primary.sign != [0, 4] || secondary.sign != [0, 4],
    error("character-field signature changed"));
  if(bnfcertify(primary) != 1 || bnfcertify(secondary) != 1,
    error("character field failed bnfcertify"));
  if(primary.tu[1] != 8 || secondary.tu[1] != 12,
    error("route e-values changed"));
  if(galoisidentify(galois_group) != [16, 13],
    error("normal-closure group changed"));
  if(secondary_action !=
      [-1, 0, 0; 0, 0, -1; 0, 1, 0],
    error("secondary C4 unit action changed"));
  if(secondary_anti_lattice !=
      [0, 0; 1, 0; 0, 1],
    error("secondary anti-unit lattice changed"));

  for(index = 1, #primary_inclusions,
    primary_images[index] = Mod(
      subst(lift(primary_unit), x, primary_inclusions[index]),
      normal_closure));

  for(group_index = 1, #galois_group.group,
    my(permutation = galois_group.group[group_index]);
    if(permutation != identity && permutation^2 == identity,
      my(fixed = galoisfixedfield(
        galois_group, permutation, 1, z));
      if(nfinit(fixed).sign[1] > 0,
        listput(complex_conjugations, group_index));
    );
  );

  for(first = -3, 3,
    for(second = -3, 3,
      if(first || second,
        my(secondary_root =
          secondary.fu[2]^first * secondary.fu[3]^second);
        my(secondary_unit = secondary_root^6);
        for(position = 1, #complex_conjugations,
          my(group_index = complex_conjugations[position]);
          my(conjugation = lift(galoispermtopol(
            galois_group, galois_group.group[group_index])));
          for(primary_index = 1, #primary_images,
            my(primary_norm =
              primary_images[primary_index]
              * Mod(subst(
                  lift(primary_images[primary_index]),
                  x, conjugation), normal_closure));
            for(secondary_index = 1, #secondary_inclusions,
              my(secondary_image = Mod(
                subst(lift(secondary_unit), x,
                  secondary_inclusions[secondary_index]),
                normal_closure));
              my(secondary_norm =
                secondary_image
                * Mod(subst(
                    lift(secondary_image), x, conjugation),
                    normal_closure));
              if(primary_norm^3 == secondary_norm^2,
                listput(matches,
                  [first, second, group_index,
                   primary_index, secondary_index, 1]));
              if(primary_norm^(-3) == secondary_norm^2,
                listput(matches,
                  [first, second, group_index,
                   primary_index, secondary_index, -1]));
            );
          );
        );
      );
    );
  );

  for(index = 1, #matches,
    my(first = matches[index][1], second = matches[index][2]);
    if(!contains_pair(Vec(match_exponent_pairs), first, second),
      listput(match_exponent_pairs, [first, second]));
  );
  if(#matches != 256,
    error(Str("normalized bridge match count changed: ", #matches)));
  if(Vec(match_exponent_pairs) !=
      [[-1, 0], [0, -1], [0, 1], [1, 0]],
    error(Str("normalized bridge exponent orbits changed: ",
      Vec(match_exponent_pairs))));

  print("CASE_ID=RQ-000129");
  print("PRIMARY_BASE=Q(sqrt(-2))");
  print("PRIMARY_E=8");
  print("PRIMARY_ALGEBRAIC_CANDIDATE=", primary_unit);
  print("PRIMARY_ALGEBRAIC_CANDIDATE_MINPOLY=",
    minpoly(primary_unit));
  print("SECONDARY_BASE=Q(sqrt(-3))");
  print("SECONDARY_E=12");
  print("SECONDARY_CHARACTER_FIELD=", secondary_polynomial);
  print("SECONDARY_ROOTS_OF_UNITY=", secondary.tu[1]);
  print("SECONDARY_C4_GENERATOR=", secondary_sigma);
  print("SECONDARY_C4_UNIT_ACTION=", secondary_action);
  print("SECONDARY_ANTI_UNIT_LATTICE=", secondary_anti_lattice);
  print("NORMAL_CLOSURE_DEGREE=", poldegree(normal_closure));
  print("NORMAL_CLOSURE_GROUP=", galoisidentify(galois_group));
  print("COMPLEX_CONJUGATIONS=", Vec(complex_conjugations));
  print("SEARCH_BOX=[-3,3]^2_EXCLUDING_ZERO");
  print("NORMALIZED_IDENTITY=q8^3=q12^2");
  print("MATCH_COUNT=", #matches);
  print("MATCH_EXPONENT_PAIRS=", Vec(match_exponent_pairs));
  print("MATCH_MULTIPLICITY_PER_EXPONENT_PAIR=",
    #matches / #match_exponent_pairs);
  print("Q6_SECOND_BASE_BRIDGE_SEARCH_COMPLETE=1");
  print("CLAIM_TAG=EXACT_SEARCH_NOT_PROMOTION");
};

run_search();
