\\ Check the arithmetic hypotheses of Roblot's cyclic-sextic theorem for
\\ the dimension-six one-infinite-place ray field.

default(realprecision, 80);
default(parisizemax, 4000000000);

K = bnfinit(y^2 - 5*y + 1, 1);
Rone = bnrinit(K, [6, [1, 0]], 1);
Hrelative = bnrclassfield(Rone, , 1);
Habsolute = rnfpolredbest(K, Hrelative, 2);
H = bnfinit(Habsolute, 1);

beta = Mod(y, y^2 - 5*y + 1);
lower_relative = x^2 - (beta-2)*x + 1;
trace_relative = x^3 + (2-5*beta)*x^2 \
  + (35*beta-11)*x + (13-78*beta);
lower_absolute = rnfpolredbest(K, lower_relative, 2);
trace_absolute = rnfpolredbest(K, trace_relative, 2);
Lower = bnfinit(lower_absolute, 1);

print("PARI_VERSION=", version());
print("SEXTIC_RAY_FIELD_CLASS_NUMBER=", H.no);
print("SEXTIC_RAY_FIELD_BNFCERTIFY=", bnfcertify(H));
print("SEXTIC_RAY_FIELD_SIGNATURE=", H.sign);
print("MAXIMAL_TOTALLY_REAL_COMPONENT_SIGNATURE=", nfinit(trace_absolute).sign);
print("QUADRATIC_COMPONENT_SIGNATURE=", nfinit(lower_absolute).sign);
print("QUADRATIC_COMPONENT_DISCRIMINANT=", Lower.disc);
print("QUADRATIC_COMPONENT_CLASS_NUMBER=", Lower.no);
print("QUADRATIC_COMPONENT_BNFCERTIFY=", bnfcertify(Lower));
print("QUADRATIC_COMPONENT_FUNDAMENTAL_UNITS=", Lower.fu);
print("QUADRATIC_COMPONENT_REGULATOR=", Lower.reg);
print("QUADRATIC_COMPONENT_RELATIVE_DISCRIMINANT=", idealfactor(K, rnfdisc(K, lower_relative)[1]));
print("CUBIC_COMPONENT_RELATIVE_DISCRIMINANT=", idealfactor(K, rnfdisc(K, trace_relative)[1]));
print("FULL_RAY_FIELD_RELATIVE_DISCRIMINANT=", idealfactor(K, rnfdisc(K, Hrelative)[1]));

prime_two = idealprimedec(K, 2)[1];
prime_three = idealprimedec(K, 3)[1];
print("PRIME_2_IN_K=", prime_two);
print("PRIME_3_IN_K=", prime_three);
print("QUADRATIC_COMPONENT_AT_2=", idealfactor(nfinit(lower_absolute), 2));
print("QUADRATIC_COMPONENT_AT_3=", idealfactor(nfinit(lower_absolute), 3));
print("CUBIC_COMPONENT_AT_2=", idealfactor(nfinit(trace_absolute), 2));
print("CUBIC_COMPONENT_AT_3=", idealfactor(nfinit(trace_absolute), 3));

quit();
