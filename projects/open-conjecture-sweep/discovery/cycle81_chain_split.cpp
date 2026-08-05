#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <stdexcept>
#include <vector>
using U=unsigned long long;
struct P{int n;std::vector<unsigned> pre;};
P closure(P q){for(int k=0;k<q.n;k++)for(int v=0;v<q.n;v++)if(q.pre[v]>>k&1)q.pre[v]|=q.pre[k];return q;}
std::vector<std::vector<U>> counts(const P&p){
 int N=1<<p.n;std::vector<U>f(N),b(N);f[0]=1;b[N-1]=1;
 for(int m=0;m<N;m++)if(f[m])for(int v=0;v<p.n;v++)if(!(m>>v&1)&&(p.pre[v]&~m)==0)f[m|1<<v]+=f[m];
 for(int m=N-2;m>=0;m--)for(int v=0;v<p.n;v++)if(!(m>>v&1)&&(p.pre[v]&~m)==0)b[m]+=b[m|1<<v];
 std::vector<std::vector<U>>c(p.n,std::vector<U>(p.n));
 for(int m=0;m<N;m++)for(int v=0;v<p.n;v++)if(!(m>>v&1)&&(p.pre[v]&~m)==0)for(int a=0;a<p.n;a++)if(m>>a&1)c[a][v]+=f[m]*b[m|1<<v];
 return c;
}
P split(const P&p,int a,bool upper){
 P q{p.n+1,std::vector<unsigned>(p.n+1)};for(int v=0;v<p.n;v++)q.pre[v]=p.pre[v];
 if(upper){for(int v=0;v<p.n;v++)if(p.pre[v]>>a&1)q.pre[v]|=1<<p.n;q.pre[p.n]=p.pre[a]|(1<<a);}
 else {q.pre[a]|=1<<p.n;q.pre[p.n]=p.pre[a];}
 return closure(q);
}
bool majority(const std::vector<std::vector<U>>&c,int a,int b){return c[a][b]>c[b][a];}
bool cyc4(const std::vector<std::vector<U>>&c,const P&p,bool inc){int n=p.n;for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(i!=j&&majority(c,i,j)&&(!inc||(!(p.pre[i]>>j&1)&&!(p.pre[j]>>i&1))))for(int k=0;k<n;k++)for(int l=0;l<n;l++)if(i!=k&&i!=l&&j!=k&&j!=l&&k!=l){auto ok=[&](int a,int b){return majority(c,a,b)&&(!inc||(!(p.pre[a]>>b&1)&&!(p.pre[b]>>a&1)));};if(ok(j,k)&&ok(k,l)&&ok(l,i))return true;}return false;}
void controls(){
 P anti{4,std::vector<unsigned>(4)};auto a=counts(anti);if(a[0][1]!=12||a[1][0]!=12)throw std::runtime_error("antichain control");
 P chain{4,std::vector<unsigned>(4)};for(int j=0;j<4;j++)for(int i=0;i<j;i++)chain.pre[j]|=1<<i;auto c=counts(chain);if(c[0][3]!=1||c[3][0]!=0)throw std::runtime_error("chain control");
 P one{4,std::vector<unsigned>(4)};one.pre[1]=1;auto o=counts(one);if(o[0][1]!=12||o[1][0]!=0||o[0][2]!=8||o[2][0]!=4)throw std::runtime_error("one-relation control");
}
int main(int ac,char**av){
 controls();uint64_t s=ac>1?std::stoull(av[1]):81001;std::mt19937_64 r(s);int rooted_tri=0,triangle_sets=0,upper_hit=0,lower_hit=0;bool emitted=false;
 for(int t=0;t<20000;t++){P p{9,std::vector<unsigned>(9)};for(int i=0;i<9;i++)for(int j=i+1;j<9;j++)if(r()%100<30)p.pre[j]|=1<<i;p=closure(p);auto c=counts(p);for(int a=0;a<9;a++)for(int b=0;b<9;b++)for(int d=0;d<9;d++)if(a!=b&&b!=d&&a!=d&&majority(c,a,b)&&majority(c,b,d)&&majority(c,d,a)){rooted_tri++;if(a<b&&a<d)triangle_sets++;if(!emitted){std::cout<<"witness "<<s<<" "<<t<<" "<<a<<" "<<b<<" "<<d<<" pre";for(unsigned x:p.pre)std::cout<<" "<<x;std::cout<<" counts "<<c[a][b]<<" "<<c[b][a]<<" "<<c[b][d]<<" "<<c[d][b]<<" "<<c[d][a]<<" "<<c[a][d]<<"\n";emitted=true;}for(int orientation=0;orientation<2;orientation++){auto q=split(p,a,orientation==0);auto z=counts(q);if(cyc4(z,q,false)&&!cyc4(z,q,true)){if(orientation==0)upper_hit++;else lower_hit++;}}}}
 std::cout<<s<<" rooted_triangles="<<rooted_tri<<" triangle_vertex_sets="<<triangle_sets<<" upper_hits="<<upper_hit<<" lower_hits="<<lower_hit<<"\n";
}
