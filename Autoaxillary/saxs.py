import numpy as np


def init_q_vector(settings)->np.ndarray:
    '''
    "q0" : 0.02,
    "qn" : 5.00,
    "q_num" : 150,
    '''
    q_min = settings["q0"]
    q_max = settings["qn"]
    q_number = settings["q_num"]
    return np.logspace(np.log10(q_min), np.log10(q_max),q_number)


def sp_volume(r):
    return 4.0/3.0*np.pi*np.power(r,3)

def sp_factor(qr):
    return 9.0*(np.sin(qr)-qr*np.cos(qr)/np.power(qr,3),2)