#!/usr/local/bin/Rscript
options(stringsAsFactors =F)
suppressMessages(suppressWarnings(require(Rcpp)))
suppressMessages(suppressWarnings(require(microbenchmark)))
suppressMessages(suppressWarnings(require(compiler)))
#sourceCpp(file="garch.cpp")

y=read.table('data.dat')$V1

S=1e3
o=0.001
a=0.85
b=0.01
y2=y^2
N=length(y)

a = "double likelihood(double o, double a, double b, double h, NumericVector y2, int N){	
    double lik=0;
	for (int j=1;j<N;j++){
		h = o+a*y2[j-1]+b*h;	
		lik += log(h)+y2[j]/h;
	}
    return(lik);   
}"

cppFunction(a)

likelihood = cmpfun(likelihood)
var = var(y)

a1=microbenchmark(likelihood(0.001,0.85,0.01,var,y2,N),times=S)
lik1 = likelihood(0.001,0.85,0.01,var,y2,N)

v=paste0(version$major,".",version$minor)

cat("output,Rcpp",v,",",lik1,",",min(a1$time/1e9)*1000,"\n")
