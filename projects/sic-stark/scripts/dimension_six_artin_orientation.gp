\\ Exact Artin-orientation certificate for the primitive d=6 ray packet.
\\
\\ The prime p=(4*beta+1), of norm 37, represents ray log 1 in
\\ Cl_(6,infinity_2)(K)=C6.  With the arithmetic Frobenius convention
\\ Frob_p(a)=a^37 on residue fields, its action on the canonical signed
\\ overlap root is the fifth nfgaloisconj automorphism, labeled -z^-1 by
\\ dimension_six_embedding_certificate.gp.

default(realprecision, 80);
default(parisizemax, 4000000000);

K = bnfinit(y^2 - 5*y + 1, 1);
Rone = bnrinit(K, [6, [1, 0]], 1);
beta = Mod(y, y^2 - 5*y + 1);
alpha = 4*beta + 1;
prime_ideal = idealhnf(K, alpha);
ray_log = lift(bnrisprincipal(Rone, prime_ideal, 0)[1]);

print("PARI_VERSION=", version());
print("PRIME_GENERATOR=", alpha);
print("PRIME_NORM=", idealnorm(K, prime_ideal));
print("PRIME_RAY_LOG=", ray_log);
print("ONE_INFINITY_RAY_GROUP=", Rone.cyc);

Q = x^12 + 3*x^11 - 6*x^10 - 16*x^9 + 3*x^8 + 27*x^6 \
  + 3*x^4 - 16*x^3 - 6*x^2 + 3*x + 1;
conjugates = nfgaloisconj(nfinit(Q));

\\ The canonical relative factor over K has X^5 coefficient beta-1.
P = x^6 + (beta-1)*x^5 + (1-beta)*x^4 \
  + (-4*beta-1)*x^3 + (1-beta)*x^2 + (beta-1)*x + 1;
print("SIGNED_RELATIVE_POLYNOMIAL=", P);

\\ At p=(4*beta+1), beta reduces to 9 modulo 37.
residue_characteristic = 37;
beta_residue = Mod(9, residue_characteristic);
P_residue = x^6 + (beta_residue-1)*x^5 \
  + (1-beta_residue)*x^4 + (-4*beta_residue-1)*x^3 \
  + (1-beta_residue)*x^2 + (beta_residue-1)*x + 1;
print("RELATIVE_POLYNOMIAL_MOD_37_IRREDUCIBLE=", \
  #factor(P_residue)[, 1] == 1);

labels = ["x", "-w^-1", "-w", "x^-1", "-z^-1", "-z"];
cycle_indices = vector(6);
cycle_labels = vector(6);
all_powers_matched = 1;

audit_frobenius_cycle() =
{
  my(frobenius_image, matching_index);
  for(power_index = 0, 5,
    frobenius_image = \
      Mod(x, P_residue)^(residue_characteristic^power_index);
    matching_index = 0;
    for(index = 1, #conjugates,
      if(
        Mod(Mod(conjugates[index], residue_characteristic), P_residue) \
          == frobenius_image,
        matching_index = index
      )
    );
    if(matching_index == 0, all_powers_matched = 0);
    cycle_indices[power_index+1] = matching_index;
    cycle_labels[power_index+1] = labels[matching_index]
  )
};
audit_frobenius_cycle();

print("ARITHMETIC_FROBENIUS_AUTOMORPHISM_INDEX=", cycle_indices[2]);
print("ARITHMETIC_FROBENIUS_CYCLE_INDICES=", cycle_indices);
print("ARITHMETIC_FROBENIUS_CYCLE_LABELS=", cycle_labels);
print("ALL_FROBENIUS_POWERS_MATCHED_EXACTLY=", all_powers_matched);

if(idealnorm(K, prime_ideal) != 37, error("wrong prime norm"));
if(ray_log != 1, error("prime does not orient the ray generator"));
if(#factor(P_residue)[, 1] != 1, error("residue polynomial reducible"));
if(cycle_indices != [1, 5, 2, 4, 6, 3], \
  error("unexpected Frobenius cycle"));
if(!all_powers_matched, error("unmatched Frobenius power"));

quit();
