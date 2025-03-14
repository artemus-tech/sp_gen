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
import numpy as np
from numba import njit



#id_gen_list = [277,278,279,280,281,282,283,284,285,286]
old_id_gen_list = [1990,1989,1981,1982,1983,1984,1985,1987,1988,1986]
#397
select_id = 487#
#397 #!!!!CHECK OLD DATA HAS INTERSECTION
#old_id_gen_list[0]
#data=dbassets.get_data_by_id(const.active_table_dict["sp_gen"], "id", select_id)


data=dbassets.get_data_by_id(const.active_table_dict["sp_gen"], "id", select_id)
matrix_xyzr = np.loadtxt(data["src_path"])
result =[]



@njit
def boost_check(matrix_xyzr: np.ndarray, stop=100000):
    n = matrix_xyzr.shape[0]
    result = np.zeros((3,))  # Correct array size (integer division)
    k = 0
    result_min=1000

    # Loop over the first point (i)
    for i in range(n):
        x1, y1, z1, r1 = matrix_xyzr[i]

        # Loop over the second point (j) from i+1 to avoid duplicate pairs
        for j in range(i + 1, n):
            x2, y2, z2, r2 = matrix_xyzr[j]

            # Calculate the scaled distance
            dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) / (r1 + r2)

            # Store the result
            #result[k] = dist
            if dist<result_min:
                result_min=dist

                result=np.array([i,j,result_min])
        if i==stop:
            return result

            # Break early if we reach the stop condition
        #if k == stop:
        #    return np.min(result)  # Return the min distance up to the stop limit

    # Return the minimum of all distances calculated
    return result


t = boost_check(matrix_xyzr)
print(t)



