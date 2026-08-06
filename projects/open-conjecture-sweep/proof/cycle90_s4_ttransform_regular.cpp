// Exact Route B for C90: reverse regular-representation tensor contraction.
#include <array>
#include <boost/multiprecision/cpp_int.hpp>
#include <iostream>
#include <vector>
using Z=boost::multiprecision::cpp_int; using P=std::array<Z,16>; constexpr int N=24;
std::vector<std::array<int,4>> g; int mul[24][24],iv[24],xg,xh;
P z(){P x{};return x;} P add(const P&a,const P&b){P c=z();for(int i=0;i<16;i++)c[i]=a[i]+b[i];return c;} P pm(const P&a,const P&b){P c=z();for(int i=0;i<16;i++)for(int j=0;i+j<16;j++)c[i+j]+=a[i]*b[j];return c;}
int ix(const std::array<int,4>&a){for(int i=0;i<24;i++)if(g[i]==a)return i;return -1;}
P w(int q){P a=z(); bool v=(g[q]==std::array<int,4>{0,1,2,3}||g[q]==std::array<int,4>{1,0,3,2}||g[q]==std::array<int,4>{2,3,0,1}||g[q]==std::array<int,4>{3,2,1,0});a[0]=1+(v?1:0);if(q==xg)a[1]=1;if(q==xh)a[1]=-1;return a;}
int main(){std::array<int,4>a={0,1,2,3};do{g.push_back(a);}while(std::next_permutation(a.begin(),a.end()));for(int i=0;i<24;i++){std::array<int,4>b;for(int k=0;k<4;k++)b[g[i][k]]=k;iv[i]=ix(b);}for(int i=0;i<24;i++)for(int j=0;j<24;j++){std::array<int,4>b;for(int k=0;k<4;k++)b[k]=g[i][g[j][k]];mul[i][j]=ix(b);}xg=ix({1,0,2,3});xh=ix({2,1,0,3});auto at=[](int a,int b,int c){return(a*24+b)*24+c;};std::vector<P>F[5];for(auto&f:F)f.resize(24*24*24);
 for(int a=0;a<24;a++)for(int b=0;b<24;b++)for(int c=0;c<24;c++)F[0][at(a,b,c)]=pm(pm(w(a),w(b)),w(c));
 for(int q=1;q<5;q++)for(int a=0;a<24;a++)for(int b=0;b<24;b++)for(int c=0;c<24;c++){P s=z();for(int l=0;l<24;l++)s=add(s,pm(pm(w(mul[iv[l]][a]),w(mul[iv[l]][b])),w(mul[iv[l]][c])));F[q][at(a,b,c)]=s;}
 P total=z();for(int r0=0;r0<24;r0++)for(int r1=0;r1<24;r1++)for(int r2=0;r2<24;r2++)for(int r3=0;r3<24;r3++)for(int r4=0;r4<24;r4++){P q=pm(F[0][at(r0,r3,r4)],F[1][at(r1,r4,r0)]);q=pm(q,F[2][at(r2,r0,r1)]);q=pm(q,F[3][at(r3,r1,r2)]);q=pm(q,F[4][at(r4,r2,r3)]);total=add(total,q);}Z d=1;for(int i=0;i<9;i++)d*=24;std::cout<<"{\"status\":\"REGULAR_CONTRACTION_PASS\",\"normalization_denominator\":\""<<d<<"\",\"coefficients\":[";for(int i=0;i<16;i++){if(i)std::cout<<',';std::cout<<'"'<<total[i]<<'"';}std::cout<<"]}"<<std::endl;}
