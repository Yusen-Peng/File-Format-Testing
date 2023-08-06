import time
import pandas as pd
from netCDF4 import Dataset

#read by properties
def read_0(file_format, filename, num_properties, num_elements):

    read_time = 0.0

    #Compound HDF5
    if file_format == 'HDF5_compound':
        #work with pandas data frame
        #read_0 benchmark
        t1 = time.perf_counter()
        df = pd.read_hdf(f'files_1/{filename}.hdf5', 'Dataset')
        for col in range(num_properties):
            #read each column/property
            print(df.iloc[:, col])
        t2 = time.perf_counter()
        read_time = t2 - t1 
    
    else: #CSV
        #use pandas dataframe to read by columns
        #read benchmark -- read by columns
        t1 = time.perf_counter()
        df = pd.read_csv(f'files_1/{filename}.csv')
        for pro in range(1, num_properties+1):
            print(df.iloc[:, pro])
        t2 = time.perf_counter()
        read_time = t2 - t1
    return read_time



#read by rows
def read_1(file_format, filename, num_properties, num_elements):
    read_time = 0.0

    #read by rows
    if file_format == 'HDF5_compound':
        #work with pandas data frame
        #read_1 benchmark
        t1 = time.perf_counter()
        df = pd.read_hdf(f'files_1/{filename}.hdf5', 'Dataset')
        for row in range(num_elements):
            #read each row
            print(df.iloc[row, :])
        t2 = time.perf_counter()
        read_time = t2 - t1

    else: #in the case of CSV
        #open the file
        #read_1 benchmark
        t1 = time.perf_counter()
        df = pd.read_csv(f'files_1/{filename}.csv')
        for row in range(num_elements):
            print(df.iloc[row, 1:])
        t2 = time.perf_counter()
        read_time = t2 - t1

    return read_time

#read all
def read_2(file_format, filename, num_properties, num_elements):
    # Compound HDF5
    if file_format == 'HDF5_compound':
        #work with pandas data frame   
        #read_2 benchmark
        t1 = time.perf_counter()
        df = pd.read_hdf(f'files_1/{filename}.hdf5', 'Dataset')
        print(df)
        t2 = time.perf_counter()
        read_time = t2 - t1
    
    else: #CSV
        #use pandas dataframe to read all
        #read benchmark
        t1 = time.perf_counter()
        df = pd.read_csv(f'files_1/{filename}.csv')
        print(df)
        t2 = time.perf_counter()
        read_time = t2 - t1
    return read_time

#read by rows for first half properties
def read_3(file_format, filename, num_properties, num_elements):
    
    read_time = 0.0

    #read by rows
    if file_format == 'HDF5_compound':
        #work with pandas data frame
        #read_3 benchmark
        t1 = time.perf_counter()
        df = pd.read_hdf(f'files_1/{filename}.hdf5', 'Dataset')
        for row in range(num_elements):
            #read each row
            print(df.iloc[row, 0:(int)(num_properties/2)])
        t2 = time.perf_counter()
        read_time = t2 - t1

    else: #in the case of CSV
        #Work with pandas dataFrame
        
        #read_3 benchmark
        t1 = time.perf_counter()   
        df = pd.read_csv(f'files_1/{filename}.csv')
        for row_index in range(num_elements):
            #select the row<->column chunk
            df_row = df.iloc[row_index, 1:(int)(num_properties/2)+1]
            print(df_row)
        t2 = time.perf_counter()
        read_time = t2 - t1

    return read_time
