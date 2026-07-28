\\ Exact ray labels and numerical partial-zeta derivatives for the
\\ conductor-two dimension-seven characteristic packet.
\\
\\ The conductor-lowering matrix is B=[2,-1;0,1], taking the reduced
\\ maximal-order point theta=2+sqrt(2) to beta=3+2sqrt(2).  Its two
\\ lifts of (a,b)/7 are
\\
\\   s_j=((a+b+7j)/14,2b/14),  j=0,1,
\\
\\ and Kopp's inverse Upsilon map at the maximal order represents them
\\ by gamma_j=14(s_{j,2}theta-s_{j,1}).

default(realprecision, 80);

K = bnfinit(y^2 - 2, 1);
bnf_certified = bnfcertify(K);
phi = Mod(1 + y, y^2 - 2);
alpha_reduced = Mod(2 + y, y^2 - 2);
full_modulus = idealhnf(K, 14);
sign_generator = idealhnf(K, 13);
M = [3, -2; 1, -1];
common_stabilizer = M^6;

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

difference_derivative(gamma) =
{
  my(gamma_ideal = idealhnf(K, gamma));
  my(common = idealadd(K, full_modulus, gamma_ideal));
  my(reduced_modulus = idealdiv(K, full_modulus, common));
  my(reduced_ideal = idealdiv(K, gamma_ideal, common));
  my(ray = bnrinit(K, [reduced_modulus, [1, 0]], 1));
  my(values = bnrL1(ray, , 6));
  my(class_log = bnrisprincipal(ray, reduced_ideal, 0));
  my(sign_log = bnrisprincipal(ray, sign_generator, 0));
  my(signed_class_log = vector(#ray.cyc, index,
    (class_log[index] + sign_log[index]) % ray.cyc[index])~);
  my(value_at_zero = partial_zeta_coefficient(ray, values, class_log, 0)
    - partial_zeta_coefficient(ray, values, signed_class_log, 0));
  my(derivative = partial_zeta_coefficient(ray, values, class_log, 1)
    - partial_zeta_coefficient(ray, values, signed_class_log, 1));
  \\ Proposition 6.2 contributes the derivative of N(common)^(-s).
  \\ The differenced value at zero is not always zero, so this term is
  \\ essential on the scalar modulus-seven stratum.
  my(lifted_derivative = derivative
    - log(idealnorm(K, common))*value_at_zero);
  [idealnorm(K, common), idealnorm(K, reduced_modulus), ray.cyc,
    class_log, sign_log, value_at_zero, derivative, lifted_derivative];
};

positive_representative(gamma) =
{
  my(answer = gamma);
  while(subst(lift(answer), y, -sqrt(2)) <= 0, answer += 14);
  answer;
};

factor_gamma(a, b, j) =
{
  2*b*alpha_reduced - a - b - 7*j;
};

lift_characteristic(a, b, j) =
{
  [(a + b + 7*j)/14, 2*b/14]~;
};

canonical_stabilizer_index(s) =
{
  my(candidate, displacement);
  for(index = 1, 3,
    candidate = M^(2*index);
    displacement = candidate*s - s;
    if(denominator(displacement[1]) == 1 && \
        denominator(displacement[2]) == 1, return(index)));
  error(Str("common stabilizer does not fix ", s));
};

negative_norm_unit(reduced_modulus) =
{
  \\ Powers in (O_K/reduced_modulus)^x repeat within N(reduced_modulus)
  \\ steps.  Twice that bound, with both signs tested, is therefore an
  \\ exhaustive search for a negative-norm unit congruent to one.
  my(difference, bound = 2*idealnorm(K, reduced_modulus));
  forstep(exponent = 1, bound, 2,
    for(sign_index = 1, 2,
      unit_sign = if(sign_index == 1, -1, 1);
      difference = idealhnf(K, unit_sign*phi^exponent - 1);
      if(idealadd(K, reduced_modulus, difference) == reduced_modulus,
        return([unit_sign, exponent]))));
  [0, 0];
};

print_factor(a, b, j) =
{
  my(s = lift_characteristic(a, b, j));
  my(gamma = factor_gamma(a, b, j));
  my(orientation = sign(subst(lift(gamma), y, -sqrt(2))));
  my(gamma_positive = positive_representative(gamma));
  my(data = difference_derivative(gamma_positive));
  my(canonical_index = canonical_stabilizer_index(s));
  my(stabilizer_power = 3/canonical_index);
  my(common = idealadd(K, full_modulus, idealhnf(K, gamma)));
  my(reduced_modulus = idealdiv(K, full_modulus, common));
  my(negative_unit = negative_norm_unit(reduced_modulus));
  my(kopp_exponent = if(negative_unit[1], 2, 1));
  print("  FACTOR_", j, "_S=", s);
  print("  FACTOR_", j, "_GAMMA=", lift(gamma));
  print("  FACTOR_", j, "_ORIENTATION=", orientation);
  print("  FACTOR_", j, "_POSITIVE_GAMMA=", lift(gamma_positive));
  print("  FACTOR_", j, "_REDUCED_MODULUS=", reduced_modulus);
  print("  FACTOR_", j, "_DATA=", data);
  print("  FACTOR_", j, "_CANONICAL_STABILIZER_INDEX=", canonical_index);
  print("  FACTOR_", j, "_COMMON_POWER=", stabilizer_power);
  print("  FACTOR_", j, "_NEGATIVE_NORM_UNIT=", negative_unit);
  print("  FACTOR_", j, "_KOPP_EXPONENT=", kopp_exponent);
  [orientation, stabilizer_power, kopp_exponent, real(data[8])];
};

print_characteristic(a, b) =
{
  print("CHARACTERISTIC=[", a, ",", b, "]");
  my(factors = vector(2, index, print_factor(a, b, index - 1)));
  my(predicted_log_square = sum(index = 1, 2,
    factors[index][2]*factors[index][3]*factors[index][4]));
  print("  PREDICTED_LOG_SQUARE=", predicted_log_square);
};

print("PARI_VERSION=", version());
print("BNF_CERTIFIED=", bnf_certified);
print("BASE_FIELD=x^2-2");
print("REDUCED_MAXIMAL_POINT=2+sqrt(2)");
print("LOWERING_MATRIX=[2,-1;0,1]");
print("COMMON_STABILIZER=", common_stabilizer);

for(a = 0, 6, for(b = 0, 6, \
  if(a != 0 || b != 0, print_characteristic(a, b))));

print("NONZERO_CHARACTERISTICS=48");
print("LOWERED_FACTORS=96");

quit();
