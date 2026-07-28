\\ Exact arithmetic audit for the maximal-order discriminant-five
\\ dimension-eight tuple (8,1,<1,-3,1>).

default(realprecision, 100);
default(parisizemax, 4000000000);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

K = bnfinit(y^2 - y - 1, 1);
phi = Mod(y, y^2 - y - 1);
beta = phi^2;
beta_conjugate = (3 - sqrt(5))/2;

C = [3, -1; 1, 0];
Lz = C^2;
At = C^6;

assert_equal("PARI_VERSION", version(), version());
assert_equal("BASE_BNFCERTIFY", bnfcertify(K), 1);
assert_equal("FORM_DISCRIMINANT", (-3)^2 - 4, 5);
assert_equal("LZ", Lz, [8, -3; 3, -1]);
assert_equal("AT", At, [377, -144; 144, -55]);
assert_equal("AT_MOD_8", At % 8, matid(2));
assert_equal("LZ_CUBE", Lz^3, At);

continued_fraction_rows = \
  [377,-144;144,-55;55,-21;21,-8;8,-3;3,-1;1,0;0,1];
period_values = continued_fraction_rows * [beta, 1]~;
assert_equal("CONTINUED_FRACTION_ROWS", continued_fraction_rows, \
  [377,-144;144,-55;55,-21;21,-8;8,-3;3,-1;1,0;0,1]);
assert_equal("CONTINUED_FRACTION_PERIOD_VALUES", \
  period_values, vector(8, index, beta^(8-index))~);
assert_equal("SIX_SIGMA_PERIOD_RATIOS", \
  vector(6, index, period_values[index+1]/period_values[index+2]), \
  vector(6, index, beta));
assert_equal("OUTER_FINITE_PRODUCT_COEFFICIENTS", \
  [-At[2,1]/8, (At[1,1]-1)/8], [-18, 47]);
print("SIX_FACTOR_AFK_SPECIALIZATION_DATA=1");

ray8_one = bnrinit(K, [8, [1, 0]], 1);
ray8_both = bnrinit(K, [8, [1, 1]], 1);
assert_equal("RAY_8_INFINITY_2_STRUCTURE", ray8_one.cyc, [2, 2]);
assert_equal("RAY_8_BOTH_STRUCTURE", ray8_both.cyc, [2, 2, 2]);

map_both_to_one = matrix(#ray8_one.cyc, #ray8_both.cyc, row, column, \
  bnrisprincipal(ray8_one, ray8_both.gen[column], 0)[row]);
assert_equal( \
  "FORGET_INFINITY_1_KERNEL_ORDER", \
  ray8_both.no / ray8_one.no, \
  2 \
);
print("MAP_BOTH_TO_ONE=", map_both_to_one);

rademacher(M) =
{
  my(a = M[1,1], c = M[2,1], d = M[2,2]);
  if(c == 0, return(M[1,2]/d));
  (a+d)/c - 3*sign(c*(a+d)) - 12*sign(c)*sum(
    n = 1, abs(c)-1,
    (n/abs(c) - 1/2) *
      (frac(n*a/abs(c)) - if(frac(n*a/abs(c)) == 0, 0, 1/2))
  );
};

\\ Use PARI's exact sumdedekind implementation for the invariant.
psi_At = (At[1,1] + At[2,2])/At[2,1] \
  - 3*sign(At[2,1]*(At[1,1] + At[2,2])) \
  - 12*sign(At[2,1])*sumdedekind(At[1,1], At[2,1]);
assert_equal("RADEMACHER_AT", psi_At, 0);

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

partial_zeta_derivative(ray, values, class_log) =
{
  my(total = 0);
  for(index = 1, #values,
    total += conj(character_value(
      values[index][1], class_log, ray.cyc
    )) * raw_derivative(values, values[index][1]));
  total / ray.no;
};

positive_gamma(first, second) =
{
  my(lifted_first = first);
  while(second*beta_conjugate - lifted_first <= 0,
    lifted_first -= 8);
  [second*beta - lifted_first, lifted_first];
};

