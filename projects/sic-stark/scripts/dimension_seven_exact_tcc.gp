\\ Exact finite TCC certificate for the canonical dimension-seven packet.
\\
\\ The twelve nonquadratic signed overlaps are the real roots of Hpol.
\\ The remaining four signed overlaps lie in two quartic subfields of H.
\\ Composing H with Q(zeta_56) gives a degree-48 field containing every
\\ overlap, Weyl phase, and normalization.  Both shifted ghost matrices are
\\ then checked by exact arithmetic in that single field.

default(parisizemax, 4000000000);
default(realprecision, 80);

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

Hpol = x^24 - 8*x^23 + 6*x^22 + 100*x^21 - 336*x^20 \
  + 264*x^19 + 834*x^18 - 2980*x^17 + 5038*x^16 - 5748*x^15 \
  + 5084*x^14 - 4060*x^13 + 3611*x^12 - 4060*x^11 \
  + 5084*x^10 - 5748*x^9 + 5038*x^8 - 2980*x^7 + 834*x^6 \
  + 264*x^5 - 336*x^4 + 100*x^3 + 6*x^2 - 8*x + 1;

plus_polynomial = x^4 - 2*x^3 - 5*x^2 - 2*x + 1;
minus_polynomial = x^4 - 4*x^3 + 4*x^2 - 4*x + 1;
cyclotomic_polynomial = polcyclo(56);

H = nfinit(Hpol);
H_generator = Mod(x, Hpol);
generator_interval = [ \
  24298120154607662818424148631780884972067133872553900249933286935412960 \
    / 10^70, \
  24298120154607662818424148631780884972067133872553900249933286935412961 \
    / 10^70 \
];
assert_equal("DISTINGUISHED_H_ROOT_COUNT", \
  polsturm(Hpol, generator_interval), 1);

