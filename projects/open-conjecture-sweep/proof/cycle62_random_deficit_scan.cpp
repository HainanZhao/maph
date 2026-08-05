// Exact integer Zhao-deficit scan of C62 PCG64 composition rows.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <boost/multiprecision/cpp_int.hpp>
using I=boost::multiprecision::cpp_int;
static constexpr std::array<std::array<int,3>,5>N{{{{2,3,4}},{{0,3,4}},{{0,1,4}},{{0,1,2}},{{1,2,3}}}};
struct G{std::vector<std::array<int,3>>p;int m[6][6],iv[6],cl[6];};
static G group(){G g;std::array<int,3>a{0,1,2};do g.p.push_back(a);while(std::next_permutation(a.begin(),a.end()));std::map<std::array<int,3>,int>x;for(int i=0;i<6;++i)x[g.p[i]]=i;for(int i=0;i<6;++i)for(int j=0;j<6;++j){std::array<int,3>z;for(int k=0;k<3;++k)z[k]=g.p[i][g.p[j][k]];g.m[i][j]=x[z];}for(int i=0;i<6;++i)for(int j=0;j<6;++j)if(g.m[i][j]==0&&g.m[j][i]==0)g.iv[i]=j;for(int z=0;z<6;++z){int v=z,n=1;while(v){v=g.m[v][z];++n;}g.cl[z]=n==1?0:n==2?1:2;}return g;}
static I num(const G&g,const std::array<long long,6>&a){I out=0;for(int x1=0;x1<6;++x1)for(int x2=0;x2<6;++x2)for(int x3=0;x3<6;++x3)for(int x4=0;x4<6;++x4){int x[5]{0,x1,x2,x3,x4};I value=1;for(auto nb:N){I sum=0;for(int y=0;y<6;++y){I term=1;for(int i:nb)term*=a[g.m[g.iv[x[i]]][y]];sum+=term;}value*=sum;}out+=value;}return out;}
static I pow6(){I z=1;for(int k=0;k<15;++k)z*=6;return z;}
static std::string text(const I& x){return x.str();}
int main(int ac,char**av){if(ac!=3)return 2;std::ifstream in(av[1]);std::ofstream out(av[2]);G g=group();I scale=pow6(),minimum=0;bool have=false;long long count=0,negative=0;std::array<long long,6>first{},minrow{},a{};while(in>>a[0]>>a[1]>>a[2]>>a[3]>>a[4]>>a[5]){std::array<long long,6>b{};long long trans=a[1]+a[2]+a[5],cycles=a[3]+a[4];b[0]=6*a[0];for(int h:{1,2,5})b[h]=2*trans;for(int h:{3,4})b[h]=3*cycles;I f=scale*num(g,a)-num(g,b);if(!have||f<minimum){have=true;minimum=f;minrow=a;}if(f<0){if(!negative)first=a;++negative;}++count;}out<<"{\"status\":\"PASS\",\"rows\":"<<count<<",\"negative_rows\":"<<negative<<",\"minimum_deficit\":\""<<text(minimum)<<"\",\"minimum_row\":[";for(int i=0;i<6;++i){if(i)out<<',';out<<minrow[i];}out<<"],\"first_negative_row\":";if(negative){out<<'[';for(int i=0;i<6;++i){if(i)out<<',';out<<first[i];}out<<']';}else out<<"null";out<<"}\n";}
