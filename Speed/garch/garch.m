

format compact
load('data.dat') ;
y=data;

N=length(y);
S=1e3;

o=0.001;
a=0.85;
b=0.01;

lik=0;
h=var(y);
y2=y.^2;
small=900;
v=var(y);
for j = 1:S
    tic;
    lik=likelihood(o,a,b,v,y2,N);
    t=toc;

    if t<small
        small=t;
    end
  end

X = sprintf('output,Matlab %s, %f, %f', version('-release'),lik,small*1000);
disp(X)