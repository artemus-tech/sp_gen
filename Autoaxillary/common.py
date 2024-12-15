import os
from datetime import datetime
from typing import Union

import numpy as np


def create_dir_with_date(path:str, prefix="sp_gen"):
    """
    Creates a directory named with the current date (YYYY-MM-DD) if it does not exist.
    Returns:
        str: The name of the directory created or found.
    """
    # Get the current date in YYYY-MM-DD format
    current_date = f'{prefix}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'

    full_data_directory_path = os.path.join(path, current_date)

    # Check if the directory exists, and create it if it doesn't
    if not os.path.exists(full_data_directory_path):
        os.makedirs(full_data_directory_path)
        print(f"Directory '{full_data_directory_path}' created.")
    else:
        print(f"Directory '{full_data_directory_path}' already exists.")
    return full_data_directory_path


def get_rmax(m:np.ndarray, column_index:int=3)->float:
    rmax = np.max(m[:, column_index])
    return np_to_pg(rmax)

def get_rmin(m:np.ndarray, column_index:int=3)->float:
    rmin = np.min(m[:, column_index])
    return np_to_pg(rmin)

def np_to_pg(value:Union[np.float64, np.int64])->Union[float,int]:
    return value.item()
