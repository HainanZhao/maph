#include <algorithm>
#include <array>
#include <atomic>
#include <cassert>
#include <cstdlib>
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
using Shape=std::array<int,4>;
static std::uint64_t choose_[64][64];
static std::atomic<std::uint64_t> cells{0};
static std::uint64_t cap=0;
struct Box{Shape lower{},splits{};};
struct Result{std::string name;std::uint64_t visited=0,certified=0,unresolved=0;int max_depth=0;bool complete=true;Shape degrees{};std::vector<Box>unresolved_boxes;};

static std::vector<std::string> split(const std::string&s){std::stringstream in(s);std::vector<std::string>f;std::string x;while(std::getline(in,x,'\t'))f.push_back(x);return f;}
static std::size_t size_of(const Shape&d){std::size_t n=1;for(int x:d)n*=x+1;return n;}
static std::size_t index_of(const Shape&i,const Shape&d){return ((i[0]*(d[1]+1)+i[1])*(d[2]+1)+i[2])*(d[3]+1)+i[3];}

static std::pair<std::vector<Big>,Shape> load_bernstein(const std::filesystem::path&path){
  struct Raw{Shape e;Big n;std::uint64_t den;};std::ifstream in(path);std::string line;std::getline(in,line);std::vector<Raw>raw;Shape d{};std::uint64_t lcm=1;
  while(std::getline(in,line)){if(line.empty())continue;auto f=split(line);assert(f.size()==5||f.size()==6);Raw r{};for(int j=0;j<4;++j){r.e[j]=std::stoi(f[j]);d[j]=std::max(d[j],r.e[j]);}r.n=Big(f[4]);r.den=f.size()==6?std::stoull(f[5]):1;lcm=std::lcm(lcm,r.den);raw.push_back(r);}
  std::vector<Big>a(size_of(d));for(const auto&r:raw)a[index_of(r.e,d)]+=Big(r.n)*(lcm/r.den);
  // Convert monomial power coefficients to tensor Bernstein coefficients,
  // one axis at a time, retaining a common positive integer scale.
  for(int axis=0;axis<4;++axis){const int degree=d[axis];std::uint64_t axis_lcm=1;for(int k=0;k<=degree;++k)axis_lcm=std::lcm(axis_lcm,choose_[degree][k]);std::vector<Big>b(a.size());
    Shape fixed{};for(int i0=0;i0<=d[0];++i0)for(int i1=0;i1<=d[1];++i1)for(int i2=0;i2<=d[2];++i2)for(int i3=0;i3<=d[3];++i3){Shape idx{i0,i1,i2,i3};const int target=idx[axis];Big value=0;for(int k=0;k<=target;++k){idx[axis]=k;value+=a[index_of(idx,d)]*choose_[target][k]*(axis_lcm/choose_[degree][k]);}idx[axis]=target;b[index_of(idx,d)]=value;}a.swap(b);}
  return {a,d};
}

static bool nonnegative(const std::vector<Big>&a){for(const auto&x:a)if(x<0)return false;return true;}

static std::pair<std::vector<Big>,std::vector<Big>> subdivide(const std::vector<Big>&a,const Shape&d,int axis){
  std::vector<Big>left(a.size()),right(a.size());const int degree=d[axis];
  Shape idx{};for(int i0=0;i0<=d[0];++i0)for(int i1=0;i1<=d[1];++i1)for(int i2=0;i2<=d[2];++i2)for(int i3=0;i3<=d[3];++i3){idx={i0,i1,i2,i3};if(idx[axis])continue;std::vector<Big>work(degree+1);for(int k=0;k<=degree;++k){idx[axis]=k;work[k]=a[index_of(idx,d)];}idx[axis]=0;left[index_of(idx,d)]=work[0]<<degree;idx[axis]=degree;right[index_of(idx,d)]=work[degree]<<degree;
      for(int r=1;r<=degree;++r){for(int k=0;k<=degree-r;++k)work[k]+=work[k+1];idx[axis]=r;left[index_of(idx,d)]=work[0]<<(degree-r);idx[axis]=degree-r;right[index_of(idx,d)]=work[degree-r]<<(degree-r);}}
  return {std::move(left),std::move(right)};
}

