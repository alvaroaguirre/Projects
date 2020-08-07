
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>
double likelihood(double o, double a, double b, double h, double *y2, int N){	
    double lik=0;
	for (int j=1;j<N;j++){
		h = o+a*y2[j-1]+b*h;	
		lik += log(h)+y2[j]/h;
	}
    return(lik);   
}

double vvar(double* v, size_t n)
{
    double mean = 0.0;
    for (int i = 0; i < n; i++) {
        mean += v[i];
    }
    mean /= n;

    double ssd = 0.0;
    for (int i = 0; i < n; i++) {
        ssd += (v[i] - mean) * (v[i] - mean);
    }
    return ssd / (n - 1);
}

int main()
{

 FILE *fp;
     fp = fopen("data.dat","r");
     int i;
    double var=0;
    double lik;
    double mean=0;
    int N=10000;
    
    double yy;
     double  y[N];
         double y2[N];
    for(i=0;i<N;i++) {
         fscanf(fp,"%lf", &yy);
         y[i]=yy;
         y2[i]=yy*yy;
 }
 fclose(fp);
    clock_t t;
    double v=vvar(y,N);
    int S=1000;
        double time_taken;
        double Best=1000.0; 
        for(int s=0;s<S;s++){
            t = clock();
            lik=likelihood(0.001,0.85,0.01, v,y2,N);
            t = clock() - t;
            time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
            if(time_taken < Best) Best=time_taken ; 
    }



 printf("output,C, %f, %f\n",lik,Best*1000);

 return 0;
}
