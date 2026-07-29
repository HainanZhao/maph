\\ Exact finite TCC certificate for the missing maximal-order d=7 tuple.
\\
\\ The six nonquadratic signed overlaps are isolated roots of Gpol; the
\\ remaining nontrivial pair lies in a quartic subfield of the already
\\ certified ray-14 field H.  Composing H with Q(zeta_56) gives the same
\\ degree-48 exact arithmetic arena used by the conductor-two proof.

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

Gpol = x^12 + 4*x^11 - 2*x^10 - 22*x^9 - 18*x^8 + 16*x^7 \
  + 41*x^6 + 16*x^5 - 18*x^4 - 22*x^3 - 2*x^2 + 4*x + 1;
quartic_polynomial = x^4 + 2*x^3 + x^2 + 2*x + 1;
cyclotomic_polynomial = polcyclo(56);

\\ The signed packet polynomials are forced by the already certified
\\ squared Stark-unit polynomials; they are not numerical guesses.
scalar_square_relative = x^6 + (-10 - 6*y)*x^5 \
  + (58 + 40*y)*x^4 + (-129 - 90*y)*x^3 \
  + (58 + 40*y)*x^2 + (-10 - 6*y)*x + 1;
scalar_signed_absolute = rnfequation( \
  y^2 - 2, subst(scalar_square_relative, x, x^2));
quartic_square_absolute = x^4 - 2*x^3 - 5*x^2 - 2*x + 1;
assert_equal("SIGNED_SCALAR_DIVIDES_ABSOLUTE_EQUATION", \
  divrem(scalar_signed_absolute, Gpol)[2], 0);
assert_equal("SIGNED_SCALAR_CONJUGATE_DIVIDES_ABSOLUTE_EQUATION", \
  divrem(scalar_signed_absolute, subst(Gpol, x, -x))[2], 0);
assert_equal("SIGNED_SCALAR_ABSOLUTE_FACTORIZATION", \
  Gpol*subst(Gpol, x, -x), scalar_signed_absolute);
assert_equal("QUARTIC_SIGNED_FACTORIZATION", \
  subst(quartic_square_absolute, x, x^2), \
  quartic_polynomial*subst(quartic_polynomial, x, -x));

assert_equal("SIGNED_SCALAR_PACKET_DEGREE", poldegree(Gpol), 12);
assert_equal("SIGNED_SCALAR_PACKET_IRREDUCIBLE", polisirreducible(Gpol), 1);
assert_equal("QUARTIC_PACKET_IRREDUCIBLE", \
  polisirreducible(quartic_polynomial), 1);
assert_equal("SIGNED_SCALAR_REAL_ROOT_COUNT", polsturm(Gpol), 6);
assert_equal("QUARTIC_REAL_ROOT_COUNT", polsturm(quartic_polynomial), 2);

H = nfinit(Hpol);
generator_interval = [ \
  24298120154607662818424148631780884972067133872553900249933286935412960 \
    / 10^70, \
  24298120154607662818424148631780884972067133872553900249933286935412961 \
    / 10^70 \
];
assert_equal("DISTINGUISHED_H_ROOT_COUNT", \
  polsturm(Hpol, generator_interval), 1);

select_subfield_root(inclusions, polynomial, left, right) =
{
  my(matches = List(), element, image_interval);
  assert_equal("TARGET_ROOT_COUNT", polsturm(polynomial, [left, right]), 1);
  for(index = 1, #inclusions,
    element = Mod(inclusions[index], Hpol);
    image_interval = ieval(lift(element), generator_interval);
    if(is_subset(image_interval, [left, right]),
      listput(matches, element)));
  if(#matches != 1,
    error(Str("subfield interval has ", #matches, " matches: ", \
      [left, right])));
  matches[1];
};