static void certify(const std::vector<Big>&a,const Shape&d,Shape lower,Shape splits,int depth,Result&r){
  auto ordinal=cells.fetch_add(1);if(ordinal>=cap){r.complete=false;++r.unresolved;r.unresolved_boxes.push_back({lower,splits});return;}++r.visited;r.max_depth=std::max(r.max_depth,depth);if(nonnegative(a)){++r.certified;return;}if(depth>=18){r.complete=false;++r.unresolved;r.unresolved_boxes.push_back({lower,splits});return;}
  int axis=-1;for(int j=0;j<4;++j)if(d[j]>0&&(axis<0||splits[j]<splits[axis]))axis=j;assert(axis>=0);auto [left,right]=subdivide(a,d,axis);++splits[axis];lower[axis]*=2;certify(left,d,lower,splits,depth+1,r);if(cells.load()>=cap){r.complete=false;++r.unresolved;r.unresolved_boxes.push_back({lower,splits});return;}++lower[axis];certify(right,d,lower,splits,depth+1,r);
}

int main(int argc,char**argv){if(argc<4){std::cerr<<"usage: tensor CHART_DIR OUTDIR CELL_CAP [CHART ...]\n";return 2;}cap=std::stoull(argv[3]);if(cap>1000000)return 2;for(int n=0;n<64;++n){choose_[n][0]=choose_[n][n]=1;for(int k=1;k<n;++k)choose_[n][k]=choose_[n-1][k-1]+choose_[n-1][k];}
  std::vector<std::string>selected;for(int i=4;i<argc;++i)selected.push_back(argv[i]);std::vector<std::filesystem::path>files;for(auto&p:std::filesystem::directory_iterator(argv[1]))if(p.path().extension()==".tsv"&&(selected.empty()||std::find(selected.begin(),selected.end(),p.path().stem().string())!=selected.end()))files.push_back(p.path());std::sort(files.begin(),files.end());std::vector<Result>results(files.size());
  #ifdef _OPENMP
  const char* configured=std::getenv("C67_THREADS");omp_set_num_threads(configured?std::stoi(configured):3);
  #pragma omp parallel for schedule(dynamic)
  #endif
  for(int i=0;i<(int)files.size();++i){auto [a,d]=load_bernstein(files[i]);Result r;r.name=files[i].stem().string();r.degrees=d;certify(a,d,Shape{},Shape{},0,r);results[i]=r;}
  std::filesystem::create_directories(argv[2]);std::ofstream out(std::filesystem::path(argv[2])/"tensor-summary.json");out<<"{\n  \"status\": \"PASS\",\n  \"epistemic_status\": \"PROVED\",\n  \"cell_cap\": "<<cap<<",\n  \"global_cells\": "<<std::min(cells.load(),cap)<<",\n  \"charts\": {\n";bool complete=true;for(int i=0;i<(int)results.size();++i){auto&r=results[i];complete&=r.complete;out<<"    \""<<r.name<<"\": {\"complete\": "<<(r.complete?"true":"false")<<", \"degrees\": ["<<r.degrees[0]<<','<<r.degrees[1]<<','<<r.degrees[2]<<','<<r.degrees[3]<<"], \"visited\": "<<r.visited<<", \"certified_leaves\": "<<r.certified<<", \"unresolved\": "<<r.unresolved<<", \"max_depth\": "<<r.max_depth<<"}"<<(i+1==(int)results.size()?"\n":",\n");}out<<"  },\n  \"complete_cover\": "<<(complete?"true":"false")<<"\n}\n";for(auto&r:results){std::ofstream boxes(std::filesystem::path(argv[2])/(r.name+"-unresolved.tsv"));boxes<<"x_lower\tx_splits\ty_lower\ty_splits\tr_lower\tr_splits\th_lower\th_splits\n";for(const auto&b:r.unresolved_boxes)for(int j=0;j<4;++j)boxes<<b.lower[j]<<'\t'<<b.splits[j]<<(j==3?'\n':'\t');std::cout<<r.name<<" complete="<<r.complete<<" visited="<<r.visited<<" certified="<<r.certified<<" unresolved="<<r.unresolved<<" depth="<<r.max_depth<<'\n';}}
