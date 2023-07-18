import os
import shutil
import time
import h5py
import zarr
import csv
import pandas as pd
from netCDF4 import Dataset
import numpy as np

def read(file_format, filename, num_datasets, dimensions):

    dataset_read_time = 0.0

    # Open files according to the format
    if file_format == 'HDF5':
        file = h5py.File(f'files_2/{filename}_copy.hdf5', 'r')
    elif file_format == 'netCDF4':
        file = Dataset(f'files_2/{filename}_copy.netc', 'r')
    elif file_format == 'Zarr':
        file = zarr.open(f'files_2/{filename}_copy.zarr', 'r')


    # Open a dataset
    for i in range(0, num_datasets):
        if file_format == 'HDF5':
            dataset = file[f'Dataset_{i}']
        elif file_format == 'netCDF4':
            dataset = file.variables[f'Dataset_{i}']
        elif file_format == 'Zarr':
            dataset = file.get(f'Dataset_{i}')
        
       #load CSV files
        else: 
            #load the CSV file
            dataset = np.loadtxt(f'CSV_data/CSV_data_{i}.csv', delimiter=',')

        
        #record read-time 
        if len(dimensions) == 1:                     
            t1 = time.perf_counter()
            print(dataset[:dimensions[0]])
        else:
            t1 = time.perf_counter()
            print(dataset[:dimensions[0], :dimensions[1]])
        t2 = time.perf_counter()

        # calculate
        dataset_read_time += (t2- t1)


    # Close the file (if applicable) and delete it to save space
    if not file_format == 'Zarr' and not file_format == 'CSV':
        file.close() 
                                    # close if HDF5 or netCDF4
        if file_format == 'HDF5':
            os.remove(f'files_2/{filename}_copy.hdf5')
        elif file_format == 'netCDF4':
            os.remove(f'files_2/{filename}_copy.netc')

    elif file_format == 'Zarr':
        shutil.rmtree(f'files_2/{filename}_copy.zarr')
                                    # if Zarr: shutil.rmtree (delete an entire directory tree)

    # Times are in milliseconds
    return 1000 * dataset_read_time / num_datasets
