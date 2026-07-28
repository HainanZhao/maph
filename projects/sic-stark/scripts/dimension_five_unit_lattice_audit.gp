\\ Exact unit-lattice data for the proposed dimension-five Stark unit.
\\ This is the arithmetic half of a possible Shintani-power proof:
\\ once a certified analytic logarithm vector is available, membership
\\ in this lattice can identify the special value without assuming Stark.

default(realprecision, 100);

iadd(A, B) = [A[1] + B[1], A[2] + B[2]];
imul(A, B) =
{
    my(values = [
        A[1] * B[1], A[1] * B[2],
        A[2] * B[1], A[2] * B[2]
    ]);
    [vecmin(values), vecmax(values)]
};
ieval(P, interval) =
{
    my(value = [0, 0]);
    forstep(
        degree = poldegree(P), 0, -1,
        value = iadd(
            imul(value, interval),
            [polcoef(P, degree), polcoef(P, degree)]
        )
    );
    value
};
is_subset(inner, outer) =
    inner[1] >= outer[1] && inner[2] <= outer[2];

Kpol = y^2 - 4*y + 1;
K = bnfinit(Kpol, 1);
beta = Mod(y, Kpol);
s = beta - 2;

P = x^8 - (8 + 5*s)*x^7 + (53 + 30*s)*x^6 \
    - (156 + 90*s)*x^5 + (225 + 130*s)*x^4 \
    - (156 + 90*s)*x^3 + (53 + 30*s)*x^2 \
    - (8 + 5*s)*x + 1;

absolute_data = rnfequation(Kpol, P, 1);
absolute_polynomial = absolute_data[1];
base_generator = Mod(absolute_data[2], absolute_polynomial);
primitive_generator = Mod(x, absolute_polynomial);
U = primitive_generator - absolute_data[3]*base_generator;

H = bnfinit(absolute_polynomial, 1);

\\ Construct the ray field with the same labeled base embedding.
\\ The eight absolute isomorphisms are all K-compatible; this is
\\ stronger than an unlabeled nfisisom check.
Rone = bnrinit(K, [5, [1, 0]], 1);
ray_relative_polynomial = bnrclassfield(Rone, , 1);
ray_absolute_data = rnfequation(Kpol, ray_relative_polynomial, 1);
ray_absolute_polynomial = ray_absolute_data[1];
ray_base_generator = Mod(ray_absolute_data[2], ray_absolute_polynomial);
candidate_to_ray_isomorphisms = nfisisom(absolute_polynomial, ray_absolute_polynomial);
audit_k_isomorphisms() =
{
    my(count = 0, mapped_base_generator);
    for(k = 1, #candidate_to_ray_isomorphisms,
        mapped_base_generator = subst(
            lift(base_generator),
            x,
            Mod(candidate_to_ray_isomorphisms[k], ray_absolute_polynomial)
        );
        if(mapped_base_generator == ray_base_generator, count++)
    );
    count
};
k_compatible_isomorphism_count = audit_k_isomorphisms();

