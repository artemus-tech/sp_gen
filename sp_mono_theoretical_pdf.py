import os
import numpy as np
import config as cfg
from Autoaxillary.saxs import init_q_vector
from scipy import integrate
from sp_assets import sp_volume,pdf
import constants as const
import Autoaxillary.common as cm

def first_summand_NSQRFdx(q):
    integrand_func_Ni_sqrFi = lambda r : pdf(r) * np.power(sp_form_factor(q,r),2)
    int_res_ni_fi = integrate.quad(integrand_func_Ni_sqrFi, 0, np.inf)[0]
    return int_res_ni_fi

def second_summand_NSQRFdx(q):
    integrand_func_Ni_Fi = lambda r: pdf(r) * sp_form_factor(q, r)
    int_res_ni_fi = integrate.quad(integrand_func_Ni_Fi,  0, np.inf)[0]
    return np.power(int_res_ni_fi, 2)

def one_div_ni():
    Ni_func = lambda Rg: pdf(Rg)
    ni = integrate.quad(Ni_func,  0, np.inf)[0]
    return np.power(ni,-1)

def stucture_factor(q):
    alpha = (1 + 2 * NC)**2 / (1 - NC)**4
    betta = -6 * NC * (1 + 0.5 * NC)**2/ (1 - NC)**4
    gamma = NC * alpha * 0.5

    A = 2 * Rhs * q

    G = alpha * (np.sin(A) - A * np.cos(A)) / A**2 + betta * (2 * A * np.sin(A) + (2 - A**2) * np.cos(A) - 2) /A**3 + gamma * (-A**4 * np.cos(A) + 4 * ((3 * A**2 - 6) * np.cos(A) + (A**3 - 6 * A) * np.sin(A) + 6)) / A**5
    Shs = 1 / (1 + 24 * NC * G / A)
    return Shs



def sum_dec_intensity(q):
    v_sqr = lambda r: pdf(r) * sp_volume(r) ** 2
    return (first_summand_NSQRFdx(q) + one_div_ni() * second_summand_NSQRFdx(q) * (stucture_factor(q) - 1))/integrate.quad(v_sqr, 0, np.inf)[0]



def sp_form_factor(q,r):
    x = q * r  
    V = sp_volume(r)
    return 3 * V * (np.sin(x) - x * np.cos(x)) / x**3


def stucture_factor_lm(q,Rp):
    alpha = (1.0 + 2.0 * NC)**2 / (1 - NC)**4
    betta = -6 * NC * (1 + 0.5 * NC)**2/ (1 - NC)**4
    gamma = NC * alpha * 0.5

    A = 2 * Rp * q

    G = alpha * (np.sin(A) - A * np.cos(A)) / A**2 + betta * (2 * A * np.sin(A) + (2 - A**2) * np.cos(A) - 2) /A**3 + gamma * (-A**4 * np.cos(A) + 4 * ((3 * A**2 - 6) * np.cos(A) + (A**3 - 6 * A) * np.sin(A) + 6)) / A**5
    Shs = 1.0 / (1.0 + 24.0 * NC * G / A)
    return Shs


def sum_intensity_local_monodisperse(q):
    func = lambda r:pdf(r) * sp_form_factor(q,r)**2 * stucture_factor_lm(q,r)
    v_sqr = lambda r:pdf(r)*sp_volume(r)**2
    return integrate.quad(func, 0, np.inf)[0]/integrate.quad(v_sqr, 0, np.inf)[0]




if __name__ == "__main__":
    result_dir_path = cm.create_dir_with_date(
        path=const.current_path,
        prefix="sp_lm_dec_intensity"
    )

    settings = cfg.load_settings()

    shape = settings["shape"]  # = 3
    scale = settings["scale"]  # = 2
    Rhs=shape*scale

    NCList = settings["NC"]  # = 0.4

    q = init_q_vector(settings)
    for nc in NCList:
        NC=nc
        vectorized_lm_intensity = np.vectorize(sum_intensity_local_monodisperse)
        result_lm = vectorized_lm_intensity(q)

        vectorized_dec_intensity = np.vectorize(sum_dec_intensity)
        result_dec = vectorized_dec_intensity(q)

        result_file_path = os.path.join(result_dir_path, f"sp_lm_dec_intensity_nc={nc}_[{q[0]},{q[-1]}].txt")
        np.savetxt(result_file_path , np.c_[q, result_lm,result_dec])