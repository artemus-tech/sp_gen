import os.path
from os.path import dirname

import numpy as np
import scipy

import dbassets

if __name__ == '__main__':
    conn = dbassets.get_conn()
    shape=3
    scale=2.5
    n=50000
    nc=0.1
    excess=1.005
    c=0.01

    sqleval = """
                SELECT m.src_path, e.src_path
            FROM model_mean_intensity m
            JOIN eval_results e
              ON m.shape = e.shape
                 AND m.scale = e.scale
                 AND m.n = e.n
                 AND m.nc = e.nc
                 AND m.c = e.c
                 AND m.excess = e.excess

            WHERE m.shape = 3
              AND m.scale = 2.5
              AND m.n = 100000
              AND m.nc = 0.1
              AND m.excess=1.006
            """


    '''
    sqleval="""
            SELECT m.src_path, e.src_path
        FROM model_mean_intensity m
        JOIN eval_results e
          ON m.shape = e.shape
             AND m.scale = e.scale
             AND m.n = e.n
             AND m.nc = e.nc
             AND m.c = e.c
             AND m.excess = e.excess
             
        WHERE m.shape = 3
          AND m.scale = 2.5
          AND m.n = 50000
          AND m.nc = 0.1
          AND m.excess=1.005
          AND m.c=0.01
        """
    '''
    '''
    sqleval = f"""
        SELECT m.src_path as mm_src_path, e.src_path  as eval_src_path FROM model_mean_intensity m JOIN eval_results e
      ON m.shape = e.shape
         AND m.scale = e.scale
         AND m.n = e.n
         AND m.nc = e.nc
         AND m.excess = e.excess
    WHERE m.shape = {shape}
      AND m.scale = {scale}
      AND m.n = {n}
      AND m.nc ={nc}
      AND m.excess = {excess}
      """
    '''
    with conn.cursor() as cursor:
        # Execute the query
        cursor.execute(sqleval)

        # Fetch all results
        results = cursor.fetchall()

        eval_list = []

        k=0
        # Print the results
        for row in results:
            qIi = np.loadtxt(os.path.join("C:/",row[1]))

            if k==0:
                q = qIi[:, 0]
            if k>0:
                if not (qIi[:,0]==q).all():
                    raise Exception("Q doesnt much")


            eval_list.append(qIi[:,1])
            k+=1

        new_mean = np.mean(eval_list,axis=0)
        for row in results:
            meanI = np.loadtxt(os.path.join("C:/",row[0]))
            if not (np.abs(new_mean/meanI[:,1] -1)<10**(-14)).all():
                raise  Exception("Error mean")

        meval_list = np.column_stack(eval_list)
        results_sem = scipy.stats.sem(meval_list, axis=1)

    path=dirname(os.path.join('C:/',row[0]))
    print(path)


    np.savetxt(os.path.join(path, f"sem_meant.txt"),np.c_[meanI[:,0], new_mean,results_sem] )
    path_to_plot = "C://pcs_for_article"






