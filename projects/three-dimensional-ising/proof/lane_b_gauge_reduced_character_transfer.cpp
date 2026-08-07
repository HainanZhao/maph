// Gauge-reduced exact character transfer for Lane B strip certificates.

#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>

#ifdef _OPENMP
#include <omp.h>
#endif

using u64 = std::uint64_t;
#ifndef MODULUS
#define MODULUS 1000000007ULL
#endif
static constexpr u64 P = MODULUS;

struct EdgeData { int layer, axis, left, right; std::uint32_t label; };
static inline u64 addmod(u64 a,u64 b){a+=b;return a>=P?a-P:a;}
static inline u64 submod(u64 a,u64 b){return a>=b?a-b:a+P-b;}
static inline u64 mulmod(u64 a,u64 b){return (a*b)%P;}
static u64 power(u64 a,u64 e){u64 r=1;while(e){if(e&1)r=mulmod(r,a);a=mulmod(a,a);e>>=1;}return r;}

static void fwht(std::vector<u64>& a,bool inverse){
    int n=static_cast<int>(a.size());
    for(int len=1;len<n;len<<=1)for(int start=0;start<n;start+=2*len)for(int j=0;j<len;++j){
        u64 x=a[start+j],y=a[start+j+len];a[start+j]=addmod(x,y);a[start+j+len]=submod(x,y);
    }
    if(inverse){u64 s=power(n,P-2);for(u64&x:a)x=mulmod(x,s);}
}

static int project_bits(std::uint32_t character,std::uint32_t support){
    int result=0,out=0;
    for(int bit=0;support;++bit,support>>=1){if(!(support&1U))continue;if(character&(1U<<bit))result|=1<<out;++out;}
    return result;
}

static std::uint32_t expand_bits(int local,std::uint32_t support){
    std::uint32_t result=0;int input=0;
    for(int bit=0;support;++bit,support>>=1){if(!(support&1U))continue;if(local&(1<<input))result|=1U<<bit;++input;}
    return result;
}

int main(){
    int n,w,dimension,edge_count,regime;
    if(!(std::cin>>n>>w>>dimension>>edge_count>>regime))return 2;
    std::vector<EdgeData> edges(edge_count);
    for(auto&e:edges)std::cin>>e.layer>>e.axis>>e.left>>e.right>>e.label;
    int m=w*w,states=1<<(m-1),characters=1<<dimension;
    std::vector<std::vector<EdgeData>> transverse(n),connector(n-1);
    for(const auto&e:edges)(e.axis==0?connector[e.layer]:transverse[e.layer]).push_back(e);

    auto base_weight=[regime](int hash,int axis)->u64{
        if(regime==0)return 2+(static_cast<u64>(hash+1)*104729ULL)%(P-3);
        if(regime==2)return 2;
        static constexpr u64 weights[3]={2,3,5};return weights[axis];
    };

    // Classify every transverse character mode as a vertex coboundary or a
    // genuine residual mode.  Potentials are represented in the quotient
    // gauge with vertex zero fixed to zero, exactly matching the spin carrier.
    std::vector<std::uint32_t> residual_support(n,0);
    std::vector<std::vector<int>> exact_gauge(n,std::vector<int>(dimension,-1));
    for(int layer=0;layer<n;++layer){
        for(int bit=0;bit<dimension;++bit){
            bool occurs=false;
            for(const auto&e:transverse[layer])if(e.label&(1U<<bit)){occurs=true;break;}
            if(!occurs)continue;
            int witness=-1;
            for(int potential=0;potential<states&&witness<0;++potential){
                bool agree=true;
                for(const auto&e:transverse[layer]){
                    int left=e.left==0?0:((potential>>(e.left-1))&1);
                    int right=e.right==0?0:((potential>>(e.right-1))&1);
                    int mode=(e.label>>bit)&1U;
                    if((left^right)!=mode){agree=false;break;}
                }
                if(agree)witness=potential;
            }
            if(witness>=0)exact_gauge[layer][bit]=witness;
            else residual_support[layer]|=1U<<bit;
        }
        if(__builtin_popcount(residual_support[layer])>4){
            std::cerr<<"more than four nonexact local modes\n";return 4;
        }
    }

    std::vector<std::vector<u64>> intra_cache(n);
    for(int layer=0;layer<n;++layer){
        int variants=1<<__builtin_popcount(residual_support[layer]);
        intra_cache[layer].resize(static_cast<std::size_t>(variants)*states);
        #pragma omp parallel for schedule(static)
        for(int local=0;local<variants;++local){
            std::uint32_t character=expand_bits(local,residual_support[layer]);
            for(int spin=0;spin<states;++spin){
                u64 value=1;
                for(const auto&e:transverse[layer]){
                    int hash=((layer*m+e.left)*m+e.right)*3+e.axis;
                    u64 weight=base_weight(hash,e.axis);
                    if(__builtin_popcount(character&e.label)&1)weight=weight?P-weight:0;
                    int left=e.left==0?0:((spin>>(e.left-1))&1);
                    int right=e.right==0?0:((spin>>(e.right-1))&1);
                    value=mulmod(value,left==right?addmod(1,weight):submod(1,weight));
                }
                intra_cache[layer][static_cast<std::size_t>(local)*states+spin]=value;
            }
        }
    }

    std::vector<std::vector<u64>> kernel_hat(n-1,std::vector<u64>(states));
    for(int layer=0;layer+1<n;++layer){
        for(const auto&e:connector[layer])if(e.label){std::cerr<<"nonzero connector label\n";return 3;}
        for(int difference=0;difference<states;++difference){
            u64 plus=1,minus=1;
            for(const auto&e:connector[layer]){
                int hash=((layer*m+e.left)*m+e.right)*3+e.axis;u64 weight=base_weight(hash,e.axis);
                int bit=e.left==0?0:((difference>>(e.left-1))&1);
                plus=mulmod(plus,bit?submod(1,weight):addmod(1,weight));
                minus=mulmod(minus,bit?addmod(1,weight):submod(1,weight));
            }
            kernel_hat[layer][difference]=addmod(plus,minus);
        }
        fwht(kernel_hat[layer],false);
    }

    std::vector<u64> answer(characters);
    #pragma omp parallel for schedule(dynamic)
    for(int character=0;character<characters;++character){
        std::vector<u64> state(states),transformed(states);
        auto diagonal_parameters=[&](int layer)->std::pair<int,const u64*>{
            int gauge=0;
            for(int bit=0;bit<dimension;++bit)if((character&(1U<<bit))&&exact_gauge[layer][bit]>=0)gauge^=exact_gauge[layer][bit];
            int local=project_bits(character,residual_support[layer]);
            return {gauge,intra_cache[layer].data()+static_cast<std::size_t>(local)*states};
        };
        auto [first_gauge,first_diagonal]=diagonal_parameters(0);
        for(int spin=0;spin<states;++spin)state[spin]=first_diagonal[spin^first_gauge];
        for(int layer=0;layer+1<n;++layer){
            transformed=state;fwht(transformed,false);
            for(int i=0;i<states;++i)transformed[i]=mulmod(transformed[i],kernel_hat[layer][i]);
            fwht(transformed,true);
            auto [gauge,diagonal]=diagonal_parameters(layer+1);
            for(int spin=0;spin<states;++spin)state[spin]=mulmod(transformed[spin],diagonal[spin^gauge]);
        }
        u64 total=0;for(u64 x:state)total=addmod(total,x);answer[character]=addmod(total,total);
    }
    for(u64 x:answer)std::cout<<x<<'\n';
    return 0;
}