\\ The H/K automorphisms give exactly the twelve signed, nonquadratic
\\ overlap values.  Select them by disjoint rational intervals rather than
\\ by an undocumented automorphism ordering.
H_conjugates = nfgaloisconj(H);
assert_equal("H_OVER_K_AUTOMORPHISM_COUNT", #H_conjugates, 12);

select_H_conjugate(left, right) =
{
  my(matches = List(), element, image_interval);
  if(polsturm(Hpol, [left, right]) != 1,
    error(Str("target H-root count is not one: ", [left, right])));
  for(index = 1, #H_conjugates,
    element = Mod(H_conjugates[index], Hpol);
    image_interval = ieval(lift(element), generator_interval);
    if(is_subset(image_interval, [left, right]),
      listput(matches, element)));
  if(#matches != 1,
    error(Str("H root interval has ", #matches, " matches: ", [left, right])));
  matches[1];
};

plus_inclusions = nfisincl(plus_polynomial, Hpol, 2);
minus_inclusions = nfisincl(minus_polynomial, Hpol, 2);
assert_equal("PLUS_SUBFIELD_INCLUSION_COUNT", #plus_inclusions, 2);
assert_equal("MINUS_SUBFIELD_INCLUSION_COUNT", #minus_inclusions, 2);

select_subfield_root(inclusions, left, right) =
{
  my(matches = List(), element, image_interval);
  for(index = 1, #inclusions,
    element = Mod(inclusions[index], Hpol);
    image_interval = ieval(lift(element), generator_interval);
    if(is_subset(image_interval, [left, right]),
      listput(matches, element)));
  if(#matches != 1,
    error(Str("subfield interval has ", #matches, " matches: ", [left, right])));
  matches[1];
};

sqrt_two_inclusions = nfisincl(x^2 - 2, Hpol, 2);
sqrt_two_H = select_subfield_root( \
  sqrt_two_inclusions, 14/10, 15/10 \
);

\\ One of the twelve possible composita identifies the common degree-12
\\ intersection in the convention required by the distinguished real
\\ embedding of H and the standard primitive 56th root.  Select it without
\\ floating-point roots: isolate the inclusion of
\\ Q(zeta_56 + zeta_56^-1) whose generator is 2*cos(2*Pi/56), then require
\\ its two exact images in the compositum to agree.
cyclotomic_generator = Mod(x, cyclotomic_polynomial);
real_cyclotomic_polynomial = minpoly( \
  cyclotomic_generator + 1/cyclotomic_generator \
);
assert_equal("REAL_CYCLOTOMIC_DEGREE", \
  poldegree(real_cyclotomic_polynomial), 12);
assert_equal("STANDARD_REAL_CYCLOTOMIC_ROOT_COUNT", \
  polsturm(real_cyclotomic_polynomial, [198/100, 199/100]), 1);
real_cyclotomic_inclusions = nfisincl( \
  real_cyclotomic_polynomial, Hpol, 2 \
);
real_cyclotomic_H = select_subfield_root( \
  real_cyclotomic_inclusions, 198/100, 199/100 \
);

composita = polcompositum(Hpol, cyclotomic_polynomial, 1);
assert_equal("COMPOSITUM_COMPONENT_COUNT", #composita, 12);
selected_component = 0;

locate_component(index) =
{
  my(H_image = composita[index][2]);
  my(zeta_image = composita[index][3]);
  my(real_cyclotomic_from_H =
    subst(lift(real_cyclotomic_H), x, H_image));
  if(real_cyclotomic_from_H == zeta_image + 1/zeta_image,
    if(selected_component,
      error("more than one compositum component matches the intersection"));
    selected_component = index);
};

for(index = 1, #composita, locate_component(index));
assert_equal("SELECTED_COMPOSITUM_COMPONENT", selected_component > 0, 1);
print("SELECTED_COMPOSITUM_COMPONENT_INDEX=", selected_component);
assert_equal("COMPOSITUM_ABSOLUTE_DEGREE", \
  poldegree(composita[selected_component][1]), 48);

Npol = composita[selected_component][1];
H_in_N = composita[selected_component][2];
zeta_56 = composita[selected_component][3];

embed_H(element) =
{
  subst(lift(element), x, H_in_N);
};

sqrt_two = embed_H(sqrt_two_H);
sqrt_eight = 2*sqrt_two;
tau = zeta_56^32;
omega_7 = zeta_56^8;

assert_equal("SQRT_TWO_SQUARE", sqrt_two^2 == 2, 1);
assert_equal("ZETA_56_ORDER_CHECK", zeta_56^28 == -1, 1);
assert_equal("REAL_CYCLOTOMIC_INTERSECTION_CERTIFIED", \
  embed_H(real_cyclotomic_H) == zeta_56 + 1/zeta_56, 1);
assert_equal("POSITIVE_SQRT_TWO_CYCLOTOMIC_COMPATIBILITY", \
  sqrt_two == zeta_56^7 + zeta_56^(-7), 1);

\\ Sixteen Zauner-orbit representatives.  Values are exact H-elements;
\\ their intervals also fix every sign.
make_representatives() =
{
  [
    0, 1, select_H_conjugate(2429/1000, 2430/1000);
    0, 2, select_H_conjugate(1781/1000, 1782/1000);
    0, 3, select_H_conjugate(1220/1000, 1221/1000);
    0, 4, select_H_conjugate(819/1000, 820/1000);
    0, 5, select_H_conjugate(561/1000, 562/1000);
    0, 6, select_H_conjugate(411/1000, 412/1000);
    1, 1, select_H_conjugate(-383/1000, -382/1000);
    1, 2, select_subfield_root(minus_inclusions, 323/1000, 324/1000);
    1, 3, select_H_conjugate(-284/1000, -283/1000);
    1, 4, select_subfield_root(plus_inclusions, 281/1000, 282/1000);
    2, 2, select_H_conjugate(208/1000, 209/1000);
    2, 6, select_H_conjugate(-2614/1000, -2613/1000);
    3, 5, select_subfield_root(plus_inclusions, 3546/1000, 3547/1000);
    3, 6, select_subfield_root(minus_inclusions, 3090/1000, 3091/1000);
    4, 4, select_H_conjugate(-3533/1000, -3532/1000);
    4, 5, select_H_conjugate(4793/1000, 4794/1000)
  ];
};

representatives = make_representatives();

overlaps_H = matrix(7, 7);
overlaps_H[1, 1] = 2*sqrt_two_H;

install_orbit(first, second, value) =
{
  my(current_first = first, current_second = second, next_first);
  for(step = 1, 3,
    overlaps_H[current_first + 1, current_second + 1] = value;
    next_first = (-current_first - current_second) % 7;
    current_second = current_first;
    current_first = next_first);
};

for(index = 1, matsize(representatives)[1], \
  install_orbit(representatives[index, 1], \
    representatives[index, 2], representatives[index, 3]));

installed_nonzero = sum(row = 1, 7, sum(column = 1, 7, \
  overlaps_H[row, column] != 0)) - 1;
assert_equal("INSTALLED_NONZERO_OVERLAPS", installed_nonzero, 48);

overlaps = matrix(7, 7, row, column, \
  embed_H(overlaps_H[row, column]));

ghost_matrix(determinant) =
{
  matrix(7, 7, row, column,
    my(first = (row - column) % 7, total = 0, transformed_second);
    for(second = 0, 6,
      transformed_second = (determinant*second) % 7;
      total += overlaps[first + 1, second + 1]
        * tau^(first*transformed_second)
        * omega_7^(transformed_second*(column - 1)));
    total/(7*sqrt_eight)
  );
};

audit_shift(label, determinant) =
{
  my(matrix_value = ghost_matrix(determinant));
  my(square = matrix_value*matrix_value);
  my(nonzero_idempotency_entries = 0, nonzero_minors = 0);
  my(minor_count = 0, minor);

  for(row = 1, 7, for(column = 1, 7,
    if(square[row, column] != matrix_value[row, column],
      nonzero_idempotency_entries++)));

  for(first_row = 1, 7, for(second_row = first_row + 1, 7,
    for(first_column = 1, 7,
      for(second_column = first_column + 1, 7,
        minor_count++;
        minor =
          matrix_value[first_row, first_column]
          * matrix_value[second_row, second_column]
          - matrix_value[first_row, second_column]
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
  assert_equal(Str(label, "_IDEMPOTENCY_CERTIFIED"), \
    nonzero_idempotency_entries == 0, 1);
  assert_equal(Str(label, "_RANK_ONE_CERTIFIED"), nonzero_minors == 0, 1);
};

audit_shift("SHIFT_1", 1);
audit_shift("SHIFT_0", -1);

quit();
