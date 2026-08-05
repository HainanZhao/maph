#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <map>
#include <numeric>
#include <set>
#include <string>
#include <vector>

using M = std::uint64_t; using U = unsigned __int128;
struct G { std::string name; int n,e; std::vector<std::vector<int>> p; std::vector<int> q; std::vector<M> cc; };
static int pc(M x){return std::popcount(x);} static int lc(int a,int b){return a/std::gcd(a,b)*b;}
static std::string ds(U x){if(!x)return"0";std::string s;while(x){s.push_back('0'+x%10);x/=10;}std::reverse(s.begin(),s.end());return s;}
static void finish(G&g){g.q.assign(g.n,-1);for(int a=0;a<g.n;++a)for(int b=0;b<g.n;++b)if(g.p[a][b]==g.e&&g.p[b][a]==g.e)g.q[a]=b;for(int a:g.q)assert(a>=0);for(int a=0;a<g.n;++a)for(int b=0;b<g.n;++b)for(int c=0;c<g.n;++c)assert(g.p[g.p[a][b]][c]==g.p[a][g.p[b][c]]);std::vector<bool>seen(g.n);for(int x=0;x<g.n;++x)if(!seen[x]){M c=0;for(int h=0;h<g.n;++h)c|=M(1)<<g.p[g.p[g.q[h]][x]][h];for(int z=0;z<g.n;++z)if(c&(M(1)<<z))seen[z]=true;g.cc.push_back(c);}}
static G sn(int n){std::vector<std::array<int,4>>v;std::array<int,4>a{0,1,2,3};do{v.push_back(a);}while(std::next_permutation(a.begin(),a.begin()+n));std::map<std::array<int,4>,int>ix;for(int i=0;i<(int)v.size();++i)ix[v[i]]=i;G g{"S"+std::to_string(n),(int)v.size(),0,{},{},{}};g.p.assign(g.n,std::vector<int>(g.n));for(int i=0;i<g.n;++i)for(int j=0;j<g.n;++j){std::array<int,4>z{0,1,2,3};for(int k=0;k<n;++k)z[k]=v[i][v[j][k]];g.p[i][j]=ix[z];}finish(g);return g;}
static G d8(){G g{"D8",8,0,{},{},{}};g.p.assign(8,std::vector<int>(8));for(int r=0;r<4;++r)for(int s=0;s<2;++s)for(int u=0;u<4;++u)for(int t=0;t<2;++t)g.p[2*r+s][2*u+t]=2*((r+(s?-u:u)+4)%4)+((s+t)&1);finish(g);return g;}
static G q8(){int b[4][4]={{0,1,2,3},{1,0,3,2},{2,3,0,1},{3,2,1,0}},s[4][4]={{0,0,0,0},{0,1,0,1},{0,1,1,0},{0,0,1,1}};G g{"Q8",8,0,{},{},{}};g.p.assign(8,std::vector<int>(8));for(int x=0;x<8;++x)for(int y=0;y<8;++y)g.p[x][y]=2*b[x/2][y/2]+((x%2)^(y%2)^s[x/2][y/2]);finish(g);return g;}
static M cl(const G&g,M h){bool go=1;while(go){go=0;for(int a=0;a<g.n;++a)if(h&(M(1)<<a))for(int b=0;b<g.n;++b)if(h&(M(1)<<b)){M z=M(1)<<g.p[a][b];if(!(h&z)){h|=z;go=1;}}}return h;}
static std::vector<M> subs(const G&g){std::set<M>x{M(1)<<g.e};bool go=1;while(go){go=0;auto c=x;for(M h:c)for(int a=0;a<g.n;++a)if(!(h&(M(1)<<a)))go|=x.insert(cl(g,h|(M(1)<<a))).second;}return{x.begin(),x.end()};}
static M prod(const G&g,M a,M b){M z=0;for(int x=0;x<g.n;++x)if(a&(M(1)<<x))for(int y=0;y<g.n;++y)if(b&(M(1)<<y))z|=M(1)<<g.p[x][y];return z;}
static constexpr std::array<std::array<int,3>,5>N{{{{2,3,4}},{{0,3,4}},{{0,1,4}},{{0,1,2}},{{1,2,3}}}};
static U plain(const G&g,M a){std::vector<M>tr(g.n);for(int x=0;x<g.n;++x)for(int z=0;z<g.n;++z)if(a&(M(1)<<z))tr[x]|=M(1)<<g.p[x][z];U ans=0;for(int d=0;d<g.n;++d)for(int c=0;c<g.n;++c)for(int b=0;b<g.n;++b)for(int a1=0;a1<g.n;++a1){int x[5]{g.e,a1,b,c,d};U v=1;for(auto r:N)v*=pc(tr[x[r[0]]]&tr[x[r[1]]]&tr[x[r[2]]]);ans+=v;}return ans;}
static U averaged(const G&g,M a,int&q){q=1;for(M c:g.cc)q=lc(q,pc(c));std::vector<int>w(g.n);for(M c:g.cc){int z=q*pc(c&a)/pc(c);for(int x=0;x<g.n;++x)if(c&(M(1)<<x))w[x]=z;}U ans=0;for(int d=0;d<g.n;++d)for(int c=0;c<g.n;++c)for(int b=0;b<g.n;++b)for(int a1=0;a1<g.n;++a1){int x[5]{g.e,a1,b,c,d};U v=1;for(auto r:N){std::uint64_t u=0;for(int y=0;y<g.n;++y)u+=(std::uint64_t)w[g.p[g.q[x[r[0]]]][y]]*w[g.p[g.q[x[r[1]]]][y]]*w[g.p[g.q[x[r[2]]]][y]];v*=u;}ans+=v;}return ans;}
static void row(std::ofstream&o,const std::string&f,const G&g,M a,int&n,int&neg,std::string&first){int q;U x=plain(g,a),y=averaged(g,a,q),s=1;for(int i=0;i<15;++i)s*=q;int z=(x*s>y)-(x*s<y);o<<f<<'\t'<<g.name<<'\t'<<a<<'\t'<<pc(a)<<'\t'<<q<<'\t'<<ds(x)<<'\t'<<ds(y)<<'\t'<<z<<'\n';++n;if(z<0){++neg;if(first.empty())first=f+":"+g.name+":"+std::to_string(a);}}
int main(int ac,char**av){if(ac!=2)return 2;std::filesystem::create_directories(av[1]);G a=sn(3),b=sn(4),d=d8(),q=q8();std::ofstream o(std::string(av[1])+"/independent-comparison-rows.tsv");o<<"family\tgroup\tindicator_mask\tindicator_size\tclass_scale\tplain_numerator\taverage_scaled_numerator\tcomparison_sign\n";int n=0,neg=0;std::string first;for(G*g:std::vector<G*>{&q,&d,&a})for(M x=(M(1)<<g->n);x-->0;)row(o,"all_indicator",*g,x,n,neg,first);for(G*g:std::vector<G*>{&b,&a}){std::set<M>z;auto s=subs(*g);for(M x:s)for(M y:s)z.insert(prod(*g,x,y));for(auto it=z.rbegin();it!=z.rend();++it)row(o,"subgroup_product",*g,*it,n,neg,first);}std::ofstream j(std::string(av[1])+"/independent-summary.json");j<<"{\n  \"status\": \"PASS\",\n  \"comparison_rows\": "<<n<<",\n  \"negative_rows\": "<<neg<<",\n  \"first_countermodel\": "<<(first.empty()?"null":"\""+first+"\"")<<"\n}\n";}
