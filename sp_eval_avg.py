import os.path
import constants as const
import dbassets
import config as cfg
import numpy as np
import Autoaxillary.common as cm

def get_I_avg_by_id_list(id_list):
    I=[]
    for id in id_list:
        sp_eval_result = dbassets.get_data_by_id(const.active_table_dict["sp_eval"], "id", id)
        matrix_qI = np.loadtxt(sp_eval_result["src_path"])

        sp_gen_id = sp_eval_result["gen_id"]
        sp_gen_result = dbassets.get_data_by_id(const.active_table_dict["sp_gen"], "id", sp_gen_id)

        matrix_xyzr = np.loadtxt(sp_gen_result["src_path"])

        r = matrix_xyzr[:, 3]

        v_sqr_summ = (4.0 / 3.0 * np.pi) ** 2 * np.sum(r ** 6)

        q, intensity = list(matrix_qI.T)

        I.append(intensity / v_sqr_summ)
    return q,I


if __name__ == '__main__':
    settings = cfg.load_settings()

    for row_id in [410]:

        sp_data_list = dbassets.get_records_by_where('sp_gen_sp_eval_join',{'row_id': row_id})
        sp_data_dict = cm.convert_list_of_dicts_to_dict(sp_data_list)
        id_list = sp_data_dict['eval_id']

        q, I_list = get_I_avg_by_id_list(id_list)

        I_avg = np.average(I_list,axis=0)
        std = cm.custom_std(I_list)

        first_id = id_list[0]
        last_id = id_list[-1]

        avg_file= f'sp_avg_eval_[{first_id}_{last_id}].txt'
        avg_path = os.path.join(const.path_avg,avg_file)
        np.savetxt(avg_path, np.c_[q,I_avg,std])

        dbassets.insert_data('sp_eval_avg', {
            'row_id': cm.np_to_pg(row_id),
            'qmin': cm.np_to_pg(settings['q0']),
            'qmax': cm.np_to_pg(settings["qn"]),
            'src_path':avg_path
        })
