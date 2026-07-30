\\ Exact cone data for RQ-000108.

default(parisizemax, 2000000000);

run_probe() =
{
  my(Kpol = y^2 - y - 1, K = bnfinit(Kpol, 1));
  my(finite_ideal = [15, 6; 0, 3]);
  my(ray = bnrinit(K, [finite_ideal, [1, 0]], 1));
  my(epsilon = Mod(y + 1, Kpol), unit_order = 0);
  my(representatives = [
    [1, 0; 0, 1],
    [11, 7; 0, 1],
    [29, 23; 0, 1],
    [11, 3; 0, 1]
  ]);
  print("RAY_STRUCTURE=", Vec(ray.cyc));
  print("RAY_GENERATOR=", ray.gen[1]);
  print("EPSILON=", epsilon);
  print("EPSILON_NORM=", nfeltnorm(K, epsilon));
  for(exponent = 1, 64,
    if(!unit_order
       && nfeltreduce(
            K, epsilon^exponent - 1, finite_ideal) == [0, 0]~,
      unit_order = exponent));
  print("EPSILON_ORDER_MOD_FINITE=", unit_order);
  for(class_log = 0, 3,
    my(class_ideal = representatives[class_log + 1]);
    if(lift(bnrisprincipal(ray, class_ideal, 0)[1]) != class_log,
      error("small representative has wrong log"));
    my(b_lattice = idealdiv(K, finite_ideal, class_ideal));
    my(best_index = 10^99, best_element = 0);
    my(best_coordinates = 0, best_matrix = 0);
    for(u = -100, 100,
      for(v = -100, 100,
        if(u || v,
          my(coords = b_lattice * [u, v]~);
          my(element = nfbasistoalg(K, coords));
          my(embeddings = nfeltembed(K, element));
          if(embeddings[1] > 0 && embeddings[2] > 0,
            my(second = nfalgtobasis(K, element * epsilon));
            my(matrix = matconcat([coords, second]));
            my(index_value =
              abs(matdet(matrix) / matdet(b_lattice)));
            if(index_value < best_index,
              best_index = index_value;
              best_element = element;
              best_coordinates = [u, v];
              best_matrix = matrix);
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
