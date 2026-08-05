#include <array>
#include <cassert>
#include <cstdlib>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>
#include <boost/multiprecision/cpp_int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
using Big=boost::multiprecision::cpp_int;
using Key=std::uint32_t;using Poly=std::unordered_map<Key,Big>;
static Key unit(int i){return Key(1)<<(6*i);}static int degree(Key k,int i){return (k>>(6*i))&63;}static Key addkey(Key a,Key b){Key r=0;for(int i=0;i<4;++i)r|=Key(degree(a,i)+degree(b,i))<<(6*i);return r;}
static Poly add(const Poly&a,const Poly&b,int sign=1){Poly r=a;for(auto&[k,c]:b)r[k]+=sign*c;for(auto it=r.begin();it!=r.end();)if(it->second==0)it=r.erase(it);else++it;return r;}
static Poly scale(const Poly&a,const Big&c){Poly r;for(auto&[k,v]:a)if(v*c!=0)r[k]=v*c;return r;}
static Poly mul(const Poly&a,const Poly&b){Poly r;r.reserve(std::min<std::size_t>(200000,a.size()*b.size()));for(auto&[x,u]:a)for(auto&[y,v]:b)r[addkey(x,y)]+=u*v;for(auto it=r.begin();it!=r.end();)if(it->second==0)it=r.erase(it);else++it;return r;}
static Poly power(Poly a,int n){Poly r{{0,1}};while(n){if(n&1)r=mul(r,a);n>>=1;if(n)a=mul(a,a);}return r;}
static Poly divide_exact(const Poly&a,int d){Poly r;for(auto&[k,v]:a){assert(v%d==0);r[k]=v/d;}return r;}
static std::vector<std::string> split(const std::string&s){std::stringstream in(s);std::vector<std::string>f;std::string x;while(std::getline(in,x,'\t'))f.push_back(x);return f;}
struct Orbit{std::array<int,6> e;Big c;};
int main(int argc,char**argv){if(argc!=4){std::cerr<<"usage: fast FORMS ORBIT OUTDIR\n";return 2;}std::map<std::string,std::array<Poly,6>>charts;{std::ifstream in(argv[1]);std::string line;std::getline(in,line);while(std::getline(in,line)){auto f=split(line);auto&forms=charts[f[0]];int value=std::stoi(f[1]);Key k=0;for(int i=0;i<4;++i)k|=Key(std::stoi(f[2+i]))<<(6*i);forms[value][k]+=Big(f[6]);}}
  std::vector<Orbit>orbit;{std::ifstream in(argv[2]);std::string line;std::getline(in,line);while(std::getline(in,line)){auto f=split(line);Orbit o{};for(int i=0;i<6;++i)o.e[i]=std::stoi(f[i]);assert(std::stoi(f[6])==0);auto den=std::stoull(f[8]);assert(64%den==0);o.c=Big(f[7])*(64/den);orbit.push_back(o);}}
  std::vector<std::string>names;for(auto&[name,_]:charts)names.push_back(name);std::filesystem::create_directories(argv[3]);
  #ifdef _OPENMP
  const char* configured=std::getenv("C67_THREADS");omp_set_num_threads(configured?std::stoi(configured):3);
  #pragma omp parallel for schedule(dynamic)
  #endif
  for(int ci=0;ci<(int)names.size();++ci){auto a=charts[names[ci]];Poly e=a[0],t=divide_exact(add(add(a[1],a[2]),a[3]),3),c=divide_exact(add(a[4],a[5]),2);Poly x=add(a[1],t,-1),y=add(a[2],t,-1),z=add(a[3],t,-1);Poly r2=add(add(mul(x,x),mul(y,y)),mul(z,z)),u=mul(mul(x,y),z),dv=divide_exact(add(a[4],a[5],-1),2),s2=mul(dv,dv);std::array<Poly,6>forms{e,t,c,r2,u,s2};std::array<std::array<Poly,16>,6>pw;for(int i=0;i<6;++i){pw[i][0]=Poly{{0,1}};for(int k=1;k<=15;++k)pw[i][k]=mul(pw[i][k-1],forms[i]);}Poly result;result.reserve(100000);
    for(const auto&o:orbit){Poly term{{0,o.c}};for(int i=0;i<6;++i)if(o.e[i])term=mul(term,pw[i][o.e[i]]);for(auto&[k,v]:term)result[k]+=v;}
    for(auto it=result.begin();it!=result.end();)if(it->second==0)it=result.erase(it);else++it;std::map<std::array<int,4>,Big>ordered;for(auto&[k,v]:result){assert(degree(k,2)>=2);ordered[{degree(k,0),degree(k,1),degree(k,2)-2,degree(k,3)}]+=v;}
    std::ofstream out(std::filesystem::path(argv[3])/(names[ci]+".tsv"));out<<"x\ty\tr\th\tcoefficient_scaled_64_times_6_pow_15\n";for(auto&[ex,v]:ordered)if(v!=0)out<<ex[0]<<'\t'<<ex[1]<<'\t'<<ex[2]<<'\t'<<ex[3]<<'\t'<<v<<'\n';std::cout<<names[ci]<<" terms="<<ordered.size()<<'\n';}
}
