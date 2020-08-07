 
#include("run.jl")
using StatsBase
using DelimitedFiles
using Statistics

y = readdlm("data.dat")
y=y[:,1]
N=length(y)
S=1e3
o,a,b=[0.001,0.85,0.01]
y2=y.^2;
v=var(y);

function likelihood(o, a, b, h, y2, N)
    local lik = 0.0
    for i in 2:N
        h = o+a*y2[i-1]+b*h
        lik += log(h)+y2[i]/h
    end
    return(lik)
end

#global  lik=likelihood(o,a,b,v,y2,N)
lik=likelihood(o,a,b,v,y2,N)

Best=100
for s in 1:S
    global Best
    z= @timed likelihood(o,a,b,v,y2,N)
    if z[2]<Best
        Best=z[2]
    end
end
println("output,Julia ",VERSION, ",",lik,",",Best * 1000)
