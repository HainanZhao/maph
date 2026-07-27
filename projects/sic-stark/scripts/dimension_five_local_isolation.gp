\\ Exact local-isolation certificate for the dimension-five rank-one point.
\\ The first four fan minors have an invertible Jacobian with respect to
\\ (x,y,z,w) at the certified factor-four packet.

print("PARI_VERSION=", version());

Fdata = polcompositum(polcyclo(5, y), y^2 - 6, 1)[1];
F = nfinit(Fdata[1]);
zeta_five = Fdata[2];
sqrt_six = Fdata[3];

Q = x^32 - 16*x^30 + 95*x^28 - 260*x^26 + 355*x^24 \
    - 348*x^22 + 388*x^20 - 300*x^18 + 195*x^16 \
    - 300*x^14 + 388*x^12 - 348*x^10 + 355*x^8 \
    - 260*x^6 + 95*x^4 - 16*x^2 + 1;

conjugates = nfgaloisconj(nfinit(Q));
factor_four = nffactor(F, Q)[, 1][4];
alpha = Mod(x, factor_four);

x_value = subst(conjugates[10], x, alpha);
y_value = subst(conjugates[5], x, alpha);
z_value = subst(conjugates[16], x, alpha);
w_value = alpha;

u = 'u;
v = 'v;
r = 'r;
s = 's;

overlap_table = [sqrt_six,u,v,1/v,1/u; 1/u,-1/r,1/s,-1/r,u; 1/v,1/s,1/s,v,-r; v,-1/r,1/v,s,s; u,1/u,-r,s,-r];

build_ghost_matrix() =
{
    my(result = matrix(5, 5), row);
    for(
        first = 0, 4,
        for(
            second = 0, 4,
            for(
                column = 0, 4,
                row = (column + first) % 5;
                result[row+1, column+1] += overlap_table[first+1, second+1] * (zeta_five^3)^(first*second) * zeta_five^(second*column)
            )
        )
    );
    return(result);
};
ghost_matrix = build_ghost_matrix();

\\ Rows (0,1), with the four column pairs (0,j), 1 <= j <= 4.
fan_minors = vector(4, j, ghost_matrix[1,1] * ghost_matrix[2,j+1] - ghost_matrix[1,j+1] * ghost_matrix[2,1]);
vars = [u, v, r, s];
jacobian = matrix(4, 4, first, second, deriv(fan_minors[first], vars[second]));

evaluate_at_packet(expression) = subst(subst(subst(subst(expression, u, x_value), v, y_value), r, z_value), s, w_value);

evaluated_minors = vector(4, index, evaluate_at_packet(fan_minors[index]));
evaluated_jacobian = matrix(4, 4, first, second, evaluate_at_packet(jacobian[first, second]));
jacobian_determinant = matdet(evaluated_jacobian);
all_fan_minors_zero = evaluated_minors == [0, 0, 0, 0];
jacobian_determinant_zero = jacobian_determinant == 0;
local_point_reduced_and_isolated = all_fan_minors_zero && !jacobian_determinant_zero;

print("FAN_MINOR_LABELS=[((0,1),(0,1)),((0,1),(0,2)),((0,1),(0,3)),((0,1),(0,4))]");
print("ALL_FOUR_FAN_MINORS_ZERO=", all_fan_minors_zero);
print("FAN_JACOBIAN_DETERMINANT_ZERO=", jacobian_determinant_zero);
print("LOCAL_POINT_REDUCED_AND_ISOLATED=", local_point_reduced_and_isolated);

quit();
