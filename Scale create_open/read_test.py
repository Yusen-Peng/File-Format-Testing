import os
import shutil
import time

import h5py
import zarr
from netCDF4 import Dataset


def read(file_format, filename, num_datasets, dimensions):
    #Open the copied file and read the data in each dataset
    dataset_open_time = 0.0

    #open files for each file format and its compressed version
    if file_format == 'HDF5':
        file = h5py.File(f'files_1/{filename}.hdf5', 'r')
    elif file_format == 'netCDF4':
        file = Dataset(f'files_1/{filename}.netc', 'r')
    else:
        file = zarr.open(f'files_1/{filename}.zarr', 'r')


    # Open a dataset within the file and record the time
    for i in range(0, num_datasets):
        if file_format == 'HDF5':
            t1 = time.perf_counter()
            dataset = file[f'Dataset_{i}']
        elif file_format == 'netCDF4':
            t1 = time.perf_counter()
            dataset = file.variables[f'Dataset_{i}']
        else:
            t1 = time.perf_counter()
            dataset = file.get(f'Dataset_{i}')
        t2 = time.perf_counter()

        # Print the values within each dataset and measure the time taken
        if len(dimensions) == 1:
            print(dataset[:dimensions[0]])
        elif len(dimensions) == 2:
            print(dataset[:dimensions[0], :dimensions[1]])
        else:
            print(dataset[:dimensions[0], :dimensions[1], :dimensions[2]])
        
        # Add up the times taken to get the total time taken to open and read all datasets
        dataset_open_time += t2 - t1


    # Close the file (if applicable) and delete it to save space
    if not file_format == 'Zarr':
        file.close()
            
    # Return average time taken to open one dataset and read from it. Times are in milliseconds
    return 1000 * dataset_open_time / num_datasets