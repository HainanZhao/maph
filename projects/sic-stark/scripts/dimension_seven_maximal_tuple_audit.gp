\\ Exact ray labels and numerical partial-zeta derivatives for the
\\ missing maximal-order d=7 tuple (7,1,<1,-4,2>).

default(realprecision, 80);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

K = bnfinit(y^2 - 2, 1);
alpha = Mod(2 + y, y^2 - 2);
negative_norm_unit_generator = Mod(1 + y, y^2 - 2);
full_modulus = idealhnf(K, 7);
sign_generator = idealhnf(K, 6);
fundamental_stabilizer = [3, -2; 1, -1];
zauner_stabilizer = fundamental_stabilizer^2;
At = zauner_stabilizer^3;

assert_equal("BASE_BNFCERTIFY", bnfcertify(K), 1);
assert_equal("FORM_DISCRIMINANT", (-4)^2 - 4*1*2, 8);
assert_equal("FORM_CONDUCTOR", 1, 1);
assert_equal("ZAUNER_STABILIZER", zauner_stabilizer, [7, -4; 2, -1]);
assert_equal("AT", At, [239, -140; 70, -41]);
assert_equal("AT_MOD_7", At % 7, matid(2));
psi_At = (At[1,1] + At[2,2])/At[2,1] \
  - 3*sign(At[2,1]*(At[1,1] + At[2,2])) \
  - 12*sign(At[2,1])*sumdedekind(At[1,1], At[2,1]);
assert_equal("RADEMACHER_AT", psi_At, 0);

ray_one = bnrinit(K, [7, [1, 0]], 1);
ray_both = bnrinit(K, [7, [1, 1]], 1);
assert_equal("RAY_7_ONE_STRUCTURE", ray_one.cyc, [6]);
assert_equal("RAY_7_BOTH_STRUCTURE", ray_both.cyc, [6, 2]);

\\ The direct ray-7 normal closure is a subfield of the ray-14
\\ normal closure and has the same intrinsic imaginary-quadratic
\\ conductor.  Hence the complete 32-divisor audit for that conductor
\\ supplies the already banked safe exponent 16128 here as well.
normal_closure = bnrclassfield(ray_both, , 2);
imaginary_base = bnfinit(y^2 + 7, 1);
relative_factors = nffactor(imaginary_base, normal_closure);
relative_normal_closure = relative_factors[1, 1];
assert_equal("NORMAL_CLOSURE_ABELIAN_OVER_Q_SQRT_MINUS_7", \
  rnfisabelian(imaginary_base, relative_normal_closure), 1);
conductor_data = rnfconductor( \
  imaginary_base, relative_normal_closure, 2);
assert_equal("IMAGINARY_CONDUCTOR", conductor_data[1][1], \
  [56, 32; 0, 8]);
print("INHERITED_SHINTANI_SAFE_EXPONENT=16128");

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
    total += conj(character_value(
      values[index][1], class_log, ray.cyc
    )) * leading_term_coefficient(values[index][2], order));
  total/prod(index = 1, #ray.cyc, ray.cyc[index]);
};

positive_representative(gamma) =
{
  my(answer = gamma);
  while(subst(lift(answer), y, -sqrt(2)) <= 0, answer += 7);
  answer;
};

negative_norm_unit(modulus) =
{
  my(difference, bound = 2*idealnorm(K, modulus));
  forstep(exponent = 1, bound, 2,
    for(sign_index = 1, 2,
      my(unit_sign = if(sign_index == 1, -1, 1));
      difference = idealhnf(
        K, unit_sign*negative_norm_unit_generator^exponent - 1
      );
      if(idealadd(K, modulus, difference) == modulus,
        return([unit_sign, exponent]))
    )
  );
  [0, 0];
};

canonical_stabilizer_index(first, second) =
{
  my(characteristic = [first/7, second/7]~);
  for(index = 1, 3,
    my(displacement =
      fundamental_stabilizer^(2*index)*characteristic-characteristic);
    if(denominator(displacement[1]) == 1
        && denominator(displacement[2]) == 1,
      return(index))
  );
  error(Str("no stabilizer index for ", characteristic));
};

difference_derivative(first, second) =
{
  my(gamma = positive_representative(second*alpha - first));
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
  my(value_at_zero =
    partial_zeta_coefficient(ray, values, class_log, 0)
    - partial_zeta_coefficient(ray, values, signed_class_log, 0));
  my(derivative =
    partial_zeta_coefficient(ray, values, class_log, 1)
    - partial_zeta_coefficient(ray, values, signed_class_log, 1));
  my(lifted_derivative =
    derivative - log(idealnorm(K, common))*value_at_zero);
  my(stabilizer_index =
    canonical_stabilizer_index(first, second));
  my(stabilizer_power = 3/stabilizer_index);
  my(unit_record = negative_norm_unit(reduced_modulus));
  my(kopp_exponent = if(unit_record[1], 2, 1));
  [
    idealnorm(K, common),
    idealnorm(K, reduced_modulus),
    ray.cyc,
    Vec(class_log),
    Vec(sign_log),
    stabilizer_index,
    stabilizer_power,
    unit_record,
    kopp_exponent,
    real(stabilizer_power*kopp_exponent*lifted_derivative)
  ];
};

audit_characteristic(first, second) =
{
  my(data = difference_derivative(first, second));
  print(
    "CHARACTERISTIC=", first, ",", second,
    " COMMON_NORM=", data[1],
    " REDUCED_MODULUS_NORM=", data[2],
    " RAY_STRUCTURE=", data[3],
    " CLASS_LOG=", data[4],
    " SIGN_LOG=", data[5],
    " STABILIZER_INDEX=", data[6],
    " STABILIZER_POWER=", data[7],
    " NEGATIVE_NORM_UNIT=", data[8],
    " KOPP_EXPONENT=", data[9],
    " LOG_SQUARE=", data[10]
  );
};

for(first = 0, 6, \
  for(second = 0, 6, \
    if(first != 0 || second != 0, \
      audit_characteristic(first, second))));

print("NONZERO_CHARACTERISTICS=48");

quit();
