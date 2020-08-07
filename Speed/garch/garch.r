#!/usr/local/bin/Rscript
options(stringsAsFactors =F)
suppressMessages(suppressWarnings(require(Rcpp)))
suppressMessages(suppressWarnings(require(compiler)))
suppressMessages(suppressWarnings(require(microbenchmark)))

y=read.table('data.dat')$V1

S=1e3
o=0.001
a=0.85
b=0.01
y2=y^2
N=length(y)


likelihood =function(o,a,b,y2,h,N){
	lik=0
	for(i in 2:N){
		h = o + a * y2[i-1]+ b * h
		lik = lik + log(h) + y2[i]/h
	}
	return(lik)
}

likelihood = cmpfun(likelihood)

var = var(y)

a1=microbenchmark(likelihood(o,a,b,y2=y2,h=var,N=N),times=S)
lik1= likelihood(o,a,b,y2=y2,h=var,N=N)

v=paste0(version$major,".",version$minor)

cat("output,R",v,",",lik1,",",min(a1$time/1e9)*1000,"\n")
