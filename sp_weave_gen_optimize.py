# -*- coding: utf-8 -*-
import os
import multiprocessing as mp
import numpy as np
from numba import jit, njit
import constants as const
import dbassets
from Autoaxillary.common import np_to_pg
from Autoaxillary.profiler import Profiler
import Autoaxillary.common as cm
import config as cfg

def generate_rand_pdf(size: int, shape: float = 3.0, scale: float = 2.5):
    gamma_pdf = np.random.gamma(shape, scale, size)
    gamma_pdf = np.sort(gamma_pdf)
    return gamma_pdf[::-1]


def in_sphere(M:np.ndarray,R: float):
    distance = np.linalg.norm(M[:, :3], axis=1)
    return M[distance < R]

def get_n_in_cube(size: int, excess: float) -> int:
    return int(excess * size * 6.0*(1+C)**3/np.pi)

@njit
def has_intersect(MGLOBAL,x0, y0, z0, r0, n):
    for i in range(n):
        dx, dy, dz = MGLOBAL[i, 0] - x0, MGLOBAL[i, 1] - y0, MGLOBAL[i, 2] - z0
        distance = np.sqrt(dx * dx + dy * dy + dz * dz)
        if distance < MGLOBAL[i, 3] + r0:
            return True
    return False

@njit
def generate(vr: np.ndarray[float], cube: float, size: int):
    #presetes
    i = 0
    try_count = 0
    MGLOBAL = np.zeros(shape=(size, 4))
    rib = cube/2.0

    while i < size and try_count < const.try_count:
        x0,y0,z0 = rib * np.random.uniform(-1.0, 1.0, size=(3,))
        r0 = vr[i]
        if i == 0 or not has_intersect(MGLOBAL, x0=x0,y0=y0,z0=z0, r0=r0, n=i):
            MGLOBAL[i, 0] = x0
            MGLOBAL[i, 1] = y0
            MGLOBAL[i, 2] = z0
            MGLOBAL[i, 3] = vr[i]

            try_count = 0
            i += 1
        try_count += 1
    return MGLOBAL

def process_and_save(i, vect_r, DCUBE, R, excess, shape, scale, sp_number, NC, more_greater_sp_number,C, path,row_id):
    with Profiler():
        sp_gen_result = generate(vr=vect_r, cube=DCUBE, size=more_greater_sp_number)
        matrix_result = in_sphere(sp_gen_result, R)
        r_max = cm.get_rmax(matrix_result)
        r_min = cm.get_rmin(matrix_result)
        file_path = os.path.join(path,f"row_id={row_id}_series_no={i}_rglobal={R}_shape={shape}_scale={scale}_excess={excess}_nc={NC}_n={more_greater_sp_number}_rmax={r_max}_rmin={r_min}.txt")
        np.savetxt(file_path, matrix_result)

    if os.path.exists(file_path):
        dbassets.insert_data(table_name='sp_gen', data_dict={
            'shape': np_to_pg(shape),
            'scale': np_to_pg(scale),
            'rglobal': np_to_pg(R),
            'rmax':r_min,
            'rmin':r_max,
            'excess': np_to_pg(excess),
            'c': np_to_pg(C),
            'nc': np_to_pg(NC),
            'real_nc': -1,
            'n': np_to_pg(sp_number),
            'real_n': np_to_pg(matrix_result.shape[0]),
            'series_no': np_to_pg(i),
            'src_path': file_path,
            'row_id':row_id
        })

if __name__ == "__main__":
    result_path = cm.create_dir_with_date(path = const.current_path,prefix="sp_gen")
    settings = cfg.load_settings()
    excess_flag = settings["excess_arr_defined"]

    if excess_flag==0:
        excess_min = settings["excess_min"]
        excess_max = settings["excess_max"]
        excess_num = settings["excess_num"]
        excess_arr = np.linspace(excess_min,excess_max,excess_num)
    else:
        excess_arr =settings["excess_arr"]
    service_uuid= settings["service_id"]

    shape_arr = settings["shape"]  # = 3
    scale_arr = settings["scale"]  # = 2
    NC_LIST = settings["NC"]  # = 0.2
    sp_number = settings["sp_number"]  # = 100000
    file_numb = settings["file_numb"]  # = 10
    C = settings["C"]  # = 0.10
    seriees_number = 5

    for shape,scale in zip(shape_arr,scale_arr):
        for nc_single_value in NC_LIST:
            for excess_single_value in excess_arr:
                # number of planning spheres with a little bit increase offset
                n_in_cube = get_n_in_cube(sp_number, excess_single_value)
                # size of this vector is planning size of system
                vect_r = generate_rand_pdf(n_in_cube, shape, scale)
                # calculate rib
                DCUBE = np.power(4.0 / 3.0 * np.pi * np.sum(np.power(vect_r, 3)) / (excess_single_value * nc_single_value), 1.0 / 3.0)
                R = DCUBE / (2.0 * (1 + C))


                k=0

                row_id = dbassets.insert_data("sp_data", data_dict={
                    'shape': np_to_pg(shape),
                    'scale': np_to_pg(scale),
                    'n': np_to_pg(sp_number),
                    'excess': np_to_pg(excess_single_value),
                    'c': np_to_pg(C),
                    'rglobal': np_to_pg(R),
                    'nc': np_to_pg(nc_single_value),
                    'source_id':service_uuid
                })

                for j in range(seriees_number):
                    processes = []
                    for i in range(file_numb):
                        p = mp.Process(
                            target=process_and_save,
                            args=(k, vect_r, DCUBE, R, excess_single_value, shape, scale, sp_number, nc_single_value, n_in_cube, C, result_path, row_id)
                        )
                        p.start()
                        processes.append(p)
                        k+=1

                    for p in processes:
                        p.join()  # Wait for all processes to complete

