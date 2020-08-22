#!/usr/local/bin/python3

# Python code for benchmarking

import timeit,sys,platform
import numpy as np
y = np.loadtxt('data.dat', delimiter = ',')

N = len(y)
o, a, b = 0.001, 0.85, 0.01
y2 = np.square(y)
S=1000
def likelihood(hh,o,a,b,y2,N):
    lik = 0.0
    h = hh
    for i in range(1,N):
        h=o+a*y2[i-1]+b*h
        lik += np.log(h) + y2[i]/h
    return(lik)

tic = timeit.default_timer()
lik = likelihood(np.var(y), o, a, b, y2, N)
toc = timeit.default_timer()

Best = 100
for s in range(S):
    tic = timeit.default_timer()
    lik = likelihood(np.var(y), o, a, b, y2, N)
    toc = timeit.default_timer()
    z = toc-tic
    if z < Best:
        Best = z
        
print("output,Python",platform.python_version(), ",",lik,", " + str(Best*1000))

