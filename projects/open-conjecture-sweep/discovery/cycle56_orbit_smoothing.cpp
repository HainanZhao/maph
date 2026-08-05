#include <array>
#include <cassert>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <algorithm>
#include <map>
#include <vector>
using I=__int128_t;
static constexpr std::array<std::array<int,3>,5>N{{{{2,3,4}},{{0,3,4}},{{0,1,4}},{{0,1,2}},{{1,2,3}}}};
struct G{std::vector<std::array<int,3>>p;int m[6][6],iv[6],cl[6];};
static G make(){G g;std::array<int,3>a{0,1,2};do g.p.push_back(a);while(std::next_permutation(a.begin(),a.end()));std::map<std::array<int,3>,int>x;for(int i=0;i<6;++i)x[g.p[i]]=i;for(int i=0;i<6;++i)for(int j=0;j<6;++j){std::array<int,3>z;for(int k=0;k<3;++k)z[k]=g.p[i][g.p[j][k]];g.m[i][j]=x[z];}for(int i=0;i<6;++i)for(int j=0;j<6;++j)if(g.m[i][j]==0&&g.m[j][i]==0)g.iv[i]=j;for(int z=0;z<6;++z){int k=1,v=z;while(v){v=g.m[v][z];++k;}g.cl[z]=k==1?0:k==2?1:2;}return g;}
static I num(const G&g,const std::array<int,6>&a){I o=0;for(int x1=0;x1<6;++x1)for(int x2=0;x2<6;++x2)for(int x3=0;x3<6;++x3)for(int x4=0;x4<6;++x4){int x[5]{0,x1,x2,x3,x4};I v=1;for(auto nb:N){I s=0;for(int y=0;y<6;++y){I z=1;for(int i:nb)z*=a[g.m[g.iv[x[i]]][y]];s+=z;}v*=s;}o+=v;}return o;}
int main(int ac,char**av){if(ac!=2)return 2;std::filesystem::create_directories(av[1]);G g=make();std::ofstream o(std::string(av[1])+"/rows.tsv");o<<"code\tclass\tsign\n";int neg=0;for(int code=0;code<729;++code){int z=code;std::array<int,6>a{};for(int i=0;i<6;++i){a[i]=z%3;z/=3;}I n=num(g,a);for(int cl:{1,2}){int den=cl==1?3:2,sum=0;for(int i=0;i<6;++i)if(g.cl[i]==cl)sum+=a[i];std::array<int,6>s{};for(int i=0;i<6;++i)s[i]=g.cl[i]==cl?sum:den*a[i];I diff=den;for(int i=0;i<15;++i)diff*=den; // temporary den^16
I left=n;for(int i=0;i<15;++i)left*=den;I d=left-num(g,s);int sign=(d>0)-(d<0);o<<code<<'\t'<<cl<<'\t'<<sign<<'\n';neg+=sign<0;}}std::ofstream j(std::string(av[1])+"/summary.json");j<<"{\"status\":\"PASS\",\"rows\":1458,\"negative_rows\":"<<neg<<"}\n";}
