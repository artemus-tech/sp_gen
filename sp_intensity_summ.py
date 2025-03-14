import numpy as np
import os

from scipy import integrate

import constants as const
import Autoaxillary.common as cm
import config as cfg
import dbassets
from Autoaxillary.saxs import init_q_vector
from sp_assets import pdf,sp_factor,sp_volume

def sum_intensity(q,rvect):
    s=0
    for r in rvect:
        s+=sp_factor(q * r) * np.power(sp_volume(r),2)
    return s

def get_sqr_voume_summ(rvect):
    return  np.sum(np.power(sp_volume(rvect),2))

def sp_intensity_sum_norm(q,rvect):
    return  sum_intensity(q,rvect)/get_sqr_voume_summ(rvect)


if __name__ == "__main__":
    result_dir_path = cm.create_dir_with_date(path = const.current_path,prefix="sp_intensity_sum")
    settings = cfg.load_settings()

    shape = settings["shape"]  # = 3
    scale = settings["scale"]  # = 2
    NCList = settings["NC"]
    rows_id_list=dbassets.fetch_all_as_dict(table_name='sp_gen_get_distinct_row_id')
    q = init_q_vector(settings)

    data = {}

    data['qmin'] = cm.np_to_pg(np.min(q))
    data['qmax'] = cm.np_to_pg(np.max(q))
    data['qmax'] = cm.np_to_pg(np.max(q))
    data['qnumb'] = cm.np_to_pg(q.shape[0])

    for el in rows_id_list:
        row_id=el["row_id"]

        sp_gen_data = dbassets.get_records_by_where(
            table_name="sp_gen", where_clauses={"row_id":row_id}
        )
        I_result_sum = []
        for series in sp_gen_data:
            x,y,z,r = list(np.loadtxt(series['src_path']).T)
            I_sum_norm = sp_intensity_sum_norm(q, r)
            I_result_sum.append(I_sum_norm)

        data['row_id'] = cm.np_to_pg(row_id)
        try:
            I_avg_norm_sum = np.average(I_result_sum,axis=0)
            std_I_avg_norm_sum  = cm.custom_std(I_result_sum)

            #full_target_path = cm.create_dir_with_date(const.path_intensity_sum_norm_avg, "sp_intens_sum_norm_avg")

            src_path_intensity  =os.path.join(const.path_intensity_sum_norm_avg, f'sp_intensity_sum_norm_avg_row_id={row_id}.txt')

            np.savetxt(src_path_intensity, np.c_[q,I_avg_norm_sum,std_I_avg_norm_sum])

            data['src_path_intensity_sum_norm_avg'] = src_path_intensity
            dbassets.insert_data(table_name="sp_intens_sum_norm_avg", data_dict=data)
        except Exception as ex :
            print(ex)
            print(row_id)
