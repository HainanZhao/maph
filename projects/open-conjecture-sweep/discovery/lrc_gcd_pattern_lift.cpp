#define main cycle8_multichoice_main
#include "lrc_p199_multichoice_lift.cpp"
#undef main

namespace {

constexpr std::uint64_t PATTERN_NODE_CAP = 2'000'000;

struct PatternSearch : Search {
  explicit PatternSearch(std::array<int, K> const& base) : Search(base) {}

  bool impossible_by_pattern_bound(Mask const& covered, int div2, int div7) const {
    int cap2 = 11 - div2;
    int cap7 = 11 - div7;
    if (cap2 < 0 || cap7 < 0) return true;
    Mask uncovered = difference(full, covered);
    int needed = popcount(uncovered);
    constexpr int NEGATIVE = -1'000'000;
    std::array<std::array<int, 12>, 12> dp{};
    for (auto& row : dp) row.fill(NEGATIVE);
    dp[0][0] = 0;
    for (int coordinate = 0; coordinate < K; ++coordinate) {
      if (digit[static_cast<std::size_t>(coordinate)] >= 0) continue;
      int best[2][2] = {{NEGATIVE, NEGATIVE}, {NEGATIVE, NEGATIVE}};
      for (int choice = 0; choice < C; ++choice) {
        int speed = base[static_cast<std::size_t>(coordinate)] + P * choice;
        int add2 = speed % 2 == 0;
        int add7 = speed % 7 == 0;
        Mask gained = bad[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(choice)];
        for (int word = 0; word < WORDS; ++word) {
          gained.word[static_cast<std::size_t>(word)] &= uncovered.word[static_cast<std::size_t>(word)];
        }
        best[add2][add7] = std::max(best[add2][add7], popcount(gained));
      }
      std::array<std::array<int, 12>, 12> next{};
      for (auto& row : next) row.fill(NEGATIVE);
      for (int used2 = 0; used2 <= cap2; ++used2) {
        for (int used7 = 0; used7 <= cap7; ++used7) {
          if (dp[used2][used7] == NEGATIVE) continue;
          for (int add2 = 0; add2 <= 1; ++add2) {
            for (int add7 = 0; add7 <= 1; ++add7) {
              if (best[add2][add7] == NEGATIVE || used2 + add2 > cap2 || used7 + add7 > cap7) continue;
              next[used2 + add2][used7 + add7] = std::max(
                  next[used2 + add2][used7 + add7], dp[used2][used7] + best[add2][add7]);
            }
          }
        }
      }
      dp = next;
    }
    int available = 0;
    for (int used2 = 0; used2 <= cap2; ++used2) {
      for (int used7 = 0; used7 <= cap7; ++used7) available = std::max(available, dp[used2][used7]);
    }
    return available < needed;
  }

