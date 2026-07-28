\\ Identify the normal closure governing the d=6 primitive character.
\\ Run with PARI/GP 2.15.4 or later:
\\     gp -fq scripts/dimension_six_normal_closure.gp

default(realprecision, 80);
default(parisizemax, 4000000000);

K = bnfinit(y^2 - 5*y + 1, 1);
Rboth = bnrinit(K, [6, [1, 1]], 1);
normal_polynomial = rnfpolredbest(K, bnrclassfield(Rboth, , 1), 2);

print("PARI_VERSION=", version());
print("BOTH_INFINITY_RAY_GROUP_OVER_K=", Rboth.cyc);
print("NORMAL_CLOSURE_POLYNOMIAL=", normal_polynomial);
print("NORMAL_CLOSURE_DEGREE=", poldegree(normal_polynomial));
print("NORMAL_CLOSURE_SIGNATURE=", nfinit(normal_polynomial).sign);

G = galoisinit(normal_polynomial);
if(type(G) == "t_INT", error("galoisinit failed to recognize the degree-24 field as Galois"));
print("NORMAL_CLOSURE_IS_GALOIS=1");
group_id = galoisidentify(G);
print("NORMAL_CLOSURE_GROUP_ID=", group_id);
print("NORMAL_CLOSURE_GROUP_ORDER=", #G.group);
if(group_id != [24, 8], error("unexpected normal-closure group"));
print("NORMAL_CLOSURE_GROUP_NAME=C3_semidirect_D4");
print("KATAYAMA_KIDA_D4_ISOCLINISM_TEST=0");
print("PRIMITIVE_FAITHFUL_QUOTIENT=D6");
print("PRIMITIVE_FAITHFUL_QUOTIENT_COMMUTATOR_ORDER=3");

quit();
