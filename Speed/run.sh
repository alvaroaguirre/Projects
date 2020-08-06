echo "" > x.out
    for i in 1 2 3 4 5
    do
        Rscript ./speed_R.R >> x.out
        Rscript ./R_compressed.R >> x.out
        python3 ./speed_python.py >> x.out
        python3 ./python_compressed.py >> x.out
        julia ./speed_julia.jl >> x.out
        julia ./julia_compressed.jl >> x.out
        /Applications/MATLAB_R2020a.app/bin/matlab -nodesktop   -nojvm -nodisplay -nosplash   -r "run('speed_MATLAB.m');exit;" >> x.out
    done
    
echo "type,language,operation,time" > x.csv
grep output x.out >> x.csv 

