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
            create_time, open_time = df.iloc[-2, 1:]
            create_error, open_error = df.iloc[-1, 1:]
            data_for_each_configuration = [create_time, create_error, open_time, open_error]
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

        
        bar_create_open = plt.bar(x=x + offset, height=[create_time_0, create_time_1, create_time_2, create_time_3], width=width,
                                  label=file_format, edgecolor='black', yerr=[create_error_0, create_error_1, create_error_2, create_error_3])
        plt.bar_label(bar_create_open, padding=2, fontsize=7)
        offset += width
    plt.legend(fontsize=7, loc='upper center')
    plt.tight_layout()
    plt.savefig(f'plot_files/create.png')
    plt.cla()
    plt.clf()


#the width of bars 
    width = .2
    #open giant-plot
    plt.figure(2)
    plt_labels = ['1MB elements', '10MB elements', '100MGB elements', '1GB elements']
    x = np.arange(len(plt_labels))
    offset = -width
    plt.ylabel('Time (ms)')
    plt.title(f'{num_datasets} Datasets -- 4 different scales Dataset open Time')
    plt.xticks(x, plt_labels)


    for file_format in file_formats:
        # Round to 2 decimal places so data shows nicely
        open_time_0 = round(database[file_format][0][2], 2)
        open_error_0 = round(database[file_format][0][3], 2)
        open_time_1 = round(database[file_format][1][2], 2)
        open_error_1 = round(database[file_format][1][3], 2)
        open_time_2 = round(database[file_format][2][2], 2)
        open_error_2 = round(database[file_format][2][3], 2)
        open_time_3 = round(database[file_format][3][2], 2)
        open_error_3 = round(database[file_format][3][3], 2)

        
        bar_create_open = plt.bar(x=x + offset, height=[open_time_0, open_time_1, open_time_2, open_time_3], width=width,
                                  label=file_format, edgecolor='black', yerr=[open_error_0, open_error_1, open_error_2, open_error_3])
        plt.bar_label(bar_create_open, padding=2, fontsize=7)
        offset += width
    plt.legend(fontsize=7, loc='upper center')
    plt.tight_layout()
    plt.savefig(f'plot_files/open.png')
    plt.cla()
    plt.clf()