print("PARI_VERSION=", version());
print("ABSOLUTE_POLYNOMIAL=", absolute_polynomial);
print("ABSOLUTE_SIGNATURE=", H.sign);
print("ABSOLUTE_DISCRIMINANT=", H.disc);
print("ABSOLUTE_CLASS_NUMBER=", H.no);
print("ABSOLUTE_BNFCERTIFY=", bnfcertify(H));
print("BASE_GENERATOR=", base_generator);
print("POSITIVE_SQRT_THREE=", base_generator - 2);
print("STARK_UNIT=", U);
P_in_absolute_field = subst(lift(P), y, base_generator);
print("STARK_UNIT_MINPOLY_CHECK=", subst(P_in_absolute_field, x, U) == 0);
print("STARK_UNIT_NORM=", nfeltnorm(H, U));
print("CANDIDATE_TO_RAY_ISOMORPHISM_COUNT=", #candidate_to_ray_isomorphisms);
print("K_COMPATIBLE_ISOMORPHISM_COUNT=", k_compatible_isomorphism_count);
print("ALL_CANDIDATE_RAY_ISOMORPHISMS_FIX_LABELED_K=", k_compatible_isomorphism_count == #candidate_to_ray_isomorphisms);
Udecomposition = bnfisunit(H, U);
Uembeddings = nfeltembed(H, U);
print("STARK_UNIT_DECOMPOSITION=", Udecomposition);
print("STARK_UNIT_ARCHIMEDEAN_VALUES=", Uembeddings);

\\ Under the nonidentity embedding of Q(sqrt(3)), all four trace roots
\\ lie in (-2,2).  The substitution T=2(X^2-1)/(X^2+1) converts that
\\ interval assertion into an exact real-root count.
trace_polynomial = x^4 - (8 + 5*s)*x^3 + (49 + 30*s)*x^2 \
    - (132 + 75*s)*x + (121 + 70*s);
trace_interval_transform = (x^2 + 1)^4 * subst(trace_polynomial, x, 2*(x^2 - 1)/(x^2 + 1));
print("TRACE_INTERVAL_MINUS_2_2_ROOT_COUNTS_BY_BASE_EMBEDDING=", nfpolsturm(K, trace_interval_transform));

audit_unit_lattice() =
{
    my(unit_log_matrix, gram_matrix, gram_roots);
    my(smallest_singular_value, Rfourier, Lvalues, ray_logs);
    my(signed_ray_logs, ray_generator_logs, matched_logs, unused);
    my(target, best, best_error, candidate_error);
    my(analytic_power_log_vector, candidate_power_log_vector);
    my(ray_generator_prime, ray_generator_log, relative_mod_three);
    my(relative_mod_three_factorization, conjugates, frobenius_target);
    my(arithmetic_frobenius_index, inverse_frobenius_index);
    my(arithmetic_frobenius, inverse_frobenius, orbit_element);
    my(U_interval, orbit_target_intervals, orbit_image_interval);
    my(all_orbit_intervals_certified);
    unit_log_matrix = matrix(
        12,
        11,
        row,
        column,
        log(abs(nfeltembed(H, H.fu[column])[row]))
    );
    gram_matrix = unit_log_matrix~ * unit_log_matrix;
    gram_roots = polroots(charpoly(gram_matrix));
    smallest_singular_value = sqrt(vecmin(vector(
        #gram_roots,
        k,
        real(gram_roots[k])
    )));
    print("UNIT_LOG_LATTICE_SMALLEST_SINGULAR_VALUE=", smallest_singular_value);

    \\ Independently recompute the four differenced partial-zeta derivatives
    \\ by Fourier inversion of PARI's Hecke L-values.  Use a fresh bnr
    \\ object so later class-field routines cannot change its cyclic basis.
    Rfourier = bnrinit(K, [5, [1, 0]], 1);
    Lvalues = bnrL1(Rfourier, , 4);
    ray_logs = vector(
        4,
        c,
        real(vecsum(vector(
            #Lvalues,
            j,
            if(
                Lvalues[j][1][1] % 2,
                exp(-2*Pi*I*Lvalues[j][1][1]*(c-1)/8)
                    * Lvalues[j][2][2],
                0
            )
        )) / 4)
    );
    signed_ray_logs = concat(ray_logs, -ray_logs);
    matched_logs = vector(8);
    unused = vector(8, k, 1);
    for(row = 1, 8,
        target = log(abs(Uembeddings[row]));
        best = 0;
        best_error = 1e100;
        for(k = 1, 8,
            if(unused[k],
                candidate_error = abs(target - signed_ray_logs[k]);
                if(candidate_error < best_error,
                    best = k;
                    best_error = candidate_error
                )
            )
        );
        matched_logs[row] = signed_ray_logs[best];
        unused[best] = 0
    );
    analytic_power_log_vector = Col(concat(5760*matched_logs, vector(4)));
    candidate_power_log_vector = unit_log_matrix * (5760*Udecomposition[1..11]);
    print("SHINTANI_SAFE_EXPONENT=5760");
    print("FOURIER_INVERTED_RAY_LOGS=", ray_logs);
    print("MATCHED_REAL_LOG_VECTOR=", matched_logs);
    print(
        "POWER_LOG_VECTOR_MAXIMUM_RESIDUAL=",
        vecmax(abs(analytic_power_log_vector - candidate_power_log_vector))
    );
    print(
        "RIGOROUS_DOUBLE_SINE_LOG_ERROR_BOUND_AT_POWER_5760=",
        5760 * 4.4e-11
    );
    print(
        "UNIT_COORDINATE_ERROR_BOUND_FROM_CERTIFIED_INTERVALS=",
        sqrt(8) * 5760 * 4.4e-11 / smallest_singular_value
    );

    \\ Exact Artin labeling.  The prime above 3 is a ray generator;
    \\ its displayed logarithm records PARI's current cyclic basis.
    \\ Modulo that prime sqrt(3)=0, so the relative unit polynomial is
    \\ the following irreducible degree-eight polynomial over F_3.
    \\ Arithmetic Frobenius is U -> U^3.
    ray_generator_prime = idealprimedec(K, 3)[1];
    ray_generator_log = lift(
        bnrisprincipal(Rfourier, ray_generator_prime, 0)[1]
    );
    ray_generator_logs = vector(
        8,
        c,
        signed_ray_logs[
            (ray_generator_log*(c-1)) % 8 + 1
        ]
    );
    relative_mod_three = Mod(1, 3) * (
        x^8 + x^7 + 2*x^6 + 2*x^2 + x + 1
    );
    relative_mod_three_factorization = factor(relative_mod_three);
    conjugates = nfgaloisconj(H);
    frobenius_target = Mod(Mod(1, 3)*x, relative_mod_three)^3;
    arithmetic_frobenius_index = 0;
    for(k = 1, #conjugates,
        if(
            Mod(Mod(1, 3)*conjugates[k], relative_mod_three)
                == frobenius_target,
            arithmetic_frobenius_index = k
        )
    );
    arithmetic_frobenius = Mod(
        conjugates[arithmetic_frobenius_index],
        absolute_polynomial
    );
    inverse_frobenius_index = 0;
    for(k = 1, #conjugates,
        if(
            subst(
                conjugates[k],
                x,
                arithmetic_frobenius
            ) == Mod(x, absolute_polynomial),
            inverse_frobenius_index = k
        )
    );
    inverse_frobenius = Mod(
        conjugates[inverse_frobenius_index],
        absolute_polynomial
    );

    \\ Propagate an exact rational isolating interval for U through
    \\ every exact Frobenius polynomial.  This certifies the archimedean
    \\ root labels used in the height comparison.
    U_interval = [
        389086171394307925533764395960567389713294085320953673463522415383235341834975405 / 10^80,
        389086171394307925533764395960567389713294085320953673463522415383235341834975406 / 10^80
    ];
    orbit_target_intervals = [
        3890/1000, 3891/1000;
        5540/1000, 5541/1000;
        612/1000, 613/1000;
        4313/1000, 4314/1000;
        257/1000, 258/1000;
        180/1000, 181/1000;
        1633/1000, 1634/1000;
        231/1000, 232/1000
    ];
    print(
        "STARK_UNIT_NARROW_INTERVAL_ROOT_COUNT=",
        polsturm(absolute_polynomial, U_interval)
    );
    orbit_element = U;
    all_orbit_intervals_certified = 1;
    for(c = 0, 7,
        orbit_image_interval = ieval(lift(orbit_element), U_interval);
        target = [
            orbit_target_intervals[c+1, 1],
            orbit_target_intervals[c+1, 2]
        ];
        candidate_error = is_subset(orbit_image_interval, target);
        all_orbit_intervals_certified *= candidate_error;
        print(
            "FROBENIUS_ORBIT_INTERVAL_", c,
            " TARGET=", target,
            " CERTIFIED=", candidate_error
        );
        orbit_element = subst(
            lift(arithmetic_frobenius),
            x,
            orbit_element
        )
    );
    print(
        "ALL_FROBENIUS_ORBIT_INTERVALS_CERTIFIED=",
        all_orbit_intervals_certified
    );

    orbit_element = U;
    print("RAY_GENERATOR_PRIME=", ray_generator_prime);
    print(
        "LOCAL_FOURIER_BASIS_PRIME_ABOVE_3_LOG=",
        ray_generator_log
    );
    print("RAY_GENERATOR_ORDERED_LOGS=", ray_generator_logs);
    print(
        "RELATIVE_UNIT_POLYNOMIAL_MOD_3_FACTORIZATION=",
        relative_mod_three_factorization
    );
    print("ARITHMETIC_FROBENIUS_INDEX=", arithmetic_frobenius_index);
    print("INVERSE_FROBENIUS_INDEX=", inverse_frobenius_index);
    for(c = 0, 7,
        print(
            "ARITHMETIC_FROBENIUS_ORBIT_", c,
            "_VALUE=", nfeltembed(H, orbit_element)[6],
            " LOG_ABS=", log(abs(nfeltembed(H, orbit_element)[6]))
        );
        orbit_element = subst(
            lift(arithmetic_frobenius),
            x,
            orbit_element
        )
    );
};
audit_unit_lattice();

quit();
