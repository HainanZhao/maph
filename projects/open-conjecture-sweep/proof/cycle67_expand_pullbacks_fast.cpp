#include <array>
#include <cassert>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <boost/multiprecision/cpp_int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif

using Big=boost::multiprecision::cpp_int;
using Key=std::uint32_t;
using Poly=std::unordered_map<Key,Big>;
static int degree(Key k,int i){return (k>>(6*i))&63;}
static Key addkey(Key a,Key b){Key r=0;for(int i=0;i<4;++i)r|=Key(degree(a,i)+degree(b,i))<<(6*i);return r;}
static Poly mul(const Poly&a,const Poly&b){Poly r;r.reserve(std::min<std::size_t>(200000,a.size()*b.size()));for(auto&[x,u]:a)for(auto&[y,v]:b)r[addkey(x,y)]+=u*v;for(auto it=r.begin();it!=r.end();)if(it->second==0)it=r.erase(it);else++it;return r;}
static std::vector<std::string> split(const std::string&s){std::stringstream in(s);std::vector<std::string>f;std::string x;while(std::getline(in,x,'\t'))f.push_back(x);return f;}
struct Pullback{std::array<int,5> exponent{};Big numerator;std::uint64_t denominator=1;};
struct Chart{std::string family;std::array<Poly,5> forms;};

int main(int argc,char**argv){
  if(argc!=4){std::cerr<<"usage: expand_pullbacks FORMS PULLBACK_DIR OUTDIR\n";return 2;}
  std::map<std::string,Chart> charts;
  {std::ifstream in(argv[1]);std::string line;std::getline(in,line);while(std::getline(in,line)){auto f=split(line);assert(f.size()==8);auto&chart=charts[f[0]];chart.family=f[1];int value=std::stoi(f[2]);Key key=0;for(int i=0;i<4;++i)key|=Key(std::stoi(f[3+i]))<<(6*i);chart.forms[value][key]+=Big(f[7]);}}
  std::map<std::string,std::vector<Pullback>> pullbacks;std::uint64_t common_denominator=1;
  for(const std::string family:{"cycle_equal","cycle_zero","trans_equal","trans_zero"}){
    std::ifstream in(std::filesystem::path(argv[2])/(family+".tsv"));std::string line;std::getline(in,line);while(std::getline(in,line)){auto f=split(line);if(f.size()!=7)return 3;Pullback row;for(int i=0;i<5;++i)row.exponent[i]=std::stoi(f[i]);row.numerator=Big(f[5]);row.denominator=std::stoull(f[6]);common_denominator=std::lcm(common_denominator,row.denominator);pullbacks[family].push_back(row);}
  }
  std::vector<std::string> names;for(auto&[name,_]:charts)names.push_back(name);std::filesystem::create_directories(argv[3]);
  #ifdef _OPENMP
  const char* configured=std::getenv("C67_THREADS");omp_set_num_threads(configured?std::stoi(configured):3);
  #pragma omp parallel for schedule(dynamic)
  #endif
  for(int ci=0;ci<(int)names.size();++ci){const auto&chart=charts[names[ci]];std::array<std::array<Poly,16>,5> powers;for(int i=0;i<5;++i){powers[i][0]=Poly{{0,1}};for(int k=1;k<=15;++k)powers[i][k]=mul(powers[i][k-1],chart.forms[i]);}Poly result;result.reserve(100000);
    for(const auto&row:pullbacks[chart.family]){if(common_denominator%row.denominator!=0)std::abort();Poly term{{0,row.numerator*(common_denominator/row.denominator)}};for(int i=0;i<5;++i)if(row.exponent[i])term=mul(term,powers[i][row.exponent[i]]);for(auto&[key,value]:term)result[key]+=value;}
    for(auto it=result.begin();it!=result.end();)if(it->second==0)it=result.erase(it);else++it;std::map<std::array<int,4>,Big> ordered;for(auto&[key,value]:result){if(degree(key,2)<2)std::abort();ordered[{degree(key,0),degree(key,1),degree(key,2)-2,degree(key,3)}]+=value;}
    std::ofstream out(std::filesystem::path(argv[3])/(names[ci]+".tsv"));out<<"x\ty\tr\th\tcoefficient_scaled_lcm_times_6_pow_15\n";for(auto&[ex,value]:ordered)if(value!=0)out<<ex[0]<<'\t'<<ex[1]<<'\t'<<ex[2]<<'\t'<<ex[3]<<'\t'<<value<<'\n';std::cout<<names[ci]<<" terms="<<ordered.size()<<" scale="<<common_denominator<<'\n';
  }
}
