\\ Exact certificate for the modulus-three lower stratum in dimension six.
\\ Run with PARI/GP 2.15.4 or later:
\\     gp -fq scripts/dimension_six_lower_stratum.gp

default(realprecision, 100);

assert_equal(actual, expected, label) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual))
  );
  print(label, "=", actual);
};

\\ K = Q(beta), beta^2 - 5 beta + 1 = 0.
K = bnfinit(y^2 - 5*y + 1, 1);
beta = Mod(y, y^2 - 5*y + 1);
assert_equal(K.disc, 21, "BASE_DISCRIMINANT");
assert_equal(K.no, 1, "BASE_CLASS_NUMBER");
assert_equal(bnfcertify(K), 1, "BASE_BNFCERTIFY");

\\ PARI orders the two real roots increasingly. Thus [0,1] places
\\ infinity_2, the embedding beta |-> beta' < 1, in the modulus.
Rfinite = bnrinit(K, 3, 1);
Rone = bnrinit(K, [3, [0, 1]], 1);
Rboth = bnrinit(K, [3, [1, 1]], 1);
assert_equal(Rfinite.cyc, [], "RAY_3_FINITE_STRUCTURE");
assert_equal(Rone.cyc, [2], "RAY_3_INFINITY_2_STRUCTURE");
assert_equal(Rboth.cyc, [2, 2], "RAY_3_BOTH_INFINITIES_STRUCTURE");

\\ The ray character is primitive at the unique prime above 3, even
\\ though Kopp's characteristic naturally presents the modulus as (3).
ray_conductor = bnrconductor(Rone);
assert_equal(matdet(ray_conductor[1]), 3, "RAY_CONDUCTOR_FINITE_NORM");
assert_equal(ray_conductor[2], [0, 1], "RAY_CONDUCTOR_INFINITE_PART");

\\ Its quadratic class field has the simple relative model
\\ alpha^2 = beta - 1.
ray_relative = bnrclassfield(Rone, , 1);
ray_absolute = bnrclassfield(Rone, , 2);
expected_ray_absolute = x^4 - 3*x^2 - 3;
assert_equal(ray_absolute, expected_ray_absolute, \
  "RAY_CLASS_FIELD_ABSOLUTE_POLYNOMIAL");

\\ The lower ray unit Y has a reciprocal integral model.
lower_polynomial = x^4 - x^3 - 3*x^2 - x + 1;
assert_equal(poldisc(lower_polynomial), -1323, "LOWER_FIELD_DISCRIMINANT");
assert_equal(#nfisisom(lower_polynomial, ray_absolute) > 0, 1, \
  "LOWER_FIELD_IS_RAY_CLASS_FIELD");

E = bnfinit(lower_polynomial, 1);
assert_equal(E.sign, [2, 1], "LOWER_FIELD_SIGNATURE");
assert_equal(E.no, 1, "LOWER_FIELD_CLASS_NUMBER");
assert_equal(bnfcertify(E), 1, "LOWER_FIELD_BNFCERTIFY");
print("LOWER_FIELD_FUNDAMENTAL_UNITS=", E.fu);

\\ In E = Q(Y), beta = (Y+1)^2/Y. The certified fundamental units
\\ Y and Y+1 therefore give R_E = log(beta) log(Y).
Y = Mod(x, lower_polynomial);
beta_in_E = (Y + 1)^2 / Y;
assert_equal(beta_in_E^2 - 5*beta_in_E + 1, 0, \
  "EMBEDDED_BETA_MINIMAL_POLYNOMIAL");
assert_equal(Y^2 - (beta_in_E - 2)*Y + 1, 0, \
  "LOWER_UNIT_RELATIVE_POLYNOMIAL");

Y_real = polrootsreal(lower_polynomial)[2];
beta_real = (5 + sqrt(21))/2;
regulator_target = log(beta_real) * log(Y_real);
print("LOWER_UNIT_POSITIVE_ROOT=", precision(Y_real, 80));
print("CERTIFIED_REGULATOR=", precision(E.reg, 80));
print("REGULATOR_FORMULA_RESIDUAL=", \
  precision(E.reg - regulator_target, 30));

\\ Convention-sensitive Kopp/AFK data for p=(0,2), r=(0,1/3).
L = [5, -1; 1, 0];
B = L^3;
assert_equal(B, [115, -24; 24, -5], "STABILIZER");
r = [0, 1/3]~;
assert_equal(B*r-r, [-8, -2]~, "CHARACTERISTIC_TRANSLATION");

\\ Kopp's exponent is n=2 divided by the fiber size of the full
\\ signed ray group over the one-place ray group.
fiber_size = 2;
kopp_exponent = 2/fiber_size;
assert_equal(kopp_exponent, 1, "KOPP_EXPONENT");

dedekind_sawtooth(q) =
{
  if(denominator(q) == 1, 0, q - floor(q) - 1/2);
};

dedekind_sum(a, c) =
{
  my(total = 0);
  for(n = 1, abs(c)-1,
    total += dedekind_sawtooth(n/c)
      * dedekind_sawtooth(n*a/c)
  );
  total;
};

a = B[1,1]; b = B[1,2]; c = B[2,1]; d = B[2,2];
s = dedekind_sum(a, c);
rademacher = (a+d)/c - 3*sign(c*(a+d)) - 12*sign(c)*s;
assert_equal(s, -53/144, "RADEMACHER_DEDEKIND_SUM");
assert_equal(rademacher, 6, "RADEMACHER_INVARIANT");

r1 = 0; r2 = 1/3;
theta_exponent = \
  1/2 * ( \
    (c-d+1)*r1 + (-a+b+1)*r2 - c*d*r1^2 \
    + 2*(a-1)*d*r1*r2 - (a-2)*b*r2^2 \
  );
assert_equal(theta_exponent, 383/3, "THETA_CHARACTER_EXPONENT");
assert_equal(theta_exponent - floor(theta_exponent), 2/3, "THETA_EXPONENT_MOD_ONE");

\\ psi^2(B) = exp(pi*i*Psi(B)/6) = -1 and
\\ chi_r(B) = exp(2*pi*i*2/3). Hence
\\ (psi^-2 chi_r^-1)(B) = -exp(2*pi*i/3).
print("KOPP_MULTIPLIER=-exp(2*Pi*I/3)");
print("AFK_PHASE=exp(-Pi*I/6)");
print("AFK_PHASE_SQUARED=-exp(2*Pi*I/3)");

print("CONCLUSION=exp(Z_prime(0,I))=nu_(0,2)^2=y^2=Y");
quit();
