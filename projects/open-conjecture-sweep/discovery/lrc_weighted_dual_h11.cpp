#include <algorithm>
#include <array>
#include <atomic>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <thread>
#include <vector>

namespace {
constexpr int K = 3, P = 11, C = 4, Q = 44, ITERATIONS = 20'000;
constexpr long long SCALE = 1LL << 20;
using Masks = std::array<std::array<std::uint64_t, C>, K>;

std::uint64_t make_mask(int speed, int modulus) {
  std::uint64_t result = 0;
  for (int time = 0; time < modulus; ++time) {
    int residue = time * speed % modulus;
    if ((K + 1) * std::min(residue, modulus - residue) < modulus) result |= 1ULL << time;
  }
  return result;
}

double dot(std::array<double, Q> const& weights, std::uint64_t mask) {
  double result = 0;
  while (mask) {
    int bit = __builtin_ctzll(mask);
    result += weights[static_cast<std::size_t>(bit)];
    mask &= mask - 1;
  }
  return result;
}

long long dot_integer(std::array<long long, Q> const& weights, std::uint64_t mask) {
  long long result = 0;
  while (mask) {
    int bit = __builtin_ctzll(mask);
    result += weights[static_cast<std::size_t>(bit)];
    mask &= mask - 1;
  }
  return result;
}

struct Result {
  std::array<int, K> base{};
  std::array<long long, Q> weight{};
  double floating_value = 0;
  long long total = 0;
  long long maximum = 0;
};

Result optimize(std::array<int, K> base, std::array<std::uint64_t, Q> const& lifted) {
  Masks options{};
  for (int coordinate = 0; coordinate < K; ++coordinate) {
    for (int digit = 0; digit < C; ++digit) options[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(digit)] = lifted[static_cast<std::size_t>(base[static_cast<std::size_t>(coordinate)] + P * digit)];
  }
  std::array<double, Q> weight{};
  weight.fill(1.0 / Q);
  std::array<double, Q> best = weight;
  double best_value = 1e100;
  for (int step = 0; step < ITERATIONS; ++step) {
    std::array<std::uint64_t, K> selected{};
    double value = 0;
    for (int coordinate = 0; coordinate < K; ++coordinate) {
      int digit = 0;
      for (int alternative = 1; alternative < C; ++alternative) {
        if (dot(weight, options[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(alternative)]) > dot(weight, options[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(digit)])) digit = alternative;
      }
      selected[static_cast<std::size_t>(coordinate)] = options[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(digit)];
      value += dot(weight, selected[static_cast<std::size_t>(coordinate)]);
    }
    if (value < best_value) { best_value = value; best = weight; }
    double eta = .7 / std::sqrt(step + 1.0);
    double normalizer = 0;
    for (int time = 0; time < Q; ++time) {
      int gradient = 0;
      for (auto mask : selected) gradient += (mask >> time) & 1ULL;
      weight[static_cast<std::size_t>(time)] *= std::exp(-eta * gradient);
      normalizer += weight[static_cast<std::size_t>(time)];
    }
    for (double& entry : weight) entry /= normalizer;
  }
  Result result;
  result.base = base;
  result.floating_value = best_value;
  for (int time = 0; time < Q; ++time) {
    result.weight[static_cast<std::size_t>(time)] = std::max(0LL, std::llround(best[static_cast<std::size_t>(time)] * SCALE));
    result.total += result.weight[static_cast<std::size_t>(time)];
  }
  for (int coordinate = 0; coordinate < K; ++coordinate) {
    long long choice = 0;
    for (int digit = 0; digit < C; ++digit) choice = std::max(choice, dot_integer(result.weight, options[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(digit)]));
    result.maximum += choice;
  }
  return result;
}
}  // namespace

int main(int argc, char** argv) try {
  if (argc != 2) { std::cerr << "usage: lrc_weighted_dual_h11 OUTPUT\n"; return 2; }
  std::array<std::uint64_t, P> base{};
  std::array<std::uint64_t, Q> lifted{};
  for (int speed = 0; speed < P; ++speed) base[static_cast<std::size_t>(speed)] = make_mask(speed, P);
  for (int speed = 0; speed < Q; ++speed) lifted[static_cast<std::size_t>(speed)] = make_mask(speed, Q);
  std::vector<std::array<int, K>> tuples;
  for (int x = 1; x < P; ++x) for (int y = 1; y < P; ++y) for (int z = 1; z < P; ++z) {
    if ((base[static_cast<std::size_t>(x)] | base[static_cast<std::size_t>(y)] | base[static_cast<std::size_t>(z)]) == ((1ULL << P) - 1)) tuples.push_back({x, y, z});
  }
  if (tuples.size() != 240) throw std::runtime_error("unexpected H11 base count");
  std::vector<Result> results(tuples.size());
  std::atomic<std::size_t> next(0);
  std::vector<std::thread> workers;
  for (int worker = 0; worker < 3; ++worker) workers.emplace_back([&] {
    while (true) { std::size_t index = next.fetch_add(1); if (index >= tuples.size()) return; results[index] = optimize(tuples[index], lifted); }
  });
  for (auto& worker : workers) worker.join();
  std::ofstream output(argv[1]);
  if (!output) throw std::runtime_error("cannot open output");
  int certificates = 0;
  output << std::setprecision(12);
  for (Result const& result : results) {
    bool accepted = result.maximum < result.total;
    certificates += accepted;
    output << result.base[0] << ' ' << result.base[1] << ' ' << result.base[2] << ' '
           << (accepted ? "CERTIFICATE" : "NO_CERTIFICATE") << ' ' << result.floating_value << ' '
           << result.total << ' ' << result.maximum;
    for (long long weight : result.weight) output << ' ' << weight;
    output << '\n';
  }
  std::cout << "raw_bases=1000 l1_improper=" << tuples.size() << " certificates=" << certificates << '\n';
  return 0;
} catch (std::exception const& error) { std::cerr << "error: " << error.what() << '\n'; return 1; }
