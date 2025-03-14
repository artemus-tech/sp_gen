import os

import numpy as np
from matplotlib import pyplot as plt

path  = "C:\sp_gen\legacy\data\sp_avg_eval"

path_trapz_vrija ="C:\sp_gen\legacy\data\sp_trapz_vrija_2025-02-03_12-51-47"
path_integral  = "C:\sp_gen\legacy\data\sp_intensity_integral"
path_vrija ="C:\sp_gen\legacy\data\sp_vrija_no_volume_complex_2025-02-01_20-47-05"
#path_lm_dec = "C:\sp_gen\legacy\data\sp_lm_dec_intensity_2025-02-01_22-13-12"
path_to_lm_dec_file="C:\sp_gen\legacy\data\sp_lm_dec_intensity_2025-02-03_13-09-33"
path_to_integral_intensity_file = os.path.join(path_integral,"sp_intensity_integral[0.020000000000000007,4.999999999999999].txt")
path_to_vrija_file = os.path.join(path_vrija,"sp_vrija_no_volume_complex_nc=0.4[0.020000000000000007,4.999999999999999].txt")
path_to_lm_dec = os.path.join(path_to_lm_dec_file,"sp_lm_dec_intensity_nc=0.4_[0.020000000000000007,4.999999999999999].txt")
path_to_vrija_trapz_file =  os.path.join(path_trapz_vrija,"sp_vrija_trapz_nc=0.4[0.020000000000000007,4.999999999999999].txt")


path_100 = os.path.join(path,"sp_avg_eval_[349_448].txt")
path_50 = os.path.join(path,"sp_avg_eval_[949_1048].txt")
path_30 = os.path.join(path,"sp_avg_eval_[1149_1248].txt")
path_75 =os.path.join(path,"sp_avg_eval_[1776_1867].txt")
path_80 = os.path.join(path,"sp_avg_eval_[1878_1967].txt")





def plot_intensity(data_q_Iavg_dI_nc_n:[(np.ndarray,float, int)], title):
    plt.figure(figsize=(8, 6))
    for q, Iavg,dI,nc,n in data_q_Iavg_dI_nc_n:

        if dI is not None:
            plt.errorbar(q, Iavg, yerr=dI, fmt='o', label=f'S(q) NC={nc}, N={n}', capsize=5)
        else:
            if n>0:
                plt.plot(q, Iavg,  label=f'S(q) NC={nc}, N={n}')
            if n==-1:
                plt.plot(q, Iavg, 'b--' , label=f'S(q) NC={nc}, vrija')
            if n==-2:
                plt.plot(q, Iavg, 'r--',  label=f'S(q) NC={nc}, vrija trapezoid')
            if n==-3:
                plt.plot(q, Iavg, 'g--',  label=f'S(q) NC={nc}, LM proxima')
            if n==-4:
                plt.plot(q, Iavg, 'k--',  label=f'S(q) NC={nc}, Dec Proxima')
    plt.loglog()

    plt.xlabel('q (nm⁻¹)', fontsize=12)
    plt.ylabel('I (arb. units)', fontsize=12)
    plt.title(title, fontsize=14)
    plt.legend()
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)
    plt.show()

q, I_avg_30, std_30 =list (np.loadtxt(path_30).T)
q, I_avg_50, std_50 = list(np.loadtxt(path_50).T)
q, I_avg_100, std_100 = list(np.loadtxt(path_100).T)
q, I_avg_75, std_75 = list(np.loadtxt(path_75).T)
q, I_avg_80, std_80 = list(np.loadtxt(path_80).T)

q,I_integral = list(np.loadtxt(path_to_integral_intensity_file).T)

q,I_vrija = list(np.loadtxt(path_to_vrija_file).T)
q,I_lm,I_dec = list(np.loadtxt(path_to_lm_dec).T)
q,I_vrija_trapz = list(np.loadtxt(path_to_vrija_trapz_file).T)

plot_intensity(data_q_Iavg_dI_nc_n=[(q, I_avg_30/I_integral, std_30, 0.4, 30000),
                                    (q, I_avg_50/I_integral, std_50, 0.4, 50000),
                                    (q, I_avg_75 / I_integral, std_75, 0.4, 75000),
                                    (q, I_avg_80 / I_integral, std_80, 0.4, 80000),

                                    (q, I_avg_100/I_integral, std_100, 0.4, 100000),
                                    (q, I_vrija / I_integral, None, 0.4, -1),
                                    (q, I_lm / I_integral, None, 0.4, -3),
                                    (q, I_dec/I_integral, None, 0.4, -4),
                                    ], title=f"nc={0.4}, gpt chat is ... of sheet")
