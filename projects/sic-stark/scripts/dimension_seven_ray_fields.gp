\\ Exact one-place ray fields for the six conductor-lowered d=7 strata.

default(realprecision, 100);

K = bnfinit(y^2 - 2, 1);
certified = bnfcertify(K);
moduli = List();
listput(moduli, [14, 0; 0, 14]);
listput(moduli, [7, 0; 0, 7]);
listput(moduli, [14, 6; 0, 2]);
listput(moduli, [14, 8; 0, 2]);
listput(moduli, [7, 3; 0, 1]);
listput(moduli, [7, 4; 0, 1]);

print("PARI_VERSION=", version());
print("BNF_CERTIFIED=", certified);

print_stratum(index) =
{
  modulus = moduli[index];
  ray = bnrinit(K, [modulus, [1, 0]], 1);
  polynomial = bnrclassfield(ray, , 2);
  print("STRATUM_", index, "_MODULUS=", modulus);
  print("STRATUM_", index, "_RAY_STRUCTURE=", ray.cyc);
  print("STRATUM_", index, "_ABSOLUTE_CLASS_FIELD=", polynomial);
};

for(index = 1, #moduli, print_stratum(index));

\\ The two nontrivial quadratic strata have positive Stark units whose
\\ logarithms are the corresponding differenced derivatives.  Their
\\ reciprocal traces and minimal polynomials are exact:
\\
\\ u_+ + u_+^-1 = 1+2sqrt(2),
\\ u_- + u_-^-1 = 4+4sqrt(2).
unit_plus_polynomial = x^4 - 2*x^3 - 5*x^2 - 2*x + 1;
unit_minus_polynomial = x^4 - 8*x^3 - 14*x^2 - 8*x + 1;

print("QUADRATIC_STRATUM_PLUS_UNIT_POLYNOMIAL=", unit_plus_polynomial);
print("QUADRATIC_STRATUM_MINUS_UNIT_POLYNOMIAL=", unit_minus_polynomial);
print("PLUS_UNIT_POLYNOMIAL_IRREDUCIBLE=", polisirreducible(unit_plus_polynomial));
print("MINUS_UNIT_POLYNOMIAL_IRREDUCIBLE=", polisirreducible(unit_minus_polynomial));

\\ Numerically recognized relative class polynomials for the scalar strata.
\\ They are reciprocal and have coefficients in Z[sqrt(2)].
scalar_seven_polynomial = \
  x^6 + (-10 - 6*y)*x^5 + (58 + 40*y)*x^4 \
  + (-129 - 90*y)*x^3 + (58 + 40*y)*x^2 \
  + (-10 - 6*y)*x + 1;

scalar_fourteen_polynomial = \
  x^12 + (-32 - 22*y)*x^11 + (486 + 344*y)*x^10 \
  + (-3314 - 2344*y)*x^9 + (11956 + 8454*y)*x^8 \
  + (-25046 - 17710*y)*x^7 + (31899 + 22556*y)*x^6 \
  + (-25046 - 17710*y)*x^5 + (11956 + 8454*y)*x^4 \
  + (-3314 - 2344*y)*x^3 + (486 + 344*y)*x^2 \
  + (-32 - 22*y)*x + 1;

scalar_seven_absolute = rnfequation(y^2 - 2, scalar_seven_polynomial);
scalar_fourteen_absolute = rnfequation(y^2 - 2, scalar_fourteen_polynomial);
ray_seven = bnrinit(K, [[7, 0; 0, 7], [1, 0]], 1);
ray_fourteen = bnrinit(K, [[14, 0; 0, 14], [1, 0]], 1);
ray_seven_absolute = bnrclassfield(ray_seven, , 2);
ray_fourteen_absolute = bnrclassfield(ray_fourteen, , 2);

print("SCALAR_7_RELATIVE_POLYNOMIAL=", scalar_seven_polynomial);
print("SCALAR_14_RELATIVE_POLYNOMIAL=", scalar_fourteen_polynomial);
print("SCALAR_7_ABSOLUTE_IRREDUCIBLE=", \
  polisirreducible(scalar_seven_absolute));
print("SCALAR_14_ABSOLUTE_IRREDUCIBLE=", \
  polisirreducible(scalar_fourteen_absolute));
print("SCALAR_7_FIELD_MATCH=", \
  #nfisisom(scalar_seven_absolute, ray_seven_absolute) > 0);
print("SCALAR_14_FIELD_MATCH=", \
  #nfisisom(scalar_fourteen_absolute, ray_fourteen_absolute) > 0);

quit();
