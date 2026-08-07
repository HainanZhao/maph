#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <tuple>
#include <vector>
using namespace std;
int main(){
  map<pair<int,int>,long long> prof; vector<tuple<int,int,int>> hits; long long states=0;
  for(int a=0;a<16;a++) for(int b=a+1;b<16;b++){
    array<int,14> v{}; for(int x=0,k=0;x<16;x++) if(x!=a&&x!=b) v[k++]=x;
    for(int mask=0;mask<(1<<13);mask++){
      int d[14]; d[0]=1; for(int i=1;i<14;i++) d[i]=((mask>>(i-1))&1)?1:-1;
      bool adj[14][14]{};
      for(int i=0;i<14;i++) for(int j=i+1;j<14;j++){
        int base=__builtin_parity((unsigned)(v[i]&v[j]))?-1:1;
        adj[i][j]=adj[j][i]=(d[i]*base*d[j]==-1);
      }
      int red=0,blue=0;
      for(int i=0;i<14;i++) for(int j=i+1;j<14;j++){
        int k=0; for(int z=0;z<14;z++) if(z!=i&&z!=j&&adj[i][z]==adj[i][j]&&adj[j][z]==adj[i][j])k++;
        if(adj[i][j])red=max(red,k); else blue=max(blue,k);
      }
      prof[{red,blue}]++; states++;
      if(red<=2&&blue<=3) hits.emplace_back(a,b,mask);
    }
  }
  cout<<"{\"status\":\"PASS\",\"states\":"<<states<<",\"hits\":[";
  for(size_t i=0;i<hits.size();i++){auto [a,b,m]=hits[i];if(i)cout<<",";cout<<"["<<a<<","<<b<<","<<m<<"]";}
  cout<<"],\"profiles\":["; bool first=true; for(auto const&[p,n]:prof){if(!first)cout<<",";first=false;cout<<"[["<<p.first<<","<<p.second<<"],"<<n<<"]";} cout<<"]}\n";
}
