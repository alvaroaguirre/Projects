#!/usr/local/bin/python3


# Python code for benchmarking

import timeit,sys,platform
import numpy as np
from numba import jit
y = np.loadtxt('data.dat', delimiter = ',')

N = len(y)
o, a, b = 0.001, 0.85, 0.01
y2 = np.square(y)
S=1000

@jit
def likelihood(hh,o,a,b,y2,N):
    lik = 0.0
    h = hh
    for i in range(1,N):
        h=o+a*y2[i-1]+b*h
        lik += np.log(h) + y2[i]/h
    return(lik)
    
Best = 100
var_y = np.var(y)
for s in range(S):
    tic = timeit.default_timer()
    lik = likelihood(var_y, o, a, b, y2, N)
    toc = timeit.default_timer()
    z = toc-tic
    if z < Best:
        Best = z
        
print("output,Numba + Python",platform.python_version(), ",",lik,", " + str(Best*1000))    
 
