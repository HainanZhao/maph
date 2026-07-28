\\ Enumerate the discrete quartic Stark orientations left by Roblot's
\\ absolute-value theorem and propagate them through the exact d=8
\\ conductor-lowering formula.
\\
\\ For each of the two conjugate quartic character pairs, the unresolved
\\ resolvent may be multiplied by a Gaussian unit and/or conjugated.  The
\\ 8 x 8 possibilities are emitted as real log-square packets for the 48
\\ primitive characteristics.  A Python companion inserts the unaffected
\\ lower-conductor values and tests the finite TCC equations.

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
  for(index = 1, #cycles,
    angle += character[index] * class_log[index] / cycles[index]);
  exp(2 * Pi * I * angle);
};

raw_derivative(values, character) =
{
  for(index = 1, #values,
    if(values[index][1] == character, return(values[index][2][2])));
  error(Str("character not found: ", character));
};

orient(value, code) =
{
  my(answer = if(code >= 4, conj(value), value));
  I^(code % 4) * answer;
};

oriented_derivative(values, character, code_zero, code_one, is_full) =
{
  my(second, base);
  if(!is_full, return(raw_derivative(values, character)));
  if(character[3] != 0 || (character[1] != 1 && character[1] != 3),
    return(raw_derivative(values, character)));
  second = character[2];
  base = raw_derivative(values, [1, second, 0]);
  base = orient(base, if(second == 0, code_zero, code_one));
  if(character[1] == 1, base, conj(base));
};

partial_zeta_derivative(ray, values, class_log, code_zero, code_one, is_full) =
{
  my(total = 0);
  for(index = 1, #values,
    total += conj(character_value(values[index][1], class_log, ray.cyc))
      * oriented_derivative( \
          values, values[index][1], code_zero, code_one, is_full \
        ));
  total / prod(index = 1, #ray.cyc, ray.cyc[index]);
};

difference_derivative(gamma, code_zero, code_one) =
{
  my(gamma_ideal = idealhnf(K, gamma));
  my(common = idealadd(K, full_modulus, gamma_ideal));
  my(common_norm = idealnorm(K, common));
  my(reduced_modulus = idealdiv(K, full_modulus, common));
  my(reduced_ideal = idealdiv(K, gamma_ideal, common));
  my(is_full = common_norm == 1);
  my(ray = if(is_full, ray24, ray8));
  my(values = if(is_full, values24, values8));
  my(class_log = bnrisprincipal(ray, reduced_ideal, 0));
  my(sign_log = bnrisprincipal(ray, idealhnf(K, 23), 0));
  my(signed_class_log = vector(#ray.cyc, index,
    (class_log[index] + sign_log[index]) % ray.cyc[index])~);
  partial_zeta_derivative( \
    ray, values, class_log, code_zero, code_one, is_full \
  ) - partial_zeta_derivative( \
    ray, values, signed_class_log, code_zero, code_one, is_full \
  );
};

factor_gamma(first, second, lift_index) =
  3*second*phi - first + 2*second - 8*lift_index;

log_square(first, second, code_zero, code_one) =
{
  my(total = 0, gamma, common);
  for(lift_index = 0, 2,
    gamma = factor_gamma(first, second, lift_index);
    common = idealadd(K, full_modulus, idealhnf(K, gamma));
    total +=
      sign(subst(lift(gamma), y, (1 - sqrt(5))/2))
      * if(idealnorm(K, common) == 9, 1, 1/2)
      * real(difference_derivative(gamma, code_zero, code_one))
  );
  total;
};

print("PARI_VERSION=", version());
for(code_zero = 0, 7, \
  for(code_one = 0, 7, \
    print("ORIENTATION=", code_zero, ",", code_one); \
    for(first = 0, 7, \
      for(second = 0, 7, \
        if((first^2 - 7*first*second + second^2) % 2, \
          print( \
            "CHARACTERISTIC=", first, ",", second, \
            " LOG_SQUARE=", \
            log_square(first, second, code_zero, code_one) \
          ) \
        ) \
      ) \
    ) \
  ) \
);

quit();
