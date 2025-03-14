import os

import numpy as np
from matplotlib import pyplot as plt

path  = "C:\sp_gen\legacy\data\sp_avg_eval"

path_trapz_vrija ="C:\sp_gen\legacy\data\sp_trapz_vrija_2025-02-03_12-51-47"
path_integral  = "C:\sp_gen\legacy\data\sp_intensity_integral"
path_vrija ="C:\sp_gen\legacy\data\sp_vrija_no_volume_complex_2025-02-01_20-47-05"
path_to_lm_dec_file="C:\sp_gen\legacy\data\sp_lm_dec_intensity_2025-02-03_13-09-33"

path_to_integral_intensity_file = os.path.join(path_integral,"sp_intensity_integral[0.020000000000000007,4.999999999999999].txt")
path_to_vrija_file = os.path.join(path_vrija,"sp_vrija_no_volume_complex_nc=0.4[0.020000000000000007,4.999999999999999].txt")
path_to_lm_dec = os.path.join(path_to_lm_dec_file,"sp_lm_dec_intensity_nc=0.4_[0.020000000000000007,4.999999999999999].txt")
path_to_vrija_trapz_file =  os.path.join(path_trapz_vrija,"sp_vrija_trapz_nc=0.4[0.020000000000000007,4.999999999999999].txt")

path_100 = os.path.join(path,"sp_avg_eval_[349_448].txt")
path_50 = os.path.join(path,"sp_avg_eval_[949_1048].txt")
path_30 = os.path.join(path,"sp_avg_eval_[1149_1248].txt")
path_75 =os.path.join(path,"sp_avg_eval_[1249_1348].txt")
path_80 = os.path.join(path,"sp_avg_eval_[1349_1448].txt")


def func_norm(x, y, a, b):
    """Integral trapezoid norm"""
    filtered_x, filtered_y = zip(*[(xi, yi) for xi, yi in zip(x, y) if xi >= a and xi<=b])

    #print(filtered_x)
    #print(filtered_y)
    return np.sqrt(np.trapezoid(np.power(filtered_y, 2),filtered_x))
'''
x =np.linspace(1,10,10)
print(x)
y = x**2
a = 1
b = 3

f = norm_pdf(x, y, a,b)
print(f)

'''
q,I_avg_100,srd100 = list(np.loadtxt(path_100).T)
q,I_avg_30,srd30 = list(np.loadtxt(path_30).T)
q,I_avg_50,srd50 = list(np.loadtxt(path_50).T)

q, I_avg_75, std_75 = list(np.loadtxt(path_75).T)
q, I_avg_80, std_80 = list(np.loadtxt(path_80).T)
q,I_integral = list(np.loadtxt(path_to_integral_intensity_file).T)
q,I_vrija = list(np.loadtxt(path_to_vrija_file).T)
q,I_lm,I_dec = list(np.loadtxt(path_to_lm_dec).T)
q,I_vrija_trapz = list(np.loadtxt(path_to_vrija_trapz_file).T)



#fr100 = func_norm(q,S100, a=0,b=1 )
#fr30_100 = func_norm(q,S100-S30, a=0,b=1 )




#print(fr30_100/fr100)


def relative_distinction(arg, f1, f2, a,b):
    n1 = func_norm(arg, f1, a, b)
    n1_f2 = func_norm(arg, f1 - f2, a, b)
    return n1_f2/n1

S100  = I_avg_100/I_integral
S50  = I_avg_50/I_integral
S30  = I_avg_30/I_integral

S_lm = I_lm/I_integral
S_Dec = I_dec/I_integral
S_vrija = I_vrija/I_integral
sd100 = srd100/I_integral
result30 = relative_distinction(arg=q,f1=S100,f2=S30,a=0,b=1)
result50 = relative_distinction(arg=q,f1=S100,f2=S50,a=0,b=1)
result_sd100 = relative_distinction(arg=q,f1=S100,f2=S100+sd100,a=0,b=1)

result_lm = relative_distinction(arg=q,f1=S100,f2=S_lm,a=0,b=1)
result_dec= relative_distinction(arg=q,f1=S100,f2=S_Dec,a=0,b=1)
result_vrija = relative_distinction(arg=q,f1=S100,f2=S_vrija,a=0,b=1)

print(f'result50={result50}')
print(f'result30={result30}')
print(f'result_sd100={result_sd100}')
print(f'result_vrija={result_vrija}')
print(f'result_lm={result_lm}')
print(f'result_dec={result_dec}')
