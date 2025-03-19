# -*- coding: utf8 -*-
import multiprocessing
import os.path
import numpy as np
from numba import  njit
from psycopg2 import Binary

import constants as const
import dbassets
import Autoaxillary.common as cm
import config as cfg
from Autoaxillary.profiler import Profiler
from Autoaxillary.saxs import init_q_vector


def sp_eval(matrix_xyzr: np.ndarray, q_vect: np.ndarray, R: float, target_n: int, NC: float):
    # volume coefficient for spheres
    sp_v_const = 4.0 / 3.0 * np.pi
    sp_global_volume = sp_v_const * R ** 3
    sp_local_volume = sp_v_const * matrix_xyzr[:,3] ** 3
    sp_global = sp_factor(R * q_vect) * sp_global_volume
    sp_tmp_const = np.linalg.norm(matrix_xyzr[:, :3], axis=1)
    return sp_local_volume,sp_global,sp_tmp_const

@njit
def sp_intens_opt(NC:float, q_num:int, real_n:int,sp_global:np.ndarray, sp_tmp_const:np.ndarray,sp_local_volume:np.ndarray,data:np.ndarray,q):
    # Extract columns once for efficiency
    x, y, z, r = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
    sp_local_volume_sqr = sp_local_volume**2
    qr = np.outer(q, r)
    sp_factor_const  = sp_factor(qr)
    sp_factor_sqr = sp_factor_const ** 2
    sp_first_summand = np.zeros(shape=(q_num, ),dtype=np.float64)
    s2 =  np.zeros(shape=(q_num, ))

    for k in range(q_num):
        for j in range(real_n):
            s2[k]+=sp_factor_sqr[k, j] * sp_local_volume_sqr[j]
            sp_first_summand[k]+= sp_local_volume[j] * sp_factor_const[k,j] * sinc(q[k] * sp_tmp_const[j])

    sp_factors = np.zeros(shape=(q_num,),dtype=np.float64)
    for j in range(real_n):
        for i in range(j+1, real_n):
            sp_volumes = sp_local_volume[i] * sp_local_volume[j]
            tmp_value = tmp_matrix(x[j], x[i], y[j], y[i], z[j], z[i])
            for k in range(q_num):
                sp_factors[k]+=sp_factor_const[k, j]*sp_factor_const[k,i]*sinc(tmp_value*q[k])*sp_volumes

    I=s2 + 2 * sp_factors + NC ** 2 * sp_global ** 2 - 2 * NC * sp_first_summand * sp_global
    return q,I

@njit
def sinc(x):
    return np.sin(x) / (x) if x != 0 else 1

@njit
def sp_factor(x):
    return 3.0 * ((np.sin(x) - x * np.cos(x)) / x ** 3)

@njit
def tmp_matrix(x, x0, y, y0, z, z0):
    return np.sqrt((x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2)

def sp_runner(row: dict, q: np.ndarray[float], res_path:str):
    #M = np.loadtxt(row['src_path'])
    M = np.loadtxt(row['extracted_path'])

    R = row['rglobal']
    NC = row['nc']
    real_n = M.shape[0]
    target_n = row['n']

    with Profiler():
        sp_local_volume, sp_global, sp_tmp_const =  sp_eval(matrix_xyzr=M, q_vect=q, R=R, NC=NC, target_n=target_n)


    with Profiler():
        q,I=sp_intens_opt(
            NC=NC, q_num=q.shape[0], real_n=real_n,
            sp_global=sp_global, sp_tmp_const=sp_tmp_const,sp_local_volume=sp_local_volume,data=M,q=q)

    result_full_path_to_file = os.path.join(res_path, f'{row["id"]}.txt')

    np.savetxt(result_full_path_to_file, np.c_[q, I])

    if os.path.exists(result_full_path_to_file):
        with open(result_full_path_to_file, 'rb') as f:
            file_data = f.read()
            dbassets.insert_data("sp_eval", {
                'gen_id':int(row["id"]),
                'src_path': result_full_path_to_file,
                'qmin': cm.array1d_get_min(q),
                'qmax': cm.array1d_get_max(q),
                'qnum': cm.array1d_get_size(q),
                'file_data': Binary(file_data)
            })
            #log state
            dbassets.update_field_by_unique_field(
                table="sp_tmp",
                target_field="evaluated",
                where_field_name="gen_id",
                where_field_value=int(row["id"]),
                new_value=True
            )


def worker(seq, q, path):
    """The worker pulls an item (row) from the list and processes it with q."""
    while True:
        # Get the next ID (data row) from the queue
        if not seq.empty():
            id_data = seq.get()  # Pull data associated with a specific ID
            sp_runner(id_data, q, path)  # Process it using the provided q
            seq.task_done()  # Indicate that the task is complete
        else:
            break




if __name__ == '__main__':
    settings = cfg.load_settings()
    q = init_q_vector(settings)

    sp_tmp_records =dbassets.get_records_by_where(table_name="sp_tmp",where_clauses={'evaluated':False})
    sp_gen_data_list = []
    res_path_dir = cm.create_dir_with_date(const.current_path, prefix=f'sp_eval')
    sp_gen_extracted = cm.create_dir_with_date(const.path_to_sp_gen, "sp_gen_extracted")

    for record in sp_tmp_records:
        sp_tmp_rec_gen_id = record["gen_id"]
        sp_gen_data = dbassets.get_data_by_id(const.active_table_dict["sp_gen"], "id", sp_tmp_rec_gen_id)
        if not sp_gen_data:
            raise  Exception(f'{sp_tmp_rec_gen_id} does not exists')
        extracted_file_name = os.path.join(sp_gen_extracted, f'{sp_gen_data["id"]}.txt')
        M = cm.from_binary(sp_gen_data['file_data'])
        np.savetxt(extracted_file_name,M )
        if os.path.exists(extracted_file_name):
            sp_gen_data['extracted_path'] = extracted_file_name
            del sp_gen_data['file_data']
        sp_gen_data_list.append(sp_gen_data)

    # Initialize the process pool and queue
    in_queue = multiprocessing.JoinableQueue()
    process_num = 20  # Number of processes you want to spawn (should not exceed number of quads ideally)

    # Fill the queue with tasks (each task is a row of data for a specific ID)
    for sp_gen_data in sp_gen_data_list:
        in_queue.put(sp_gen_data)

    # Create and start worker processes
    processes = []
    for i in range(process_num):
        p = multiprocessing.Process(target=worker, args=(in_queue, q, res_path_dir))
        p.daemon = True  # Ensure processes exit when the main program finishes
        processes.append(p)
        p.start()

    # Wait for all tasks to be processed
    in_queue.join()

    # Optionally stop workers by sending None (sentinel) to indicate the end
    for _ in range(process_num):
        in_queue.put(None)  # Send sentinel value to stop the worker processes

    # Ensure all processes finish
    for p in processes:
        p.join()

    print("All tasks have been processed.")

