# -*- coding: utf-8 -*-
import os
import glob
import numpy as np
from itertools import product, combinations
import sp_assets as assets
from scipy import weave as weave
from scipy.weave import converters
from scipy.weave import ext_tools
from profiler import *
from sp_config import *

print "Just a begining"
 
def concentration(r_global, vr):
    """concentration"""
    return np.sum(np.power(vr,3)) / np.power(r_global,3)
   
def generate():
    with Profiler() as p:
        weave.inline(code,['x','y','z','r', 'vr', 'r_global','srcSize','n','Xend','Yend','Zend','Rend'], headers=['<math.h>'], force=1,compiler = 'gcc', verbose = 1, support_code = add_code)
 
def getSize(size,excess):
    return int(excess * size * 6.0/np.pi) 
 
def generate_rand_pdf(size, shape=3.0, scale=2.5):
    #newSize= getSize(size) 
    """generate gamma pdf"""
    gamma_pdf = np.random.gamma(shape,scale,size)
    gamma_pdf=np.sort(gamma_pdf)
    return np.array(gamma_pdf[::-1])
# config

# vector of Radius value
srcSize = getSize(n,excess)
vr = generate_rand_pdf(srcSize, shape, scale)
#vr = generate_rand_pdf(n, shape, scale)
pdfD = os.getcwd() + "/tmp/"
# check dirrectory existance
if not os.path.exists(pdfD):
    os.makedirs(pdfD)
#np.savetxt(pdfD+"pdf.txt",np.transpose([vr]))
#r_global = np.power(np.sum(np.power(vr,3))/NC, 1.0/3.0)

DCUBE = np.power( 4.0/3.0*np.pi*np.sum(np.power(vr,3)) / (excess*NC), 1.0/3.0 )
r_global=DCUBE /2.0
 
r_max = np.max(vr)
r_min = np.min(vr)
# declartion
#srcSize=getSize(n,excess)
x=np.zeros(srcSize)
y=np.zeros(srcSize)
z=np.zeros(srcSize)
r=np.zeros(srcSize)
##############################Result

Xend=np.zeros(n)
Yend=np.zeros(n)
Zend=np.zeros(n)
Rend=np.zeros(n)


# numerical concentration
#NC = concentration(r_global,vr)
 
cur_dir = os.getcwd()
print cur_dir 
# location to save path
gen="shape"+str(shape)+"_scale="+str(scale)+"_n=" + str(n) + "_rmax=" + str(r_max) + "_rmin=" + str(r_min) + "_R=" + str(r_global) + "_NC=" + str(NC)+ "_excess="+str(excess)
d = cur_dir + "/sp_gen/" + gen
# check dirrectory existance
if not os.path.exists(d):
    os.makedirs(d)
 
add_code = """

int intersect(double x[], double y[], double z[], double r[], double x0, double y0, double z0, double r0, double r_global, int n)
{
    int i;
    if(n > 0)
    {
        i = 0;
        while(i < n)
        {
            if(sqrt(pow(x[i] - x0, 2) + pow(y[i] - y0, 2) + pow(z[i] - z0, 2)) < r[i] + r0)
            {
                return 0;
            }
            i+=1;
        }
    }
    return 1;
}


int in_sphere(double x0, double y0, double z0, double r0, double r_global)
{
  //  int i;
  //  i = 0;

    if(sqrt(pow(x0, 2) + pow( y0, 2) + pow( z0, 2)) > r_global)
    {
        return 0;
     }
    return 1;
}


 
double uniform(double a, double b)
{  
    return rand() / (RAND_MAX + 1.0) * (b - a) + a;
}
"""
 
code="""
    /* generation */
    int i;
    i = 0;
    int k;
    k=0;
    int kEND;
    kEND=0;
    int try_count = 0;
    double x0, y0, z0, r0;
    srand(time(NULL));
    
    while(i < srcSize and try_count < pow(10,12))
    {
        
        x0 = (double)r_global * uniform(-1.0,1.0);
        y0 = (double)r_global * uniform(-1.0,1.0);
        z0 = (double)r_global * uniform(-1.0,1.0);
        r0 = vr[i];
        if(intersect(x, y, z, r, x0, y0, z0, r0, r_global, i) == 1)
        {
            x[i] = x0;
            y[i] = y0;
            z[i] = z0;
            r[i] = r0;
            printf("i = %d; Numbers of trying = %d; r[%d]  = %f\\n", i, try_count, i, r[i]);
            try_count = 0;
            i+=1;
        }
        try_count+=1;
    }
  
  
  
    while(k < srcSize)
    {
        if(in_sphere(x[k],y[k],z[k],r[k], r_global)==1)
        {    
             if(kEND < n)
             {
                Xend[kEND] = x[k];
                Yend[kEND] = y[k];
                Zend[kEND] = z[k];
                Rend[kEND] = r[k];
                kEND+=1;
              }
        }
        k+=1;
    }
"""
 
 
for i in range(file_numb):
    # generate cordinates arrays
    generate()   
    # save results
    MResultTranspose = np.transpose([Xend,Yend,Zend,Rend])
    save = MResultTranspose[~np.all(MResultTranspose == 0, axis=1)]
    np.savetxt(d + "/sp_gen@x_y_z_r_" + "No" + str(i) + ".txt", save)
 
assets.set_collection(cur_dir,"sp_gen", gen)
