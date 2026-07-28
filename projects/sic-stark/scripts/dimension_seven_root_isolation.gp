\\ Exact real-root isolation for the recognized d=7 scalar unit packets.

default(realprecision, 100);

P7 = x^6 + (-10 - 6*y)*x^5 + (58 + 40*y)*x^4 \
  + (-129 - 90*y)*x^3 + (58 + 40*y)*x^2 \
  + (-10 - 6*y)*x + 1;

P14 = x^12 + (-32 - 22*y)*x^11 + (486 + 344*y)*x^10 \
  + (-3314 - 2344*y)*x^9 + (11956 + 8454*y)*x^8 \
  + (-25046 - 17710*y)*x^7 + (31899 + 22556*y)*x^6 \
  + (-25046 - 17710*y)*x^5 + (11956 + 8454*y)*x^4 \
  + (-3314 - 2344*y)*x^3 + (486 + 344*y)*x^2 \
  + (-32 - 22*y)*x + 1;

A7 = rnfequation(y^2 - 2, P7);
A14 = rnfequation(y^2 - 2, P14);

intervals7 = List(); labels7 = List();
listput(intervals7, [133387/10^6,133388/10^6]); listput(labels7, "class_4");
listput(intervals7, [163671/10^6,163672/10^6]); listput(labels7, "class_3");
listput(intervals7, [229797/10^6,229798/10^6]); listput(labels7, "class_5");
listput(intervals7, [4351649/10^6,4351650/10^6]); listput(labels7, "class_2");
listput(intervals7, [6109797/10^6,6109798/10^6]); listput(labels7, "class_0");
listput(intervals7, [7496977/10^6,7496978/10^6]); listput(labels7, "class_1");

intervals14 = List(); labels14 = List();
listput(intervals14, [22592/10^6,22593/10^6]); listput(labels14, "class_3_1");
listput(intervals14, [154316/10^6,154317/10^6]); listput(labels14, "class_2_0");
listput(intervals14, [189353/10^6,189354/10^6]); listput(labels14, "class_2_1");
listput(intervals14, [519217/10^6,519218/10^6]); listput(labels14, "class_4_0");
listput(intervals14, [600688/10^6,600689/10^6]); listput(labels14, "class_3_0");
listput(intervals14, [894502/10^6,894503/10^6]); listput(labels14, "class_4_1");
listput(intervals14, [1117939/10^6,1117940/10^6]); listput(labels14, "class_1_0");
listput(intervals14, [1664756/10^6,1664757/10^6]); listput(labels14, "class_0_1");
listput(intervals14, [1925975/10^6,1925976/10^6]); listput(labels14, "class_1_1");
listput(intervals14, [5281130/10^6,5281131/10^6]); listput(labels14, "class_5_0");
listput(intervals14, [6480169/10^6,6480170/10^6]); listput(labels14, "class_5_1");
listput(intervals14, [44262055/10^6,44262056/10^6]); listput(labels14, "class_0_0");

print("P7_ABSOLUTE_DEGREE=", poldegree(A7));
print("P14_ABSOLUTE_DEGREE=", poldegree(A14));
print("P7_TOTAL_REAL_ROOTS=", polsturm(A7));
print("P14_TOTAL_REAL_ROOTS=", polsturm(A14));

print_intervals(polynomial, intervals, labels, prefix) =
{
  my(interval);
  for(index = 1, #labels,
    interval = intervals[index];
    print(prefix, "_", labels[index], "_INTERVAL=", interval,
      " ROOT_COUNT=", polsturm(polynomial, interval));
  );
};

print_intervals(A7, intervals7, labels7, "P7");
print_intervals(A14, intervals14, labels14, "P14");

quit();
