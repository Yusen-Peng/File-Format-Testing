import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yaml
def plot(file_formats, config_files):

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
            create_time, write_time, open_time, read_time = df.iloc[-2, 1:]
            create_error, write_error, open_error, read_error = df.iloc[-1, 1:]
            data_for_each_configuration = [create_time, create_error, write_time, write_error, open_time, open_error, read_time, read_error]
            data_for_all_configurations.append(data_for_each_configuration)
        
        #configure the dictionary
        database[file_format] = data_for_all_configurations
        

    #the width of bars
    width = .16
    #write giant-plot
    plt.figure(1)
    plt_labels = ['1MB elements', '10MB elements', '100MGB elements', '1GB elements']
    x = np.arange(len(plt_labels))
    offset = -2*width
    plt.ylabel('Time (ms)')
    plt.title(f'{num_datasets} Datasets -- 4 different scales Dataset create Time')
    plt.xticks(x, plt_labels)
    for file_format in file_formats:
        # Round to 2 decimal places so data shows nicely
        create_time_0 = round(database[file_format][0][0], 2)
        create_error_0 = round(database[file_format][0][1], 2)
        create_time_1 = round(database[file_format][1][0], 2)
        create_error_1 = round(database[file_format][1][1], 2)
        create_time_2 = round(database[file_format][2][0], 2)
        create_error_2 = round(database[file_format][2][1], 2)
        create_time_3 = round(database[file_format][3][0], 2)
        create_error_3 = round(database[file_format][3][1], 2)
        
        bar_create = plt.bar(x=x + offset, height=[create_time_0, create_time_1, create_time_2, create_time_3], width=width,
                                  label=file_format, edgecolor='black', yerr=[create_error_0, create_error_1, create_error_2, create_error_3])
        plt.bar_label(bar_create, padding=2, fontsize=7)
        offset += width
    plt.legend(fontsize=7, loc='upper center')
    plt.tight_layout()
    plt.savefig(f'plot_files/create.png')
    plt.cla()
    plt.clf()
    
    #write giant-plot
    plt.figure(2)
    plt_labels = ['1MB elements', '10MB elements', '100MGB elements', '1GB elements']
    x = np.arange(len(plt_labels))
    offset = -2*width
    plt.ylabel('Time (ms)')
    plt.title(f'{num_datasets} Datasets -- 4 different scales Dataset write Time')
    plt.xticks(x, plt_labels)
    for file_format in file_formats:
        # Round to 2 decimal places so data shows nicely
        write_time_0 = round(database[file_format][0][2], 2)
        write_error_0 = round(database[file_format][0][3], 2)
        write_time_1 = round(database[file_format][1][2], 2)
        write_error_1 = round(database[file_format][1][3], 2)
        write_time_2 = round(database[file_format][2][2], 2)
        write_error_2 = round(database[file_format][2][3], 2)
        write_time_3 = round(database[file_format][3][2], 2)
        write_error_3 = round(database[file_format][3][3], 2)
        
        bar_write = plt.bar(x=x + offset, height=[write_time_0, write_time_1, write_time_2, write_time_3], width=width,
                                  label=file_format, edgecolor='black', yerr=[write_error_0, write_error_1, write_error_2, write_error_3])
        plt.bar_label(bar_write, padding=2, fontsize=7)
        offset += width
    plt.legend(fontsize=7, loc='upper center')
    plt.tight_layout()
    plt.savefig(f'plot_files/write.png')
    plt.cla()
    plt.clf()

#the width of bars 
    #open giant-plot
    plt.figure(3)
    plt_labels = ['1MB elements', '10MB elements', '100MGB elements', '1GB elements']
    x = np.arange(len(plt_labels))
    offset = -2*width
    plt.ylabel('Time (ms)')
    plt.title(f'{num_datasets} Datasets -- 4 different scales Dataset open Time')
    plt.xticks(x, plt_labels)


    for file_format in file_formats:
        # Round to 2 decimal places so data shows nicely
        open_time_0 = round(database[file_format][0][4], 2)
        open_error_0 = round(database[file_format][0][5], 2)
        open_time_1 = round(database[file_format][1][4], 2)
        open_error_1 = round(database[file_format][1][5], 2)
        open_time_2 = round(database[file_format][2][4], 2)
        open_error_2 = round(database[file_format][2][5], 2)
        open_time_3 = round(database[file_format][3][4], 2)
        open_error_3 = round(database[file_format][3][5], 2)

        
        bar_write_read = plt.bar(x=x + offset, height=[open_time_0, open_time_1, open_time_2, open_time_3], width=width,
                                  label=file_format, edgecolor='black', yerr=[open_error_0, open_error_1, open_error_2, open_error_3])
        plt.bar_label(bar_write_read, padding=2, fontsize=7)
        offset += width
    plt.legend(fontsize=7, loc='upper center')
    plt.tight_layout()
    plt.savefig(f'plot_files/open.png')
    plt.cla()
    plt.clf()

    #open giant-plot
    plt.figure(4)
    plt_labels = ['1MB elements', '10MB elements', '100MGB elements', '1GB elements']
    x = np.arange(len(plt_labels))
    offset = -2*width
    plt.ylabel('Time (ms)')
    plt.title(f'{num_datasets} Datasets -- 4 different scales Dataset read Time')
    plt.xticks(x, plt_labels)
    for file_format in file_formats:
        # Round to 2 decimal places so data shows nicely
        read_time_0 = round(database[file_format][0][6], 2)
        read_error_0 = round(database[file_format][0][7], 2)
        read_time_1 = round(database[file_format][1][6], 2)
        read_error_1 = round(database[file_format][1][7], 2)
        read_time_2 = round(database[file_format][2][6], 2)
        read_error_2 = round(database[file_format][2][7], 2)
        read_time_3 = round(database[file_format][3][6], 2)
        read_error_3 = round(database[file_format][3][7], 2)

        
        bar_write_read = plt.bar(x=x + offset, height=[read_time_0, read_time_1, read_time_2, read_time_3], width=width,
                                  label=file_format, edgecolor='black', yerr=[read_error_0, read_error_1, read_error_2, read_error_3])
        plt.bar_label(bar_write_read, padding=2, fontsize=7)
        offset += width
    plt.legend(fontsize=7, loc='upper center')
    plt.tight_layout()
    plt.savefig(f'plot_files/read.png')
    plt.cla()
    plt.clf()
