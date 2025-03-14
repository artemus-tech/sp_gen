import constants as const
import Autoaxillary.common as cm
import config as cfg
from Autoaxillary.saxs import init_q_vector
from sp_assets import sp_volume, pdf
import numpy as np
import os
from scipy import integrate
from sp_assets import *

def get_global_radius(nc):
    mean_func = lambda r: r ** 3 * pdf(r)
    mean_int = integrate.quad(mean_func, 0, np.inf)[0]
    return np.sqrt(mean_int / nc)


def get_volume_mean():
    volume_func = lambda r: pdf(r) * sp_volume(r)
    all_vol = integrate.quad(volume_func, 0, np.inf)[0]

    pdf_func = lambda r: pdf(r)
    norm_pdf = integrate.quad(pdf_func, 0, np.inf)[0]

    return all_vol / norm_pdf

def get_sqr_volume_mean():
    sqr_mean_volume= lambda r: pdf(r) * sp_volume(r)**2
    sqr_all_volume = integrate.quad(sqr_mean_volume, 0, np.inf)[0]

    pdf_func = lambda r: pdf(r)
    norm_pdf = integrate.quad(pdf_func, 0, np.inf)[0]

    return sqr_all_volume / norm_pdf

def ksi(nu):
    meanfunc = lambda r: pdf(r) * np.power(2 * r, nu)
    mean_int = integrate.quad(meanfunc, 0, np.inf)[0]
    return c * mean_int

def Psi(X):
    return np.sinc(X / np.pi)

def Fi(X):
    return (3.0 / (X) ** 3.0 * (np.sin(X) - X * np.cos(X)))

def mean_dnu_eiX_Fi(q, nu):
    meanfuncRE = lambda r: pdf(r) * np.power(2 * r, nu) * np.cos(q * r) * Fi(q * r)
    mean_intRE = integrate.quad(meanfuncRE, 0, np.inf)[0]
    meanfuncIM = lambda r: pdf(r) * np.power(2 * r, nu) * np.sin(q * r) * Fi(q * r)
    mean_intIM = integrate.quad(meanfuncIM, 0, np.inf)[0]
    return c * (mean_intRE + 1j * mean_intIM)

def mean_dnu_eiX_Psi(q, nu):
    meanfuncRE = lambda r: pdf(r) * np.power(2 * r, nu) * np.cos(q * r) * Psi(q * r)
    mean_intRE = integrate.quad(meanfuncRE, 0, np.inf)[0]
    meanfuncIM = lambda r: pdf(r) * np.power(2 * r, nu) * np.sin(q * r) * Psi(q * r)
    mean_intIM = integrate.quad(meanfuncIM, 0, np.inf)[0]
    return c * (mean_intRE + 1j * mean_intIM)

def F11(q):
    return 1 - ksi(3) + mean_dnu_eiX_Fi(q, 3)

def F12(q):
    return mean_dnu_eiX_Fi(q, 4)

def F22(q):
    return 1 - ksi(3) + 3.0 * mean_dnu_eiX_Psi(q, 3)

def F21(q):
    return 0.5 * (1 - ksi(3)) * 1j * q - 3.0 * ksi(2) + 3.0 * mean_dnu_eiX_Psi(q, 2)

def DeltaK(q):
    return np.power(1 - ksi(3), -4) * np.abs(F11(q) * F22(q) - F12(q) * F21(q)) ** 2

def B(q, r):
    X = q * r
    return (3.0 / (X) ** 3.0 * (np.sin(X) - X * np.cos(X)))

def f(r):
    return sp_volume(r)

def mean_f_B_eiX(q):
    meanfuncRE = lambda r: pdf(r) * f(r) * B(q, r) * np.cos(q * r)
    mean_intRE = integrate.quad(meanfuncRE, 0, np.inf)[0]

    meanfuncIM = lambda r: pdf(r) * f(r) * B(q, r) * np.sin(q * r)
    mean_intIM = integrate.quad(meanfuncIM, 0, np.inf)[0]

    return c * (mean_intRE + 1j * mean_intIM)

