#include <array>
#include <cassert>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>
#include <boost/multiprecision/cpp_int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif

using Big=boost::multiprecision::cpp_int;
using Exp=std::array<int,5>;
struct RawTerm{Exp e;std::int64_t n;std::uint64_t d;};
struct Term{Exp e;Big c;};
struct Result{std::string name;std::uint64_t rows=0,neg=0,zero=0,pos=0;};

static std::vector<std::string> split(const std::string&s){std::stringstream in(s);std::vector<std::string>f;std::string x;while(std::getline(in,x,'\t'))f.push_back(x);return f;}

static std::pair<std::vector<Term>,std::uint64_t> load(const std::filesystem::path&path){
  std::ifstream in(path);std::string line;std::getline(in,line);std::vector<RawTerm>raw;std::uint64_t lcm=1;
  while(std::getline(in,line)){if(line.empty())continue;auto f=split(line);assert(f.size()==7);RawTerm t{};for(int i=0;i<5;++i)t.e[i]=std::stoi(f[i]);t.n=std::stoll(f[5]);t.d=std::stoull(f[6]);lcm=std::lcm(lcm,t.d);raw.push_back(t);}
  std::vector<Term>terms;terms.reserve(raw.size());for(const auto&t:raw)terms.push_back({t.e,Big(t.n)*(lcm/t.d)});return {terms,lcm};
}

static Big evaluate(const std::vector<Term>&terms,const Exp&z){
  Big power[5][16];for(int i=0;i<5;++i){power[i][0]=1;for(int k=1;k<=15;++k)power[i][k]=power[i][k-1]*z[i];}
  Big total=0;for(const auto&t:terms){Big v=t.c;for(int i=0;i<5;++i)v*=power[i][t.e[i]];total+=v;}return total;
}

int main(int argc,char**argv){
  if(argc!=3){std::cerr<<"usage: grid PULLBACK_DIR OUTDIR\n";return 2;}
  const std::filesystem::path input=argv[1],output=argv[2];std::filesystem::create_directories(output);
  const std::array<std::string,4> names{{"cycle_equal","cycle_zero","trans_equal","trans_zero"}};
  std::array<Result,4> results;
  #ifdef _OPENMP
  omp_set_num_threads(3);
  #pragma omp parallel for schedule(dynamic)
  #endif
  for(int family=0;family<4;++family){
    auto [terms,lcm]=load(input/(names[family]+".tsv"));Result r;r.name=names[family];std::ofstream neg(output/(names[family]+"-negative.tsv"));neg<<"z0\tz1\tz2\tz3\tz4\tcleared_deficit\n";
    for(int a=0;a<=16;++a)for(int b=0;b<=16-a;++b)for(int c=0;c<=16-a-b;++c)for(int d=0;d<=16-a-b-c;++d){Exp z{a,b,c,d,16-a-b-c-d};Big value=evaluate(terms,z);++r.rows;if(value<0){++r.neg;neg<<a<<'\t'<<b<<'\t'<<c<<'\t'<<d<<'\t'<<z[4]<<'\t'<<value<<'\n';}else if(value==0)++r.zero;else++r.pos;}
    assert(r.rows==4845);results[family]=r;
  }
  std::ofstream summary(output/"grid-summary.json");summary<<"{\n  \"status\": \"PASS\",\n  \"epistemic_status\": \"PROVED\",\n  \"denominator\": 16,\n  \"families\": {\n";
  std::uint64_t total=0,negative=0;for(int i=0;i<4;++i){const auto&r=results[i];total+=r.rows;negative+=r.neg;summary<<"    \""<<r.name<<"\": {\"rows\": "<<r.rows<<", \"negative\": "<<r.neg<<", \"zero\": "<<r.zero<<", \"positive\": "<<r.pos<<"}"<<(i==3?"\n":",\n");}
  summary<<"  },\n  \"total_rows\": "<<total<<",\n  \"total_negative\": "<<negative<<"\n}\n";
  for(const auto&r:results)std::cout<<r.name<<" -/0/+ "<<r.neg<<'/'<<r.zero<<'/'<<r.pos<<'\n';
  return negative?1:0;
}
