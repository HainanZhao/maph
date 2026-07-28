\\ Explore Kopp's conductor-lowering factors for the d=8 principal form.
\\ This is a numerical diagnostic, not yet a proof certificate.

default(realprecision, 80);

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
  for(j = 1, #cycles,
    angle += character[j] * class_log[j] / cycles[j]);
  exp(2 * Pi * I * angle);
};

partial_zeta_derivative(ray, values, class_log) =
{
  my(total = 0);
  for(j = 1, #values,
    total += conj(character_value(values[j][1], class_log, ray.cyc))
      * values[j][2][2]);
  total / prod(k = 1, #ray.cyc, ray.cyc[k]);
};

difference_derivative(gamma) =
{
  my(gamma_ideal = idealhnf(K, gamma));
  my(common = idealadd(K, full_modulus, gamma_ideal));
  my(common_norm = idealnorm(K, common));
  my(reduced_modulus = idealdiv(K, full_modulus, common));
  my(reduced_ideal = idealdiv(K, gamma_ideal, common));
  if(common_norm != 1 && common_norm != 9,
    error(Str("unexpected common ideal norm ", common_norm)));
  my(ray = if(common_norm == 1, ray24, ray8));
  my(values = if(common_norm == 1, values24, values8));
  my(class_log = bnrisprincipal(ray, reduced_ideal, 0));
  \\ The positive integer 23 is congruent to -1 modulo every divisor
  \\ of (24), and hence represents Kopp's sign class R.
  my(sign_log = bnrisprincipal(ray, idealhnf(K, 23), 0));
  my(signed_class_log = vector(#ray.cyc, j,
    (class_log[j] + sign_log[j]) % ray.cyc[j])~);
  my(value = partial_zeta_derivative(ray, values, class_log)
    - partial_zeta_derivative(ray, values, signed_class_log));
  [common_norm, ray.cyc, class_log, sign_log, value];
};

factor_gamma(a, b, j) =
{
  3*b*phi - a + 2*b - 8*j;
};

print_factor(j, gamma, data) =
{
  print("  FACTOR_", j, "_GAMMA=", lift(gamma));
  print("  FACTOR_", j, "_DATA=", data);
};

print_characteristic(a, b) =
{
  my(gammas = vector(3, j, factor_gamma(a, b, j - 1)));
  my(data = vector(3, j, difference_derivative(gammas[j])));
  my(predicted_log_square = sum(j = 1, 3,
    sign(subst(lift(gammas[j]), y, (1 - sqrt(5))/2))
      * if(data[j][1] == 9, 1, 1/2) * real(data[j][5])));
  print("CHARACTERISTIC=[", a, ",", b, "]");
  for(j = 1, 3, print_factor(j - 1, gammas[j], data[j]));
  print("  PREDICTED_LOG_SQUARE=", predicted_log_square);
};

print("PARI_VERSION=", version());
\\ For B=[3,2;0,1], the three preimages of (a/8,b/8)
\\ have 24*s=(a-2b+8j,3b).  Thus
\\ 24(s_2*phi-s_1)=3b*phi-a+2b-8j.
for(a = 0, 7, \
  for(b = 0, 7, \
    if((a^2 - 7*a*b + b^2) % 2, print_characteristic(a, b))));

quit();