def mean_d_f_B_eiX(q):
    meanfuncRE = lambda r: pdf(r) * (2 * r) * f(r) * B(q, r) * np.cos(q * r)
    mean_intRE = integrate.quad(meanfuncRE, 0, np.inf)[0]

    meanfuncIM = lambda r: pdf(r) * (2 * r) * f(r) * B(q, r) * np.sin(q * r)
    mean_intIM = integrate.quad(meanfuncIM, 0, np.inf)[0]

    return c * (mean_intRE + 1j * mean_intIM)

def T1(q):
    return F11(q) * F22(q) - F12(q) * F21(q)

def T2(q):
    return F21(q) * mean_d_f_B_eiX(q) - F22(q) * mean_f_B_eiX(q)

def T3(q):
    return F12(q) * mean_f_B_eiX(q) - F11(q) * mean_d_f_B_eiX(q)

def mean_f2_B2(q):
    meanfunc = lambda r: pdf(r) * f(r) ** 2 * B(q, r) ** 2
    mean_int = integrate.quad(meanfunc, 0, np.inf)[0]
    return c * mean_int

def mean_d6_Fi2(q):
    meanfunc = lambda r: pdf(r) * (2 * r) ** 6 * Fi(q * r) ** 2
    mean_int = integrate.quad(meanfunc, 0, np.inf)[0]
    return c * mean_int

def mean_d4_Psi2(q):
    meanfunc = lambda r: pdf(r) * (2 * r) ** 4 * Psi(q * r) ** 2
    mean_int = integrate.quad(meanfunc, 0, np.inf)[0]
    return c * mean_int

def mean_f_B_d3_Fi(q):
    meanfunc = lambda r: pdf(r) * f(r) * B(q, r) * (2 * r) ** 3 * Fi(q * r)
    mean_int = integrate.quad(meanfunc, 0, np.inf)[0]
    return c * mean_int

def mean_f_B_d2_Psi(q):
    meanfunc = lambda r: pdf(r) * f(r) * B(q, r) * (2 * r) ** 2 * Psi(q * r)
    mean_int = integrate.quad(meanfunc, 0, np.inf)[0]
    return c * mean_int

def mean_d5_FiPsi(q):
    meanfunc = lambda r: pdf(r) * (2 * r) ** 5 * Fi(q * r) * Psi(q * r)
    mean_int = integrate.quad(meanfunc, 0, np.inf)[0]
    return c * mean_int

def Df(q):
    AA = mean_f2_B2(q) * np.abs(T1(q)) ** 2
    BB = mean_d6_Fi2(q) * np.abs(T2(q)) ** 2
    CC = 9.0 * mean_d4_Psi2(q) * np.abs(T3(q)) ** 2
    DD = mean_f_B_d3_Fi(q) * 2 * np.real(T1(q) * np.conj(T2(q)))
    EE = 3.0 * mean_f_B_d2_Psi(q) * 2 * np.real(T1(q) * np.conj(T3(q)))
    FF = 3.0 * mean_d5_FiPsi(q) * 2 * np.real(T2(q) * np.conj(T3(q)))
    return (AA + BB + CC + DD + EE + FF) / (-np.pi / 6 * (1 - ksi(3)) ** 4)

def sum_intensity_vrija(q:np.ndarray)->np.ndarray:
    return -Df(q) / DeltaK(q)




if __name__ == "__main__":
    result_dir_path = cm.create_dir_with_date(
        path = const.current_path,
        prefix="sp_vrija_no_volume_complex"
    )

    settings = cfg.load_settings()

    shape = settings["shape"]  # = 3
    scale = settings["scale"]  # = 2
    NC = settings["NC"]  # = 0.4


    for nc in NC:
        c = np.pi * nc / (6.0 * get_volume_mean())

        q = init_q_vector(settings)

        result_file_path = os.path.join(result_dir_path, f"sp_vrija_no_volume_complex_nc={nc}[{q[0]},{q[-1]}].txt")

        vectorized_vrija_intensity = np.vectorize(sum_intensity_vrija)
        result = vectorized_vrija_intensity(q)/(nc* get_sqr_volume_mean())* get_volume_mean()

        np.savetxt(result_file_path , np.c_[q, result])