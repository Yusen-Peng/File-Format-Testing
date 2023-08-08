import os
import shutil
import time
import h5py
import zarr
import pandas as pd
from netCDF4 import Dataset
import numpy as np

def read(file_format, filename, num_datasets, dimensions):

    dataset_open_time = 0.0

    # Open files according to the format
    if file_format == 'HDF5':
        file = h5py.File(f'files_1/{filename}.hdf5', 'r')
    elif file_format == 'netCDF4':
        file = Dataset(f'files_1/{filename}.netc', 'r')
    elif file_format == 'Zarr':
        file = zarr.open(f'files_1/{filename}.zarr', 'r')


    # Open a dataset
    for i in range(0, num_datasets):
        t1 = time.perf_counter()
        if file_format == 'HDF5':
            dataset = file[f'Dataset_{i}']
        elif file_format == 'netCDF4':
            dataset = file.variables[f'Dataset_{i}']
        elif file_format == 'Zarr':
            dataset = file.get(f'Dataset_{i}')
        t2 = time.perf_counter()

        # record read-time 
        if len(dimensions) == 1:                     
            print(dataset[:dimensions[0]])
        elif len(dimensions) == 2:
            print(dataset[:dimensions[0], :dimensions[1]])
        else:
            print(dataset[:dimensions[0], :dimensions[1], :dimensions[2]])
        # calculate
        dataset_open_time += (t2- t1)


    # Close the file (if applicable) and delete it to save space
    if not file_format == 'Zarr':
        file.close() 
                                    # close if HDF5 or netCDF4

    # Times are in milliseconds
    return 1000 * dataset_open_time / num_datasets
