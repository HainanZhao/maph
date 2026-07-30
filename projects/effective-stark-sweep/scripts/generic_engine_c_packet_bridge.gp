\\ Exact common-normal-closure bridge from an isolated Engine-C
\\ anti-unit coordinate to its positive real norm packet.

default(realprecision, 100);
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
    for(row = 1, rank, answer[row, column] = exponents[row]);
  );
  answer;
};

inspect_involution(gal, normal_polynomial, inclusions, candidate, group_index) =
{
  my(output = List());
  my(identity = gal.group[1]);
  my(permutation = gal.group[group_index]);
  if(permutation != identity && permutation^2 == identity,
    my(fixed = galoisfixedfield(
      gal, permutation, 1, z));
    my(fixed_nf = nfinit(fixed));
    print("INVOLUTION_", group_index,
      "_FIXED_SIGNATURE=", fixed_nf.sign);
    \\ The one-place ray field has mixed signature [4,2], not a
    \\ totally real fixed field.  A complex conjugation is one of the
    \\ involutions whose fixed field has a real place.
    if(fixed_nf.sign[1] > 0,
      my(conjugation =
        lift(galoispermtopol(gal, permutation)));
      for(inclusion_index = 1, #inclusions,
        my(image = Mod(subst(
          lift(candidate), x, inclusions[inclusion_index]),
          normal_polynomial));
        my(norm_image = image * Mod(subst(
          lift(image), x, conjugation), normal_polynomial));
        listput(output, [
          group_index,
          inclusion_index,
          minpoly(norm_image)
        ]);
      );
    );
  );
  Vec(output);
};

