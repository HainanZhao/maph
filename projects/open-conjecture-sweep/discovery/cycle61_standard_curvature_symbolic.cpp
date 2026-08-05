// Exact symbolic class-zero standard curvature for C61; output only t^2 terms.
#include <algorithm>
#include <array>
#include <filesystem>
#include <fstream>
#include <map>
#include <vector>
using P=std::map<unsigned short,long long>;
static unsigned short add(unsigned short a,unsigned short b){unsigned short r=0,m=1;for(int i=0;i<4;++i){r+=m*((a/m%16)+(b/m%16));m*=16;}return r;}
static P plus(P a,const P&b){for(auto[k,v]:b)a[k]+=v;return a;}
static P mul(const P&a,const P&b){P r;for(auto[x,u]:a)for(auto[y,v]:b)r[add(x,y)]+=u*v;return r;}
static P var(int i,int sign=1){P p;p[1u<<(4*i)]=sign;return p;}
static constexpr std::array<std::array<int,3>,5>N{{{{2,3,4}},{{0,3,4}},{{0,1,4}},{{0,1,2}},{{1,2,3}}}};
int main(int ac,char**av){if(ac!=2)return 2;std::vector<std::array<int,3>>q;std::array<int,3>a{0,1,2};do q.push_back(a);while(std::next_permutation(a.begin(),a.end()));std::map<std::array<int,3>,int>ix;for(int i=0;i<6;++i)ix[q[i]]=i;int m[6][6],iv[6],cl[6];for(int i=0;i<6;++i)for(int j=0;j<6;++j){std::array<int,3>z;for(int k=0;k<3;++k)z[k]=q[i][q[j][k]];m[i][j]=ix[z];}for(int i=0;i<6;++i)for(int j=0;j<6;++j)if(m[i][j]==0&&m[j][i]==0)iv[i]=j;for(int z=0;z<6;++z){int v=z,n=1;while(v){v=m[v][z];++n;}cl[z]=n==1?0:n==2?1:2;}P A=var(0),B=var(1),C=var(2),T=var(3),one;one[0]=1;
const std::array<std::array<int,6>,3>dirs{{{{0,-1,0,0,0,1}},{{0,-1,-2,0,0,3}},{{0,0,0,-1,1,0}}}};const char*label[3]{"standard_axis","standard_generic","sign"};std::filesystem::create_directories(av[1]);std::ofstream o(std::string(av[1])+"/transverse-curvature.tsv");o<<"direction\tdegree\te\tt\tc\tcoefficient\n";
for(int d=0;d<3;++d){P total;for(int x1=0;x1<6;++x1)for(int x2=0;x2<6;++x2)for(int x3=0;x3<6;++x3)for(int x4=0;x4<6;++x4){int x[5]{0,x1,x2,x3,x4};P product=one;for(auto nb:N){P sum;for(int y=0;y<6;++y){P z=one;for(int i:nb){int h=m[iv[x[i]]][y];P f=cl[h]==0?A:cl[h]==1?B:C;if(dirs[d][h])f=plus(f,var(3,dirs[d][h]));z=mul(z,f);}sum=plus(sum,z);}product=mul(product,sum);}total=plus(total,product);}for(auto[k,v]:total){int e[4];for(int i=0;i<4;++i)e[i]=k>>(4*i)&15;if((e[3]==2||e[3]==3)&&v)o<<label[d]<<'\t'<<e[3]<<'\t'<<e[0]<<'\t'<<e[1]<<'\t'<<e[2]<<'\t'<<v<<'\n';}}
}
