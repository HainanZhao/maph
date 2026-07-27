\\ Dimension-five ray-group and Stark-polynomial audit.
default(realprecision, 80);

K = bnfinit(y^2 - 4*y + 1, 1);
print("PARI_VERSION=", version());
print("BASE_DISCRIMINANT=", K.disc);
print("BASE_CLASS_NUMBER=", K.no);
print("BASE_BNFCERTIFY=", bnfcertify(K));
print("BASE_FUNDAMENTAL_UNITS=", K.fu);

Rfinite = bnrinit(K, 5, 1);
\\ PARI orders the real roots of y^2-4y+1 increasingly.  Thus [1,0]
\\ selects infinity_2(sqrt(3))=-sqrt(3).
Rone = bnrinit(K, [5, [1, 0]], 1);
Rboth = bnrinit(K, [5, [1, 1]], 1);
print("RAY_5_FINITE_STRUCTURE=", Rfinite.cyc);
print("RAY_5_INFINITY_2_STRUCTURE=", Rone.cyc);
print("RAY_5_BOTH_INFINITIES_STRUCTURE=", Rboth.cyc);

beta = Mod(y, y^2 - 4*y + 1);
\\ For (p,q) modulo 5, choose ptilde congruent to p such that
\\ q*(2-sqrt(3))-ptilde is positive.  The following function returns
\\ [ptilde, discrete logarithm in Cl_(5)infinity_2 = C8].
positive_class_log(p, q) =
{
  my(ptilde = p, beta_conjugate = 2-sqrt(3), discrete_log);
  while(q*beta_conjugate-ptilde <= 0, ptilde -= 5);
  discrete_log = lift(
    bnrisprincipal(Rone, idealhnf(K, q*beta-ptilde), 0)[1]
  );
  [ptilde, discrete_log];
};

print("POSITIVE_CLASS_LOG_P01=", positive_class_log(0, 1));
print("POSITIVE_CLASS_LOG_P02=", positive_class_log(0, 2));
print("POSITIVE_CLASS_LOG_P03=", positive_class_log(0, 3));
print("POSITIVE_CLASS_LOG_P04=", positive_class_log(0, 4));
print("POSITIVE_CLASS_LOG_P10=", positive_class_log(1, 0));
print("POSITIVE_CLASS_LOG_P11=", positive_class_log(1, 1));
print("POSITIVE_CLASS_LOG_P12=", positive_class_log(1, 2));
print("POSITIVE_CLASS_LOG_P13=", positive_class_log(1, 3));
print("POSITIVE_CLASS_LOG_P14=", positive_class_log(1, 4));
print("POSITIVE_CLASS_LOG_P20=", positive_class_log(2, 0));
print("POSITIVE_CLASS_LOG_P21=", positive_class_log(2, 1));
print("POSITIVE_CLASS_LOG_P22=", positive_class_log(2, 2));
print("POSITIVE_CLASS_LOG_P23=", positive_class_log(2, 3));
print("POSITIVE_CLASS_LOG_P24=", positive_class_log(2, 4));
print("POSITIVE_CLASS_LOG_P30=", positive_class_log(3, 0));
print("POSITIVE_CLASS_LOG_P31=", positive_class_log(3, 1));
print("POSITIVE_CLASS_LOG_P32=", positive_class_log(3, 2));
print("POSITIVE_CLASS_LOG_P33=", positive_class_log(3, 3));
print("POSITIVE_CLASS_LOG_P34=", positive_class_log(3, 4));
print("POSITIVE_CLASS_LOG_P40=", positive_class_log(4, 0));
print("POSITIVE_CLASS_LOG_P41=", positive_class_log(4, 1));
print("POSITIVE_CLASS_LOG_P42=", positive_class_log(4, 2));
print("POSITIVE_CLASS_LOG_P43=", positive_class_log(4, 3));
print("POSITIVE_CLASS_LOG_P44=", positive_class_log(4, 4));
ray_generator_prime = idealprimedec(K, 3)[1];
print("RAW_CHARACTERISTIC_BASIS_PRIME_ABOVE_3_LOG=", lift(bnrisprincipal(Rone, ray_generator_prime, 0)[1]));

Hrelative = bnrclassfield(Rone,,1);
print("ONE_INFINITY_CLASS_FIELD_POLYNOMIAL=", Hrelative);
print("FINITE_STARK_POLYNOMIAL=", bnrstark(Rfinite));

s = beta - 2;
P = (x^8 - (8+5*s)*x^7 + (53+30*s)*x^6 \
    - (156+90*s)*x^5 + (225+130*s)*x^4 \
    - (156+90*s)*x^3 + (53+30*s)*x^2 \
    - (8+5*s)*x + 1);
print("RECIPROCAL_STARK_UNIT_POLYNOMIAL=", P);

V = (x^4 - (8+5*s)*x^3 + (49+30*s)*x^2 \
    - (132+75*s)*x + (121+70*s));
print("TRACE_POLYNOMIAL=", V);
print("TRACE_LIFT_IDENTITY=", x^4 * subst(V, x, x + 1/x) - P);

Pabsolute = rnfpolredbest(K, P, 2);
Habsolute = rnfpolredbest(K, Hrelative, 2);
print("STARK_UNIT_FIELD_ABSOLUTE_POLYNOMIAL=", Pabsolute);
print("RAY_FIELD_ABSOLUTE_POLYNOMIAL=", Habsolute);
print("ABSOLUTE_FIELD_ISOMORPHISM_COUNT=", #nfisisom(Pabsolute, Habsolute));

quit();
