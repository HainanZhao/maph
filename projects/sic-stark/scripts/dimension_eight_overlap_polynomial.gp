\\ Recognize the relative class polynomial of the sixteen primitive
\\ squared d=8 principal overlaps.

default(realprecision, 180);
default(parisizemax, 3000000000);

K = bnfinit(y^2 - y - 1, 1);
phi = Mod(y, y^2 - y - 1);
full_modulus = idealhnf(K, 24);
ray24 = bnrinit(K, [24, [1, 0]], 1);
ray8 = bnrinit(K, [8, [1, 0]], 1);
values24 = bnrL1(ray24, , 6);
values8 = bnrL1(ray8, , 6);

character_value(character, class_log, cycles) =
{
  my(angle = 0);
  for(index = 1, #cycles,
    angle += character[index] * class_log[index] / cycles[index]);
  exp(2 * Pi * I * angle);
};

partial_zeta_derivative(ray, values, class_log) =
{
  my(total = 0);
  for(index = 1, #values,
    total += conj(character_value(values[index][1], class_log, ray.cyc))
      * values[index][2][2]);
  total / prod(index = 1, #ray.cyc, ray.cyc[index]);
};

difference_derivative(gamma) =
{
  my(gamma_ideal = idealhnf(K, gamma));
  my(common = idealadd(K, full_modulus, gamma_ideal));
  my(common_norm = idealnorm(K, common));
  my(reduced_modulus = idealdiv(K, full_modulus, common));
  my(reduced_ideal = idealdiv(K, gamma_ideal, common));
  my(ray = if(common_norm == 1, ray24, ray8));
  my(values = if(common_norm == 1, values24, values8));
  my(class_log = bnrisprincipal(ray, reduced_ideal, 0));
  my(sign_log = bnrisprincipal(ray, idealhnf(K, 23), 0));
  my(signed_class_log = vector(#ray.cyc, index,
    (class_log[index] + sign_log[index]) % ray.cyc[index])~);
  partial_zeta_derivative(ray, values, class_log)
    - partial_zeta_derivative(ray, values, signed_class_log);
};

factor_gamma(first, second, lift_index) =
  3*second*phi - first + 2*second - 8*lift_index;

log_square(first, second) =
{
  my(total = 0, gamma, common);
  for(lift_index = 0, 2,
    gamma = factor_gamma(first, second, lift_index);
    common = idealadd(K, full_modulus, idealhnf(K, gamma));
    total +=
      sign(subst(lift(gamma), y, (1 - sqrt(5))/2))
      * if(idealnorm(K, common) == 9, 1, 1/2)
      * real(difference_derivative(gamma))
  );
  total;
};

recognize_in_base(value) =
{
  my(relation = lindep([value, 1, sqrt(5)]));
  if(relation[1] == 0, error("base-field recognition failed"));
  [
    -relation[2]/relation[1],
    -relation[3]/relation[1],
    abs(relation[1]*value + relation[2] + relation[3]*sqrt(5))
  ];
};

representatives = [ \
  0,1; 0,3; 0,5; 0,7; \
  1,1; 1,2; 1,3; 1,4; 1,5; \
  2,3; 2,7; 3,6; 3,7; 4,5; 4,7; 5,5 \
];

class_polynomial = 1;
for(index = 1, matsize(representatives)[1], \
  first = representatives[index, 1]; \
  second = representatives[index, 2]; \
  root = exp(log_square(first, second)); \
  print("ROOT_", first, "_", second, "=", root); \
  class_polynomial *= x - root; \
);

recognized_polynomial = 0;
for(degree = 0, poldegree(class_polynomial), \
  recognition = recognize_in_base( \
    real(polcoef(class_polynomial, degree)) \
  ); \
  print("COEFFICIENT_", degree, "_RECOGNITION=", recognition); \
  recognized_polynomial += \
    (recognition[1] - recognition[2] + 2*recognition[2]*y)*x^degree; \
);

print("RECOGNIZED_RELATIVE_POLYNOMIAL=", recognized_polynomial);
candidate_absolute = rnfequation(y^2 - y - 1, recognized_polynomial);
ray_absolute = bnrclassfield(ray24, , 2);
print("CANDIDATE_ABSOLUTE_IRREDUCIBLE=", \
  polisirreducible(candidate_absolute));
print("CANDIDATE_ABSOLUTE_DEGREE=", poldegree(candidate_absolute));
print("RAY_ABSOLUTE_DEGREE=", poldegree(ray_absolute));
print("CANDIDATE_FIELD_MATCHES_RAY_24=", \
  #nfisisom(candidate_absolute, ray_absolute) > 0);

quit();
