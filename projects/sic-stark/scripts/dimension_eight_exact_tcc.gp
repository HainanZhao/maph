\\ Exact finite TCC certificate for the selected dimension-eight packet.
\\
\\ The primitive squared overlaps generate the degree-32 one-place ray
\\ field H.  Adjoining one signed square root gives a degree-64 field F
\\ containing all primitive signed overlaps and the degree-eight
\\ lower-conductor field.  A compatible compositum with Q(zeta_16) has
\\ degree 128 and contains every overlap, Weyl phase, and normalization.

default(realprecision, 100);
default(parisize, 256000000);
default(parisizemax, 6000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

iadd(first, second) =
  [first[1] + second[1], first[2] + second[2]];
imul(first, second) =
{
  my(values = [
    first[1]*second[1], first[1]*second[2],
    first[2]*second[1], first[2]*second[2]
  ]);
  [vecmin(values), vecmax(values)];
};
ieval(polynomial, interval) =
{
  my(value = [0, 0]);
  forstep(degree = poldegree(polynomial), 0, -1,
    value = iadd(
      imul(value, interval),
      [polcoef(polynomial, degree), polcoef(polynomial, degree)]
    )
  );
  value;
};
is_subset(inner, outer) =
  inner[1] >= outer[1] && inner[2] <= outer[2];

relative_squared_polynomial = \
  x^16 + (-56*y - 32)*x^15 + (2696*y + 1668)*x^14 \
  + (-70632*y - 43656)*x^13 + (1085616*y + 670940)*x^12 \
  + (-10068808*y - 6222872)*x^11 \
  + (55400584*y + 34239444)*x^10 \
  + (-169674744*y - 104864752)*x^9 \
  + (255738816*y + 158055290)*x^8 \
  + (-169674744*y - 104864752)*x^7 \
  + (55400584*y + 34239444)*x^6 \
  + (-10068808*y - 6222872)*x^5 \
  + (1085616*y + 670940)*x^4 \
  + (-70632*y - 43656)*x^3 + (2696*y + 1668)*x^2 \
  + (-56*y - 32)*x + 1;

Hpol = rnfequation(y^2 - y - 1, relative_squared_polynomial);
Fpol = subst(Hpol, x, x^2);
assert_equal("SIGNED_FIELD_DEGREE", poldegree(Fpol), 64);
assert_equal("SIGNED_FIELD_IRREDUCIBLE", polisirreducible(Fpol), 1);

H = bnfinit(Hpol, 1);
H_generator = Mod(x, Hpol);
H_conjugates = nfgaloisconj(H);
assert_equal("RAY_FIELD_AUTOMORPHISM_COUNT", #H_conjugates, 16);

F_generator = Mod(x, Fpol);
F_interval = [ \
  26288661864440375095695895416815929695628410837504829959130525110258236 \
    / 10^70, \
  26288661864440375095695895416815929695628410837504829959130525110258237 \
    / 10^70 \
];
H_interval = imul(F_interval, F_interval);
assert_equal("DISTINGUISHED_SIGNED_ROOT_COUNT", \
  polsturm(Fpol, F_interval), 1);

free_rank = H.r1 + H.r2 - 1;
ratio_roots = vector(#H_conjugates);
for(index = 1, #H_conjugates, \
{
  my(conjugate = Mod(H_conjugates[index], Hpol));
  my(ratio = conjugate/H_generator);
  my(exponents = bnfisunit(H, ratio));
  my(root = Mod(1, Hpol));
  assert_equal(Str("RATIO_", index, "_IS_A_UNIT"), #exponents > 0, 1);
  assert_equal(Str("RATIO_", index, "_PARITY"), \
    vecsum(vector(#exponents, k, exponents[k] % 2)), 0);
  for(k = 1, free_rank, root *= H.fu[k]^(exponents[k]/2));
  root *= H.tu[2]^(exponents[free_rank + 1]/2);
  assert_equal(Str("RATIO_", index, "_SQUARE_ROOT"), root^2 == ratio, 1);
  ratio_roots[index] = root;
});

positive_primitive_root(left, right) =
{
  my(matches = List(), image_interval, root_F, root_interval);
  for(index = 1, #H_conjugates,
    image_interval = ieval(H_conjugates[index], H_interval);
    if(is_subset(image_interval, [left, right]),
      root_F = F_generator \
        * subst(lift(ratio_roots[index]), x, F_generator^2);
      root_interval = ieval(lift(root_F), F_interval);
      if(root_interval[2] < 0, root_F = -root_F);
      if(ieval(lift(root_F), F_interval)[1] <= 0,
        error("primitive square root sign was not isolated"));
      listput(matches, root_F)
    )
  );
  if(#matches != 1,
    error(Str("primitive squared interval has ", #matches, \
      " matches: ", [left, right])));
  matches[1];
};

lower_polynomial = \
  x^8 - 8*x^7 + 12*x^6 + 8*x^5 - 22*x^4 \
    + 8*x^3 + 12*x^2 - 8*x + 1;
lower_inclusions = nfisincl(lower_polynomial, Fpol, 2);
assert_equal("LOWER_FIELD_INCLUSION_COUNT", #lower_inclusions, 4);

positive_lower_root(left, right) =
{
  my(matches = List(), element, image_interval);
  assert_equal("LOWER_ROOT_STURM_COUNT", \
    polsturm(lower_polynomial, [left, right]), 1);
  for(index = 1, #lower_inclusions,
    element = Mod(lower_inclusions[index], Fpol);
    image_interval = ieval(lift(element), F_interval);
    if(is_subset(image_interval, [left, right]),
      listput(matches, element))
  );
  if(#matches != 1,
    error(Str("lower root interval has ", #matches, \
      " matches: ", [left, right])));
  matches[1];
};

overlaps_F = matrix(8, 8);
overlaps_F[1, 1] = 3;

principal_sign(first, second) =
  (-1)^(8*(first + second) + first*second + min(8, first + second));

install_orbit(first, second, absolute_value, use_phase) =
{
  my(current_first = first, current_second = second, next_first, value);
  for(step = 1, 3,
    value = if(use_phase, \
      principal_sign(current_first, current_second)*absolute_value, \
      absolute_value);
    overlaps_F[current_first + 1, current_second + 1] = value;
    next_first = (7*current_first - current_second) % 8;
    current_second = current_first;
    current_first = next_first
  );
};

\\ Primitive representatives, with intervals for their squared values.
primitive_windows = [ \
  0,1, 6910937, 6910938, 1000000; \
  0,3, 2061122, 2061123, 1000000; \
  0,5,  485172,  485173, 1000000; \
  0,7,  144698,  144699, 1000000; \
  1,1,  125112,  125113, 1000000; \
  1,2,   90044,   90045, 1000000; \
  1,3,   65762,   65763, 1000000; \
  1,4,   54831,   54832, 1000000; \
  1,5,   60665,   60666, 1000000; \
  2,3,   22955,   22956, 1000000; \
  2,7, 7992821, 7992822, 1000000; \
  3,6,16483891,16483892, 1000000; \
  3,7,11105600,11105601, 1000000; \
  4,5,18237810,18237811, 1000000; \
  4,7,15206346,15206347, 1000000; \
  5,5,43562131,43562132, 1000000 \
];
for(row = 1, matsize(primitive_windows)[1], \
  install_orbit( \
    primitive_windows[row, 1], primitive_windows[row, 2], \
    positive_primitive_root( \
      primitive_windows[row, 3]/primitive_windows[row, 5], \
      primitive_windows[row, 4]/primitive_windows[row, 5]), \
    1));

\\ Five lower-conductor orbits: four reciprocal roots and the unit value.
install_orbit(0, 2, positive_lower_root(2005/1000, 2006/1000), 0);
install_orbit(0, 4, 1, 0);
install_orbit(0, 6, positive_lower_root(498/1000, 499/1000), 0);
install_orbit(2, 2, positive_lower_root(172/1000, 173/1000), 0);
install_orbit(4, 6, positive_lower_root(5795/1000, 5796/1000), 0);

assert_equal("INSTALLED_OVERLAP_COUNT", \
  sum(row = 1, 8, sum(column = 1, 8, \
    overlaps_F[row, column] != 0)), 64);

\\ Select the compatible degree-128 compositum with the standard zeta_16.
cyclotomic_polynomial = polcyclo(16);
zeta_symbol = Mod(x, cyclotomic_polynomial);
real_cyclotomic_polynomial = minpoly(zeta_symbol + 1/zeta_symbol);
real_inclusions = nfisincl(real_cyclotomic_polynomial, Fpol, 2);

select_F_element(inclusions, left, right) =
{
  my(matches = List(), element);
  for(index = 1, #inclusions,
    element = Mod(inclusions[index], Fpol);
    if(is_subset(ieval(lift(element), F_interval), [left, right]),
      listput(matches, element))
  );
  if(#matches != 1, error("real cyclotomic inclusion was not unique"));
  matches[1];
};

real_cyclotomic_F = select_F_element( \
  real_inclusions, 1847/1000, 1848/1000);
composita = polcompositum(Fpol, cyclotomic_polynomial, 1);
assert_equal("COMPOSITUM_COMPONENT_COUNT", #composita, 4);
selected_component = 0;
for(index = 1, #composita, \
  F_image = composita[index][2]; \
  zeta_image = composita[index][3]; \
  if(subst(lift(real_cyclotomic_F), x, F_image) \
      == zeta_image + 1/zeta_image, \
    if(selected_component, \
      error("multiple compatible compositum components")); \
    selected_component = index));
assert_equal("COMPATIBLE_COMPOSITUM_SELECTED", \
  selected_component > 0, 1);

Npol = composita[selected_component][1];
F_in_N = composita[selected_component][2];
zeta_16 = composita[selected_component][3];
assert_equal("COMMON_EXACT_FIELD_DEGREE", poldegree(Npol), 128);

embed_F(element) = subst(lift(element), x, F_in_N);
overlaps = matrix(8, 8, row, column, \
  embed_F(overlaps_F[row, column]));
tau = -zeta_16;
omega_8 = zeta_16^2;

ghost_matrix(determinant) =
{
  matrix(8, 8, row, column,
    my(first = (row - column) % 8, total = 0);
    my(transformed_second, wrap_sign);
    for(second = 0, 7,
      transformed_second = (determinant*second) % 8;
      wrap_sign = if(determinant == -1 && second != 0, \
        (-1)^first, 1);
      total += overlaps[first + 1, second + 1] \
        * wrap_sign \
        * tau^(first*transformed_second) \
        * omega_8^(transformed_second*(column - 1))
    );
    total/24
  );
};

audit_shift(label, determinant) =
{
  my(matrix_value = ghost_matrix(determinant));
  my(square = matrix_value*matrix_value);
  my(nonzero_idempotency_entries = 0, nonzero_minors = 0);
  my(minor_count = 0, minor);

  for(row = 1, 8, for(column = 1, 8,
    if(square[row, column] != matrix_value[row, column],
      nonzero_idempotency_entries++)));

  for(first_row = 1, 8, for(second_row = first_row + 1, 8,
    for(first_column = 1, 8,
      for(second_column = first_column + 1, 8,
        minor_count++;
        minor = \
          matrix_value[first_row, first_column] \
          * matrix_value[second_row, second_column] \
          - matrix_value[first_row, second_column] \
          * matrix_value[second_row, first_column];
        if(minor != 0, nonzero_minors++)
      )
    )
  ));

  print(label, "_TRACE_IS_ONE=", trace(matrix_value) == 1);
  print(label, "_NONZERO_IDEMPOTENCY_ENTRIES=", \
    nonzero_idempotency_entries);
  print(label, "_MINOR_COUNT=", minor_count);
  print(label, "_NONZERO_MINORS=", nonzero_minors);
  assert_equal(Str(label, "_TRACE_CERTIFIED"), \
    trace(matrix_value) == 1, 1);
  assert_equal(Str(label, "_NONZERO_IDEMPOTENCY_RESIDUAL_COUNT"), \
    nonzero_idempotency_entries, 0);
  assert_equal(Str(label, "_NONZERO_MINOR_COUNT"), nonzero_minors, 0);
  print(label, "_IDEMPOTENCY_CERTIFIED=1");
  print(label, "_RANK_ONE_CERTIFIED=1");
};

audit_shift("SHIFT_1", 1);
audit_shift("SHIFT_0", -1);
print("DIMENSION_EIGHT_EXACT_FINITE_TCC_CERTIFIED=1");

quit();
