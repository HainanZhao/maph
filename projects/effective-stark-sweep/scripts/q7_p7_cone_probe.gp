\\ Research probe for exact Yamamoto cone data in the
\\ Q(sqrt(7)), p_7 infinity_2 case.  This script is not a certificate:
\\ it finds small totally positive cone generators before the separate
\\ exact enumeration and Arb enclosure stages.

run_probe() =
{
  my(K = bnfinit(y^2 - 7, 1));
  my(finite_ideal = [7, 0; 0, 1]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(ray_generator = idealhnf(K, ray.gen[1]));
  my(epsilon = Mod(8 + 3*y, y^2 - 7));

  for(class_log = 0, 5,
    my(class_ideal = idealpow(K, ray_generator, class_log));
    my(b_lattice = idealdiv(K, finite_ideal, class_ideal));
    my(best_element = 0, best_index = 10^99, best_coordinates = 0);

    for(u = -20, 20,
      for(v = -20, 20,
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
    print("CONE_INDEX=", best_index);
  );
};

run_probe();
