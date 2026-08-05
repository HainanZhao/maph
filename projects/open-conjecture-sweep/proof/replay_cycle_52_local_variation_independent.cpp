#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

using I=std::int64_t; using P=std::array<I,16>;
static constexpr std::array<std::pair<int,int>,15>E{{{0,2},{0,3},{0,4},{1,0},{1,3},{1,4},{2,0},{2,1},{2,4},{3,0},{3,1},{3,2},{4,1},{4,2},{4,3}}};
struct D{int q;std::vector<int>b;}; struct R{D d;P p{};int k=-1,s=0;};
static int gg(const std::vector<int>&x){int g=0;for(int z:x)g=std::gcd(g,std::abs(z));return g;}
static bool canon(const std::vector<int>&x){for(int z:x)if(z)return z<0;return false;}
static std::vector<D> make(int q){std::vector<std::pair<int,int>>v;for(int i=0;i<q;++i)for(int j=i;j<q;++j)v.push_back({i,j});std::vector<int>x(v.size());std::vector<D>o;auto f=[&](auto&&f,int a)->void{if(a==(int)x.size()){int s=0;for(int z=0;z<(int)x.size();++z)s+=(v[z].first==v[z].second?1:2)*x[z];if(s||gg(x)!=1||!canon(x))return;D d{q,std::vector<int>(q*q)};for(int z=0;z<(int)x.size();++z){auto[i,j]=v[z];d.b[i*q+j]=d.b[j*q+i]=x[z];}o.push_back(std::move(d));return;}for(int z=-2;z<=2;++z){x[a]=z;f(f,a+1);}};f(f,0);return o;}
static std::string mat(const D&d){std::ostringstream o;for(int i=0;i<d.q*d.q;++i){if(i)o<<',';o<<d.b[i];}return o.str();}
static std::string pol(const P&p){std::ostringstream o;for(int i=0;i<=15;++i){if(i)o<<',';o<<p[i];}return o.str();}
// Deliberately out-of-place recurrence in reverse edge order: coefficient k is
// the literal sum over k-edge subsets, grouped dynamically rather than expanded.
static P eval(const D&d){P ans{};int n=1;for(int i=0;i<10;++i)n*=d.q;for(int c=n;c-->0;){int z=c;std::array<int,10>a{};for(int i=0;i<10;++i){a[i]=z%d.q;z/=d.q;}P old{},nw{};old[0]=1;int deg=0;for(int ee=14;ee>=0;--ee){auto[l,r]=E[ee];int w=d.b[a[l]*d.q+a[5+r]];for(int k=0;k<=deg+1;++k)nw[k]=old[k]+(k?I(w)*old[k-1]:0);old=nw;nw={};++deg;}for(int k=0;k<=15;++k)ans[k]+=old[k];}ans[0]-=n;return ans;}
static int sign(const P&p,int&k){for(k=1;k<=15;++k)if(p[k])return(p[k]>0)-(p[k]<0);k=-1;return 0;}
static void literal_control(){D d{2,{1,-1,-1,1}};P a=eval(d),b{};for(int code=0;code<1024;++code){int z=code;std::array<int,10>x{};for(int i=0;i<10;++i){x[i]=z&1;z>>=1;}for(int mask=0;mask<(1<<15);++mask){int prod=1,k=0;for(int e=0;e<15;++e)if(mask&(1<<e)){auto[l,r]=E[e];prod*=d.b[x[l]*2+x[5+r]];++k;}b[k]+=prod;}}b[0]-=1024;assert(a==b);}
int main(int ac,char**av){if(ac!=2)return 2;std::filesystem::create_directories(av[1]);literal_control();auto a=make(2),b=make(3);a.insert(a.end(),b.begin(),b.end());assert(a.size()<=20000);std::vector<R>rs(a.size());for(int i=(int)a.size();i-->0;){rs[i].d=a[i];rs[i].p=eval(a[i]);rs[i].s=sign(rs[i].p,rs[i].k);}std::ofstream o(std::string(av[1])+"/independent-rows.tsv");o<<"q\tmatrix\tcoefficients_Q\tfirst_degree\tclassification\trealized_epsilon\n";int neg=0,pos=0,zero=0;for(int i=(int)rs.size();i-->0;){auto&r=rs[i];std::string c=r.s<0?"LOCAL_NEGATIVE":r.s>0?"LOCAL_POSITIVE":"IDENTICALLY_ZERO";neg+=r.s<0;pos+=r.s>0;zero+=r.s==0;o<<r.d.q<<'\t'<<mat(r.d)<<'\t'<<pol(r.p)<<'\t'<<r.k<<'\t'<<c<<"\t-\n";}std::ofstream j(std::string(av[1])+"/independent-summary.json");j<<"{\n  \"status\": \"PASS\",\n  \"direction_count\": "<<rs.size()<<",\n  \"local_negative\": "<<neg<<",\n  \"local_positive\": "<<pos<<",\n  \"identically_zero\": "<<zero<<"\n}\n";}
