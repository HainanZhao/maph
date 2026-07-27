\\ Exact dimension-six minor reduction in the Artin-labeled overlap field.
\\
\\ The primitive polynomial already includes the AFK signs: at the
\\ interval-defined root x its six K-conjugates are
\\   x, -w^-1, -w, x^-1, -z^-1, -z.
\\ We extend by Q(zeta_12,sqrt(7)), recover all eight possible lower
\\ roots y, and let the 225 minors select the compatible root exactly.

default(realprecision, 80);
default(parisizemax, 4000000000);
print("PARI_VERSION=", version());

\\ Weyl coefficient field F = Q(zeta_12,sqrt(7)).
Fdata = polcompositum(polcyclo(12, y), y^2 - 7, 1)[1];
Fpol = Fdata[1];
zeta_twelve_in_F = Fdata[2];
sqrt_seven_in_F = Fdata[3];
F = nfinit(Fpol);

primitive_polynomial = \
  x^12 + 3*x^11 - 6*x^10 - 16*x^9 + 3*x^8 + 27*x^6 \
  + 3*x^4 - 16*x^3 - 6*x^2 + 3*x + 1;
primitive_field = nfinit(primitive_polynomial);
primitive_conjugates = nfgaloisconj(primitive_field);

\\ The second factor is the beta=(5+sqrt(21))/2 factor. Its x^5
\\ coefficient is beta-1=(3+sqrt(21))/2.
relative_factors = nffactor(F, primitive_polynomial)[, 1];
selected_factor = relative_factors[2];

\\ Flatten F(alpha) to one absolute field so that nfroots can recover y.
flattened = rnfequation(F, selected_factor, 1);
Lpol = flattened[1];
F_generator_in_L = Mod(lift(flattened[2]), Lpol);
flattening_shift = flattened[3];
L = nfinit(Lpol);
L_generator = Mod(variable(Lpol), Lpol);
alpha = L_generator - flattening_shift*F_generator_in_L;

embed_F(element) = \
  Mod(subst(lift(element), y, lift(F_generator_in_L)), Lpol);

zeta_twelve = embed_F(zeta_twelve_in_F);
sqrt_seven = embed_F(sqrt_seven_in_F);
omega_six = zeta_twelve^2;
tau = zeta_twelve^7;
sqrt_twenty_one = (zeta_twelve + zeta_twelve^-1)*sqrt_seven;
beta = (5 + sqrt_twenty_one)/2;
if(embed_F(polcoef(selected_factor, 5)) != beta-1, \
  error("selected factor does not have x^5 coefficient beta-1"));

\\ Exact primitive labels, certified separately by rational intervals.
x_value = alpha;
x_inverse = subst(primitive_conjugates[4], x, alpha);
w_inverse = -subst(primitive_conjugates[2], x, alpha);
w_value = -subst(primitive_conjugates[3], x, alpha);
z_inverse = -subst(primitive_conjugates[5], x, alpha);
z_value = -subst(primitive_conjugates[6], x, alpha);
if(x_value*x_inverse != 1, error("x reciprocal label failed"));
if(z_value*z_inverse != 1, error("z reciprocal label failed"));
if(w_value*w_inverse != 1, error("w reciprocal label failed"));

\\ The eight roots comprise y, y^-1, their negatives, and the four
\\ nonreal conjugates over the other real embedding of K.
lower_variable = varhigher("lower_variable", variable(Lpol));
lower_polynomial = Polrev( \
  [1, 0, -1, 0, -3, 0, -1, 0, 1], lower_variable);
lower_roots = nfroots(L, lower_polynomial);
if(#primitive_conjugates != 6, error("expected six K-conjugates"));
if(#relative_factors != 2, error("expected two coefficient-field factors"));
if(#lower_roots != 8, error("expected eight lower roots"));

audit_lower_root(lower_value) =
{
  my(table, ghost_matrix, row, minor, nonzero_minors = 0);
  table = [
    sqrt_seven, -x_value, lower_value, -1, \
      lower_value^-1, -x_inverse;
    -x_inverse, -lower_value^-2, -z_value, -w_value, \
      -lower_value^-2, -x_value;
    lower_value^-1, -w_value, lower_value^-3, -z_value, \
      lower_value, lower_value^2;
    -1, -z_value, -w_value, -1, w_inverse, -z_inverse;
    lower_value, -lower_value^-2, lower_value^-1, z_inverse, \
      lower_value^3, w_inverse;
    -x_value, -x_inverse, lower_value^2, -w_inverse, \
      z_inverse, -lower_value^2
  ];

  ghost_matrix = matrix(6, 6);
  for(first = 0, 5,
    for(second = 0, 5,
      for(column = 0, 5,
        row = (column + first) % 6;
        ghost_matrix[row+1, column+1] += \
          table[first+1, second+1] \
          * tau^(first*second) * omega_six^(second*column)
      )
    )
  );

  for(first_row = 1, 5,
    for(second_row = first_row+1, 6,
      for(first_column = 1, 5,
        for(second_column = first_column+1, 6,
          minor = ghost_matrix[first_row, first_column] \
            * ghost_matrix[second_row, second_column] \
            - ghost_matrix[first_row, second_column] \
            * ghost_matrix[second_row, first_column];
          if(minor != 0, nonzero_minors++)
        )
      )
    )
  );
  return(nonzero_minors);
};

print("COEFFICIENT_FIELD_POLYNOMIAL=", Fpol);
print("PRIMITIVE_OVERLAP_POLYNOMIAL=", primitive_polynomial);
print("PRIMITIVE_CONJUGATE_COUNT=", #primitive_conjugates);
print("FACTOR_COUNT_OVER_COEFFICIENT_FIELD=", #relative_factors);
print("SELECTED_FACTOR_DEGREE=", poldegree(selected_factor));
print("SELECTED_FACTOR_X5_COEFFICIENT=beta-1");
print("ABSOLUTE_COMPOSITUM_DEGREE=", poldegree(Lpol));
print("LOWER_ROOT_COUNT_IN_COMPOSITUM=", #lower_roots);
print("TWO_BY_TWO_MINOR_COUNT=", binomial(6, 2)^2);
minor_counts = vector(#lower_roots, root_index, \
  audit_lower_root(lower_roots[root_index]));
expected_minor_counts = [201, 224, 225, 225, 225, 225, 225, 0];
if(minor_counts != expected_minor_counts, \
  error(Str("unexpected minor counts: ", minor_counts)));
for(root_index = 1, #lower_roots, \
  print("LOWER_ROOT_", root_index, "_NONZERO_MINOR_COUNT=", \
    minor_counts[root_index]));

quit();
