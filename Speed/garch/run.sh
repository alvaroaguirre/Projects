#!/bin/bash
echo "starting " > x.out

echo "julia"
/Applications/Julia-1.5.app/Contents/Resources/julia/bin/julia ./garch.jl >> x.out

echo "R"
Rscript ./garch.r >> x.out

echo "Rcpp"
Rscript ./Rcpp.r >> x.out

echo "Python"
python3 ./garch.py >> x.out

echo "Numba"
python3 ./garch_numba.py >> x.out

echo "Matlab"
/Applications/MATLAB_R2020a.app/bin/matlab -nodesktop   -nojvm -nodisplay -nosplash   -r "run('garch.m');exit;" >> x.out

echo "C"
gcc -march=native -ffast-math -Ofast run.c
./a.out >> x.out
 
echo "type,language,likelihood,time" > x.csv
grep output x.out >> x.csv 

