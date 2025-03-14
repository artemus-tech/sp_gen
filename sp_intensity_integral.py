import os.path

import numpy as np
import constants as const
import Autoaxillary.common as cm
import config as cfg
from scipy import integrate
from Autoaxillary.saxs import init_q_vector

from sp_assets import pdf
from sp_assets import sp_factor
from sp_assets import sp_volume

def full_intensity(q:np.ndarray):
    integrand_func = lambda Rg: pdf(Rg) * sp_factor(q*Rg) * np.power(sp_volume(Rg),2)
    return integrate.quad(integrand_func, 0, np.inf, limit = 100)[0]

def integral_norm():
    integrand_func = lambda Rg: pdf(Rg) * np.power(sp_volume(Rg), 2)
    return integrate.quad(integrand_func, 0, np.inf, limit = 100)[0]

if __name__ == "__main__":
    result_dir_path = cm.create_dir_with_date(path = const.current_path,prefix="sp_intensity_integral")
    settings = cfg.load_settings()

    shape = settings["shape"]  # = 3
    scale = settings["scale"]  # = 2

    q = init_q_vector(settings)
    result_file_path = os.path.join(result_dir_path, f"sp_intensity_integral[{q[0]},{q[-1]}].txt")

    vectorized_full_intensity = np.vectorize(full_intensity)
    result = vectorized_full_intensity(q) / integral_norm()
    np.savetxt(result_file_path , np.c_[q, result])