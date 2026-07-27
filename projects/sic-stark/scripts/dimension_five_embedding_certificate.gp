\\ Exact embedding certificate for the dimension-five algebraic packet.
\\
\\ This closes the link
\\   interval-defined real roots -> nfgaloisconj labels -> factor 4
\\ that is needed by the exact minor calculation.

print("PARI_VERSION=", version());

iadd(A, B) = [A[1] + B[1], A[2] + B[2]];
imul(A, B) =
{
    my(values = [
        A[1] * B[1], A[1] * B[2],
        A[2] * B[1], A[2] * B[2]
    ]);
    return([vecmin(values), vecmax(values)]);
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
    return(value);
};
is_subset(inner, outer) =
    inner[1] >= outer[1] && inner[2] <= outer[2];

Q = x^32 - 16*x^30 + 95*x^28 - 260*x^26 + 355*x^24 \
    - 348*x^22 + 388*x^20 - 300*x^18 + 195*x^16 \
    - 300*x^14 + 388*x^12 - 348*x^10 + 355*x^8 \
    - 260*x^6 + 95*x^4 - 16*x^2 + 1;

E = nfinit(Q);
conjugates = nfgaloisconj(E);

\\ A width-2*10^-78 rational interval around the largest real root w.
w_interval = [2353849830451566541437316857060507920817202107250349556892264918326613486608103 / 10^78, 2353849830451566541437316857060507920817202107250349556892264918326613486608105 / 10^78];
print("W_NARROW_ROOT_COUNT=", polsturm(Q, w_interval));

labels = ["w", "w^-1", "y", "y^-1", "x", "x^-1", "z", "z^-1"];
indices = [2, 8, 5, 4, 10, 6, 16, 12];
target_intervals = [2353849/10^6, 2353850/10^6; 424835/10^6, 424836/10^6; 1278133/10^6, 1278134/10^6; 782390/10^6, 782391/10^6; 1972526/10^6, 1972527/10^6; 506963/10^6, 506964/10^6; 2076946/10^6, 2076947/10^6; 481476/10^6, 481477/10^6];

audit_conjugate_labels() =
{
    my(all_certified = 1, image_interval, target_interval, certified);
    for(
        k = 1, #indices,
        image_interval = ieval(conjugates[indices[k]], w_interval);
        target_interval = [target_intervals[k, 1], target_intervals[k, 2]];
        certified = is_subset(image_interval, target_interval);
        all_certified *= certified;
        print("CONJUGATE_LABEL_", labels[k], "_INDEX=", indices[k], " TARGET_INTERVAL=", target_interval, " CERTIFIED=", certified)
    );
    return(all_certified);
};
all_labels_certified = audit_conjugate_labels();
print("ALL_CONJUGATE_INTERVAL_LABELS_CERTIFIED=", all_labels_certified);

\\ The real embedding selected by w contains canonical square roots.
sqrt_five_embeddings = nfisincl(t^2 - 5, E);
sqrt_six_embeddings = nfisincl(t^2 - 6, E);
sqrt_five_in_E = sqrt_five_embeddings[2];
sqrt_six_in_E = sqrt_six_embeddings[1];

sqrt_five_interval = ieval(sqrt_five_in_E, w_interval);
sqrt_six_interval = ieval(sqrt_six_in_E, w_interval);
print("SQRT5_POSITIVE_EMBEDDING_CERTIFIED=", is_subset(sqrt_five_interval, [2236067/10^6, 2236068/10^6]));
print("SQRT6_POSITIVE_EMBEDDING_CERTIFIED=", is_subset(sqrt_six_interval, [2449489/10^6, 2449490/10^6]));

\\ Identify which factor over Q(zeta_5,sqrt(6)) has those same two
\\ positive real-subfield embeddings.  This is an exact equality test.
Fdata = polcompositum(polcyclo(5, y), y^2 - 6, 1)[1];
Fpol = Fdata[1];
zeta_five = Fdata[2];
sqrt_six_in_F = Fdata[3];
sqrt_five_in_F = 2 * (zeta_five + zeta_five^-1) + 1;
F = nfinit(Fpol);
factors = nffactor(F, Q)[, 1];

audit_factors() =
{
    my(positive_count = 0, positive_index = 0, alpha);
    my(embedded_sqrt_five, embedded_sqrt_six, positive_five, positive_six);
    for(
        factor_index = 1, #factors,
        alpha = Mod(x, factors[factor_index]);
        embedded_sqrt_five = subst(sqrt_five_in_E, x, alpha);
        embedded_sqrt_six = subst(sqrt_six_in_E, x, alpha);
        positive_five = embedded_sqrt_five == sqrt_five_in_F;
        positive_six = embedded_sqrt_six == sqrt_six_in_F;
        if(
            positive_five && positive_six,
            positive_count++;
            positive_index = factor_index
        );
        print("FACTOR_", factor_index, "_SQRT5_POSITIVE=", positive_five, " SQRT6_POSITIVE=", positive_six)
    );
    return([positive_count, positive_index]);
};
factor_audit = audit_factors();
positive_factor_count = factor_audit[1];
positive_factor_index = factor_audit[2];
print("POSITIVE_FACTOR_COUNT=", positive_factor_count);
print("POSITIVE_FACTOR_INDEX=", positive_factor_index);

quit();
