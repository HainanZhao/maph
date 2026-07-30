\\ Exact cone-lattice probe for RQ-002057.

default(parisizemax, 2000000000);

run_probe() =
{
  my(K = bnfinit(y^2 - y - 14, 1));
  my(finite_ideal = [9, 3; 0, 3]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(ray_generator = idealhnf(K, ray.gen[1]));
  my(unit = K.fu[1]);
  my(unit_embeddings = nfeltembed(K, unit));
  if(unit_embeddings[1] < 0 || unit_embeddings[2] < 0,
    unit = unit^2
  );
  if(nfeltembed(K, unit)[1] < 1, unit = unit^-1);

  print("RAY_GENERATOR=", ray_generator);
  print("RAY_GENERATOR_LOG=",
    bnrisprincipal(ray, ray_generator, 0));
  print("EPSILON=", unit);
  print("EPSILON_EMBEDDINGS=", nfeltembed(K, unit));
  print("EPSILON_NORM=", nfeltnorm(K, unit));
  print("EPSILON_MINUS_ONE_MOD_FINITE=",
    nfeltreduce(K, unit - 1, finite_ideal));

  for(class_log = 0, 5,
    my(class_ideal = idealpow(K, ray_generator, class_log));
    my(b_lattice = idealdiv(K, finite_ideal, class_ideal));
    my(best_element = 0, best_index = 10^99);
    my(best_coordinates = 0, best_matrix = 0);
    for(u = -300, 300,
      for(v = -300, 300,
        if(u || v,
          my(element_coordinates = b_lattice * [u, v]~);
          my(element = nfbasistoalg(K, element_coordinates));
          my(embeddings = nfeltembed(K, element));
          if(embeddings[1] > 0 && embeddings[2] > 0,
            my(unit_coordinates =
              nfalgtobasis(K, element * unit));
            my(cone_lattice =
              matconcat([element_coordinates, unit_coordinates]));
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
    print("BEST_CONE_MATRIX_IN_B_COORDINATES=",
      b_lattice^-1 * best_matrix);
    print("AFFINE_ONE_SHIFT_IN_B_COORDINATES=",
      b_lattice^-1 * [1, 0]~);
    print("CONE_INDEX=", best_index);
  );
};

run_probe();
