\\ Exact dimension-five minor reduction in the Stark conjugate field.

print("PARI_VERSION=", version());

Fdata = polcompositum(polcyclo(5,y), y^2 - 6, 1)[1];
Fpol = Fdata[1];
zz = Fdata[2];
sqrt_six = Fdata[3];
F = nfinit(Fpol);

Q = (x^32 - 16*x^30 + 95*x^28 - 260*x^26 + 355*x^24 \
    - 348*x^22 + 388*x^20 - 300*x^18 + 195*x^16 \
    - 300*x^14 + 388*x^12 - 348*x^10 + 355*x^8 \
    - 260*x^6 + 95*x^4 - 16*x^2 + 1);

conjugates = nfgaloisconj(nfinit(Q));
factors = nffactor(F, Q)[,1];

audit_factor(factor_index) =
{
    my(factor, alpha, x_value, x_inverse, y_value, y_inverse);
    my(z_value, z_inverse, w_value, w_inverse, overlap_table);
    my(ghost_matrix, row, minor, nonzero_minors = 0);

    factor = factors[factor_index];
    alpha = Mod(x, factor);

    \\ Numerical root isolation labels alpha as w in the fourth factor.
    x_value = subst(lift(conjugates[10]), x, alpha);
    x_inverse = subst(lift(conjugates[6]), x, alpha);
    y_value = subst(lift(conjugates[5]), x, alpha);
    y_inverse = subst(lift(conjugates[4]), x, alpha);
    z_value = subst(lift(conjugates[16]), x, alpha);
    z_inverse = subst(lift(conjugates[12]), x, alpha);
    w_value = alpha;
    w_inverse = subst(lift(conjugates[8]), x, alpha);

    overlap_table = [sqrt_six,x_value,y_value,y_inverse,x_inverse; x_inverse,-z_inverse,w_inverse,-z_inverse,x_value; y_inverse,w_inverse,w_inverse,y_value,-z_value; y_value,-z_inverse,y_inverse,w_value,w_value; x_value,x_inverse,-z_value,w_value,-z_value];

    ghost_matrix = matrix(5,5);
    for (first = 0, 4,
        for (second = 0, 4,
            for (column = 0, 4,
                row = (column + first) % 5;
                ghost_matrix[row+1,column+1] +=
                    overlap_table[first+1,second+1]
                    * (zz^3)^(first*second) * zz^(second*column)
            )
        )
    );

    for (first_row = 1, 4,
        for (second_row = first_row+1, 5,
            for (first_column = 1, 4,
                for (second_column = first_column+1, 5,
                    minor = ghost_matrix[first_row,first_column]
                        * ghost_matrix[second_row,second_column]
                        - ghost_matrix[first_row,second_column]
                        * ghost_matrix[second_row,first_column];
                    if (minor != 0, nonzero_minors++)
                )
            )
        )
    );
    return(nonzero_minors);
};

print("COEFFICIENT_FIELD_POLYNOMIAL=", Fpol);
print("ABSOLUTE_STARK_SQUARE_ROOT_POLYNOMIAL=", Q);
print("FACTOR_COUNT_OVER_COEFFICIENT_FIELD=", #factors);
print("SELECTED_FACTOR_CERTIFICATE=dimension-five-embedding-certificate.txt");
for (factor_index = 1, #factors, print("FACTOR_",factor_index,"_NONZERO_MINOR_COUNT=",audit_factor(factor_index)));

quit();
