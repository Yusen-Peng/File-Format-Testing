import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yaml
import glob
def plot(file_formats, config_files, dimensions):

    #dictionary: file format -> its data for all configurations
    database = {}
    for file_format in file_formats:
        data_for_all_configurations = []
        for config_file in config_files:
            #get configuration data from the configuration file
            with open(f'{config_file}', 'r') as file:
                config = yaml.safe_load(file)
                num_datasets = config.get('NUMBER_DATASETS')
                dimensions = config.get('NUMBER_ELEMENTS')

            #get the data for each configuration and add it to the list
            df = pd.read_csv(f'csv_file/{file_format}_{num_datasets}_{dimensions}.csv')
            write_time, read_time = df.iloc[-2, 1:]
            write_error, read_error = df.iloc[-1, 1:]
            data_for_each_configuration = [write_time, write_error, read_time, read_error]
            data_for_all_configurations.append(data_for_each_configuration)
        
        #configure the dictionary
        database[file_format] = data_for_all_configurations
        
    
    #the width of bars 
    width = .2
    #create giant-plot
    plt.figure(1)
    plt_labels = ['1MB elements', '10MB elements', '100MGB elements', '1GB elements']
    x = np.arange(len(plt_labels))
    offset = -width
    plt.ylabel('Time (ms)')
    plt.title(f'{num_datasets} Datasets -- 4 different scales Dataset write Time')
    plt.xticks(x, plt_labels)



    for file_format in file_formats:
        # Round to 2 decimal places so data shows nicely
        write_time_0 = round(database[file_format][0][0], 2)
        write_error_0 = round(database[file_format][0][1], 2)
        write_time_1 = round(database[file_format][1][0], 2)
        write_error_1 = round(database[file_format][1][1], 2)
        write_time_2 = round(database[file_format][2][0], 2)
        write_error_2 = round(database[file_format][2][1], 2)
        write_time_3 = round(database[file_format][3][0], 2)
        write_error_3 = round(database[file_format][3][1], 2)

        
        bar_write_read = plt.bar(x=x + offset, height=[write_time_0, write_time_1, write_time_2, write_time_3], width=width,
                                  label=file_format, edgecolor='black', yerr=[write_error_0, write_error_1, write_error_2, write_error_3])
        plt.bar_label(bar_write_read, padding=2, fontsize=7)
        offset += width
    plt.legend(fontsize=7, loc='upper center')
    plt.tight_layout()
    plt.savefig(f'plot_files/write.png')
    plt.cla()
    plt.clf()



#the width of bars 
    width = .2
    #open giant-plot
    plt.figure(2)
    plt_labels = ['1MB elements', '10MB elements', '100MGB elements', '1GB elements']
    x = np.arange(len(plt_labels))
    offset = -width
    plt.ylabel('Time in ms')
    plt.yscale('log')
    plt.title(f'{num_datasets} Datasets -- 4 different scales Dataset read Time')
    plt.xticks(x, plt_labels)


    for file_format in file_formats:
        # Round to 2 decimal places so data shows nicely
        read_time_0 = round(database[file_format][0][2], 2)
        read_error_0 = round(database[file_format][0][3], 2)
        read_time_1 = round(database[file_format][1][2], 2)
        read_error_1 = round(database[file_format][1][3], 2)
        read_time_2 = round(database[file_format][2][2], 2)
        read_error_2 = round(database[file_format][2][3], 2)
        read_time_3 = round(database[file_format][3][2], 2)
        read_error_3 = round(database[file_format][3][3], 2)

        
        bar_write_read = plt.bar(x=x + offset, height=[read_time_0, read_time_1, read_time_2, read_time_3], width=width,
                                  label=file_format, edgecolor='black', yerr=[read_error_0, read_error_1, read_error_2, read_error_3])
        plt.bar_label(bar_write_read, padding=2, fontsize=7)
        offset += width
    plt.legend(fontsize=7, loc='upper center')
    plt.tight_layout()
    plt.savefig(f'plot_files/read.png')
    plt.cla()
    plt.clf()

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