difference_derivative(first, second) =
{
  my(gamma_record = positive_gamma(first, second));
  my(gamma = gamma_record[1]);
  my(gamma_ideal = idealhnf(K, gamma));
  my(common = idealadd(K, idealhnf(K, 8), gamma_ideal));
  my(reduced_modulus = idealdiv(K, idealhnf(K, 8), common));
  my(reduced_ideal = idealdiv(K, gamma_ideal, common));
  my(modulus_norm = idealnorm(K, reduced_modulus));
  my(stabilizer_power);
  my(ray, values, class_log, sign_log, signed_class_log);

  if(modulus_norm == 1,
    return([0, gamma_record[2], modulus_norm, [], [], 8]));

  ray = bnrinit(K, [reduced_modulus, [1, 0]], 1);
  values = bnrL1(ray, , 6);
  class_log = bnrisprincipal(ray, reduced_ideal, 0);

  \\ Every reduced finite modulus here is (2^e).  The positive integer
  \\ 2^e-1 represents Kopp's residue/sign class R.
  my(integer_modulus = sqrtint(modulus_norm));
  stabilizer_power = 8 / integer_modulus;
  assert_equal( \
    Str("REDUCED_MODULUS_NORM_", first, "_", second), \
    integer_modulus^2, \
    modulus_norm \
  );
  sign_log = bnrisprincipal(
    ray, idealhnf(K, integer_modulus - 1), 0
  );
  signed_class_log = vector(#ray.cyc, index, \
    (class_log[index] + sign_log[index]) % ray.cyc[index]);
  signed_class_log = signed_class_log~;

  [
    stabilizer_power * real(
      partial_zeta_derivative(ray, values, class_log)
      - partial_zeta_derivative(ray, values, signed_class_log)
    ),
    gamma_record[2],
    modulus_norm,
    Vec(class_log),
    Vec(sign_log),
    stabilizer_power
  ];
};

\\ The fibre of the full two-place ray group over the one-place ray
\\ group has order two, hence Kopp's exponent n=2/|fibre| is one.
kopp_exponent = 2 / (ray8_both.no / ray8_one.no);
assert_equal("KOPP_EXPONENT", kopp_exponent, 1);

orbit_seen = Map();
orbit_count = 0;
orbit_lengths = List();
for(first = 0, 7, \
  for(second = 0, 7, \
    my(key = Str(first, ",", second)); \
    if(!mapisdefined(orbit_seen, key), \
      my(a = first, b = second, orbit_length = 0); \
      orbit_count++; \
      while(!mapisdefined(orbit_seen, Str(a, ",", b)), \
        mapput(orbit_seen, Str(a, ",", b), orbit_count); \
        orbit_length++; \
        my(next_a = (Lz[1,1]*a + Lz[1,2]*b) % 8); \
        my(next_b = (Lz[2,1]*a + Lz[2,2]*b) % 8); \
        a = next_a; \
        b = next_b; \
      ); \
      listput(orbit_lengths, orbit_length); \
    ); \
  ) \
);
assert_equal("LZ_ORBIT_COUNT", orbit_count, 22);
assert_equal("LZ_ORBIT_LENGTHS", vecsort(Vec(orbit_lengths)), \
  concat([1], vector(21, k, 3)));

magnitude_label(record) =
{
  my(modulus_norm = record[3], class_log = record[4]);
  if(modulus_norm == 64,
    if(class_log == [0, 0], return("A"));
    if(class_log == [0, 1], return("A_INVERSE"));
    if(class_log == [1, 0], return("D_INVERSE"));
    if(class_log == [1, 1], return("D"));
    error(Str("unexpected ray-8 class log: ", class_log));
  );
  if(modulus_norm == 16,
    if(class_log == [0], return("X_SQUARED"));
    if(class_log == [1], return("X_SQUARED_INVERSE"));
    error(Str("unexpected ray-4 class log: ", class_log));
  );
  if(modulus_norm == 4, return("ONE"));
  error(Str("unexpected reduced modulus norm: ", modulus_norm));
};

magnitude_counts = Map();
for(first = 0, 7, \
  for(second = 0, 7, \
    if(first != 0 || second != 0, \
      my(record = difference_derivative(first, second)); \
      my(label = magnitude_label(record)); \
      my(count = if(mapisdefined(magnitude_counts, label), \
        mapget(magnitude_counts, label), 0)); \
      mapput(magnitude_counts, label, count + 1); \
      print( \
        "CHARACTERISTIC=", first, ",", second, \
        " POSITIVE_LIFT=", record[2], \
        " REDUCED_MODULUS_NORM=", record[3], \
        " CLASS_LOG=", record[4], \
        " SIGN_LOG=", record[5], \
        " STABILIZER_POWER=", record[6], \
        " MAGNITUDE_LABEL=", label, \
        " LOG_SQUARE=", record[1] \
      ); \
    ); \
  ) \
);

for(label_index = 1, 7, \
  my(labels = ["A", "A_INVERSE", "D", "D_INVERSE", \
    "X_SQUARED", "X_SQUARED_INVERSE", "ONE"]); \
  my(expected = if(label_index <= 4, 12, \
    if(label_index <= 6, 6, 3))); \
  assert_equal(Str("MAGNITUDE_COUNT_", labels[label_index]), \
    mapget(magnitude_counts, labels[label_index]), expected); \
);
print("EXACT_QUADRATIC_INVERSE_FOURIER_MAGNITUDE_TABLE=1");

quit();
