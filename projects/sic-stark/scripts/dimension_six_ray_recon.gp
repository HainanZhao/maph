\\ Preliminary ray arithmetic for the dimension-six canonical form.
\\ This script is exploratory: it determines the group structures and
\\ separates characteristics whose associated principal ideals are coprime
\\ to the level from the singular strata at 2 and 3.

default(realprecision, 80);

K = bnfinit(y^2 - 5*y + 1, 1);
print("PARI_VERSION=", version());
print("BASE_DISCRIMINANT=", K.disc);
print("BASE_CLASS_NUMBER=", K.no);
print("BASE_BNFCERTIFY=", bnfcertify(K));
print("BASE_FUNDAMENTAL_UNITS=", K.fu);

Rfinite = bnrinit(K, 6, 1);
\\ PARI orders the roots increasingly; [1,0] selects beta' < 1.
Rone = bnrinit(K, [6, [1, 0]], 1);
Rboth = bnrinit(K, [6, [1, 1]], 1);
print("RAY_6_FINITE_STRUCTURE=", Rfinite.cyc);
print("RAY_6_INFINITY_2_STRUCTURE=", Rone.cyc);
print("RAY_6_BOTH_INFINITIES_STRUCTURE=", Rboth.cyc);

beta = Mod(y, y^2 - 5*y + 1);
beta_conjugate = (5-sqrt(21))/2;

audit_characteristics() =
{
  my(ptilde, element, norm_element, coprime_to_six, ray_log);
  for(p = 0, 5,
    for(q = 0, 5,
      if(p == 0 && q == 0, next());
      ptilde = p;
      while(q*beta_conjugate-ptilde <= 0, ptilde -= 6);
      element = q*beta-ptilde;
      norm_element = ptilde^2-5*ptilde*q+q^2;
      coprime_to_six = gcd(abs(norm_element), 6) == 1;
      if(coprime_to_six,
        ray_log = lift(
          bnrisprincipal(Rone, idealhnf(K, element), 0)[1]
        );
        print(
          "CHAR_", p, "_", q,
          " LIFT=", ptilde,
          " NORM=", norm_element,
          " COPRIME=1 LOG=", ray_log
        ),
        print(
          "CHAR_", p, "_", q,
          " LIFT=", ptilde,
          " NORM=", norm_element,
          " COPRIME=0"
        )
      )
    )
  )
};
audit_characteristics();

print("ONE_INFINITY_CLASS_FIELD_POLYNOMIAL=", bnrclassfield(Rone,,1));
print("FINITE_STARK_POLYNOMIAL=", bnrstark(Rfinite));

quit();
