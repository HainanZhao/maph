\\ Independent PARI/GP audit for the dimension-four SIC--Stark paper.
default(realprecision, 80);

print("PARI_VERSION=", version());

P = x^4 - x^2 - 1;
L = bnfinit(P, 1);
print("L_POLYNOMIAL=", P);
print("L_SIGNATURE=", L.sign);
print("L_DISCRIMINANT=", L.disc);
print("L_CLASS_NUMBER=", L.no);
print("L_CLASS_GROUP=", L.cyc);
print("L_REGULATOR=", L.reg);
print("L_FUNDAMENTAL_UNITS=", L.fu);
print("L_INTEGRAL_BASIS=", L.zk);

K = bnfinit(y^2 - y - 1, 1);
print("K_POLYNOMIAL=", y^2 - y - 1);
print("K_DISCRIMINANT=", K.disc);
print("K_CLASS_NUMBER=", K.no);
print("K_REGULATOR=", K.reg);

R1 = bnrinit(K, [4, [0, 1]], 1);
R2 = bnrinit(K, [4, [1, 1]], 1);
print("RAY_4_INFINITY_2_STRUCTURE=", R1.cyc);
print("RAY_4_BOTH_INFINITIES_STRUCTURE=", R2.cyc);

phi = (1 + sqrt(5.0))/2;
u = phi + sqrt(phi);
print("TARGET_UNIT_NUMERIC=", u);
print("TARGET_UNIT_LOG=", log(abs(u)));
print("EXPECTED_REGULATOR=", log((1+sqrt(5))/2) * log(abs(u)));

quit();
