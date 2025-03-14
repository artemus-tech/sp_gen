import glob
import os
import fnmatch
import scipy as sps
from scipy import integrate
import constants as const
import Autoaxillary.common as cm
import config as cfg
import numpy as np

from Autoaxillary.saxs import init_q_vector
from sp_assets import sp_volume, pdf

lim_const = np.power(10, 3)
Epsrel = 1.49e-03


def get_Vmean():
    Vfunc = NDF * sp_volume(vector_rg)
    all_vol = np.trapezoid(Vfunc, vector_rg)
    norm_pdf = np.trapezoid(NDF,vector_rg)
    return all_vol / norm_pdf


def get_RGlob(nc):
    meanfunc = vector_rg ** 3 * NDF
    mean_int = np.trapezoid(meanfunc, vector_rg)
    return np.sqrt(mean_int / nc)


def ksi(nu):
    mean_func = NDF * np.power(2 * vector_rg, nu)
    mean_int = np.trapezoid(mean_func, vector_rg)
    return c * mean_int


def Psi(X):
    return np.sinc(X / np.pi)


def Fi(X):
    return (3.0 / (X) ** 3.0 * (np.sin(X) - X * np.cos(X)))


def mean_dnu_eiX_Fi(q, nu):
    meanfuncRE = NDF * np.power(2 * vector_rg, nu) * np.cos(q * vector_rg) * Fi(q * vector_rg)
    mean_intRE = np.trapezoid(meanfuncRE, vector_rg)
    meanfuncIM = NDF * np.power(2 * vector_rg, nu) * np.sin(q * vector_rg) * Fi(q * vector_rg)
    mean_intIM = np.trapezoid(meanfuncIM, vector_rg)
    return c * (mean_intRE + 1j * mean_intIM)


def mean_dnu_eiX_Psi(q, nu):
    meanfuncRE = NDF * np.power(2 * vector_rg, nu) * np.cos(q * vector_rg) * Psi(q * vector_rg)
    mean_intRE = np.trapezoid(meanfuncRE, vector_rg)
    meanfuncIM = NDF * np.power(2 * vector_rg, nu) * np.sin(q * vector_rg) * Psi(q * vector_rg)
    mean_intIM = np.trapezoid(meanfuncIM, vector_rg)
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
    meanfuncRE = NDF * f(vector_rg) * B(q, vector_rg) * np.cos(q * vector_rg)
    mean_intRE = np.trapezoid(meanfuncRE, vector_rg)
    meanfuncIM = NDF * f(vector_rg) * B(q, vector_rg) * np.sin(q * vector_rg)
    mean_intIM = np.trapezoid(meanfuncIM, vector_rg)
    return c * (mean_intRE + 1j * mean_intIM)


def mean_d_f_B_eiX(q):
    meanfuncRE = NDF * (2 * vector_rg) * f(vector_rg) * B(q, vector_rg) * np.cos(q * vector_rg)
    mean_intRE = np.trapezoid(meanfuncRE, vector_rg)
    meanfuncIM = NDF * (2 * vector_rg) * f(vector_rg) * B(q, vector_rg) * np.sin(q * vector_rg)
    mean_intIM = np.trapezoid(meanfuncIM, vector_rg)
    return c * (mean_intRE + 1j * mean_intIM)


def T1(q):
    return F11(q) * F22(q) - F12(q) * F21(q)


def T2(q):
    return F21(q) * mean_d_f_B_eiX(q) - F22(q) * mean_f_B_eiX(q)


def T3(q):
    return F12(q) * mean_f_B_eiX(q) - F11(q) * mean_d_f_B_eiX(q)

'''
def pdf(Rg):
    # interpolate.CubicSpline(M[:,6], M[:,7], axis=0, bc_type='not-a-knot', extrapolate=None)
    return np.interp(Rg, vector_rg, NDF) / norm
    # return np.power(Rg,shape-1)*np.exp(-Rg/scale) /(sps.gamma(shape)*np.power(scale,shape))
'''

