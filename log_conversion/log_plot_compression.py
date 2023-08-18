import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import glob
import yaml

def plot(file_formats, num_datasets, dimensions):    

    create_time = []
    write_time = [] 
    open_time = []
    read_time = [] 
    error = []
    for i in range(0, len(file_formats)):
        df = pd.read_csv(f'csv_file_compression/{file_formats[i]}_{num_datasets}_{dimensions}.csv')
        create, write, open, read = df.iloc[-1, 1: ]
        create_err = df.iloc[1:-1, 1].std(axis=0)
        write_err = df.iloc[1:-1,2].std(axis=0)
        open_err = df.iloc[1:-1,3].std(axis=0)
        read_err = df.iloc[1:-1,4].std(axis=0)
        create_time.append(create)
        write_time.append(write)
        open_time.append(open)
        read_time.append(read)
        error.append([create_err, write_err, open_err, read_err])


    width = .10

    #plot read/write time
    plt.figure(1)
    plt_labels = ['Dataset Read Time', 'Dataset Write Time']
    x = np.arange(len(plt_labels))
    offset = -width
    plt.ylabel('Time in ms')
    plt.yscale('log')
    plt.title(f'{num_datasets} Datasets {dimensions} Elements Dataset Read / Write Times')
    plt.xticks(x, plt_labels)
                                                # plot formatting 

    for i in range(0, len(file_formats)):
        # Round to 5 decimal places so data shows nicely
        #natural log average
        write_time_rounded = round(write_time[i], 3)
        read_time_rounded = round(read_time[i], 3)
        
        bar_create_open = plt.bar(x=x + offset, height=[read_time_rounded, write_time_rounded], width=width,
                                  label=file_formats[i], edgecolor='black')
                                                #retrieve data and create the bar chart for every file format

        plt.bar_label(bar_create_open, padding=3)
                                                #label with padding

        offset += width

    plt.legend()
    plt.tight_layout()
    plt.savefig(f'plot_files/{num_datasets}_{dimensions}_read_write_log.png')
    plt.cla()
    plt.clf()
                                                #save figure and clear it

    #plot read/write time
    plt.figure(2)
    plt_labels = ['Dataset Create Time', 'Dataset Open Time']
    x = np.arange(len(plt_labels))
    offset = -width
    plt.ylabel('Time in ms')
    plt.yscale('log')
    plt.title(f'{num_datasets} Datasets {dimensions} Elements Dataset Create / Open Times')
    plt.xticks(x, plt_labels)
                                                # plot formatting 

    for i in range(0, len(file_formats)):
        # Round to 5 decimal places so data shows nicely
        #natural log average
        create_time_rounded = round(create_time[i], 3)
        open_time_rounded = round(open_time[i], 3)
        
        bar_create_open = plt.bar(x=x + offset, height=[create_time_rounded,open_time_rounded], width=width,
                                  label=file_formats[i], edgecolor='black')
                                                #retrieve data and create the bar chart for every file format

        plt.bar_label(bar_create_open, padding=3)
                                                #label with padding

        offset += width

    plt.legend()
    plt.tight_layout()
    plt.savefig(f'plot_files/{num_datasets}_{dimensions}_create_open_log.png')
    plt.cla()
    plt.clf()

if __name__ == '__main__':
    file_formats = ['HDF5','HDF5_compressed','netCDF4', 'netCDF4_compressed', 'Zarr', 'Zarr_compressed']
                                                            # 3 file format to explore
    config_files = glob.glob('config/*.yaml')
    
    for config_file in config_files:
        with open(f'{config_file}', 'r') as file:
            config = yaml.safe_load(file)
            filename = config.get('FILE_NAME')
            num_datasets = config.get('NUMBER_DATASETS')
            dimensions = config.get('NUMBER_ELEMENTS')

        plot(file_formats, num_datasets, dimensions)
    