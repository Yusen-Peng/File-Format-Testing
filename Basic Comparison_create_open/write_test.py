import pandas as pd
import time
import h5py
import numpy as np
import zarr
from netCDF4 import Dataset


def write(file_format, filename, num_datasets, dimensions):

    dataset_create_time = 0.0 

    # Create files according to the format
    if file_format == 'HDF5':
        file = h5py.File(f'files_1/{filename}.hdf5', 'w')
    elif file_format == 'netCDF4':  # netCDF4 dimensions must be assigned upon file creation
        file = Dataset(f'files_1/{filename}.netc', 'w', format='NETCDF4')
        if len(dimensions) == 1:
            file.createDimension('x', None)
            axes = ('x',)
        elif len(dimensions) == 2:
            file.createDimension('x', None)
            file.createDimension('y', None)
            axes = ('x', 'y',) 
        else:
            file.createDimension('x', None)
            file.createDimension('y', None)
            axes = ('x', 'y','z') 
    elif file_format == 'Zarr':
        file = zarr.open(f'files_1/{filename}.zarr', 'w')

    #Create datasets
    for i in range(num_datasets):
        if file_format == 'HDF5':
            t1 = time.perf_counter()     
            dataset = file.create_dataset(f'Dataset_{i}', shape=dimensions, dtype='f')
        elif file_format == 'Zarr':  
            t1 = time.perf_counter()
            dataset = file.create_dataset(f'Dataset_{i}', shape=dimensions, dtype='f')
        elif file_format == 'netCDF4':
            t1 = time.perf_counter()
            dataset = file.createVariable(f'Dataset_{i}', dimensions=axes, datatype='f')  
        t2 = time.perf_counter()

    #Write benchmark
    for i in range(num_datasets):
        # generate the random array
        data = generate_array(tuple(dimensions))

        #retrieve the dataset
        if file_format == 'HDF5':
            dataset = file[f'Dataset_{i}']
        elif file_format == 'netCDF4':
            dataset = file.variables[f'Dataset_{i}']
        else:
             dataset = file.get(f'Dataset_{i}')
        if len(dimensions) == 1:          
            dataset[:dimensions[0]] = data
        elif len(dimensions) == 2:
            dataset[:dimensions[0], :dimensions[1]] = data
        else:
            dataset[:dimensions[0], :dimensions[1], :dimensions[2]] = data

        #calculate
        dataset_create_time += (t2 - t1)

    # Zarr files can not be closed
    if not file_format == 'Zarr':
        file.close()

    # Return the average time taken to create one dataset and write to it. 
    # Times are in milliseconds
    return 1000 * dataset_create_time / num_datasets

def generate_array(num_elements):                      
    np.random.seed(None)

    if len(num_elements) == 1:
        a = num_elements[0]
        arr = np.random.rand(a).astype(np.float32)
                                # "a" random numbers [0,1)
    elif len(num_elements) == 2:
        a, b = tuple(num_elements)
        arr = np.random.rand(a, b).astype(np.float32)
                                # "a*b" random numbers [0,1) 
    else:
        a, b, c = tuple(num_elements)
        arr = np.random.rand(a,b,c).astype(np.float32)
    return arr

