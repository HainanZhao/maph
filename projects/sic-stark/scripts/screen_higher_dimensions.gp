\\ Coarse ray-group screen for later canonical dimensions.
\\
\\ When CANONICAL_ORDER_IS_MAXIMAL=0 this is only a maximal-order proxy:
\\ AFK uses the quadratic order of discriminant (d+1)(d-3), whereas
\\ bnrinit works with the maximal order of its fraction field.

default(parisizemax, 4000000000);
print("PARI_VERSION=", version());

group_order(cyclic_invariants) =
{
  my(result = 1);
  for(index = 1, #cyclic_invariants,
    result *= cyclic_invariants[index]
  );
  return(result);
};

screen() =
{
  my(canonical_discriminant, K, order_conductor_squared);
  my(finite_ray, one_place_ray);
  for(dimension = 4, 20,
    canonical_discriminant = (dimension+1)*(dimension-3);
    if(issquare(canonical_discriminant), next());
    K = bnfinit(x^2 - (dimension-1)*x + 1);
    order_conductor_squared = canonical_discriminant/K.disc;
    finite_ray = bnrinit(K, dimension, 1);
    one_place_ray = bnrinit(K, [dimension, [0, 1]], 1);
    print(
      "DIMENSION=", dimension,
      " CANONICAL_DISCRIMINANT=", canonical_discriminant,
      " FIELD_DISCRIMINANT=", K.disc,
      " CANONICAL_ORDER_IS_MAXIMAL=", order_conductor_squared == 1,
      " ORDER_CONDUCTOR_SQUARED=", order_conductor_squared,
      " CLASS_NUMBER=", K.no,
      " FINITE_RAY_STRUCTURE=", finite_ray.cyc,
      " ONE_PLACE_RAY_STRUCTURE=", one_place_ray.cyc,
      " ONE_PLACE_RAY_ORDER=", group_order(one_place_ray.cyc),
      " ABSOLUTE_RAY_FIELD_DEGREE_PROXY=", \
        2*group_order(one_place_ray.cyc)
    )
  );
};
screen();

quit();
