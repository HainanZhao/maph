\\ Exact cone-lattice probe for the B route of RQ-000458.

default(parisizemax, 2000000000);

run_probe() =
{
  my(K = bnfinit(y^2 - 14, 1));
  my(finite_ideal = [12, 0; 0, 6]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(epsilon = Mod(15 + 4*y, y^2 - 14));
  my(unit_order = 0);
  my(representatives = [
    [1, 0; 0, 1],
    [7, 0; 0, 1],
    [47, 25; 0, 1],
    [113, 50; 0, 1],
    [11, 5; 0, 1],
    [5, 3; 0, 1],
    [11, 6; 0, 1],
    [5, 2; 0, 1]
  ]);

  print("RAY_STRUCTURE=", Vec(ray.cyc));
  print("RAY_GENERATORS=", ray.gen);
  for(index = 1, #ray.gen,
    print("RAY_GENERATOR_", index, "_HNF=",
      idealhnf(K, ray.gen[index]));
    print("RAY_GENERATOR_", index, "_LOG=",
      bnrisprincipal(ray, ray.gen[index], 0));
  );
  print("EPSILON=", epsilon);
  print("EPSILON_NORM=", nfeltnorm(K, epsilon));
  for(exponent = 1, 64,
    if(!unit_order
       && nfeltreduce(
            K, epsilon^exponent - 1, finite_ideal) == [0, 0]~,
      unit_order = exponent);
  );
  print("EPSILON_ORDER_MOD_FINITE=", unit_order);
  print("CONGRUENCE_UNIT=", epsilon^unit_order);

  for(second_log = 0, 1,
    for(first_log = 0, 3,
      my(class_ideal = representatives[
        1 + first_log + 4*second_log]);
      if(Vec(bnrisprincipal(ray, class_ideal, 0))
           != [first_log, second_log],
        error("small representative has wrong ray log"));
      my(b_lattice = idealdiv(K, finite_ideal, class_ideal));
      my(best_element = 0, best_index = 10^99);
      my(best_coordinates = 0, best_matrix = 0);
      for(u = -120, 120,
        for(v = -120, 120,
          if(u || v,
            my(element_coordinates = b_lattice * [u, v]~);
            my(element = nfbasistoalg(K, element_coordinates));
            my(embeddings = nfeltembed(K, element));
            if(embeddings[1] > 0 && embeddings[2] > 0,
              my(epsilon_coordinates =
                nfalgtobasis(K, element * epsilon));
              my(cone_lattice = matconcat(
                [element_coordinates, epsilon_coordinates]
              ));
              my(cone_index = abs(
                matdet(cone_lattice) / matdet(b_lattice)
              ));
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
      print("CLASS_LOG=[", first_log, ",", second_log, "]");
      print("CLASS_IDEAL=", class_ideal);
      print("B_LATTICE=", b_lattice);
      print("BEST_ELEMENT=", best_element);
      print("BEST_B_COORDINATES=", best_coordinates);
      print("BEST_CONE_MATRIX=", best_matrix);
      print("CONE_INDEX=", best_index);
    );
  );
};

run_probe();
