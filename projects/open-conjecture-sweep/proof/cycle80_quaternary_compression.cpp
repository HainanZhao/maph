// C80 exact convention control for periodic quaternary Legendre pairs.
//
// The executable performs only the preregistered n=2 and n=6 controls.  It
// does not inspect any length-42 lift.  All arithmetic is integral pairs
// representing Gaussian integers.

#include <array>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

struct G {
  int re = 0;
  int im = 0;
};

G add(G a, G b) { return {a.re + b.re, a.im + b.im}; }
G sub(G a, G b) { return {a.re - b.re, a.im - b.im}; }
G conj(G a) { return {a.re, -a.im}; }
G mul(G a, G b) {
  return {a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re};
}
bool eq(G a, G b) { return a.re == b.re && a.im == b.im; }

const std::array<G, 4> alphabet = {{{1, 0}, {-1, 0}, {0, 1}, {0, -1}}};

std::vector<G> decode(unsigned code, int n) {
  std::vector<G> out(n);
  for (int j = 0; j < n; ++j) {
    out[j] = alphabet[code & 3U];
    code >>= 2U;
  }
  return out;
}

std::vector<G> paf(const std::vector<G>& c) {
  const int n = static_cast<int>(c.size());
  std::vector<G> out(n);
  for (int s = 0; s < n; ++s) {
    G total{};
    for (int j = 0; j < n; ++j) {
      total = add(total, mul(c[j], conj(c[(j + s) % n])));
    }
    out[s] = total;
  }
  return out;
}

std::vector<G> compress(const std::vector<G>& c, int d) {
  const int n = static_cast<int>(c.size());
  const int m = n / d;
  std::vector<G> out(m);
  for (int r = 0; r < m; ++r) {
    for (int t = 0; t < d; ++t) out[r] = add(out[r], c[r + t * m]);
  }
  return out;
}

bool check_compressions(const std::vector<G>& a, const std::vector<G>& b) {
  const int n = static_cast<int>(a.size());
  const auto pa = paf(a);
  const auto pb = paf(b);
  for (int d = 1; d <= n; ++d) {
    if (n % d != 0) continue;
    const int m = n / d;
    const auto ca = paf(compress(a, d));
    const auto cb = paf(compress(b, d));
    for (int s = 0; s < m; ++s) {
      G rhs{};
      for (int v = 0; v < d; ++v) rhs = add(rhs, add(pa[s + v * m], pb[s + v * m]));
      if (!eq(add(ca[s], cb[s]), rhs)) return false;
    }
  }
  return true;
}

struct Result {
  unsigned long long count = 0;
  bool compression_ok = true;
};

Result control(int n) {
  const unsigned words = 1U << (2 * n);
  Result r;
  for (unsigned ai = 0; ai < words; ++ai) {
    const auto a = decode(ai, n);
    const auto pa = paf(a);
    for (unsigned bi = 0; bi < words; ++bi) {
      const auto b = decode(bi, n);
      const auto pb = paf(b);
      bool pair = true;
      for (int s = 1; s < n; ++s) {
        if (!eq(add(pa[s], pb[s]), {-2, 0})) {
          pair = false;
          break;
        }
      }
      if (!pair) continue;
      ++r.count;
      r.compression_ok = r.compression_ok && check_compressions(a, b);
      if (!r.compression_ok) return r;
    }
  }
  return r;
}

int main() {
  const Result n2 = control(2);
  const Result n6 = control(6);
  if (!n2.compression_ok || !n6.compression_ok) {
    std::cerr << "compression identity control failed\n";
    return EXIT_FAILURE;
  }

  std::cout
      << "{\"status\":\"PASS\",\"convention\":\"periodic_PAF\","
      << "\"control_pair_counts\":{\"2\":" << n2.count << ",\"6\":" << n6.count
      << "},\"compression_coordinate_domain\":{\"d6\":49,\"d7\":64},"
      << "\"length42_compressed_pair_paf\":{\"d6\":{\"zero\":74,\"nonzero\":-12},"
      << "\"d7\":{\"zero\":72,\"nonzero\":-14}}}\n";
  return EXIT_SUCCESS;
}
