#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <string>
#include <vector>
using I=__int128_t;
static constexpr std::array<std::array<int,3>,5>N{{{{2,3,4}},{{0,3,4}},{{0,1,4}},{{0,1,2}},{{1,2,3}}}};
struct G{std::vector<std::array<int,3>>p;int m[6][6],iv[6],cl[6];};
static G gg(){G g;std::array<int,3>a{0,1,2};do g.p.push_back(a);while(std::next_permutation(a.begin(),a.end()));std::map<std::array<int,3>,int>x;for(int i=0;i<6;++i)x[g.p[i]]=i;for(int i=0;i<6;++i)for(int j=0;j<6;++j){std::array<int,3>z;for(int k=0;k<3;++k)z[k]=g.p[i][g.p[j][k]];g.m[i][j]=x[z];}for(int i=0;i<6;++i)for(int j=0;j<6;++j)if(g.m[i][j]==0&&g.m[j][i]==0)g.iv[i]=j;for(int z=0;z<6;++z){int k=1,v=z;while(v){v=g.m[v][z];++k;}g.cl[z]=k==1?0:k==2?1:2;}return g;}
static std::vector<std::array<int,6>> ds(const G&g){std::array<int,6>b{};std::vector<std::array<int,6>>o;auto f=[&](auto&&f,int i)->void{if(i==6){for(int q=0;q<3;++q){int s=0;for(int z=0;z<6;++z)if(g.cl[z]==q)s+=b[z];if(s)return;}int h=0;for(int z:b)h=std::gcd(h,std::abs(z));if(h!=1)return;for(int z:b)if(z){if(z<0)o.push_back(b);return;}return;}for(int z=-1;z<=1;++z){b[i]=z;f(f,i+1);}};f(f,0);return o;}
static I num(const G&g,const std::array<int,6>&a){I out=0;for(int x1=0;x1<6;++x1)for(int x2=0;x2<6;++x2)for(int x3=0;x3<6;++x3)for(int x4=0;x4<6;++x4){int x[5]{0,x1,x2,x3,x4};I v=1;for(auto nb:N){I s=0;for(int y=0;y<6;++y){I z=1;for(int i:nb)z*=a[g.m[g.iv[x[i]]][y]];s+=z;}v*=s;}out+=v;}return out;}
static I direct(const G&g,const std::array<int,6>&a){I out=0;for(int x0=0;x0<6;++x0)for(int x1=0;x1<6;++x1)for(int x2=0;x2<6;++x2)for(int x3=0;x3<6;++x3)for(int x4=0;x4<6;++x4)for(int y0=0;y0<6;++y0)for(int y1=0;y1<6;++y1)for(int y2=0;y2<6;++y2)for(int y3=0;y3<6;++y3)for(int y4=0;y4<6;++y4){int x[5]{x0,x1,x2,x3,x4},y[5]{y0,y1,y2,y3,y4};I z=1;for(int j=0;j<5;++j)for(int i:N[j])z*=a[g.m[g.iv[x[i]]][y[j]]];out+=z;}return out;}
static std::string key(const std::array<int,3>&c,const std::array<int,6>&b,int r){std::string s=std::to_string(c[0])+","+std::to_string(c[1])+","+std::to_string(c[2])+"\t";for(int i=0;i<6;++i){if(i)s+=',';s+=std::to_string(b[i]);}return s+'\t'+std::to_string(r);}
int main(int ac,char**av){if(ac!=2)return 2;std::filesystem::create_directories(av[1]);G g=gg();auto b=ds(g);std::ofstream o(std::string(av[1])+"/independent-rays.tsv");o<<"base\tdirection\tr\tsign\n";int rows=0,neg=0;for(int u=1;u<=2;++u)for(int v=1;v<=2;++v)for(int w=1;w<=2;++w){std::array<int,3>c{u,v,w},cc{8*u,8*v,8*w};std::array<int,6>central{};for(int z=0;z<6;++z)central[z]=cc[g.cl[z]];I nc=num(g,central);for(auto d:b)for(int r=-8;r<=8;++r){std::array<int,6>a{};bool ok=1;for(int z=0;z<6;++z){a[z]=8*c[g.cl[z]]+r*d[z];ok&=a[z]>=0;}if(!ok)continue;I diff=num(g,a)-nc;int s=(diff>0)-(diff<0);o<<key(c,d,r)<<'\t'<<s<<'\n';++rows;neg+=s<0;}}std::array<int,6>a{16,8,8,0,16,8};I n=num(g,a),d=direct(g,a);assert(d==6*n);std::ofstream z(std::string(av[1])+"/direct-control.txt");z<<"direct_equals_6_times_translation_fixed\n";std::ofstream j(std::string(av[1])+"/independent-summary.json");j<<"{\"status\":\"PASS\",\"rays\":"<<rows<<",\"negative_rays\":"<<neg<<",\"direct_control\":\"PASS\"}\n";}
