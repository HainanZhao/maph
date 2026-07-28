\\ Recognize the class polynomial of the sixteen distinct squared
\\ normalized d=7 principal overlaps.

default(realprecision, 160);

K = bnfinit(y^2 - 2, 1);
phi = Mod(1 + y, y^2 - 2);
alpha_reduced = Mod(2 + y, y^2 - 2);
full_modulus = idealhnf(K, 14);
sign_generator = idealhnf(K, 13);

character_value(character, class_log, cycles) =
{
  my(angle = 0);
  for(index = 1, #cycles,
    angle += character[index]*class_log[index]/cycles[index]);
  exp(2*Pi*I*angle);
};

leading_term_coefficient(data, order) =
{
  if(data[1] == order, data[2], 0);
};

partial_zeta_coefficient(ray, values, class_log, order) =
{
  my(total = 0);
  if(#ray.cyc == 0,
    return(leading_term_coefficient(values[1][2], order)));
  for(index = 1, #values,
    total += conj(character_value(values[index][1], class_log, ray.cyc))
      * leading_term_coefficient(values[index][2], order));
  total/prod(index = 1, #ray.cyc, ray.cyc[index]);
};

negative_norm_unit(modulus) =
{
  my(difference, bound = 2*idealnorm(K, modulus));
  forstep(exponent = 1, bound, 2,
    for(sign_index = 1, 2,
      unit_sign = if(sign_index == 1, -1, 1);
      difference = idealhnf(K, unit_sign*phi^exponent - 1);
      if(idealadd(K, modulus, difference) == modulus,
        return([unit_sign, exponent]))));
  [0, 0];
};

positive_representative(gamma) =
{
  my(answer = gamma);
  while(subst(lift(answer), y, -sqrt(2)) <= 0, answer += 14);
  answer;
};

factor_derivative(a, b, j) =
{
  my(gamma = 2*b*alpha_reduced - a - b - 7*j);
  my(gamma_positive = positive_representative(gamma));
  my(gamma_ideal = idealhnf(K, gamma_positive));
  my(common = idealadd(K, full_modulus, gamma_ideal));
  my(reduced_modulus = idealdiv(K, full_modulus, common));
  my(reduced_ideal = idealdiv(K, gamma_ideal, common));
  my(ray = bnrinit(K, [reduced_modulus, [1, 0]], 1));
  my(values = bnrL1(ray, , 6));
  my(class_log = bnrisprincipal(ray, reduced_ideal, 0));
  my(sign_log = bnrisprincipal(ray, sign_generator, 0));
  my(signed_class_log = vector(#ray.cyc, index,
    (class_log[index] + sign_log[index]) % ray.cyc[index])~);
  my(value_at_zero =
    partial_zeta_coefficient(ray, values, class_log, 0)
    - partial_zeta_coefficient(ray, values, signed_class_log, 0));
  my(derivative =
    partial_zeta_coefficient(ray, values, class_log, 1)
    - partial_zeta_coefficient(ray, values, signed_class_log, 1));
  my(lifted_derivative = derivative
    - log(idealnorm(K, common))*value_at_zero);
  my(negative_unit = negative_norm_unit(reduced_modulus));
  my(kopp_exponent = if(negative_unit[1], 2, 1));
  kopp_exponent*real(lifted_derivative);
};

overlap_log_square(a, b) =
{
  factor_derivative(a, b, 0) + factor_derivative(a, b, 1);
};

recognize_quadratic(value) =
{
  my(relation = lindep([value, 1, sqrt(2)]));
  if(relation[1] == 0, return(["FAILED", value, relation]));
  [
    -relation[2]/relation[1],
    -relation[3]/relation[1],
    abs(relation[1]*value + relation[2] + relation[3]*sqrt(2))
  ];
};

representatives = List();
listput(representatives, [0,1]); listput(representatives, [0,2]);
listput(representatives, [0,3]); listput(representatives, [0,4]);
listput(representatives, [0,5]); listput(representatives, [0,6]);
listput(representatives, [1,1]); listput(representatives, [1,2]);
listput(representatives, [1,3]); listput(representatives, [1,4]);
listput(representatives, [2,2]); listput(representatives, [2,6]);
listput(representatives, [3,5]); listput(representatives, [3,6]);
listput(representatives, [4,4]); listput(representatives, [4,5]);

build_class_polynomial() =
{
  my(result = 1, point, log_square, root);
  for(index = 1, #representatives,
    point = representatives[index];
    log_square = overlap_log_square(point[1], point[2]);
    root = exp(log_square);
    print("ROOT_", point, "=", root);
    result *= x - root;
  );
  result;
};

print_coefficients(class_polynomial) =
{
  my(coefficient);
  for(coefficient_index = 0, poldegree(class_polynomial),
    coefficient = real(polcoef(class_polynomial, coefficient_index));
    print(
      "COEFFICIENT_", coefficient_index, "_RECOGNITION=",
      recognize_quadratic(coefficient)
    );
  );
};

class_polynomial = build_class_polynomial();
print("NUMERICAL_OVERLAP_SQUARE_CLASS_POLYNOMIAL=", class_polynomial);
print_coefficients(class_polynomial);

quit();