  bool search_pattern(Mask const& covered, int div2, int div7) {
    if (++nodes > PATTERN_NODE_CAP || std::chrono::steady_clock::now() > deadline) {
      capped = true;
      return false;
    }
    if (div2 >= 12 || div7 >= 12) return false;
    if (is_full(covered, full)) return finish_if_covered(covered, div2, div7);
    if (impossible_by_pattern_bound(covered, div2, div7)) return false;

    int target = -1;
    int best_choices = 1'000'000;
    int inspected = 0;
    for (int point = 0; point < Q && inspected < 128; ++point) {
      if (contains(covered, point)) continue;
      ++inspected;
      int count = 0;
      for (auto [coordinate, choice] : options[static_cast<std::size_t>(point)]) {
        if (digit[static_cast<std::size_t>(coordinate)] >= 0) continue;
        int speed = base[static_cast<std::size_t>(coordinate)] + P * choice;
        if (div2 + (speed % 2 == 0) < 12 && div7 + (speed % 7 == 0) < 12) ++count;
      }
      if (count == 0) return false;
      if (count < best_choices) { best_choices = count; target = point; }
    }
    if (target < 0) throw std::runtime_error("pattern target selection failed");

    Mask uncovered = difference(full, covered);
    struct Choice { int coordinate; int digit; int gain; int add2; int add7; };
    std::vector<Choice> choices;
    for (auto [coordinate, choice] : options[static_cast<std::size_t>(target)]) {
      if (digit[static_cast<std::size_t>(coordinate)] >= 0) continue;
      int speed = base[static_cast<std::size_t>(coordinate)] + P * choice;
      int add2 = speed % 2 == 0;
      int add7 = speed % 7 == 0;
      if (div2 + add2 >= 12 || div7 + add7 >= 12) continue;
      Mask gained = bad[static_cast<std::size_t>(coordinate)][static_cast<std::size_t>(choice)];
      for (int word = 0; word < WORDS; ++word) gained.word[static_cast<std::size_t>(word)] &= uncovered.word[static_cast<std::size_t>(word)];
      choices.push_back({coordinate, choice, popcount(gained), add2, add7});
    }
    std::sort(choices.begin(), choices.end(), [](Choice const& left, Choice const& right) {
      if (left.gain != right.gain) return left.gain > right.gain;
      if (left.add2 + left.add7 != right.add2 + right.add7) return left.add2 + left.add7 < right.add2 + right.add7;
      if (left.coordinate != right.coordinate) return left.coordinate < right.coordinate;
      return left.digit < right.digit;
    });
    for (Choice const& choice : choices) {
      digit[static_cast<std::size_t>(choice.coordinate)] = choice.digit;
      if (search_pattern(unite(covered, bad[static_cast<std::size_t>(choice.coordinate)][static_cast<std::size_t>(choice.digit)]),
                         div2 + choice.add2, div7 + choice.add7)) return true;
      digit[static_cast<std::size_t>(choice.coordinate)] = -1;
      if (capped) return false;
    }
    return false;
  }
};

}  // namespace

int main(int argc, char** argv) try {
  if (argc != 3) { std::cerr << "usage: lrc_gcd_pattern_lift INPUT OUTPUT\n"; return 2; }
  std::ifstream input(argv[1]);
  std::ofstream output(argv[2]);
  if (!input || !output) throw std::runtime_error("cannot open input or output");
  std::vector<std::array<int, K>> bases;
  for (std::string line; std::getline(input, line);) {
    std::istringstream stream(line);
    std::array<int, K> base{};
    for (int coordinate = 0; coordinate < K; ++coordinate) if (!(stream >> base[coordinate])) throw std::runtime_error("malformed row");
    bases.push_back(base);
  }
  if (bases.size() != 100) throw std::runtime_error("sample must have 100 rows");
  struct Result { bool sat=false, cap=false; std::uint64_t nodes=0; long long micros=0; std::array<int,K> digit{}; };
  std::vector<Result> results(100);
  std::atomic<std::size_t> next(0);
  std::vector<std::thread> workers;
  for (int worker=0; worker<3; ++worker) workers.emplace_back([&] {
    while (true) {
      std::size_t row=next.fetch_add(1); if (row>=bases.size()) return;
      auto start=std::chrono::steady_clock::now(); PatternSearch search(bases[row]);
      bool sat=search.greedy() || search.search_pattern(Mask{},0,0);
      results[row]={sat,search.capped,search.nodes,std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::steady_clock::now()-start).count(),search.digit};
    }
  });
  for (auto& worker:workers) worker.join();
  for (std::size_t row=0; row<results.size(); ++row) {
    auto const& result=results[row];
    output<<row<<' '<<(result.sat?"SAT":result.cap?"CAP":"UNSAT")<<' '<<result.nodes<<' '<<result.micros;
    if(result.sat) for(int digit:result.digit) output<<' '<<digit;
    output<<'\n';
  }
  return 0;
} catch(std::exception const& error) { std::cerr<<"error: "<<error.what()<<'\n'; return 1; }
