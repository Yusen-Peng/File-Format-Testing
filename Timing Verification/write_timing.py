import pandas as pd
import time
import yaml
import h5py
import glob
import numpy as np
import zarr
import csv
from netCDF4 import Dataset

#generate a random data array 
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


#write random data and time everything
def write(file_format, filename, num_datasets, dimensions):
    file_creation_time = 0.0
    dataset_creation_time = 0.0
    random_data_generate_time = 0.0
    dataset_population_time = 0.0

    # Create files according to the format
    file_create_t1 = time.perf_counter()
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
    file_create_t2 = time.perf_counter()
    file_creation_time = file_create_t2 - file_create_t1 

    #Create datasets
    for i in range(num_datasets):
        t1 = time.perf_counter()
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
        t2 = time.perf_counter()
        dataset_creation_time += t2 - t1

        # generate the random array
        t3 = time.perf_counter()
        data = generate_array(tuple(dimensions))
        t4 = time.perf_counter()
        random_data_generate_time = t4 - t3

        #CSV -- write: 
        #step1: load CSV file; 
        #step2: populate it with random data;
        #step3: save CSV file.
        t5 = time.perf_counter()
        if file_format == 'CSV':
            #load CSV file
            dataset = np.loadtxt(f'CSV_data/CSV_data_{i}.csv', delimiter=',')
            #write a vector       
            if len(dimensions) == 1:  
                #populate it with random data
                dataset[:dimensions[0]] = data   
            #write a matrix
            elif len(dimensions) == 2:
                #populate it with random data
                dataset[:dimensions[0], :dimensions[1]] = data
            #save CSV file
            dataset = np.savetxt(f'CSV_data/CSV_data_{i}.csv', dataset, delimiter=',',fmt='%f')   
            
        else:
            if len(dimensions) == 1:
                dataset[:dimensions[0]] = data
            else:
                dataset[:dimensions[0], :dimensions[1]] = data
        t6 = time.perf_counter()
        dataset_population_time += (t6 - t5)

    #Zarr files can not be closed
    if not file_format == 'Zarr' and not file_format == 'CSV':
        file.close()

    # Return the average time taken to create one dataset and write to it. 
    # Times are in milliseconds
    timer_list = list(range(4))
    timer_list[0] = 1000 * file_creation_time
    timer_list[1] = 1000 * dataset_creation_time / num_datasets
    timer_list[2] = 1000 * random_data_generate_time / num_datasets
    timer_list[3] = 1000 * dataset_population_time / num_datasets
    return timer_list


def pushDataToCSV(time_table, file_format, num_datasets, dimensions):
    #enter all timing data by csv writer
    with open(f'timer_csv/{file_format}_{num_datasets}_{dimensions}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([file_format, 'file_creation_time', 'dataset_creation_time', 'random_data_generate_time', 'dataset_population_time'])
        for i in range(len(time_table)):
            time_data = time_table[i]
            writer.writerow([f'trial_{i}', time_data[0], time_data[1], time_data[2], time_data[3]])

    #evaluate the average by pandas
    df = pd.read_csv(f'timer_csv/{file_format}_{num_datasets}_{dimensions}.csv')
    file, create, random, write = df.iloc[:, 1:].mean(axis=0)
    avg = pd.DataFrame({
        file_format: 'Average',
        'file_creation_time': [file],
        'dataset_creation_time': [create],
        'random_data_generate_time': [random],
        'dataset_population_time': [write]
    })
    df = pd.concat([df, avg], ignore_index=True)
    df.to_csv(f'timer_csv/{file_format}_{num_datasets}_{dimensions}.csv', index=False)

def main(file_formats, num_trials):
    config_files = glob.glob('config/*.yaml')

    for config_file in config_files:
        with open(f'{config_file}', 'r') as file:
            config = yaml.safe_load(file)
            filename = config.get('FILE_NAME')
            num_datasets = config.get('NUMBER_DATASETS')
            dimensions = config.get('NUMBER_ELEMENTS')

            for file_format in file_formats:
                time_table = []
                for i in range(num_trials):
                    time_data = write(file_format, filename, num_datasets, dimensions)
                    time_table.append(time_data)
                pushDataToCSV(time_table, file_format,num_datasets, dimensions)  

if __name__ == '__main__':
    file_formats = ['HDF5', 'netCDF4', 'Zarr'] 
    num_trials = 5
    main(file_formats, num_trials)