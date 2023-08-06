import csv
import pandas as pd
from pandas import HDFStore
import time
import h5py
import numpy as np


def write(file_format, filename, num_properties, num_elements):

    #generate random data for all columns
    data_sheet = []
    for i in range(num_properties):
        data = generate_array(num_elements)
        transpose_shape = (num_elements,1)
        data = data.reshape(transpose_shape)
        data_sheet.append(data)

    write_time = 0.0 

    if file_format == 'HDF5_compound':  
        #create HDF5 file
        file = h5py.File(f'files_1/{filename}.hdf5', 'w')

        #'setup': the dictionary that configures the compound datatype
        setup = {}
        #set up properties
        properties = []
        for i in range(num_properties):
            properties.append(f'D_{i}')
        #set up data formats
        data_formats = []
        for i in range(num_properties):
            #float scalar for each property
            format = ('f', (1,))
            data_formats.append(format)
        #configure properties and data formats
        setup['names'] = properties
        setup['formats'] = data_formats
        compound = np.dtype(setup)

        #create one single compound HDF5 dataset
        dataset = file.create_dataset(f'Dataset', shape=num_elements, dtype=compound)

        #write benchmark
        t1 = time.perf_counter()
        for i in range(num_properties):
            #retrieve the property and corresponding random data    
            dataset[f'D_{i}'] = data_sheet[i]
        t2 = time.perf_counter()
        write_time = t2 - t1
        #close HDF5 file
        file.close()

        #write time are in milliseconds
        return [1000 * write_time] 

 
    else:
        #necessary header
        header = []
        for i in range(num_properties):
            header.append(f'D_{i}')

        #write by columns -- Pandas dataframe
        file = open(f'files_1/{filename}.csv', 'w')
        writer = csv.writer(file)

        #write the header           
        writer.writerow(header)
        
        #set up the initial dataframe
        init_frame_shape = (num_elements, num_properties)
        writer.writerows(np.empty(shape=init_frame_shape))
        file.close()                                               

        #write benchmark
        t_column_1 = time.perf_counter()
        df = pd.read_csv(f'files_1/{filename}.csv')
        for i in range(num_properties):
            #populate the random data using dataframe
            df[f'D_{i}'] = data_sheet[i]
        #write the dataframe to CSV file
        df.to_csv(f'files_1/{filename}.csv')
        t_column_2 = time.perf_counter()
        write_time = t_column_2 - t_column_1


        #write by rows -- CSV writer
        file_alternative = open(f'files_1/{filename}_alternative.csv', 'w')
        writer_alternative = csv.writer(file_alternative)

        #write benchmark
        t_row_1 = time.perf_counter()
        for i in range(num_elements):
            writer_alternative.writerow(generate_array(num_elements))
        t_row_2 = time.perf_counter()
        write_time_alternative = t_row_2 - t_row_1
        
        #return both time (write by column AND write by row)
        return [1000 * write_time, 1000 * write_time_alternative]


#generate a random array for one property/column
def generate_array(num_elements):                      
    np.random.seed(None)
    arr = np.random.rand(num_elements).astype(np.float32)
    return arr
