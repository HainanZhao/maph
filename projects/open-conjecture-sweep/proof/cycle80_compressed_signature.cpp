// C80 bounded exact witness search for the d=6,m=7 compressed PAF system.
#include <algorithm>
#include <array>
#include <chrono>
#include <climits>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <map>
#include <random>
#include <vector>

struct G { int x=0,y=0; };
G add(G a,G b){return {a.x+b.x,a.y+b.y};}
G sub(G a,G b){return {a.x-b.x,a.y-b.y};}
G cj(G a){return {a.x,-a.y};}
G mul(G a,G b){return {a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x};}
using V=std::array<G,7>;
std::vector<G> D; std::map<std::pair<int,int>,std::vector<std::pair<int,int>>> pairs;
long long cost(const V&a,const V&b){
 long long z=0; for(int s=0;s<7;s++){G q{}; for(int j=0;j<7;j++){q=add(q,mul(a[j],cj(a[(j+s)%7])));q=add(q,mul(b[j],cj(b[(j+s)%7])));}
 int t=s? -12:74; z+=1LL*(q.x-t)*(q.x-t)+1LL*q.y*q.y;} return z;
}
bool initial(V&v,G target,std::mt19937_64&r){
 std::uniform_int_distribution<int> u(0,(int)D.size()-1);
 for(int tries=0;tries<10000;tries++){G s{};for(int j=0;j<6;j++){v[j]=D[u(r)];s=add(s,v[j]);}G q=sub(target,s);
  if(std::find_if(D.begin(),D.end(),[&](G w){return w.x==q.x&&w.y==q.y;})!=D.end()){v[6]=q;return true;}} return false;
}
void mutate(V&v,std::mt19937_64&r){
 std::uniform_int_distribution<int> p(0,6); int i=p(r),j=p(r);if(i==j)j=(j+1)%7;
 auto &q=pairs[{v[i].x+v[j].x,v[i].y+v[j].y}]; if(q.size()<2)return;
 std::uniform_int_distribution<int> u(0,(int)q.size()-1);auto t=q[u(r)];v[i]=D[t.first];v[j]=D[t.second];
}
int main(int argc,char**argv){
 for(int x=-6;x<=6;x++)for(int y=-6;y<=6;y++)if(std::abs(x)+std::abs(y)<=6 && ((x+y-6)&1)==0)D.push_back({x,y});
 for(int i=0;i<(int)D.size();i++)for(int j=0;j<(int)D.size();j++)pairs[{D[i].x+D[j].x,D[i].y+D[j].y}].push_back({i,j});
 uint64_t seed=argc>1?std::stoull(argv[1]):71237;std::mt19937_64 r(seed);V a,b;long long best=LLONG_MAX;V ba,bb;
 for(int restart=0;restart<10000;restart++){if(!initial(a,{0,0},r)||!initial(b,{1,1},r))return 2;long long c=cost(a,b);
  for(int it=0;it<20000;it++){V oa=a,ob=b; if(r()&1)mutate(a,r);else mutate(b,r);long long n=cost(a,b);double T=20.0*(1.0-double(it)/20000.0)+0.05;
   if(n<=c || std::generate_canonical<double,53>(r)<std::exp(double(c-n)/T))c=n;else{a=oa;b=ob;} if(c<best){best=c;ba=a;bb=b;} if(!c){std::cout<<"{\"status\":\"WITNESS\",\"seed\":"<<seed<<",\"cost\":0,\"A\":[";for(int j=0;j<7;j++)std::cout<<(j?",":"")<<"["<<a[j].x<<","<<a[j].y<<"]";std::cout<<"],\"B\":[";for(int j=0;j<7;j++)std::cout<<(j?",":"")<<"["<<b[j].x<<","<<b[j].y<<"]";std::cout<<"]}\n";return 0;}}}
 std::cout<<"{\"status\":\"CAP\",\"seed\":"<<seed<<",\"best_exact_residual\":"<<best<<"}\n";return 0;
}