G_inclusions = nfisincl(Gpol, Hpol, 2);
quartic_inclusions = nfisincl(quartic_polynomial, Hpol, 2);
sqrt_two_inclusions = nfisincl(x^2 - 2, Hpol, 2);
assert_equal("SIGNED_SCALAR_INCLUSION_COUNT", #G_inclusions, 6);
assert_equal("QUARTIC_INCLUSION_COUNT", #quartic_inclusions, 2);

sqrt_two_H = select_subfield_root( \
  sqrt_two_inclusions, x^2 - 2, 14/10, 15/10 \
);

\\ Match the common real cyclotomic subfield exactly, fixing the
\\ compositum component and the positive square-root convention.
cyclotomic_generator = Mod(x, cyclotomic_polynomial);
real_cyclotomic_polynomial = minpoly( \
  cyclotomic_generator + 1/cyclotomic_generator \
);
real_cyclotomic_inclusions = nfisincl( \
  real_cyclotomic_polynomial, Hpol, 2 \
);
real_cyclotomic_H = select_subfield_root( \
  real_cyclotomic_inclusions, \
  real_cyclotomic_polynomial, \
  198/100, \
  199/100 \
);

composita = polcompositum(Hpol, cyclotomic_polynomial, 1);
selected_component = 0;
locate_component(index) =
{
  my(H_image = composita[index][2]);
  my(zeta_image = composita[index][3]);
  my(real_from_H = subst(lift(real_cyclotomic_H), x, H_image));
  if(real_from_H == zeta_image + 1/zeta_image,
    if(selected_component,
      error("multiple compositum components match the intersection"));
    selected_component = index);
};
for(index = 1, #composita, locate_component(index));
assert_equal("SELECTED_COMPOSITUM_COMPONENT", selected_component > 0, 1);
assert_equal("COMPOSITUM_ABSOLUTE_DEGREE", \
  poldegree(composita[selected_component][1]), 48);

H_in_N = composita[selected_component][2];
zeta_56 = composita[selected_component][3];
embed_H(element) = subst(lift(element), x, H_in_N);

sqrt_two = embed_H(sqrt_two_H);
sqrt_eight = 2*sqrt_two;
tau = zeta_56^32;
omega_7 = zeta_56^8;
assert_equal("SQRT_TWO_SQUARE", sqrt_two^2 == 2, 1);
assert_equal("ZETA_56_ORDER_CHECK", zeta_56^28 == -1, 1);
assert_equal("POSITIVE_SQRT_TWO_CYCLOTOMIC_COMPATIBILITY", \
  sqrt_two == zeta_56^7 + zeta_56^(-7), 1);

scalar_root(left, right) =
  select_subfield_root(G_inclusions, Gpol, left, right);
quartic_root(left, right) =
  select_subfield_root( \
    quartic_inclusions, quartic_polynomial, left, right \
  );

\\ One representative for each of the sixteen nonzero Zauner orbits.
\\ The interval is part of the exact root label, not a floating-point
\\ definition of the value.
representatives = [ \
  0, 1, scalar_root(-2739/1000, -2738/1000); \
  0, 2, scalar_root(-405/1000, -404/1000); \
  0, 3, scalar_root(2086/1000, 2087/1000); \
  0, 4, scalar_root(479/1000, 480/1000); \
  0, 5, scalar_root(-2472/1000, -2471/1000); \
  0, 6, scalar_root(-366/1000, -365/1000); \
  1, 1, scalar_root(-405/1000, -404/1000); \
  1, 3, quartic_root(-1884/1000, -1883/1000); \
  1, 4, scalar_root(2086/1000, 2087/1000); \
  1, 6, -1; \
  2, 1, scalar_root(-366/1000, -365/1000); \
  2, 2, scalar_root(479/1000, 480/1000); \
  3, 2, quartic_root(-532/1000, -531/1000); \
  3, 4, -1; \
  4, 2, scalar_root(-2472/1000, -2471/1000); \
  4, 4, scalar_root(-2739/1000, -2738/1000) \
];

overlaps_H = matrix(7, 7);
overlaps_H[1, 1] = 2*sqrt_two_H;

install_orbit(first, second, value) =
{
  my(current_first = first, current_second = second);
  my(next_first, next_second);
  for(step = 1, 3,
    if(overlaps_H[current_first + 1, current_second + 1] != 0,
      error(Str("duplicate orbit installation at ", \
        [current_first, current_second])));
    overlaps_H[current_first + 1, current_second + 1] = value;
    next_first = (3*current_second) % 7;
    next_second = (2*current_first - current_second) % 7;
    current_first = next_first;
    current_second = next_second
  );
};

for(index = 1, matsize(representatives)[1], \
  install_orbit( \
    representatives[index, 1], \
    representatives[index, 2], \
    representatives[index, 3]));

installed_nonzero = sum(row = 1, 7, sum(column = 1, 7, \
  overlaps_H[row, column] != 0)) - 1;
assert_equal("INSTALLED_NONZERO_OVERLAPS", installed_nonzero, 48);

overlaps = matrix(7, 7, row, column, \
  embed_H(overlaps_H[row, column]));

ghost_matrix(determinant) =
{
  matrix(7, 7, row, column,
    my(first = (row - column) % 7, total = 0);
    my(transformed_second);
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
  assert_equal(Str(label, "_RANK_ONE_CERTIFIED"), \
    nonzero_minors == 0, 1);
};

audit_shift("SHIFT_1", 1);
audit_shift("SHIFT_0", -1);
print("DIMENSION_SEVEN_DISCRIMINANT_EIGHT_EXACT_TCC_CERTIFIED=1");

quit();
