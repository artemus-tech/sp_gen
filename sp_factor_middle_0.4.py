import os
import numpy as np
from matplotlib import pyplot as plt
import constants as const
import dbassets

path_to_integral_intensity_file = os.path.join(const.path_integral,"sp_intensity_integral[0.020000000000000007,4.999999999999999].txt")

nc=0.4
q0 = 0.02
qn = 5.0

path_to_vrija_file = os.path.join(const.path_vrija,f'sp_vrija_no_volume_complex_nc={nc}[{q0},{qn}].txt')
path_to_lm_dec_file = os.path.join(const.path_to_lm_dec,f'sp_lm_dec_intensity_nc={nc}[{q0},{qn}].txt')
path_to_vrija_trapezoid_file =  os.path.join(const.path_trapezoid_vrija,f'sp_vrija_trapezoid_nc={nc}[{q0},{qn}].txt')


sp_eval_avg_150 =dbassets.get_data_by_id(table_name="sp_eval_avg",column_name="row_id",record_id=410) ##dbassets.get_data_by_id()

sp_eval_avg_100 =dbassets.get_data_by_id(table_name="sp_eval_avg",column_name="row_id",record_id=100) ##dbassets.get_data_by_id()
sp_eval_avg_50 =dbassets.get_data_by_id(table_name="sp_eval_avg",column_name="row_id",record_id=124) #os.path.join(const.path_avg,"sp_avg_eval_[849_948].txt")
sp_eval_avg_30 =dbassets.get_data_by_id(table_name="sp_eval_avg",column_name="row_id",record_id=131) #os.path.join(const.path_avg,"sp_avg_eval_[1978_2067].txt")
sp_eval_avg_75 =dbassets.get_data_by_id(table_name="sp_eval_avg",column_name="row_id",record_id=109) #os.path.join(const.path_avg,"sp_avg_eval_[1978_2067].txt")
sp_eval_avg_80 =dbassets.get_data_by_id(table_name="sp_eval_avg",column_name="row_id",record_id=111) #os.path.join(const.path_avg,"sp_avg_eval_[1978_2067].txt")

sp_intens_sum_norm_avg_150 =dbassets.get_data_by_id(table_name="sp_intens_sum_norm_avg",column_name="row_id",record_id=410) ##dbassets.get_data_by_id()
sp_intens_sum_norm_avg_100 =dbassets.get_data_by_id(table_name="sp_intens_sum_norm_avg",column_name="row_id",record_id=100) ##dbassets.get_data_by_id()
sp_intens_sum_norm_avg_50 =dbassets.get_data_by_id(table_name="sp_intens_sum_norm_avg",column_name="row_id",record_id=124) #os.path.join(const.path_avg,"sp_avg_eval_[849_948].txt")
sp_intens_sum_norm_avg_30 =dbassets.get_data_by_id(table_name="sp_intens_sum_norm_avg",column_name="row_id",record_id=131) #os.path.join(const.path_avg,"sp_avg_eval_[1978_2067].txt")
sp_intens_sum_norm_avg_75 =dbassets.get_data_by_id(table_name="sp_intens_sum_norm_avg",column_name="row_id",record_id=109) #os.path.join(const.path_avg,"sp_avg_eval_[1978_2067].txt")
sp_intens_sum_norm_avg_80 =dbassets.get_data_by_id(table_name="sp_intens_sum_norm_avg",column_name="row_id",record_id=111) #os.path.join(const.path_avg,"sp_avg_eval_[1978_2067].txt")


def plot_intensity(data_q_Iavg_dI_nc_n:[(np.ndarray,float, int)], title):
    plt.figure(figsize=(8, 6))
    for q,Iavg,dI,nc,n in data_q_Iavg_dI_nc_n:
        #plt.plot(q, Iavg, label=f"Intensity NC={nc}, N={n}")
        if dI is not None:
            plt.errorbar(q, Iavg, yerr=dI, fmt='o', label=f'S(q) NC={nc}, N={n}', capsize=5)
        else:
            if n>0:
                plt.plot(q, Iavg,  label=f'S(q) NC={nc}, N={n}')
            if n==-1:
                plt.plot(q, Iavg, 'bx-' , label=f'S(q) NC={nc}, vrija')
            if n==-2:
                plt.plot(q, Iavg, 'ro-',  label=f'S(q) NC={nc}, vrija trapezoid')
            if n==-3:
                plt.plot(q, Iavg, 'g^-',  label=f'S(q) NC={nc}, LM proxima')
            if n==-4:
                plt.plot(q, Iavg, 'k*-',  label=f'S(q) NC={nc}, Dec Proxisma')


    plt.loglog()

    plt.xlabel('q (nm⁻¹)', fontsize=12)
    plt.ylabel('I (arb. units)', fontsize=12)
    plt.title(title, fontsize=14)
    plt.legend()
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)
    plt.show()








