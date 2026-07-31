\\ Exact Cycle-106 conductor and ray-class transport gates for B5-015.
default(parisizemax, 2000000000);
K = bnfinit(y^2 - 2, 1);
f_source = [7, 0; 0, 7];
f_target = [14, 0; 0, 7];
q = idealdiv(K, f_target, f_source);
r_source = bnrinit(K, [f_source, [1, 0]], 1);
r_target = bnrinit(K, [f_target, [1, 0]], 1);
M = bnrmap(r_target, r_source);

print("SOURCE_FINITE_NORM=", idealnorm(K, f_source));
print("TARGET_FINITE_NORM=", idealnorm(K, f_target));
print("QUOTIENT_IDEAL=", q);
print("QUOTIENT_NORM=", idealnorm(K, q));
print("QUOTIENT_FACTOR=", idealfactor(K, q));
print("SOURCE_RAY_CYC=", Vec(r_source.cyc));
print("TARGET_RAY_CYC=", Vec(r_target.cyc));
print("SOURCE_RAY_GENERATOR=", r_source.gen);
print("TARGET_RAY_GENERATOR=", r_target.gen);
print("SOURCE_SIGN_LOG=", bnrisprincipal(r_source, idealhnf(K, 6), 0)[1]);
print("TARGET_SIGN_LOG=", bnrisprincipal(r_target, idealhnf(K, 13), 0)[1]);
print("RAY_MAP=", M);
print("RAY_MAP_MATRIX=", M[1]);
print("RAY_MAP_TARGET_IDENTITY=", bnrmap(M, [0]));
print("RAY_MAP_TARGET_GENERATOR=", bnrmap(M, [1]));
print("RAY_MAP_TARGET_SIGN=", bnrmap(M, [3]));
print("RQ000039_TRANSPORT_GATES_1_2=PASS");
