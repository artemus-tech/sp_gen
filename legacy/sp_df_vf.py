from os.path import dirname

import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import re

import psycopg2
import glob

import constants
import dbassets
from Autoaxillary.common import create_dir_with_date
from dbassets import get_field_data


def get_spheres_intersect(r1, r2, centerDistance):
    if centerDistance >= r1 + r2:
        print("ERRROR intersect not found")
        return 0
    return np.pi * (2.0 / 3.0 * (r1 ** 3 + r2 ** 3) - (r1 ** 2 - r2 ** 2) ** 2 / (
                4 * centerDistance) - 0.5 * centerDistance * (r1 ** 2 + r2 ** 2) + centerDistance ** 3 / 12.0)


def get_sphere_segment(h, R):
    return np.pi * (R * h ** 2 - h ** 3 / 3)


def get_sphere_volume(R):
    return 4.0 / 3.0 * np.pi * R ** 3


def get_sphere_radius(V):
    return np.power(3.0 / 4.0 * V / np.pi, 1.0 / 3.0)


def get_height_segments(r, R0, R):
    inner = R0 + (R0 ** 2 - R ** 2 + r ** 2) / (2 * r)
    outer = R + (R0 ** 2 - R ** 2 - r ** 2) / (2 * r)
    return (inner, outer)


def get_outer_volume(r, R0, R):
    inner, outer = get_height_segments(r, R0, R)
    return get_sphere_segment(inner, R0) - get_sphere_segment(outer, R)


# R1,R2 slices
def getVolumeDependsOn(x, y, z, rParticle, R1, R2):
    if R1 > R2:
        print("Inner layer's bound can't be larger than outer")
        return None
    # x0,y0,z0 = (0,0,0)
    RVect = np.sqrt((x * x + y * y + z * z))
    # RVect = np.sqrt((x-x0)**2+(y-y0)**2+(z-z0)**2)

    a = np.abs(RVect - rParticle)
    b = RVect + rParticle
    # 1st cast
    if a <= R1 and b <= R1:
        return 0
        ##########################
    if a <= R1 and b > R1 and b <= R2:
        # if get_sphere_volume(rParticle) -  get_spheres_intersect(rParticle,R1,RVect)<0:
        # print("OLOLO")
        # print(get_sphere_volume(rParticle))
        # print(get_spheres_intersect(rParticle,R1,RVect))
        # print(get_sphere_volume(rParticle) -  get_spheres_intersect(rParticle,R1,RVect))
        return get_sphere_volume(rParticle) - get_spheres_intersect(rParticle, R1, RVect)
    if a <= R1 and b > R2:
        # if get_spheres_intersect(rParticle,R2,RVect) -  get_spheres_intersect(rParticle,R1,RVect)<0:
        #    print(get_spheres_intersect(rParticle,R2,RVect) -  get_spheres_intersect(rParticle,R1,RVect))

        return get_spheres_intersect(rParticle, R2, RVect) - get_spheres_intersect(rParticle, R1, RVect)
        ##########################
    if a > R1 and a <= R2 and b > R1 and b <= R2:
        ##########################
        if rParticle > RVect:
            return get_sphere_volume(rParticle) - get_sphere_volume(R1)
        if rParticle < RVect:
            return get_sphere_volume(rParticle)
            ############
    if a <= R2 and a > R1 and R2 < b:
        ##########################
        if rParticle > RVect:
            return get_spheres_intersect(rParticle, R2, RVect) - get_sphere_volume(R1)
        if rParticle < RVect:
            return get_spheres_intersect(rParticle, R2, RVect)

    if a > R2 and b > R2:
        ##########################
        if rParticle > RVect:
            return get_sphere_volume(R2) - get_sphere_volume(R1)
            ############
        if rParticle < RVect:
            return 0


# when radius is not similar
def get_global_radius(d):
    return float(d[d.find("R=") + 2:d.find("_NC")])


def get_particle_region_distant(m):
    x0, y0, z0 = (0, 0, 0)
    return np.sqrt((m[:, 0] - x0) ** 2 + (m[:, 1] - y0) ** 2 + (m[:, 2] - z0) ** 2)


# 2*rmax for edge spgere particle
def get_slices(upperR, nstep):
    print("#########################UPPERR###############################")
    print(upperR)
    print("#########################UPPERR###############################")
    print("#########################nstep###############################")
    print(nstep)
    print("#########################nstep###############################")
    VUpper = get_sphere_volume(upperR)
    print("#########################VUpper###############################")
    print(VUpper)
    print("#########################VUpper###############################")
    print("#########################linspace###############################")
    print(np.linspace(0, VUpper, nstep, endpoint=True))
    print("#########################linspace###############################")
    v = list(np.linspace(0, VUpper, nstep, endpoint=True))
    print(v)
    v.append(VUpper * (1 + 1.0 / (nstep - 1)))
    print(np.shape(v))
    print(v)
    print(get_sphere_radius(np.array(v)))
    return get_sphere_radius(np.array(v))


def get_density_df(upperR, step, m):
    """
    upperR+rmax:rglobal
    step - step
    m all data
    """
    counter = 0
    sl = get_slices(upperR, step)
    v = []
    args = []
    for i in range(len(sl) - 1):
        summaryVolume = 0
        R1 = sl[i]
        R2 = sl[i + 1]
        # half summ
        args.append((R1 + R2) * 0.5)

        row, col = m.shape

        for j in range(row):
            x = m[j, 0]
            y = m[j, 1]
            z = m[j, 2]
            R0 = m[j, 3]
            # if getVolumeDependsOn(x,y,z,R0,R1,R2)<0:
            #    print(x,y,z,R0,R1,R2)
            #    print(getVolumeDependsOn(x,y,z,R0,R1,R2))
            summaryVolume += getVolumeDependsOn(x, y, z, R0, R1, R2)
        v.append(summaryVolume / (get_sphere_volume(R2) - get_sphere_volume(R1)))

    return (args, v)

'''
def clear():
    files = glob.glob(f"C:\sp-df-volume-fraction\*")

    for f in files:
        os.remove(f)
'''

if __name__ == '__main__':
    conn = dbassets.get_conn()
    sql_result = dbassets.get_fields_data(conn, "sp_gen",["id","src_path", "rglobal","rmin", "rmax"])


    for row in sql_result:
        plt.clf()
        rglobal = float(row['rglobal'])
        rmax = float(row['rmax'])
        data = np.loadtxt(row["src_path"])
        n=10
        rmiddle = float(np.array([el for el in data[:, 3]]).mean())

        dbassets.update_field_double(conn, field = "rmean",table="sp_gen",id=row['id'], value=rmiddle)
        conn.commit()
        arg, func = get_density_df(rglobal + rmax, n, data)

        phi_by_five_sp_layers=float(np.mean(func[:5]))
        dbassets.update_field_double(conn, field = "real_nc",table='sp_gen',id=row['id'], value=phi_by_five_sp_layers)

        conn.commit()
        dbassets.update_field_double(conn, field = "real_n",table='sp_gen',id=row['id'], value=data.shape[0])
        conn.commit()

        plt.grid(True)
        plt.ylabel('volume fraction')
        plt.xlabel('R,nm')
        plt.plot(arg, func, "go-", markersize=8, label="Density")
        plt.gcf()
        current_path=dirname(row["src_path"])
        full_target_path = create_dir_with_date(current_path,"sp_df_vol_fr")
        plt.savefig(f"{full_target_path}\\{row['id']}.png")
        np.savetxt(f"{full_target_path}\\{row['id']}.txt", np.c_[arg, func])
    conn.close()