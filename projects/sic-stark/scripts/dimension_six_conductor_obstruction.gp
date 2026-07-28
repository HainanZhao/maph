\\ Exact conductor-lowering obstruction for the primitive d=6 packet.
\\
\\ The relevant one-real-place ray group for K=Q(sqrt(21)) and modulus
\\ (6) is C6.  Its proper divisor moduli give only the trivial group and
\\ C2.  Thus conductor lowering can recover the quadratic character but
\\ cannot recover either primitive order-six character.

assert_equal(actual, expected, label) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
}

y = 'y;
K = bnfinit(y^2 - 5*y + 1, 1);
assert_equal(bnfcertify(K), 1, "BNF_CERTIFIED");

infinite_part = [0, 1];
R1 = bnrinit(K, [1, infinite_part], 1);
R2 = bnrinit(K, [2, infinite_part], 1);
R3 = bnrinit(K, [3, infinite_part], 1);
R6 = bnrinit(K, [6, infinite_part], 1);

assert_equal(R1.no, 1, "RAY_ORDER_MOD_1");
assert_equal(R2.no, 1, "RAY_ORDER_MOD_2");
assert_equal(R3.no, 2, "RAY_ORDER_MOD_3");
assert_equal(R6.no, 6, "RAY_ORDER_MOD_6");

assert_equal(R1.cyc, [], "RAY_STRUCTURE_MOD_1");
assert_equal(R2.cyc, [], "RAY_STRUCTURE_MOD_2");
assert_equal(R3.cyc, [2], "RAY_STRUCTURE_MOD_3");
assert_equal(R6.cyc, [6], "RAY_STRUCTURE_MOD_6");

conductor3 = bnrconductor(R3);
conductor6 = bnrconductor(R6);
assert_equal(idealnorm(K, conductor3[1]), 3, "CONDUCTOR_NORM_MOD_3");
assert_equal(conductor3[2], infinite_part, "CONDUCTOR_INFINITY_MOD_3");
assert_equal(idealnorm(K, conductor6[1]), 36, "CONDUCTOR_NORM_MOD_6");
assert_equal(conductor6[2], infinite_part, "CONDUCTOR_INFINITY_MOD_6");

\\ Write g for a generator of C6 and chi_k(g)=zeta_6^k.
\\ The reduction C6 -> C2 has kernel <g^2>, of order three.
\\ A character descends precisely when chi_k(g^2)=1, i.e. 3 | k.
descends_to_mod3(k) = ((2*k) % 6 == 0);
assert_equal(descends_to_mod3(1), 0, "CHI_1_PRIMITIVE");
assert_equal(descends_to_mod3(3), 1, "CHI_3_DESCENDS");
assert_equal(descends_to_mod3(5), 0, "CHI_5_PRIMITIVE");

print("BNF_CERTIFIED=1");
print("ONE_PLACE_RAY_STRUCTURES=mod1:trivial,mod2:trivial,mod3:C2,mod6:C6");
print("MOD3_CONDUCTOR_NORM=", idealnorm(K, conductor3[1]));
print("MOD6_CONDUCTOR_NORM=", idealnorm(K, conductor6[1]));
print("REDUCTION_KERNEL=C3=<g^2>");
print("DESCENDING_CHARACTERS_AMONG_ODD_INDICES=[chi_3]");
print("PRIMITIVE_CHARACTERS_KILLED_BY_CONDUCTOR_LOWERING=[chi_1,chi_5]");
