// Exact symbolic S3 class-exchange derivatives for the C62 Zhao deficit.
#include <algorithm>
#include <array>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <map>
#include <vector>
using Key=uint32_t; using P=std::map<Key,long long>;
static constexpr std::array<std::array<int,3>,5>N{{{{2,3,4}},{{0,3,4}},{{0,1,4}},{{0,1,2}},{{1,2,3}}}};
static Key add(Key a,Key b){Key r=0,m=1;for(int i=0;i<6;++i){r+=m*((a/m%16)+(b/m%16));m*=16;}return r;}
static P plus(P a,const P&b){for(auto[k,v]:b)a[k]+=v;return a;}
static P mul(const P&a,const P&b){P r;for(auto[x,u]:a)for(auto[y,v]:b)r[add(x,y)]+=u*v;return r;}
static P var(int i){P p;p[Key(1)<<(4*i)]=1;return p;}
static void add_derivative(P&out,const P&in,int positive,int negative){Key up=Key(1)<<(4*positive),un=Key(1)<<(4*negative);for(auto[k,v]:in){int ep=(k/up)&15,en=(k/un)&15;if(ep)out[k-up]+=v*ep;if(en)out[k-un]-=v*en;}}
int main(int ac,char**av){if(ac!=2)return 2;std::vector<std::array<int,3>>q;std::array<int,3>a{0,1,2};do q.push_back(a);while(std::next_permutation(a.begin(),a.end()));std::map<std::array<int,3>,int>ix;for(int i=0;i<6;++i)ix[q[i]]=i;int m[6][6],iv[6];for(int i=0;i<6;++i)for(int j=0;j<6;++j){std::array<int,3>z;for(int k=0;k<3;++k)z[k]=q[i][q[j][k]];m[i][j]=ix[z];}for(int i=0;i<6;++i)for(int j=0;j<6;++j)if(m[i][j]==0&&m[j][i]==0)iv[i]=j;
// Variable order is identity, transpositions 1/2/5, then cycles 3/4.
std::array<P,6>V{var(0),var(1),var(2),var(3),var(4),var(5)};P one,total;one[0]=1;
for(int x1=0;x1<6;++x1)for(int x2=0;x2<6;++x2)for(int x3=0;x3<6;++x3)for(int x4=0;x4<6;++x4){int x[5]{0,x1,x2,x3,x4};P graph=one;for(auto nb:N){P sum;for(int y=0;y<6;++y){P term=one;for(int i:nb){int h=m[iv[x[i]]][y];term=mul(term,V[h]);}sum=plus(sum,term);}graph=mul(graph,sum);}total=plus(total,graph);}
P d,s;add_derivative(d,total,2,1);add_derivative(s,total,4,3);std::filesystem::create_directories(av[1]);std::ofstream o(std::string(av[1])+"/exchange-derivatives.tsv");o<<"class\ta0\ta1\ta2\ta5\ta3\ta4\tcoefficient\n";for(auto[key,co]:d)if(co){int e[6];for(int i=0;i<6;++i)e[i]=(key>>(4*i))&15;o<<"trans\t"<<e[0]<<'\t'<<e[1]<<'\t'<<e[2]<<'\t'<<e[5]<<'\t'<<e[3]<<'\t'<<e[4]<<'\t'<<co<<'\n';}for(auto[key,co]:s)if(co){int e[6];for(int i=0;i<6;++i)e[i]=(key>>(4*i))&15;o<<"cycle\t"<<e[0]<<'\t'<<e[1]<<'\t'<<e[2]<<'\t'<<e[5]<<'\t'<<e[3]<<'\t'<<e[4]<<'\t'<<co<<'\n';}
}
