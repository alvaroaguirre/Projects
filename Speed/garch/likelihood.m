function lik = likelihood(o,a,b,h,y2,N)
    lik=0;
    for i = 2:N
        h=o+a*y2(i-1)+b*h;
        lik=lik+log(h)+y2(i)/h;
    end
end


