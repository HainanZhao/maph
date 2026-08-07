// Exploratory rotation-system search; output is not proof until replayed and
// independently validated by the exact Python verifier.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>

using Rotation = std::vector<std::vector<int>>;

static int vertex(int x, int y, int z) { return (x * 3 + y) * 3 + z; }

static int face_count(const Rotation& rotation, std::vector<int>* lengths = nullptr) {
  std::array<std::array<bool, 36>, 36> seen{};
  int faces = 0;
  if (lengths) lengths->clear();
  for (int u = 0; u < 36; ++u) {
    for (int v : rotation[u]) {
      if (seen[u][v]) continue;
      ++faces;
      int a = u, b = v, length = 0;
      while (!seen[a][b]) {
        seen[a][b] = true;
        ++length;
        const auto& cyclic = rotation[b];
        auto position = std::find(cyclic.begin(), cyclic.end(), a);
        int c = cyclic[(position - cyclic.begin() + 1) % cyclic.size()];
        a = b;
        b = c;
      }
      if (lengths) lengths->push_back(length);
    }
  }
  return faces;
}

int main(int argc, char** argv) {
  std::uint64_t seed = argc > 1 ? std::stoull(argv[1]) : 20260807ULL;
  long long iterations = argc > 2 ? std::stoll(argv[2]) : 50000000LL;
  std::mt19937_64 random(seed);
  Rotation adjacency(36);
  const int dx[3] = {1, 0, 0};
  const int dy[3] = {0, 1, 0};
  const int dz[3] = {0, 0, 1};
  for (int x = 0; x < 4; ++x)
    for (int y = 0; y < 3; ++y)
      for (int z = 0; z < 3; ++z)
        for (int axis = 0; axis < 3; ++axis) {
          int xx = x + dx[axis], yy = y + dy[axis], zz = z + dz[axis];
          if (xx >= 4 || yy >= 3 || zz >= 3) continue;
          int u = vertex(x, y, z), v = vertex(xx, yy, zz);
          adjacency[u].push_back(v);
          adjacency[v].push_back(u);
        }

  int global_best = -1;
  Rotation best_rotation;
  std::vector<int> best_lengths;
  long long completed = 0;
  while (completed < iterations) {
    Rotation rotation = adjacency;
    for (auto& cyclic : rotation) std::shuffle(cyclic.begin(), cyclic.end(), random);
    int score = face_count(rotation);
    constexpr int tranche = 200000;
    for (int local = 0; local < tranche && completed < iterations; ++local, ++completed) {
      int u = random() % 36;
      auto& cyclic = rotation[u];
      int i = random() % cyclic.size();
      int j = random() % cyclic.size();
      if (i == j) continue;
      std::swap(cyclic[i], cyclic[j]);
      int candidate = face_count(rotation);
      double fraction = static_cast<double>(local) / tranche;
      double temperature = std::max(0.035, 1.4 * std::exp(-8.0 * fraction));
      bool accept = candidate >= score;
      if (!accept) {
        double uniform = (random() + 0.5) / (static_cast<double>(random.max()) + 1.0);
        accept = uniform < std::exp((candidate - score) / temperature);
      }
      if (accept) score = candidate;
      else std::swap(cyclic[i], cyclic[j]);
      if (score > global_best) {
        global_best = score;
        best_rotation = rotation;
        face_count(best_rotation, &best_lengths);
        std::sort(best_lengths.begin(), best_lengths.end());
        std::cerr << "best=" << global_best << " iteration=" << completed << " lengths=";
        for (int length : best_lengths) std::cerr << length << ',';
        std::cerr << '\n';
        if (global_best >= 35) {
          completed = iterations;
          break;
        }
      }
    }
  }
  std::cout << "ROTATION\n";
  for (int u = 0; u < 36; ++u) {
    std::cout << u << ':';
    for (int v : best_rotation[u]) std::cout << ' ' << v;
    std::cout << '\n';
  }
  return global_best >= 35 ? 0 : 1;
}
