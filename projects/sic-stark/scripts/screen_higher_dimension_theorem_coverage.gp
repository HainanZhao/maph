\\ Exact maximal-order theorem-coverage data for canonical dimensions.
\\
\\ For the canonical order O_d of conductor f in O_K, the multiplier
\\ ideal of d O_d is d*f O_K.  We compute the one-place and both-place
\\ maximal-order ray groups at that modulus.  Conjugation on the
\\ both-place group A determines the commutator subgroup
\\
\\     C = image(conjugation - 1).
\\
\\ If B is the kernel obtained by removing the second infinite place,
\\ then the one-place ray field H satisfies
\\
\\     [H : H intersect Q_ab] = |C| / |B intersect C|.
\\
\\ Shintani's quadratic-over-absolutely-abelian condition is therefore
\\ the exact test SHINTANI_INDEX=2.

default(parisizemax, 4000000000);

group_elements(cyclic_invariants) =
{
  my(result = List(), rank = #cyclic_invariants, bounds);
  if(rank == 0,
    listput(result, []),
    bounds = vector(rank, index, [0, cyclic_invariants[index] - 1]);
    forvec(value = bounds, listput(result, Vec(value))));
  return(Vec(result));
};

apply_homomorphism(matrix_value, source, target_cyclic) =
{
  my(target_rank = #target_cyclic);
  if(target_rank == 0, return([]));
  return(vector(target_rank, row,
    lift(sum(column = 1, #source,
      matrix_value[row, column] * source[column])) % target_cyclic[row]));
};

subtract_in_group(left, right, cyclic_invariants) =
{
  return(vector(#cyclic_invariants, index,
    (left[index] - right[index]) % cyclic_invariants[index]));
};

ray_coverage(dimension) =
{
  my(canonical_discriminant, K, field_discriminant, conductor);
  my(multiplier_modulus, one_ray, both_ray, automorphism);
  my(both_rank, one_rank, conjugation_matrix, forgetful_matrix);
  my(elements, kernel = List(), commutators = List(), commutator_set);
  my(kernel_set, intersection_order, shintani_index);

  canonical_discriminant = (dimension + 1) * (dimension - 3);
  K = bnfinit(y^2 - (dimension - 1)*y + 1, 1);
  field_discriminant = K.disc;
  conductor = sqrtint(canonical_discriminant / field_discriminant);
  multiplier_modulus = dimension * conductor;

  one_ray = bnrinit(K, [multiplier_modulus, [0, 1]], 1);
  both_ray = bnrinit(K, [multiplier_modulus, [1, 1]], 1);
  automorphism = Mod((dimension - 1) - y,
    y^2 - (dimension - 1)*y + 1);

  both_rank = #both_ray.cyc;
  one_rank = #one_ray.cyc;
  conjugation_matrix = matrix(both_rank, both_rank, row, column,
    bnrisprincipal(
      both_ray,
      nfgaloisapply(K, automorphism, both_ray.gen[column]),
      0
    )[row]
  );
  if(one_rank == 0,
    forgetful_matrix = Mat(),
    forgetful_matrix = matrix(one_rank, both_rank, row, column,
      bnrisprincipal(one_ray, both_ray.gen[column], 0)[row]
    )
  );

  elements = group_elements(both_ray.cyc);
  for(index = 1, #elements,
    my(value = elements[index]);
    my(conjugate = apply_homomorphism(
      conjugation_matrix, value, both_ray.cyc));
    my(image = apply_homomorphism(
      forgetful_matrix, value, one_ray.cyc));
    if(image == vector(one_rank), listput(kernel, value));
    listput(commutators,
      subtract_in_group(conjugate, value, both_ray.cyc));
  );
  kernel_set = Set(Vec(kernel));
  commutator_set = Set(Vec(commutators));
  intersection_order = 0;
  for(index = 1, #commutator_set,
    if(setsearch(kernel_set, commutator_set[index]),
      intersection_order++));
  shintani_index = #commutator_set / intersection_order;

  print(
    "DIMENSION=", dimension,
    "|CANONICAL_DISCRIMINANT=", canonical_discriminant,
    "|FIELD_DISCRIMINANT=", field_discriminant,
    "|ORDER_CONDUCTOR=", conductor,
    "|ORDER_CLASS_NUMBER=", qfbclassno(canonical_discriminant),
    "|MULTIPLIER_MODULUS=", multiplier_modulus,
    "|MAXIMAL_ONE_RAY_STRUCTURE=", one_ray.cyc,
    "|MAXIMAL_ONE_RAY_ORDER=", one_ray.no,
    "|MAXIMAL_BOTH_RAY_STRUCTURE=", both_ray.cyc,
    "|KERNEL_ORDER=", #kernel_set,
    "|COMMUTATOR_ORDER=", #commutator_set,
    "|KERNEL_COMMUTATOR_INTERSECTION_ORDER=", intersection_order,
    "|SHINTANI_INDEX=", shintani_index,
    "|BASE_BNFCERTIFY=", bnfcertify(K)
  );
};

print("PARI_VERSION=", version());
for(dimension = 4, 20, \
{
  my(discriminant = (dimension + 1) * (dimension - 3));
  if(!issquare(discriminant), ray_coverage(dimension));
});

quit();
