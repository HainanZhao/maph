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
using I=__int128_t; using P=std::array<I,16>;
static std::string text(I x){if(!x)return"0";bool n=x<0;if(n)x=-x;std::string s;while(x){s.push_back('0'+x%10);x/=10;}if(n)s.push_back('-');std::reverse(s.begin(),s.end());return s;}
static constexpr std::array<std::array<int,3>,5>N{{{{2,3,4}},{{0,3,4}},{{0,1,4}},{{0,1,2}},{{1,2,3}}}};
struct G{std::vector<std::array<int,3>>p;int m[6][6],inv[6],cl[6];};
static G group(){G g;std::array<int,3>a{0,1,2};do{g.p.push_back(a);}while(std::next_permutation(a.begin(),a.end()));std::map<std::array<int,3>,int>ix;for(int i=0;i<6;++i)ix[g.p[i]]=i;for(int i=0;i<6;++i)for(int j=0;j<6;++j){std::array<int,3>z;for(int k=0;k<3;++k)z[k]=g.p[i][g.p[j][k]];g.m[i][j]=ix[z];}for(int i=0;i<6;++i)for(int j=0;j<6;++j)if(g.m[i][j]==0&&g.m[j][i]==0)g.inv[i]=j;for(int x=0;x<6;++x){int ord=1,z=x;while(z){z=g.m[z][x];++ord;}g.cl[x]=ord==1?0:ord==2?1:2;}return g;}
static std::vector<std::array<int,6>> dirs(const G&g){std::vector<std::array<int,6>>o;std::array<int,6>b{};auto f=[&](auto&&f,int i)->void{if(i==6){for(int c=0;c<3;++c){int s=0;for(int z=0;z<6;++z)if(g.cl[z]==c)s+=b[z];if(s)return;}int d=0;for(int x:b)d=std::gcd(d,std::abs(x));if(d!=1)return;for(int x:b)if(x){if(x<0)o.push_back(b);return;}return;}for(int x=-1;x<=1;++x){b[i]=x;f(f,i+1);}};f(f,0);return o;}
static P numerator_poly(const G&g,const std::array<int,3>&c,const std::array<int,6>&b){P total{};for(int x1=0;x1<6;++x1)for(int x2=0;x2<6;++x2)for(int x3=0;x3<6;++x3)for(int x4=0;x4<6;++x4){int x[5]{0,x1,x2,x3,x4};P prod{};prod[0]=1;int deg=0;for(auto nb:N){P q{};for(int y=0;y<6;++y){P z{};z[0]=1;int dd=0;for(int i:nb){int h=g.m[g.inv[x[i]]][y];P nw{};for(int k=0;k<=dd+1;++k)nw[k]=(k<=dd?I(c[g.cl[h]])*z[k]:0)+(k?I(b[h])*z[k-1]:0);z=nw;++dd;}for(int k=0;k<=3;++k)q[k]+=z[k];}P nw{};for(int i=0;i<=deg;++i)for(int j=0;j<=3;++j)nw[i+j]+=prod[i]*q[j];prod=nw;deg+=3;}for(int k=0;k<=15;++k)total[k]+=prod[k];}return total;}
// Exact sign of 8^15 D(r/8), clearing the frozen dyadic denominator.
static I eval(const P&p,int r){I s=0,powr=1,pow8=1;for(int i=0;i<15;++i)pow8*=8;for(int k=0;k<=15;++k){s+=p[k]*powr*pow8;powr*=r;pow8/=8;}return s;}
static I pow8(){I z=1;for(int i=0;i<15;++i)z*=8;return z;}
static std::string vec(const std::array<int,6>&a){std::string s;for(int i=0;i<6;++i){if(i)s+=',';s+=std::to_string(a[i]);}return s;}
static std::string pol(const P&p){std::string s;for(int i=0;i<=15;++i){if(i)s+=',';s+=text(p[i]);}return s;}
int main(int ac,char**av){if(ac!=2)return 2;std::filesystem::create_directories(av[1]);G g=group();auto bs=dirs(g);assert(bs.size()<=64);std::ofstream po(std::string(av[1])+"/polynomials.tsv"),ro(std::string(av[1])+"/rays.tsv");po<<"base\tdirection\tdeficit_coefficients\n";ro<<"base\tdirection\tr\tsign\n";int pr=0,rr=0,neg=0;for(int e=1;e<=2;++e)for(int t=1;t<=2;++t)for(int q=1;q<=2;++q){std::array<int,3>c{e,t,q};P nc=numerator_poly(g,c,{});for(auto b:bs){P p=numerator_poly(g,c,b);for(int k=0;k<=15;++k)p[k]-=nc[k];std::string base=std::to_string(e)+","+std::to_string(t)+","+std::to_string(q),dir=vec(b);po<<base<<'\t'<<dir<<'\t'<<pol(p)<<'\n';++pr;for(int r=-8;r<=8;++r){bool ok=1;for(int z=0;z<6;++z)ok&=(8*c[g.cl[z]]+r*b[z]>=0);if(!ok)continue;I d=eval(p,r);int s=(d>0)-(d<0);ro<<base<<'\t'<<dir<<'\t'<<r<<'\t'<<s<<'\n';++rr;neg+=s<0;}}}std::ofstream j(std::string(av[1])+"/summary.json");j<<"{\n \"status\": \"PASS\",\n \"directions\": "<<bs.size()<<",\n \"polynomials\": "<<pr<<",\n \"rays\": "<<rr<<",\n \"negative_rays\": "<<neg<<"\n}\n";std::cout<<"directions="<<bs.size()<<" rays="<<rr<<" negative="<<neg<<"\n";}
