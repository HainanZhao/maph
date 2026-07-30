\\ Exact lattice probe for Q(sqrt(14)), p_7 infinity_2.
\\ Research-only: the separate Arb script freezes the selected cone.

run_probe() =
{
  my(K = bnfinit(y^2 - 14, 1));
  my(finite_ideal = [7, 0; 0, 1]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(ray_generator = idealhnf(K, ray.gen[1]));
  my(epsilon = Mod(15 + 4*y, y^2 - 14));

  print("RAY_GENERATOR=", ray_generator);
  print("RAY_GENERATOR_LOG=",
    bnrisprincipal(ray, ray_generator, 0));
  print("EPSILON=", epsilon);
  print("EPSILON_NORM=", nfeltnorm(K, epsilon));
  print("EPSILON_MINUS_ONE_MOD_P7=",
    nfeltreduce(K, epsilon - 1, finite_ideal));

  for(class_log = 0, 5,
    my(class_ideal = idealpow(K, ray_generator, class_log));
    my(b_lattice = idealdiv(K, finite_ideal, class_ideal));
    my(best_element = 0, best_index = 10^99);
    my(best_coordinates = 0, best_matrix = 0);
    for(u = -80, 80,
      for(v = -80, 80,
        if(u || v,
          my(element_coordinates = b_lattice * [u, v]~);
          my(element = nfbasistoalg(K, element_coordinates));
          my(embeddings = nfeltembed(K, element));
          if(embeddings[1] > 0 && embeddings[2] > 0,
            my(epsilon_coordinates =
              nfalgtobasis(K, element * epsilon));
            my(cone_lattice =
              matconcat([element_coordinates, epsilon_coordinates]));
            my(cone_index =
              abs(matdet(cone_lattice) / matdet(b_lattice)));
            if(cone_index < best_index,
              best_element = element;
              best_index = cone_index;
              best_coordinates = [u, v];
              best_matrix = cone_lattice;
            );
          );
        );
      );
    );
    print("CLASS_LOG=", class_log);
    print("CLASS_IDEAL=", class_ideal);
    print("B_LATTICE=", b_lattice);
    print("BEST_ELEMENT=", best_element);
    print("BEST_B_COORDINATES=", best_coordinates);
    print("BEST_CONE_MATRIX=", best_matrix);
    print("CONE_INDEX=", best_index);
  );
};

run_probe();
