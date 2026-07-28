\\ Exact Sturm isolation for the sixteen primitive squared d=8 overlaps.

default(realprecision, 100);

relative_polynomial = \
  x^16 + (-56*y - 32)*x^15 + (2696*y + 1668)*x^14 \
  + (-70632*y - 43656)*x^13 + (1085616*y + 670940)*x^12 \
  + (-10068808*y - 6222872)*x^11 \
  + (55400584*y + 34239444)*x^10 \
  + (-169674744*y - 104864752)*x^9 \
  + (255738816*y + 158055290)*x^8 \
  + (-169674744*y - 104864752)*x^7 \
  + (55400584*y + 34239444)*x^6 \
  + (-10068808*y - 6222872)*x^5 \
  + (1085616*y + 670940)*x^4 \
  + (-70632*y - 43656)*x^3 + (2696*y + 1668)*x^2 \
  + (-56*y - 32)*x + 1;

absolute_polynomial = rnfequation(y^2 - y - 1, relative_polynomial);

assert_equal(label, actual, expected) =
{
  if(actual != expected,
    error(Str(label, ": expected ", expected, ", got ", actual)));
  print(label, "=", actual);
};

\\ [a,b,left numerator,right numerator,denominator]
windows = [ \
  0,1, 6910937, 6910938, 1000000; \
  0,3, 2061122, 2061123, 1000000; \
  0,5,  485172,  485173, 1000000; \
  0,7,  144698,  144699, 1000000; \
  1,1,  125112,  125113, 1000000; \
  1,2,   90044,   90045, 1000000; \
  1,3,   65762,   65763, 1000000; \
  1,4,   54831,   54832, 1000000; \
  1,5,   60665,   60666, 1000000; \
  2,3,   22955,   22956, 1000000; \
  2,7, 7992821, 7992822, 1000000; \
  3,6,16483891,16483892, 1000000; \
  3,7,11105600,11105601, 1000000; \
  4,5,18237810,18237811, 1000000; \
  4,7,15206346,15206347, 1000000; \
  5,5,43562131,43562132, 1000000 \
];

assert_equal("RELATIVE_DEGREE", poldegree(relative_polynomial), 16);
assert_equal("ABSOLUTE_DEGREE", poldegree(absolute_polynomial), 32);
assert_equal("ABSOLUTE_IRREDUCIBLE", \
  polisirreducible(absolute_polynomial), 1);
assert_equal("TOTAL_REAL_ROOT_COUNT", \
  polsturm(absolute_polynomial), 16);

for(row = 1, matsize(windows)[1], \
  left = windows[row, 3]/windows[row, 5]; \
  right = windows[row, 4]/windows[row, 5]; \
  assert_equal( \
    Str("ROOT_", windows[row, 1], "_", windows[row, 2], "_COUNT"), \
    polsturm(absolute_polynomial, [left, right]), \
    1 \
  ) \
);

assert_equal("ISOLATED_PRIMITIVE_ROOT_COUNT", matsize(windows)[1], 16);

quit();
