#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

namespace {

constexpr int MAX_WORDS = 8;
using Mask = std::array<std::uint64_t, MAX_WORDS>;

struct Predicate {
  int k;
  int p;
  int c;
  int q;
  int words;
  Mask full{};
  std::vector<Mask> bad;

  Predicate(int k_in, int p_in, int c_in)
      : k(k_in), p(p_in), c(c_in), q(p * c), words((q + 63) / 64), bad(q) {
    if (words > MAX_WORDS) throw std::runtime_error("mask capacity exceeded");
    for (int word = 0; word < words; ++word) full[static_cast<std::size_t>(word)] = ~0ULL;
    if (q % 64) full[static_cast<std::size_t>(words - 1)] = (1ULL << (q % 64)) - 1ULL;
    for (int speed = 0; speed < q; ++speed) {
      for (int time = 0; time < q; ++time) {
        int residue = static_cast<int>((static_cast<long long>(time) * speed) % q);
        int distance = std::min(residue, q - residue);
        if ((k + 1) * distance < q) {
          bad[static_cast<std::size_t>(speed)][static_cast<std::size_t>(time / 64)] |=
              1ULL << (time % 64);
        }
      }
    }
  }

  bool improper(std::vector<int> const& speed) const {
    for (int omitted = 0; omitted < k; ++omitted) {
      int divisor = c;
      for (int coordinate = 0; coordinate < k; ++coordinate) {
        if (coordinate != omitted) divisor = std::gcd(divisor, speed[static_cast<std::size_t>(coordinate)]);
      }
      if (divisor > 1) return false;
    }
    Mask covered{};
    for (int value : speed) {
      Mask const& add = bad[static_cast<std::size_t>(value)];
      for (int word = 0; word < words; ++word) covered[static_cast<std::size_t>(word)] |= add[static_cast<std::size_t>(word)];
    }
    for (int word = 0; word < words; ++word) {
      if (covered[static_cast<std::size_t>(word)] != full[static_cast<std::size_t>(word)]) return false;
    }
    return true;
  }
};

std::string key(std::vector<int> const& tuple) {
  std::string result;
  for (int value : tuple) {
    if (!result.empty()) result.push_back(',');
    result += std::to_string(value);
  }
  return result;
}

void increment_digits(std::vector<int>& digits, int base) {
  for (int& digit : digits) {
    if (++digit < base) return;
    digit = 0;
  }
}

bool has_improper_lift(Predicate const& lifted, std::vector<int> const& base,
                        std::vector<int>* certificate = nullptr) {
  std::vector<int> digits(base.size(), 0);
  std::uint64_t count = 1;
  for (std::size_t i = 0; i < base.size(); ++i) count *= static_cast<std::uint64_t>(lifted.c);
  std::vector<int> speed(base.size());
  for (std::uint64_t row = 0; row < count; ++row) {
    for (std::size_t i = 0; i < base.size(); ++i) speed[i] = base[i] + lifted.p * digits[i];
    if (lifted.improper(speed)) {
      if (certificate) *certificate = digits;
      return true;
    }
    increment_digits(digits, lifted.c);
  }
  return false;
}

std::set<std::string> fused_h11(Predicate const& base, Predicate const& lifted) {
  std::set<std::string> retained;
  for (int x = 1; x < 11; ++x) {
    for (int y = 1; y < 11; ++y) {
      for (int z = 1; z < 11; ++z) {
        std::vector<int> tuple{x, y, z};
        if (base.improper(tuple) && has_improper_lift(lifted, tuple)) retained.insert(key(tuple));
      }
    }
  }
  return retained;
}

std::set<std::string> raw_h11(Predicate const& base, Predicate const& lifted) {
  std::set<std::string> retained;
  for (int x = 1; x < 11; ++x) {
    for (int y = 1; y < 11; ++y) {
      for (int z = 1; z < 11; ++z) {
        std::vector<int> tuple{x, y, z};
        if (!base.improper(tuple)) continue;
        for (int dx = 0; dx < 4; ++dx) for (int dy = 0; dy < 4; ++dy) for (int dz = 0; dz < 4; ++dz) {
          std::vector<int> lift{x + 11 * dx, y + 11 * dy, z + 11 * dz};
          if (lifted.improper(lift)) retained.insert(key(tuple));
        }
      }
    }
  }
  return retained;
}

}  // namespace