def mean_f2_B2(q):
    mean_func = NDF * f(vector_rg) ** 2 * B(q, vector_rg) ** 2
    mean_int = np.trapezoid(mean_func, vector_rg)
    return c * mean_int


def mean_d6_Fi2(q):
    mean_func = NDF * (2 * vector_rg) ** 6 * Fi(q * vector_rg) ** 2
    mean_int = np.trapezoid(mean_func, vector_rg)
    return c * mean_int

def mean_d4_Psi2(q):
    mean_func = NDF * (2 * vector_rg) ** 4 * Psi(q * vector_rg) ** 2
    mean_int = np.trapezoid(mean_func, vector_rg)
    return c * mean_int


def mean_f_B_d3_Fi(q):
    mean_func = NDF * f(vector_rg) * B(q, vector_rg) * (2 * vector_rg) ** 3 * Fi(q * vector_rg)
    mean_int = np.trapezoid(mean_func, vector_rg)
    return c * mean_int


def mean_f_B_d2_Psi(q):
    mean_func = NDF * f(vector_rg) * B(q, vector_rg) * (2 * vector_rg) ** 2 * Psi(q * vector_rg)
    mean_int = np.trapezoid(mean_func, vector_rg)
    return c * mean_int


def mean_d5_FiPsi(q):
    mean_func = NDF * (2 * vector_rg) ** 5 * Fi(q * vector_rg) * Psi(q * vector_rg)
    mean_int = np.trapezoid(mean_func, vector_rg)
    return c * mean_int


def Df(q):
    AA = mean_f2_B2(q) * np.abs(T1(q)) ** 2
    BB = mean_d6_Fi2(q) * np.abs(T2(q)) ** 2
    CC = 9.0 * mean_d4_Psi2(q) * np.abs(T3(q)) ** 2
    DD = mean_f_B_d3_Fi(q) * 2 * np.real(T1(q) * np.conj(T2(q)))
    EE = 3.0 * mean_f_B_d2_Psi(q) * 2 * np.real(T1(q) * np.conj(T3(q)))
    FF = 3.0 * mean_d5_FiPsi(q) * 2 * np.real(T2(q) * np.conj(T3(q)))
    return (AA + BB + CC + DD + EE + FF) / (-np.pi / 6 * (1 - ksi(3)) ** 4)


def sum_intensity_vrija(q):
    return -Df(q) / DeltaK(q)

def get_sqr_volume_mean():
    sqr_mean_volume = lambda r: pdf(r) * sp_volume(r)**2
    sqr_all_volume = integrate.quad(sqr_mean_volume, 0, np.inf)[0]

    pdf_func = lambda r: pdf(r)
    norm_pdf = integrate.quad(pdf_func, 0, np.inf)[0]

    return sqr_all_volume / norm_pdf



if __name__ == "__main__":
    result_dir_path = cm.create_dir_with_date(
        path = const.current_path,
        prefix="sp_trapz_vrija"
    )

    settings = cfg.load_settings()

    shape = settings["shape"]  # = 3
    scale = settings["scale"]  # = 2
    moda =(shape-1)*scale
    rmin = moda / 100.0
    rmax = 20.0 * moda
    vector_rg  = np.linspace(rmin,rmax, 200)
    NC = settings["NC"]  # = 0.4
    NDF  =pdf(vector_rg)
    q = init_q_vector(settings)

    for nc in NC:
        c = np.pi * nc / (6.0 * get_Vmean())
        norm = np.trapezoid(NDF, vector_rg)
        result_file_path = os.path.join(result_dir_path, f"sp_vrija_trapz_nc={nc}[{q[0]},{q[-1]}].txt")

        vectorized_vrija_intensity = np.vectorize(sum_intensity_vrija)
        result = vectorized_vrija_intensity(q)/(nc* get_sqr_volume_mean())* get_Vmean()

        np.savetxt(result_file_path , np.c_[q, result])


