\\ Test whether the dimension-five ray field has an accidental
\\ cyclotomic/CM/subfield realization that could make its Stark value
\\ accessible through known lower-degree formulas.

print("PARI_VERSION=", version());

Hpol = x^16 - 4*x^15 - 4*x^14 + 24*x^13 + 3*x^12 - 64*x^11 \
    + 34*x^10 + 72*x^9 - 127*x^8 + 76*x^7 + 41*x^6 - 118*x^5 \
    + 113*x^4 - 68*x^3 + 29*x^2 - 8*x + 1;

H = nfinit(Hpol);
print("ABSOLUTE_SIGNATURE=", H.sign);
print("ABSOLUTE_DISCRIMINANT=", H.disc);
print("ABSOLUTE_GALOIS_OVER_Q=", galoisinit(Hpol) != 0);

quadratic_subfields = nfsubfields(Hpol, 2);
quartic_subfields = nfsubfields(Hpol, 4);
octic_subfields = nfsubfields(Hpol, 8);
print("QUADRATIC_SUBFIELD_COUNT=", #quadratic_subfields);
print("QUADRATIC_SUBFIELD_POLYNOMIALS=", vector(#quadratic_subfields, k, quadratic_subfields[k][1]));
print("QUARTIC_SUBFIELD_COUNT=", #quartic_subfields);
print("QUARTIC_SUBFIELD_POLYNOMIALS=", vector(#quartic_subfields, k, quartic_subfields[k][1]));
print("OCTIC_SUBFIELD_COUNT=", #octic_subfields);
print("OCTIC_SUBFIELD_POLYNOMIALS=", vector(#octic_subfields, k, octic_subfields[k][1]));

conductor_sixty_octic_fields = concat([], polsubcyclo(60, 8));
print("CONDUCTOR_60_OCTIC_FIELD_COUNT=", #conductor_sixty_octic_fields);
audit_conductor_sixty_octic_fields() =
{
    my(match_count = 0);
    for(k = 1, #conductor_sixty_octic_fields,
        my(is_match = #nfisisom(
            octic_subfields[1][1],
            conductor_sixty_octic_fields[k]
        ) > 0);
        print("CONDUCTOR_60_OCTIC_", k, "_SIGNATURE=", nfinit(conductor_sixty_octic_fields[k]).sign, " MATCH=", is_match, " POLYNOMIAL=", conductor_sixty_octic_fields[k]);
        match_count += is_match
    );
    return(match_count);
};
print("OCTIC_SUBFIELD_IS_CONDUCTOR_60_ABELIAN=", audit_conductor_sixty_octic_fields());

Kpol = y^2 - 4*y + 1;
s = Mod(y - 2, Kpol);
trace_relative_polynomial = x^4 - (8 + 5*s)*x^3 + (49 + 30*s)*x^2 \
    - (132 + 75*s)*x + (121 + 70*s);
trace_absolute_data = rnfequation(Kpol, trace_relative_polynomial, 1);
trace_absolute_polynomial = trace_absolute_data[1];
real_cyclotomic_polynomial = conductor_sixty_octic_fields[1];
trace_to_real_cyclotomic = nfisisom(trace_absolute_polynomial, real_cyclotomic_polynomial);
print("TRACE_ABSOLUTE_POLYNOMIAL=", trace_absolute_polynomial);
print("TRACE_ABSOLUTE_GENERATOR_SHIFT=", trace_absolute_data[3]);
print("TRACE_TO_REAL_CYCLOTOMIC_EMBEDDING_COUNT=", #trace_to_real_cyclotomic);
print("TRACE_TO_REAL_CYCLOTOMIC_IMAGES=", trace_to_real_cyclotomic);

audit_quadratic_lift() =
{
    my(M, eta, trace_value, radicand, factorization, half_exponents);
    my(odd_exponents, square_root_ideal, odd_ideal);
    my(principal_data, odd_principal_data, square_generator, odd_generator);
    my(residual_radicand, unit_squareclass, positive_sqrt_three);
    M = bnfinit(real_cyclotomic_polynomial, 1);
    eta = Mod(x, real_cyclotomic_polynomial);
    trace_value = -eta^7 + 8*eta^5 - 18*eta^3 + 9*eta + 2;
    positive_sqrt_three = eta^5 - 5*eta^3 + 5*eta;
    radicand = trace_value^2 - 4;
    factorization = idealfactor(M, radicand);
    print("REAL_CYCLOTOMIC_CLASS_NUMBER=", M.no);
    print("POSITIVE_SQRT_THREE_IN_ETA=", positive_sqrt_three);
    print("POSITIVE_SQRT_THREE_SQUARE_CHECK=", positive_sqrt_three^2 == 3);
    print("TARGET_TRACE_IN_ETA=", trace_value);
    print("TARGET_TRACE_NUMERIC=", trace_value * 1.0);
    print("TARGET_TRACE_TRIGONOMETRIC_FORM=2+2cos(3pi/30)+2cos(5pi/30)-2cos(7pi/30)");
    print("TARGET_TRACE_RELATIVE_POLYNOMIAL_CHECK=", trace_value^4 - (8 + 5*positive_sqrt_three)*trace_value^3 + (49 + 30*positive_sqrt_three)*trace_value^2 - (132 + 75*positive_sqrt_three)*trace_value + (121 + 70*positive_sqrt_three) == 0);
    print("TRACE_RADICAND_IDEAL_FACTORIZATION=", factorization);
    print("TRACE_RADICAND_ALL_FINITE_VALUATIONS_EVEN=", vecsum(vector(matsize(factorization)[1], k, factorization[k, 2] % 2)) == 0);
    half_exponents = vector(matsize(factorization)[1], k, (factorization[k, 2] - (factorization[k, 2] % 2)) / 2);
    odd_exponents = vector(matsize(factorization)[1], k, factorization[k, 2] % 2);
    square_root_ideal = idealfactorback(M, Vec(factorization[, 1]), half_exponents);
    odd_ideal = idealfactorback(M, Vec(factorization[, 1]), odd_exponents);
    principal_data = bnfisprincipal(M, square_root_ideal);
    odd_principal_data = bnfisprincipal(M, odd_ideal);
    square_generator = nfbasistoalg(M, principal_data[2]);
    odd_generator = nfbasistoalg(M, odd_principal_data[2]);
    residual_radicand = radicand / square_generator^2;
    unit_squareclass = residual_radicand / odd_generator;
    print("TRACE_RADICAND_HALF_IDEAL_PRINCIPAL_CLASS=", principal_data[1]);
    print("TRACE_RADICAND_SQUARE_GENERATOR=", square_generator);
    print("TRACE_RADICAND_ODD_IDEAL_PRINCIPAL_CLASS=", odd_principal_data[1]);
    print("TRACE_RADICAND_ODD_IDEAL_GENERATOR=", odd_generator);
    print("TRACE_RADICAND_UNIT_SQUARECLASS=", unit_squareclass);
    print("TRACE_RADICAND_UNIT_DECOMPOSITION=", bnfisunit(M, unit_squareclass));
    print("TRACE_RADICAND_UNIT_REAL_EMBEDDINGS=", nfeltembed(M, unit_squareclass));
};
audit_quadratic_lift();

cyclotomic_orders = [15, 16, 17, 20, 24, 30, 32, 34, 40, 48, 60];
audit_cyclotomic_orders() =
{
    my(n, C);
    for(k = 1, #cyclotomic_orders,
        n = cyclotomic_orders[k];
        C = polcyclo(n);
        if(poldegree(C) == 16,
            print("ISOMORPHIC_TO_CYCLOTOMIC_", n, "=", #nfisisom(Hpol, C) > 0)
        )
    );
};
audit_cyclotomic_orders();

quit();
