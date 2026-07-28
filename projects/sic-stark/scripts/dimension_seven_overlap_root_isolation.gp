\\ Exact root isolation for the recognized class polynomial of the sixteen
\\ distinct squared normalized d=7 principal overlaps.

default(realprecision, 100);

P = x^16 + (-37 - 28*y)*x^15 + (1212 + 854*y)*x^14 \
  + (-20685 - 14630*y)*x^13 + (210371 + 148750*y)*x^12 \
  + (-1313872 - 929054*y)*x^11 \
  + (5031845 + 3558044*y)*x^10 \
  + (-11531249 - 8153832*y)*x^9 \
  + (15288774 + 10810788*y)*x^8 \
  + (-11531249 - 8153832*y)*x^7 \
  + (5031845 + 3558044*y)*x^6 \
  + (-1313872 - 929054*y)*x^5 \
  + (210371 + 148750*y)*x^4 \
  + (-20685 - 14630*y)*x^3 + (1212 + 854*y)*x^2 \
  + (-37 - 28*y)*x + 1;

A = rnfequation(y^2 - 2, P);
K = bnfinit(y^2 - 2, 1);
relative_factors = nffactor(K, P)[, 1];

intervals = List(); labels = List();
listput(intervals, [43513/10^6,43514/10^6]); listput(labels, "2_2");
listput(intervals, [79508/10^6,79509/10^6]); listput(labels, "1_4");
listput(intervals, [80124/10^6,80125/10^6]); listput(labels, "1_3");
listput(intervals, [104688/10^6,104689/10^6]); listput(labels, "1_2");
listput(intervals, [146404/10^6,146405/10^6]); listput(labels, "1_1");
listput(intervals, [169377/10^6,169378/10^6]); listput(labels, "0_6");
listput(intervals, [315227/10^6,315228/10^6]); listput(labels, "0_5");
listput(intervals, [671533/10^6,671534/10^6]); listput(labels, "0_4");
listput(intervals, [1489129/10^6,1489130/10^6]); listput(labels, "0_3");
listput(intervals, [3172313/10^6,3172314/10^6]); listput(labels, "0_2");
listput(intervals, [5903986/10^6,5903987/10^6]); listput(labels, "0_1");
listput(intervals, [6830385/10^6,6830386/10^6]); listput(labels, "2_6");
listput(intervals, [9552165/10^6,9552166/10^6]); listput(labels, "3_6");
listput(intervals, [12480646/10^6,12480647/10^6]); listput(labels, "4_4");
listput(intervals, [12577346/10^6,12577347/10^6]); listput(labels, "3_5");
listput(intervals, [22981630/10^6,22981631/10^6]); listput(labels, "4_5");

print("RELATIVE_POLYNOMIAL=", P);
print("ABSOLUTE_DEGREE=", poldegree(A));
print("ABSOLUTE_IRREDUCIBLE=", polisirreducible(A));
print("TOTAL_REAL_ROOTS=", polsturm(A));
factor_degrees = vector(#relative_factors, index, \
  poldegree(relative_factors[index]));
print("RELATIVE_FACTOR_DEGREES=", factor_degrees);

ray14_data = bnrinit(K, [[14, 0; 0, 14], [1, 0]], 1);
ray_plus_data = bnrinit(K, [[14, 6; 0, 2], [1, 0]], 1);
ray_minus_data = bnrinit(K, [[14, 8; 0, 2], [1, 0]], 1);
ray14 = bnrclassfield(ray14_data, , 2);
ray_plus = bnrclassfield(ray_plus_data, , 2);
ray_minus = bnrclassfield(ray_minus_data, , 2);

audit_factor_fields() =
{
  my(absolute_factor);
  for(index = 1, #relative_factors,
    absolute_factor = rnfequation(y^2 - 2, lift(relative_factors[index]));
    print("FACTOR_", index, "_DEGREE=", poldegree(relative_factors[index]));
    print("FACTOR_", index, "_MATCH_RAY14=", \
      #nfisisom(absolute_factor, ray14) > 0);
    print("FACTOR_", index, "_MATCH_RAY_PLUS=", \
      #nfisisom(absolute_factor, ray_plus) > 0);
    print("FACTOR_", index, "_MATCH_RAY_MINUS=", \
      #nfisisom(absolute_factor, ray_minus) > 0);
  );
};

audit_factor_fields();

print_intervals() =
{
  my(interval);
  for(index = 1, #labels,
    interval = intervals[index];
    print("OVERLAP_", labels[index], "_INTERVAL=", interval,
      " ROOT_COUNT=", polsturm(A, interval));
  );
};

print_intervals();

quit();
