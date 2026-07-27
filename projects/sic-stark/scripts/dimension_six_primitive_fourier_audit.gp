\\ Oriented Fourier audit for the primitive d=6 Stark packet.
\\
\\ This compares two independently constructed logarithm vectors:
\\   (1) Fourier inversion of imprimitive Hecke L_S leading terms for
\\       Cl_(6,infinity_2)(Q(sqrt(21))) = C6;
\\   (2) the six arithmetic-Frobenius conjugates of the exact signed
\\       overlap root.
\\
\\ Flag 6 in bnrL1 is essential: bit 2 retains the Euler factors at
\\ primes dividing the ray modulus.  Flag 4 instead returns primitive
\\ L-functions and gives the wrong full-modulus quadratic component.

default(realprecision, 100);
default(parisizemax, 4000000000);

K = bnfinit(y^2 - 5*y + 1, 1);
Rone = bnrinit(K, [6, [1, 0]], 1);
L_imprimitive = bnrL1(Rone, , 6);
L_primitive = bnrL1(Rone, , 4);

print("PARI_VERSION=", version());
print("ONE_INFINITY_RAY_GROUP=", Rone.cyc);

\\ Fourier inversion of Z_A'=zeta_A'-zeta_(R*A)'.
\\ For R=g^3, only odd characters survive and 2/|C6|=1/3.
ray_logs = vector(6);
compute_ray_logs() =
{
  my(total, exponent);
  for(class_index = 1, 6,
    total = 0;
    for(character_index = 1, #L_imprimitive,
      exponent = L_imprimitive[character_index][1][1];
      if(exponent % 2,
        total += exp(
          -2*Pi*I*exponent*(class_index-1)/6
        ) * L_imprimitive[character_index][2][2]
      )
    );
    ray_logs[class_index] = real(total)/3
  )
};
compute_ray_logs();

print("IMPRIMITIVE_LS_CHARACTER_DATA=", L_imprimitive);
print("FOURIER_INVERTED_DIFFERENCED_RAY_LOGS=", ray_logs);

\\ The primitive and imprimitive order-six characters agree.  The
\\ conductor-three quadratic character acquires the omitted Euler
\\ factor and its leading term is doubled.
order_six_euler_factor_ratios = vector(2, index, \
  L_imprimitive[index][2][2] / L_primitive[index][2][2]);
quadratic_euler_factor_ratio = \
  L_imprimitive[5][2][2] / L_primitive[5][2][2];
print("ORDER_SIX_IMPRIMITIVE_TO_PRIMITIVE_RATIOS=", \
  order_six_euler_factor_ratios);
print("QUADRATIC_IMPRIMITIVE_TO_PRIMITIVE_RATIO=", \
  quadratic_euler_factor_ratio);

Q = x^12 + 3*x^11 - 6*x^10 - 16*x^9 + 3*x^8 + 27*x^6 \
  + 3*x^4 - 16*x^3 - 6*x^2 + 3*x + 1;
H = nfinit(Q);
root = Mod(x, Q);
conjugates = nfgaloisconj(H);
arithmetic_frobenius = Mod(conjugates[5], Q);

\\ The canonical real embedding is isolated by x in (2.212,2.213).
root_embeddings = nfeltembed(H, root);
canonical_embedding = 0;
find_canonical_embedding() =
{
  for(index = 1, H.sign[1],
    if(
      root_embeddings[index] > 2212/1000 \
        && root_embeddings[index] < 2213/1000,
      canonical_embedding = index
    )
  )
};
find_canonical_embedding();
if(canonical_embedding == 0, error("canonical embedding not found"));

orbit = vector(6);
orbit_logs = vector(6);
orbit_element = root;
compute_orbit() =
{
  for(index = 1, 6,
    orbit[index] = orbit_element;
    orbit_logs[index] = 2*log(abs(
      nfeltembed(H, orbit_element)[canonical_embedding]
    ));
    orbit_element = subst(
      lift(arithmetic_frobenius),
      x,
      orbit_element
    )
  )
};
compute_orbit();

labels = ["x", "-z^-1", "-w^-1", "x^-1", "-z", "-w"];
print("FROBENIUS_ORBIT_LABELS=", labels);
print("ALGEBRAIC_FROBENIUS_LOGS=", orbit_logs);
print("LOG_VECTOR_MAXIMUM_RESIDUAL=", \
  vecmax(abs(ray_logs-orbit_logs)));

\\ Recover beta and the already-proved quadratic unit Y inside H.
beta_in_H = 1 - vecsum(orbit);
Y_in_H = orbit[1]*orbit[3]/orbit[2];
print("RECOVERED_BETA_MINPOLY=", minpoly(beta_in_H));
print("RECOVERED_LOWER_UNIT_MINPOLY=", minpoly(Y_in_H));
print("LOWER_RELATIVE_POLYNOMIAL_CHECK=", \
  Y_in_H^2-(beta_in_H-2)*Y_in_H+1 == 0);
print("FULL_ORBIT_NORM=", vecprod(orbit));

\\ The quadratic Fourier component is already unconditional:
\\ L_S'(0,chi_3)=Z_0-Z_1+Z_2=2 log(Y).
quadratic_analytic = L_imprimitive[5][2][2];
quadratic_algebraic = \
  orbit_logs[1]-orbit_logs[2]+orbit_logs[3];
print("QUADRATIC_ANALYTIC_COMPONENT=", quadratic_analytic);
print("QUADRATIC_ALGEBRAIC_COMPONENT=", quadratic_algebraic);
print("QUADRATIC_COMPONENT_RESIDUAL=", \
  quadratic_analytic-quadratic_algebraic);

\\ The whole remaining bridge is the following one complex equality.
\\ Its conjugate gives chi_5, and Fourier inversion together with the
\\ quadratic identity recovers all six ray logarithms.
zeta_six = exp(2*Pi*I/6);
primitive_analytic = L_imprimitive[1][2][2];
primitive_algebraic = \
  orbit_logs[1] + zeta_six*orbit_logs[2] \
  + zeta_six^2*orbit_logs[3];
print("PRIMITIVE_ORDER_SIX_ANALYTIC_COMPONENT=", primitive_analytic);
print("PRIMITIVE_ORDER_SIX_ALGEBRAIC_REGULATOR=", primitive_algebraic);
print("PRIMITIVE_ORDER_SIX_COMPONENT_RESIDUAL=", \
  primitive_analytic-primitive_algebraic);

if(order_six_euler_factor_ratios != [1, 1], \
  error("unexpected Euler factor on primitive order-six pair"));
if(abs(quadratic_euler_factor_ratio-2) > 1e-90, \
  error("quadratic Euler-factor ratio is not two"));
if(vecmax(abs(ray_logs-orbit_logs)) > 1e-90, \
  error("analytic and algebraic ray packets do not match"));
if(minpoly(beta_in_H) != x^2-5*x+1, \
  error("base unit recovery failed"));
if(minpoly(Y_in_H) != x^4-x^3-3*x^2-x+1, \
  error("lower unit recovery failed"));
if(Y_in_H^2-(beta_in_H-2)*Y_in_H+1 != 0, \
  error("lower relative polynomial failed"));
if(vecprod(orbit) != 1, error("primitive orbit is not a unit orbit"));

quit();
