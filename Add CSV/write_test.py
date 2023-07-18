import os
import shutil
import csv
import pandas as pd
import time
import h5py
import numpy as np
import zarr
from netCDF4 import Dataset


def write(file_format, filename, num_datasets, dimensions):

    dataset_population_time = 0.0 

    # Create files according to the format
    if file_format == 'HDF5':
        file = h5py.File(f'files_1/{filename}.hdf5', 'w')
    elif file_format == 'netCDF4':  # netCDF4 dimensions must be assigned upon file creation
        file = Dataset(f'files_1/{filename}.netc', 'w', format='NETCDF4')
        if len(dimensions) == 1:
            file.createDimension('x', None)
            axes = ('x',)
        else:
            file.createDimension('x', None)
            file.createDimension('y', None)
            axes = ('x', 'y',)        
    elif file_format == 'Zarr':
        file = zarr.open(f'files_1/{filename}.zarr', 'w')


    # Create datasets and populate them with data
    for i in range(0, num_datasets):
        
        # generate the random array
        data = generate_array(tuple(dimensions))
                                            
        #create dataset
        if file_format == 'HDF5':     
            dataset = file.create_dataset(f'Dataset_{i}', shape=dimensions, dtype='f')
        elif file_format == 'Zarr':  
            dataset = file.create_dataset(f'Dataset_{i}', shape=dimensions, dtype='f')
        elif file_format == 'netCDF4':
            dataset = file.createVariable(f'Dataset_{i}', dimensions=axes, datatype='f')  

        #CSV -- create: create an empty dataset by NumPy and save it as a CSV file
        elif file_format == 'CSV':  
            #create an empty dataset by NumPy
            dataset = np.empty(shape=dimensions, dtype='f')
            #save it as a CSV file
            np.savetxt(f'CSV_data/CSV_data_{i}.csv', dataset, delimiter=',',fmt='%f')
    
        #CSV -- write: 
        #step1: load CSV file; 
        #step2: populate it with random data;
        #step3: save CSV file.
        if file_format == 'CSV':
            t1 = time.perf_counter()
            #load CSV file
            dataset = np.loadtxt(f'CSV_data/CSV_data_{i}.csv', delimiter=',')
            #populate it with random data
            dataset[:dimensions[0]] = data  
            #save CSV file
            dataset = np.savetxt(f'CSV_data/CSV_data_{i}.csv', dataset, delimiter=',',fmt='%f')   
            t2 = time.perf_counter()
    
        else: 
            if len(dimensions) == 1:
                t1 = time.perf_counter()
                dataset[:dimensions[0]] = data
                t2 = time.perf_counter()
            else:
                t1 = time.perf_counter()
                dataset[:dimensions[0], :dimensions[1]] = data
                t2 = time.perf_counter()


        #calculate
        dataset_population_time += (t2 - t1)

    # Zarr files can not be closed
    if not file_format == 'Zarr' and not file_format == 'CSV':
        file.close()

    # Copy the file to a new directory and rename it to begin the read operations. 
    # This helps avoid any caching effects
    if not file_format == 'CSV':
        copy_file(file_format, filename)

    # Return the average time taken to create one dataset and write to it. 
    # Times are in milliseconds
    return 1000 * dataset_population_time / num_datasets

def generate_array(num_elements):                      
    np.random.seed(None)

    if len(num_elements) == 1:
        a = num_elements[0]
        arr = np.random.rand(a).astype(np.float32)
                                # "a" random numbers [0,1)
    else:
        a, b = tuple(num_elements)
        arr = np.random.rand(a, b).astype(np.float32)
                                # "a*b" random numbers [0,1) 
    return arr


def copy_file(file_format, filename):
    
    if file_format == 'HDF5':
        shutil.copy(f'files_1/{filename}.hdf5', 'files_2')
        os.rename(f'files_2/{filename}.hdf5', f'files_2/{filename}_copy.hdf5')
        os.remove(f'files_1/{filename}.hdf5')
                                                        # copy -> rename -> remove 
    elif file_format == 'netCDF4':
        shutil.copy(f'files_1/{filename}.netc', "files_2")
        os.rename(f'files_2/{filename}.netc', f'files_2/{filename}_copy.netc')
        os.remove(f'files_1/{filename}.netc')

    else:
        shutil.copytree(f'files_1/{filename}.zarr', f'files_2/{filename}.zarr')
        os.rename(f'files_2/{filename}.zarr', f'files_2/{filename}_copy.zarr')
        shutil.rmtree(f'files_1/{filename}.zarr')
                                                        # copytree -> rename -> rmtree
