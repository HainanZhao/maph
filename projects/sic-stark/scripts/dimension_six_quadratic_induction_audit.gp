\\ Exact audit of every quadratic induction base for the faithful
\\ dimension-six Artin quotient.
\\
\\ The normal closure of the one-place ray field has group [24,8].
\\ Its unique normal order-two quotient kernel gives a degree-twelve
\\ Galois field with group [12,4] (the dihedral group of order twelve).
\\ We enumerate all three index-two subgroups of that quotient and test
\\ which quadratic base makes the degree-six relative extension abelian.

default(parisizemax, 4000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

permutation_compose(left, right) =
{
  Vecsmall(vector(#left, index, left[right[index]]));
};

generators_commute(generators) =
{
  my(result = 1);
  for(left = 1, #generators,
    for(right = left + 1, #generators,
      if(permutation_compose(generators[left], generators[right]) \
          != permutation_compose(generators[right], generators[left]),
        result = 0)));
  result;
};

normal_polynomial = \
  x^24 - 3*x^23 + 15*x^22 - 21*x^21 + 27*x^20 - 29*x^18 \
  - 27*x^17 + 156*x^16 - 282*x^15 + 321*x^14 + 12*x^13 \
  - 3*x^12 + 78*x^11 + 549*x^10 - 708*x^9 + 1068*x^8 \
  - 393*x^7 + 169*x^6 + 174*x^5 - 177*x^4 + 21*x^3 \
  + 27*x^2 - 9*x + 1;

normal_group = galoisinit(normal_polynomial);
assert_equal("NORMAL_CLOSURE_GROUP_ID", \
  galoisidentify(normal_group), [24, 8]);

\\ Locate the unique normal order-two subgroup by asking which fixed
\\ degree-twelve field is itself Galois over Q.
normal_subgroups = galoissubgroups(normal_group);
faithful_quotient_polynomial = 0;
galois_degree_twelve_count = 0;

inspect_order_two_subgroup(subgroup) =
{
  my(candidate, candidate_group);
  if(vecprod(Vec(subgroup[2])) == 2,
    candidate = polredabs(
      galoisfixedfield(normal_group, subgroup[1], 1, 'z));
    candidate_group = galoisinit(candidate);
    if(type(candidate_group) != "t_INT",
        galois_degree_twelve_count++;
        faithful_quotient_polynomial = candidate));
};
for(index = 1, #normal_subgroups, \
  inspect_order_two_subgroup(normal_subgroups[index]));
assert_equal("GALOIS_DEGREE_TWELVE_FIXED_FIELD_COUNT", \
  galois_degree_twelve_count, 1);

faithful_group = galoisinit(faithful_quotient_polynomial);
assert_equal("FAITHFUL_QUOTIENT_GROUP_ID", \
  galoisidentify(faithful_group), [12, 4]);
print("FAITHFUL_QUOTIENT_POLYNOMIAL=", faithful_quotient_polynomial);

\\ A quadratic induction base corresponds to an index-two subgroup,
\\ hence a subgroup of order six.  Pairwise commutation of a generating
\\ set is equivalent to abelianness of that subgroup.
faithful_subgroups = galoissubgroups(faithful_group);
quadratic_subfield_count = 0;
real_abelian_count = 0;
imaginary_abelian_count = 0;
seen_disc_21 = 0;
seen_disc_minus_3 = 0;
seen_disc_minus_7 = 0;

inspect_index_two_subgroup(subgroup) =
{
  my(base_polynomial, base_discriminant, base_signature);
  my(relative_group_is_abelian);
  if(vecprod(Vec(subgroup[2])) == 6,
    base_polynomial = polredabs(
      galoisfixedfield(faithful_group, subgroup[1], 1, 'z));
    base_discriminant = nfdisc(base_polynomial);
    base_signature = nfinit(base_polynomial).sign;
    relative_group_is_abelian = generators_commute(subgroup[1]);
    quadratic_subfield_count++;
    print(Str("QUADRATIC_BASE_", quadratic_subfield_count,
      "_POLYNOMIAL="), base_polynomial);
    print(Str("QUADRATIC_BASE_", quadratic_subfield_count,
      "_DISCRIMINANT="), base_discriminant);
    print(Str("QUADRATIC_BASE_", quadratic_subfield_count,
      "_SIGNATURE="), base_signature);
    print(Str("QUADRATIC_BASE_", quadratic_subfield_count,
      "_RELATIVE_GROUP_ABELIAN="), relative_group_is_abelian);

    if(base_discriminant == 21,
        seen_disc_21++;
        assert_equal("REAL_BASE_SIGNATURE", base_signature, [2, 0]);
        assert_equal("REAL_BASE_RELATIVE_GROUP_ABELIAN", \
          relative_group_is_abelian, 1);
        real_abelian_count++);
    if(base_discriminant == -3,
        seen_disc_minus_3++;
        assert_equal("IMAGINARY_MINUS_3_BASE_SIGNATURE", \
          base_signature, [0, 1]);
        assert_equal("IMAGINARY_MINUS_3_RELATIVE_GROUP_ABELIAN", \
          relative_group_is_abelian, 0);
        imaginary_abelian_count += relative_group_is_abelian);
    if(base_discriminant == -7,
        seen_disc_minus_7++;
        assert_equal("IMAGINARY_MINUS_7_BASE_SIGNATURE", \
          base_signature, [0, 1]);
        assert_equal("IMAGINARY_MINUS_7_RELATIVE_GROUP_ABELIAN", \
          relative_group_is_abelian, 0);
        imaginary_abelian_count += relative_group_is_abelian));
};
for(index = 1, #faithful_subgroups, \
  inspect_index_two_subgroup(faithful_subgroups[index]));

assert_equal("QUADRATIC_SUBFIELD_COUNT", quadratic_subfield_count, 3);
assert_equal("DISCRIMINANT_21_BASE_COUNT", seen_disc_21, 1);
assert_equal("DISCRIMINANT_MINUS_3_BASE_COUNT", seen_disc_minus_3, 1);
assert_equal("DISCRIMINANT_MINUS_7_BASE_COUNT", seen_disc_minus_7, 1);
assert_equal("REAL_ABELIAN_QUADRATIC_BASE_COUNT", real_abelian_count, 1);
assert_equal("IMAGINARY_ABELIAN_QUADRATIC_BASE_COUNT", \
  imaginary_abelian_count, 0);
print("QUADRATIC_BASE_DISCRIMINANTS=[21,-3,-7]");
print("UNIQUE_ABELIAN_QUADRATIC_BASE_DISCRIMINANT=21");
print("IMAGINARY_QUADRATIC_ELLIPTIC_UNIT_TRANSFER_AVAILABLE=0");

quit();
