\\ Exact interval and factor-selection certificate for dimension six.

default(realprecision, 100);
default(parisizemax, 4000000000);
print("PARI_VERSION=", version());

iadd(A, B) = [A[1] + B[1], A[2] + B[2]];
imul(A, B) =
{
  my(values = [
    A[1]*B[1], A[1]*B[2],
    A[2]*B[1], A[2]*B[2]
  ]);
  return([vecmin(values), vecmax(values)]);
};
ieval(P, interval) =
{
  my(value = [0, 0]);
  forstep(degree = poldegree(P), 0, -1,
    value = iadd(imul(value, interval), \
      [polcoef(P, degree), polcoef(P, degree)])
  );
  return(value);
};
is_subset(inner, outer) = \
  inner[1] >= outer[1] && inner[2] <= outer[2];

Q = x^12 + 3*x^11 - 6*x^10 - 16*x^9 + 3*x^8 + 27*x^6 \
  + 3*x^4 - 16*x^3 - 6*x^2 + 3*x + 1;
conjugates = nfgaloisconj(nfinit(Q));

\\ Width 10^-80 rational interval around the canonical positive root x.
x_interval = [221288528901718260906871660373412561554511223034960258447271869517479776057069934/10^80, 221288528901718260906871660373412561554511223034960258447271869517479776057069935/10^80];
print("X_NARROW_ROOT_COUNT=", polsturm(Q, x_interval));

labels = ["x", "-w^-1", "-w", "x^-1", "-z^-1", "-z"];
target_intervals = [2212885/10^6,2212886/10^6; -2978734/10^6,-2978733/10^6; -335714/10^6,-335713/10^6; 451898/10^6,451899/10^6; -2782197/10^6,-2782196/10^6; -359429/10^6,-359428/10^6];

audit_labels() =
{
  my(all_certified = 1, image_interval, target_interval, certified);
  for(index = 1, #conjugates,
    image_interval = ieval(conjugates[index], x_interval);
    target_interval = \
      [target_intervals[index, 1], target_intervals[index, 2]];
    certified = is_subset(image_interval, target_interval);
    all_certified *= certified;
    print("CONJUGATE_", index, "_LABEL=", labels[index], \
      " TARGET_INTERVAL=", target_interval, " CERTIFIED=", certified)
  );
  return(all_certified);
};
all_labels_certified = audit_labels();
print("ALL_PRIMITIVE_LABELS_CERTIFIED=", all_labels_certified);

\\ Exact coefficient-field factor selection.
Fdata = polcompositum(polcyclo(12, y), y^2 - 7, 1)[1];
F = nfinit(Fdata[1]);
zeta_twelve = Fdata[2];
sqrt_seven = Fdata[3];
sqrt_twenty_one = (zeta_twelve + zeta_twelve^-1)*sqrt_seven;
beta = (5 + sqrt_twenty_one)/2;
factors = nffactor(F, Q)[, 1];
print("FACTOR_COUNT_OVER_Q_ZETA12_SQRT7=", #factors);
audit_factors() =
{
  for(index = 1, #factors,
    print("FACTOR_", index, "_DEGREE=", poldegree(factors[index]), \
      " X5_COEFFICIENT_IS_BETA_MINUS_ONE=", \
      polcoef(factors[index], 5) == beta-1)
  );
};
audit_factors();

\\ The lower polynomial has exactly one root in each displayed interval.
lower_polynomial = x^8 - x^6 - 3*x^4 - x^2 + 1;
lower_large_interval = [1539222/10^6, 1539223/10^6];
lower_small_interval = [649678/10^6, 649679/10^6];
print("LOWER_Y_GREATER_THAN_ONE_ROOT_COUNT=", \
  polsturm(lower_polynomial, lower_large_interval));
print("LOWER_Y_INVERSE_ROOT_COUNT=", \
  polsturm(lower_polynomial, lower_small_interval));

quit();
