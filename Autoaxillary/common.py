import os
import typing
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

def array1d_get_min(arr:np.ndarray)->typing.Union[float,None]:
    if array1d_is_non_zero_or_empty(arr):
        min = np.min(arr)
        return np_to_pg(min)

def array1d_get_max(arr:np.ndarray)->typing.Union[float,None]:
    if array1d_is_non_zero_or_empty(arr):
        max = np.max(arr)
        return np_to_pg(max)

def array1d_get_size(arr:np.ndarray)->typing.Union[float,None]:
    if array1d_is_non_zero_or_empty(arr):
        num = arr.shape[0]
        return np_to_pg(num)

def array1d_is_non_zero_or_empty(a: np.ndarray):
    """
    :param a:assume that it's 1d numpy array
    :return: will get True if dimensions are correct
    """
    if a is not None:
        if a.ndim == 1:
            if a.shape[0] > 0 and not np.all(a == 0):
                return True
    return False

def np_to_pg(value:Union[np.float64, np.int64])->Union[float,int]:
    if isinstance(value, (np.generic, np.number)):
        try:
            result=value.item()
        except AttributeError:
            print("Has not item() method")
            result = value
        return result
    else:
        return value



def custom_std(arrays):
    # Stack the arrays to form a 2D matrix (rows = arrays, columns = elements in each array)
    stacked_arrays = np.array(arrays)

    # Number of arrays (N) and elements per array (M)
    N = stacked_arrays.shape[0]

    # Calculate the mean of each column (i.e., each corresponding element across arrays)
    means = np.mean(stacked_arrays, axis=0)

    # Calculate the sum of squared differences from the mean for each column
    sum_squared_diff = np.sum((stacked_arrays - means) ** 2, axis=0)

    # Return the standard deviation with the custom divisor (N * (N - 1))
    return np.sqrt(sum_squared_diff / (N * (N - 1)))



def convert_list_of_dicts_to_dict(list_of_dicts):
    # Initialize an empty dictionary to store the results
    result = {}

    # Loop through each dictionary in the list
    for d in list_of_dicts:
        for key, value in d.items():
            # If the key is not already in the result dictionary, add it with an empty list
            if key not in result:
                result[key] = []
            # Append the value to the corresponding key's list
            result[key].append(value)

    return result