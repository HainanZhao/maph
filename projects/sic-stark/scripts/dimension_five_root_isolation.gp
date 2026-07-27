\\ Certified real-root isolation for the dimension-five Stark packet.
default(realprecision, 100);

Qabs = x^32-16*x^30+95*x^28-260*x^26+355*x^24-348*x^22 \
  +388*x^20-300*x^18+195*x^16-300*x^14+388*x^12 \
  -348*x^10+355*x^8-260*x^6+95*x^4-16*x^2+1;

intervals = [424835/10^6,424836/10^6;481476/10^6,481477/10^6;506963/10^6,506964/10^6;782390/10^6,782391/10^6;1278133/10^6,1278134/10^6;1972526/10^6,1972527/10^6;2076946/10^6,2076947/10^6;2353849/10^6,2353850/10^6];
labels = ["w^-1", "z^-1", "x^-1", "y^-1", "y", "x", "z", "w"];

print("POLYNOMIAL=", Qabs);
print("TOTAL_REAL_ROOTS=", polsturm(Qabs));
for(k = 1, matsize(intervals)[1], print("ISOLATING_INTERVAL_", labels[k], "=", [intervals[k,1], intervals[k,2]], " ROOT_COUNT=", polsturm(Qabs, [intervals[k,1], intervals[k,2]])));
for(k = 1, matsize(intervals)[1], print("NEGATIVE_ISOLATING_INTERVAL_", labels[k], "=", [-intervals[k,2], -intervals[k,1]], " ROOT_COUNT=", polsturm(Qabs, [-intervals[k,2], -intervals[k,1]])));

print("ALL_REAL_ROOTS=", polrootsreal(Qabs));
quit();
