import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot(file_formats, num_properties, num_elements):    


    write_time, error_w = process_csv_write(file_formats, num_properties, num_elements)
    read_0_time, read_1_time, read_2_time, read_3_time, error_r = process_csv_read(file_formats, num_properties, num_elements)

    width = .17
    #plot write time
    plt.figure(1)
    plt_labels = ['Dataset Write Time']
    x = np.arange(len(plt_labels))
    offset = -width
    plt.ylabel('Time (ms)')
    plt.title(f'{num_properties} Properties {num_elements} Elements Dataset Write Time')
    plt.xticks(x, plt_labels)
    
    for i in range(len(file_formats)):
        if file_formats[i] == 'HDF5_compound':
            write_time_rounded = round(write_time[i][0], 3)
            write_error = error_w[i][0]

            bar_write = plt.bar(x = x + offset, height=[write_time_rounded],
                            width=width,label=file_formats[i],
                            edgecolor='black',yerr=[write_error])

            plt.bar_label(bar_write, padding=6, fontsize=7)

            offset += width

        else:
            write_time_rounded = round(write_time[i][0], 3)
            alternative_time_rounded = round(write_time[i][1], 3)
            write_error = error_w[i][0]
            alternative_error = error_w[i][1]
            bar_write = plt.bar(x = x + offset, height=[write_time_rounded],
                            width=width,label=f'{file_formats[i]}_by_column',
                            edgecolor='black',yerr=[write_error])
            
            plt.bar_label(bar_write, padding=6, fontsize=7)
            offset += width

            bar_write = plt.bar(x = x + offset, height=[alternative_time_rounded],
                            width=width, label=f'{file_formats[i]}_by_row',
                            edgecolor='black',yerr=[alternative_error])
            
            plt.bar_label(bar_write, padding=6, fontsize=7)
            offset += width

    plt.legend(fontsize=7, loc='best')
    plt.tight_layout()
    plt.savefig(f'plot_files/{num_properties}_{num_elements}_write.png')
    plt.cla()
    plt.clf()

    width = .17
    offset = -0.5*width
    #plot read time
    plt.figure(2)
    plt_labels = ['Read by column', 
                  'Read by row',
                  'Read all',
                  'Read by half row'
                 ]
    x = np.arange(len(plt_labels))
    plt.ylabel('Time (ms)')
    plt.title(f'{num_properties} Properties {num_elements} Elements Dataset Read Times')
    plt.xticks(x, plt_labels)
                                                # plot formatting 
                                                
    for i in range(0, len(file_formats)):
        # Round to 3 decimal places
        read_0_time_rounded = round(read_0_time[i], 3)
        read_1_time_rounded = round(read_1_time[i], 3)
        read_2_time_rounded = round(read_2_time[i], 3)
        read_3_time_rounded = round(read_3_time[i], 3)
        
        read_0_error = error_r[i][0]
        read_1_error = error_r[i][1]
        read_2_error = error_r[i][2]
        read_3_error = error_r[i][3]
        
        bar_read = plt.bar(x= x + offset, height=[read_0_time_rounded, 
                                                  read_1_time_rounded,
                                                  read_2_time_rounded,
                                                  read_3_time_rounded
                                                ], width=width,
                                  label=file_formats[i], edgecolor='black', yerr=[
                                                                                  read_0_error,
                                                                                  read_1_error, 
                                                                                  read_2_error,
                                                                                  read_3_error])
                                                #retrieve data and create the bar chart for every file format

        plt.bar_label(bar_read, padding=5, fontsize=7)
                                                #label with padding

        offset += width

    plt.legend(fontsize=7, loc='best')
    plt.tight_layout()
    plt.savefig(f'plot_files/{num_properties}_{num_elements}_read.png')
    plt.cla()
    plt.clf()
                                                #save figure and clear it

    
def process_csv_write(file_formats, num_properties, num_elements):

    total_dataset_write_time = []
    error = []

    for file_format in file_formats:
        df = pd.read_csv(f'csv_file/{file_format}_{num_properties}_{num_elements}_write.csv')
                                                        # read corresponding csv file

        dataset_write_time = df.iloc[:, 1].mean(axis=0)
        dataset_write_time_alternative = df.iloc[:,2].mean(axis=0)
        write_deviation = df.iloc[:, 1].std(axis=0)
        alternative_deviation = df.iloc[:,2].std(axis=0)

        total_dataset_write_time.append([dataset_write_time, dataset_write_time_alternative])

        error.append([write_deviation, alternative_deviation])
    
        average_values = pd.DataFrame({
            file_format: 'Average',
            'Dataset Write Time': [dataset_write_time],
            'Alternative Time': [dataset_write_time_alternative]
        })
                                                        # create a dataframe of mean-values

        df = pd.concat([df, average_values], ignore_index=True)
                                                        # concatenate df & mean-values vertically

        df.to_csv(f'csv_file/{file_format}_{num_properties}_{num_elements}_write.csv', index=False)
                                                        # convert the dataframe back to csv file

    return total_dataset_write_time, error



def process_csv_read(file_formats, num_properties, num_elements):
    
    total_dataset_read_0_time = []
    total_dataset_read_1_time = []
    total_dataset_read_2_time = []
    total_dataset_read_3_time = []
    error = []

    for file_format in file_formats:
        df = pd.read_csv(f'csv_file/{file_format}_{num_properties}_{num_elements}_read.csv')
                                                        #read corresponding csv file

        dataset_read_0_time, dataset_read_1_time, dataset_read_2_time, dataset_read_3_time = df.iloc[:, 1:].mean(axis=0)
        read_0_deviation, read_1_deviation, read_2_deviation, read_3_deviation = df.iloc[:, 1:].std(axis=0)
    
        total_dataset_read_0_time.append(dataset_read_0_time)
        total_dataset_read_1_time.append(dataset_read_1_time)
        total_dataset_read_2_time.append(dataset_read_2_time)
        total_dataset_read_3_time.append(dataset_read_3_time)
                                                        # append each mean to the corresponding list

        error.append([read_0_deviation, read_1_deviation,read_2_deviation,read_3_deviation])
                                                        # append 4 std as a list to "error" list 
                                                        # ("error") ends up as a list of list
    
        average_values = pd.DataFrame({
            file_format: 'Average',
            'Dataset Read_0 Time': [dataset_read_0_time],
            'Dataset Read_1 Time': [dataset_read_1_time],
            'Dataset Read_2 Time': [dataset_read_2_time],
            'Dataset Read_3 Time': [dataset_read_3_time],
        })
                                                        # create a dataframe of mean-values

        df = pd.concat([df, average_values], ignore_index=True)
                                                        # concatenate df & mean-values vertically

        df.to_csv(f'csv_file/{file_format}_{num_properties}_{num_elements}_read.csv', index=False)
                                                        # convert the dataframe back to csv file

    return total_dataset_read_0_time, total_dataset_read_1_time, total_dataset_read_2_time, total_dataset_read_3_time, error