q, I_eval_avg_30, std_30 =list(np.loadtxt(sp_eval_avg_30["src_path"]).T)
q, I_eval_avg_50, std_50 =list(np.loadtxt(sp_eval_avg_50["src_path"]).T)
q, I_eval_avg_75, std_75 =list(np.loadtxt(sp_eval_avg_75["src_path"]).T)
q, I_eval_avg_80, std_80 =list(np.loadtxt(sp_eval_avg_80["src_path"]).T)
q, I_eval_avg_100, std_100 =list(np.loadtxt(sp_eval_avg_100["src_path"]).T)
q, I_eval_avg_150, std_150 =list(np.loadtxt(sp_eval_avg_150["src_path"]).T)


q, I_sum_avg_30, std_I_sum_avg_30 =list(np.loadtxt(sp_intens_sum_norm_avg_30["src_path_intensity_sum_norm_avg"]).T)
q, I_sum_avg_50, std_I_sum_avg_50 =list(np.loadtxt(sp_intens_sum_norm_avg_50["src_path_intensity_sum_norm_avg"]).T)
q, I_sum_avg_75,std_I_sum_avg_75 = list(np.loadtxt(sp_intens_sum_norm_avg_75["src_path_intensity_sum_norm_avg"]).T)
q, I_sum_avg_80, std_I_sum_avg_80 = list(np.loadtxt(sp_intens_sum_norm_avg_80["src_path_intensity_sum_norm_avg"]).T)
q, I_sum_avg_100 ,std_I_sum_avg_100 =list(np.loadtxt(sp_intens_sum_norm_avg_100["src_path_intensity_sum_norm_avg"]).T)
q, I_sum_avg_150,std_I_sum_avg_150 =list(np.loadtxt(sp_intens_sum_norm_avg_150["src_path_intensity_sum_norm_avg"]).T)

q,I_integral = list(np.loadtxt(path_to_integral_intensity_file).T)
q,I_vrija = list(np.loadtxt(path_to_vrija_file).T)
q,I_lm,I_dec = list(np.loadtxt(path_to_lm_dec_file).T)
q,I_vrija_trapz = list(np.loadtxt(path_to_vrija_trapezoid_file).T)


std_S_30 = get_s_sigma(I_eval_avg=I_eval_avg_30,
                       I_sum_avg=I_sum_avg_30,
                       std_I_eval_avg=std_30,
                       std_I_avg_sum=std_I_sum_avg_30)

std_S_50 = get_s_sigma(I_eval_avg=I_eval_avg_50,
                       I_sum_avg=I_sum_avg_50,
                       std_I_eval_avg=std_50,
                       std_I_avg_sum=std_I_sum_avg_50)

std_S_75 = get_s_sigma(I_eval_avg=I_eval_avg_75,
                       I_sum_avg=I_sum_avg_75,
                       std_I_eval_avg=std_75,
                       std_I_avg_sum=std_I_sum_avg_75)

std_S_80 = get_s_sigma(I_eval_avg=I_eval_avg_80,
                       I_sum_avg=I_sum_avg_80,
                       std_I_eval_avg=std_80,
                       std_I_avg_sum=std_I_sum_avg_80)

std_S_100 = get_s_sigma(I_eval_avg=I_eval_avg_100,
                       I_sum_avg=I_sum_avg_100,
                       std_I_eval_avg=std_100,
                       std_I_avg_sum=std_I_sum_avg_100)

std_S_150 = get_s_sigma(I_eval_avg=I_eval_avg_150,
                       I_sum_avg=I_sum_avg_150,
                       std_I_eval_avg=std_150,
                       std_I_avg_sum=std_I_sum_avg_150)


plot_intensity(data_q_Iavg_dI_nc_n=[#(q, I_eval_avg_30/I_sum_avg_30, std_S_30, nc, 30000),
                                    #(q, I_eval_avg_50/I_sum_avg_50, std_S_50, nc, 50000),
                                    #(q, I_eval_avg_75 / I_sum_avg_75, std_S_75, nc, 75000),
                                    #(q, I_eval_avg_80 / I_sum_avg_80, std_S_80, nc, 80000),
                                    (q, I_eval_avg_100/I_sum_avg_100, std_S_100, nc, 100000),
                                    (q, I_eval_avg_150 / I_sum_avg_150, std_S_150, nc, 150000),

                                    (q,I_vrija_trapz/I_integral, None, nc, -2),
                                    (q, I_vrija / I_integral, None, nc, -1),
                                    (q, I_lm / I_integral, None, nc, -3),
                                    (q, I_dec/I_integral, None, nc, -4),
                                   # (q,I_lm/I_integral, None,nc, -1)
                                    ], title=f"nc={nc}, gpt chat is ... of sheet")
