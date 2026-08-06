// Exact Route A for C90: translation-fixed Cayley contraction on S4.
#include <array>
#include <boost/multiprecision/cpp_int.hpp>
#include <iostream>
#include <map>
#include <vector>
using Z = boost::multiprecision::cpp_int;
using Poly = std::array<Z,16>;
constexpr int N=24;
std::vector<std::array<int,4>> p;
int mul[N][N], invv[N], gid, hid;

Poly zero(){ Poly x{}; return x; }
Poly one(){ Poly x=zero(); x[0]=1; return x; }
Poly add(const Poly&a,const Poly&b){ Poly c=zero(); for(int i=0;i<16;i++)c[i]=a[i]+b[i]; return c; }
Poly prod(const Poly&a,const Poly&b){ Poly c=zero(); for(int i=0;i<16;i++)for(int j=0;i+j<16;j++)c[i+j]+=a[i]*b[j]; return c; }
Poly weight(int x){ Poly q=zero(); bool in_v4=(p[x]==std::array<int,4>{0,1,2,3}||p[x]==std::array<int,4>{1,0,3,2}||p[x]==std::array<int,4>{2,3,0,1}||p[x]==std::array<int,4>{3,2,1,0}); q[0]=1+(in_v4?1:0); if(x==gid)q[1]=1; if(x==hid)q[1]=-1; return q; }
int idx(const std::array<int,4>&x){for(int i=0;i<N;i++)if(p[i]==x)return i;return -1;}
std::string show(const Z&x){return x.convert_to<std::string>();}
int main(){
 std::array<int,4>a={0,1,2,3}; do{p.push_back(a);}while(std::next_permutation(a.begin(),a.end()));
 for(int i=0;i<N;i++){std::array<int,4> q;for(int j=0;j<4;j++)q[p[i][j]]=j;invv[i]=idx(q);}
 for(int i=0;i<N;i++)for(int j=0;j<N;j++){std::array<int,4> q;for(int k=0;k<4;k++)q[k]=p[i][p[j][k]];mul[i][j]=idx(q);}
 gid=idx({1,0,2,3}); hid=idx({2,1,0,3});
 std::vector<Poly> F[5]; for(int j=0;j<5;j++)F[j].resize(N*N*N);
 auto at=[](int x,int y,int z){return (x*N+y)*N+z;};
 for(int j=0;j<5;j++) for(int x=0;x<N;x++)for(int y=0;y<N;y++)for(int z=0;z<N;z++){
   Poly sum=zero(); for(int r=0;r<N;r++) sum=add(sum,prod(prod(weight(mul[invv[x]][r]),weight(mul[invv[y]][r])),weight(mul[invv[z]][r])));
   F[j][at(x,y,z)]=sum;
 }
 Poly total=zero(); int e=idx({0,1,2,3});
 for(int l1=0;l1<N;l1++)for(int l2=0;l2<N;l2++)for(int l3=0;l3<N;l3++)for(int l4=0;l4<N;l4++){
   Poly q=prod(F[0][at(e,l1,l2)],F[1][at(l1,l2,l3)]); q=prod(q,F[2][at(l2,l3,l4)]); q=prod(q,F[3][at(l3,l4,e)]); q=prod(q,F[4][at(l4,e,l1)]); total=add(total,q);
 }
 Z den=1;for(int i=0;i<9;i++)den*=N;
 std::cout << "{\"status\":\"DIRECT_CONTRACTION_PASS\",\"normalization_denominator\":\""<<show(den)<<"\",\"coefficients\":[";
 for(int i=0;i<16;i++){if(i)std::cout<<',';std::cout<<'"'<<show(total[i])<<'"';} std::cout<<"],\"derivative_numerators\":[";
 for(int i=1;i<16;i++){if(i>1)std::cout<<',';std::cout<<'"'<<show(total[i]*i)<<'"';} std::cout<<"]}"<<std::endl;
}
