\\ Fourier reconstruction of the sixteen maximal-order ray-(24)
\\ partial-zeta differences used after conductor lowering.
\\
\\ Warning: these are not the partial zetas of the nonmaximal order
\\ O_3 modulo 8.  Equality of the two ray class groups does not identify
\\ their partial-zeta functions.  The bridge to the d=8 cocycle is the
\\ three-factor conductor-lowering formula audited in
\\ explore_dimension_eight_conductor_lowering.gp.

default(realprecision, 100);

assert_small(label, actual, tolerance) =
{
  if(abs(actual) > tolerance,
    error(Str(label, ": residual ", actual, " exceeds ", tolerance)));
  print(label, "=", actual);
};

K = bnfinit(y^2 - y - 1, 1);
ray24 = bnrinit(K, [24, [1, 0]], 1);
L_values = bnrL1(ray24, , 6);

find_l_derivative(character) =
{
  for(k = 1, #L_values,
    if(L_values[k][1] == character, return(L_values[k][2][2])));
  error(Str("character not found: ", character));
};

maximal_dual_character(a, b, c) =
{
  [(a - 2*b) % 4, b % 2, (c - a) % 2];
};

order_character_value(a, b, c, A, B, C) =
{
  I^(a*A) * (-1)^(b*B + c*C);
};

fourier_term(a, b, A, B, C) =
{
  my(character = maximal_dual_character(a, b, 1));
  my(value = order_character_value(a, b, 1, A, B, C));
  conj(value) * find_l_derivative(character);
};

print("PARI_VERSION=", version());
print("MAXIMAL_RAY_24_GROUP=C4 x C2 x <R>");
print("FOURIER_CONVENTION=L_chi=sum_C chi(C) zeta_C");

differences = vector(16);
for(class_index = 0, 15, \
{
  my(A = class_index % 4);
  my(B = (class_index \ 4) % 2);
  my(C = class_index \ 8);
  my(difference_derivative = 0);
  for(character_index = 0, 7, \
    difference_derivative += fourier_term(character_index % 4, \
      character_index \ 4, A, B, C));
  difference_derivative /= 8;
  differences[class_index + 1] = difference_derivative;
  assert_small(Str("CLASS_[", A, ",", B, ",", C, "]_IMAGINARY_RESIDUAL"), \
    imag(difference_derivative), 1e-90);
  print("CLASS_[", A, ",", B, ",", C, "]_DPRIME=", \
    difference_derivative);
  print("CLASS_[", A, ",", B, ",", C, "]_EXP_DPRIME=", \
    exp(difference_derivative));
});

for(class_index = 1, 8, \
  assert_small(Str("R_RECIPROCITY_RESIDUAL_", class_index), \
    differences[class_index] + differences[class_index + 8], 1e-90));

quit();