run_bridge() =
{
  my(polynomial = CHARACTER_FIELD_POLYNOMIAL);
  my(field = bnfinit(polynomial, 1));
  my(automorphisms = nfgaloisconj(polynomial));
  my(order_four = List());
  for(index = 1, #automorphisms,
    my(action =
      unit_action_matrix(field, polynomial, automorphisms[index]));
    if(action^2 != matid(#field.fu) &&
        action^4 == matid(#field.fu),
      listput(order_four, [
        Str(automorphisms[index]), automorphisms[index], action
      ]));
  );
  my(primes_five = idealprimedec(field, 5));
  my(frobenius_pairs = List());
  for(automorphism_index = 1, #order_four,
    for(prime_index = 1, #primes_five,
      \\ Absolute ramification may come from the quadratic base
      \\ (Q(sqrt(-10)) is ramified at 5); relative Frobenius is still
      \\ defined.  Residue degree four selects the quartic factor.
      if(primes_five[prime_index].f == 4,
        my(modpr =
          nfmodprinit(field, primes_five[prime_index]));
        if(nfmodpr(field,
            Mod(order_four[automorphism_index][2], polynomial),
            modpr) ==
            nfmodpr(field, Mod(x, polynomial)^5, modpr),
          listput(frobenius_pairs, [
            automorphism_index, prime_index
          ]));
      );
    );
  );
  print("ORDER_FOUR_CANDIDATE_COUNT=", #order_four);
  print("PRIMES_ABOVE_SEPARATOR=", primes_five);
  print("FROBENIUS_PAIRS=", Vec(frobenius_pairs));
  if(#frobenius_pairs != 1,
    error(Str("Frobenius pair count: ", #frobenius_pairs)));
  my(frobenius_pair = frobenius_pairs[1]);
  my(sigma =
    order_four[frobenius_pair[1]][2]);
  my(action =
    order_four[frobenius_pair[1]][3]);
  my(anti_lattice =
    matkerint(matid(#field.fu) + action^2));
  my(anti_units = vector(2, column,
    prod(row = 1, #field.fu,
      field.fu[row]^anti_lattice[row, column])));
  my(candidate =
    anti_units[1]^CANDIDATE_COORDINATES[1] *
    anti_units[2]^CANDIDATE_COORDINATES[2]);
  my(normal_polynomial =
    nfsplitting(polynomial, 16, 1)[1]);
  my(gal = galoisinit(normal_polynomial));
  my(inclusions = nfisincl(polynomial, normal_polynomial, 2));
  my(inclusion_pairs = vector(#inclusions, index,
    [Str(inclusions[index]), inclusions[index]]));
  my(inclusion = vecsort(inclusion_pairs, 1)[1][2]);

  \\ The least exact separator is n=5 and a_5=-i.  Recover the
  \\ corresponding order-four Frobenius without numerical recognition:
  \\ sigma(alpha) == alpha^5 modulo the unique usable prime.
  \\ Lift sigma through a canonical inclusion into the normal closure.
  my(normal_sigma_matches = List());
  my(sigma_image = Mod(subst(
    lift(sigma), x, inclusion), normal_polynomial));
  for(group_index = 1, #gal.group,
    my(group_polynomial =
      lift(galoispermtopol(gal, gal.group[group_index])));
    if(Mod(subst(inclusion, x, group_polynomial),
        normal_polynomial) == sigma_image,
      listput(normal_sigma_matches, [
        Str(group_polynomial), group_index
      ]));
  );
  if(#normal_sigma_matches == 0,
    error("normal sigma has no lift"));
  \\ Choose sigma-lift/conjugation jointly.  The relative automorphism
  \\ has two normal-closure lifts; only the compatible pairs satisfy
  \\ the D4 relation and fix a field with a real place.
  my(dihedral_pairs = List());
  for(lift_index = 1, #normal_sigma_matches,
    my(normal_sigma_index =
      normal_sigma_matches[lift_index][2]);
    my(normal_sigma_permutation =
      gal.group[normal_sigma_index]);
    my(normal_sigma = lift(galoispermtopol(
      gal, normal_sigma_permutation)));
    for(group_index = 1, #gal.group,
      my(permutation = gal.group[group_index]);
      if(permutation != gal.group[1] &&
          permutation^2 == gal.group[1] &&
          permutation * normal_sigma_permutation * permutation ==
            normal_sigma_permutation^(-1),
        my(fixed = galoisfixedfield(
          gal, permutation, 1, z));
        if(nfinit(fixed).sign[1] > 0,
          my(conjugation = lift(galoispermtopol(
            gal, permutation)));
          listput(dihedral_pairs, [
            Str(normal_sigma, "|", conjugation),
            normal_sigma_index, group_index,
            normal_sigma, conjugation
          ]);
        );
      );
    );
  );
  if(#dihedral_pairs == 0,
    error("no compatible sigma/conjugation pair"));
  my(dihedral_sorted = vecsort(Vec(dihedral_pairs), 1));
  my(normal_sigma_index = dihedral_sorted[1][2]);
  my(conjugation_index = dihedral_sorted[1][3]);
  my(normal_sigma = dihedral_sorted[1][4]);
  my(conjugation = dihedral_sorted[1][5]);
  my(candidate_image = Mod(subst(
    lift(candidate), x, inclusion), normal_polynomial));
  my(labeled_norms = vector(4, label_index,
    my(power = label_index - 1);
    my(orbit_image = candidate_image);
    for(repetition = 1, power,
      orbit_image = Mod(subst(
        lift(orbit_image), x, normal_sigma),
        normal_polynomial));
    orbit_image * Mod(subst(
      lift(orbit_image), x, conjugation),
      normal_polynomial)));
  if(#Set(labeled_norms) != 4,
    error("Artin-labeled norm orbit is not free"));
  my(labeled_polynomials =
    Set(vector(4, index, minpoly(labeled_norms[index]))));
  if(#labeled_polynomials != 1 ||
      poldegree(labeled_polynomials[1]) != 8,
    error("Artin-labeled norm orbit polynomial mismatch"));
  my(norm_records = List());
  for(group_index = 1, #gal.group,
    my(local_records = inspect_involution(
      gal, normal_polynomial, inclusions, candidate,
      group_index));
    for(record_index = 1, #local_records,
      listput(norm_records, local_records[record_index]));
  );
  my(records = Vec(norm_records));
  if(#records == 0,
    error("no real-conjugation norm records"));
  my(polynomials =
    Set(vector(#records, index, records[index][3])));
  my(selector_nf = nfinit(REAL_SELECTOR_FIELD_POLYNOMIAL));
  my(isomorphic = vector(#polynomials, index,
    #nfisisom(nfinit(polynomials[index]), selector_nf) > 0));
  my(positive = vector(#polynomials, index,
    my(roots = polrootsreal(polynomials[index]));
    #roots > 0 && vecmax(roots) > 0));

  print("CASE_ID=", CASE_ID);
  print("ROUTE_ID=", ROUTE_ID);
  print("CANDIDATE_COORDINATES=", CANDIDATE_COORDINATES);
  print("CANDIDATE_MINPOLY=", minpoly(candidate));
  print("CANDIDATE_NORM=", norm(candidate));
  print("SEPARATOR_RATIONAL_PRIME=5");
  print("SELECTED_SEPARATOR_COEFFICIENT=-I");
  print("CANONICAL_SIGMA_IS_FROBENIUS_AT_SEPARATOR=1");
  print("NORMAL_SIGMA_GROUP_INDEX=", normal_sigma_index);
  print("COMPLEX_CONJUGATION_GROUP_INDEX=", conjugation_index);
  print("DIHEDRAL_RELATION_VERIFIED=1");
  for(label_index = 1, 4,
    print("ARTIN_LABEL_", label_index - 1,
      "_POSITIVE_NORM=", labeled_norms[label_index]);
  );
  print("ARTIN_LABELED_PACKET_POLYNOMIAL=",
    labeled_polynomials[1]);
  print("NORMAL_CLOSURE_DEGREE=", poldegree(normal_polynomial));
  print("REAL_CONJUGATION_RECORD_COUNT=", #records);
  print("DISTINCT_POSITIVE_NORM_POLYNOMIAL_COUNT=", #polynomials);
  for(index = 1, #polynomials,
    print("POSITIVE_NORM_POLYNOMIAL_", index, "=", polynomials[index]);
    print("POSITIVE_NORM_POLYNOMIAL_", index,
      "_IS_SELECTOR_FIELD=", isomorphic[index]);
    print("POSITIVE_NORM_POLYNOMIAL_", index,
      "_HAS_POSITIVE_REAL_ROOT=", positive[index]);
  );
  if(vecmin(isomorphic) != 1,
    error("a norm packet does not generate the selector field"));
  if(vecmin(positive) != 1,
    error("a norm packet has no positive real embedding"));
  print("GENERIC_ENGINE_C_PACKET_BRIDGE_VERIFIED=1");
};

run_bridge();
