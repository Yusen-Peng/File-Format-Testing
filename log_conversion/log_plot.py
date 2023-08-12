import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import glob
import yaml

def plot(file_formats, num_datasets, dimensions):    

    write_time = [] 
    read_time = [] 
    error = []
    for i in range(0, len(file_formats)):
        df = pd.read_csv(f'csv_file/{file_formats[i]}_{num_datasets}_{dimensions}.csv')
        write, read = df.iloc[-1, 1: ]
        write_err = df.iloc[1:-1,1].std(axis=0)
        read_err = df.iloc[1:-1,2].std(axis=0)
        write_time.append(write)
        read_time.append(read)
        error.append([write_err, read_err])


    width = .17

    #plot read/write time
    plt.figure(1)
    plt_labels = ['Dataset Read Time', 'Dataset Write Time']
    x = np.arange(len(plt_labels))
    offset = -width
    plt.ylabel('Natural log of Time + 2 /ms')
    plt.title(f'{num_datasets} Datasets {dimensions} Elements Dataset Read / Write Times')
    plt.xticks(x, plt_labels)
                                                # plot formatting 

    for i in range(0, len(file_formats)):
        # Round to 5 decimal places so data shows nicely
        #natural log average
        read_time_rounded = math.log(round(read_time[i], 5)) + 2
        write_time_rounded = math.log(round(write_time[i], 5)) + 2
        
        #error
        read_error = math.log(error[i][1])
        write_error = math.log(error[i][0])
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

if __name__ == '__main__':
    file_formats = ['CSV','HDF5','netCDF4', 'Zarr']
                                                            # 3 file format to explore
    config_files = glob.glob('config/*.yaml')
    
    for config_file in config_files:
        with open(f'{config_file}', 'r') as file:
            config = yaml.safe_load(file)
            filename = config.get('FILE_NAME')
            num_datasets = config.get('NUMBER_DATASETS')
            dimensions = config.get('NUMBER_ELEMENTS')

        plot(file_formats, num_datasets, dimensions)
    