int main(int argc, char** argv) try {
  if (argc != 3) {
    std::cerr << "usage: lrc_fused_first_lift BASE_EXPONENTS OUTPUT\n";
    return 2;
  }
  auto start = std::chrono::steady_clock::now();
  Predicate h11_base(3, 11, 1);
  Predicate h11_lift(3, 11, 4);
  std::set<std::string> fused = fused_h11(h11_base, h11_lift);
  std::set<std::string> raw = raw_h11(h11_base, h11_lift);
  if (fused != raw) throw std::runtime_error("H11 fused/raw retained-set mismatch");

  std::ifstream input(argv[1]);
  if (!input) throw std::runtime_error("cannot open base tuple input");
  std::vector<std::vector<int>> exponent_rows;
  for (std::string line; std::getline(input, line);) {
    std::istringstream stream(line);
    std::vector<int> row;
    for (int value; stream >> value;) row.push_back(value);
    if (row.empty()) continue;
    if (row.size() != 6) throw std::runtime_error("invalid p47 base row");
    exponent_rows.push_back(std::move(row));
  }
  if (exponent_rows.size() != 53) throw std::runtime_error("p47 base input is not the frozen 53-row control");

  Predicate p47_base(6, 47, 1);
  Predicate p47_lift(6, 47, 7);
  std::vector<std::vector<int>> base_rows;
  for (auto const& representative : exponent_rows) {
    std::vector<int> base = representative;
    if (!p47_base.improper(base)) throw std::runtime_error("frozen p47 input is not l=1 improper");
    base_rows.push_back(std::move(base));
  }
  std::vector<std::vector<int>> certificates(base_rows.size());
  std::vector<char> retained(base_rows.size(), 0);
  std::atomic<std::size_t> next(0);
  std::vector<std::thread> workers;
  for (int worker = 0; worker < 3; ++worker) {
    workers.emplace_back([&] {
      while (true) {
        std::size_t index = next.fetch_add(1);
        if (index >= base_rows.size()) return;
        std::vector<int> certificate;
        if (has_improper_lift(p47_lift, base_rows[index], &certificate)) {
          certificates[index] = std::move(certificate);
          retained[index] = 1;
        }
      }
    });
  }
  for (auto& worker : workers) worker.join();

  std::ofstream output(argv[2]);
  if (!output) throw std::runtime_error("cannot open output");
  std::size_t p47_retained = 0;
  for (std::size_t index = 0; index < exponent_rows.size(); ++index) {
    if (!retained[index]) continue;
    ++p47_retained;
    for (int value : exponent_rows[index]) output << value << ' ';
    output << "| ";
    for (int value : certificates[index]) output << value << ' ';
    output << '\n';
  }
  if (!output) throw std::runtime_error("output failure");
  auto elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
  std::cout << "h11_raw_tuples=64000\n";
  std::cout << "h11_retained_raw_bases=" << raw.size() << '\n';
  std::cout << "h11_fused_equal_raw=1\n";
  std::cout << "p47_base_orbits=" << base_rows.size() << '\n';
  std::cout << "p47_retained_orbits=" << p47_retained << '\n';
  std::cout << "p47_eliminated_orbits=" << (base_rows.size() - p47_retained) << '\n';
  std::cout << "wall_seconds=" << elapsed << '\n';
  return 0;
} catch (std::exception const& error) {
  std::cerr << "error: " << error.what() << '\n';
  return 1;
}
