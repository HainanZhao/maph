// C80 exact balance-and-norm census for compressed quaternary coordinates.
//
// This is deliberately an upper-interface census: it imposes coordinate
// domains, original sequence sums, and the compressed zero-shift PAF total,
// but not the nonzero compressed PAF equations.  Thus it cannot be used as a
// construction, a lift, or a nonexistence statement.

#include <boost/multiprecision/cpp_int.hpp>

#include <cstdlib>
#include <iostream>
#include <map>
#include <tuple>
#include <vector>

using boost::multiprecision::cpp_int;

struct Point {
  int re;
  int im;
  int norm;
};

using Key = std::tuple<int, int, int>;
using Table = std::map<Key, cpp_int>;

std::vector<Point> coordinate_domain(int d) {
  std::vector<Point> out;
  for (int x = -d; x <= d; ++x) {
    for (int y = -d; y <= d; ++y) {
      if (std::abs(x) + std::abs(y) > d) continue;
      if ((x + y - d) % 2 != 0) continue;
      out.push_back({x, y, x * x + y * y});
    }
  }
  return out;
}

Table ordered_profiles(int d, int m) {
  const auto domain = coordinate_domain(d);
  Table current;
  current[{0, 0, 0}] = 1;
  for (int place = 0; place < m; ++place) {
    Table next;
    for (const auto& [key, multiplicity] : current) {
      const auto [re, im, norm] = key;
      for (const Point& p : domain) {
        next[{re + p.re, im + p.im, norm + p.norm}] += multiplicity;
      }
    }
    current.swap(next);
  }
  return current;
}

cpp_int pair_count(const Table& profiles, int target_norm) {
  cpp_int total = 0;
  for (int a_norm = 0; a_norm <= target_norm; ++a_norm) {
    const auto a = profiles.find({0, 0, a_norm});
    const auto b = profiles.find({1, 1, target_norm - a_norm});
    if (a != profiles.end() && b != profiles.end()) total += a->second * b->second;
  }
  return total;
}

void report(int d, int m, int target_norm) {
  const auto domain = coordinate_domain(d);
  const Table profiles = ordered_profiles(d, m);
  const cpp_int raw = pair_count(profiles, target_norm);
  std::cout << "{\"d\":" << d << ",\"m\":" << m
            << ",\"coordinate_domain\":" << domain.size()
            << ",\"profile_states\":" << profiles.size()
            << ",\"balance_norm_pair_upper_bound\":\"" << raw << "\"}";
}

int main() {
  // The normalization in the frozen C80 target is sum(A)=0, sum(B)=1+i.
  // The compressed PAF zero rows are 74 and 72 respectively.
  std::cout << "{\"status\":\"PASS\",\"scope\":\"balance_and_zero_shift_only\","
            << "\"normalization\":{\"A\":\"0\",\"B\":\"1+i\"},\"results\":[";
  report(6, 7, 74);
  std::cout << ",";
  report(7, 6, 72);
  std::cout << "]}\n";
  return EXIT_SUCCESS;
}
