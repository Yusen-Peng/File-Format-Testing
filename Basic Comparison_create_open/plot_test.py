import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot(file_formats, num_datasets, dimensions):    


    create_time, open_time, error = process_csv(file_formats, num_datasets, dimensions)
                                                # get list of total times and error for ALL file_formats

    width = .17

    #plot read/write time
    plt.figure(1)
    plt_labels = ['Dataset Create Time', 'Dataset Open Time']
    x = np.arange(len(plt_labels))
    offset = -width
    plt.ylabel('Time (ms)')
    plt.title(f'{num_datasets} Datasets {dimensions} Elements Dataset Create/Open Times')
    plt.xticks(x, plt_labels)
                                                # plot formatting 

    for i in range(0, len(file_formats)):
        # Round to 5 decimal places so data shows nicely
        open_time_rounded = round(open_time[i], 5)
        create_time_rounded = round(create_time[i], 5)
        create_error = error[i][0]
        open_error = error[i][1]
        
        bar_create_open = plt.bar(x=x + offset, height=[create_time_rounded, open_time_rounded], width=width,
                                  label=file_formats[i], edgecolor='black', yerr=[create_error, open_error])
                                                #retrieve data and create the bar chart for every file format

        plt.bar_label(bar_create_open, padding=3)
                                                #label with padding

        offset += width

    plt.legend()
    plt.tight_layout()
    plt.savefig(f'plot_files/{num_datasets}_{dimensions}_create_open.png')
    plt.cla()
    plt.clf()
                                                #save figure and clear it


    
    
def process_csv(file_formats, num_datasets, dimensions):

    total_dataset_create_time = []
    total_dataset_open_time = []
    error = []

    for file_format in file_formats:
        df = pd.read_csv(f'csv_file/{file_format}_{num_datasets}_{dimensions}.csv')
                                                        # read corresponding csv file

        dataset_create_time, dataset_open_time = df.iloc[:, 1:].mean(axis=0)
        create_deviation, open_deviation = df.iloc[:, 1:].std(axis=0)
                                                        # extract everything except the first column
                                                        # axis=0: calculate mean & std vertically

        total_dataset_create_time.append(dataset_create_time)
        total_dataset_open_time.append(dataset_open_time)
                                                        # append each mean to the corresponding list

        error.append([create_deviation, open_deviation])
                                                        # append 4 std as a list to "error" list 
                                                        # ("error") ends up as a list of list
        
        
        if df.iloc[-1, 0] == 'Average':
            # Go to next iteration if the last column of the CSV file has the average times
            continue


        average_values = pd.DataFrame({
            file_format: 'Average',
            'Dataset Create Time': [dataset_create_time],
            'Dataset Open Time': [dataset_open_time]
        })
                                                        # create a dataframe of mean-values

        df = pd.concat([df, average_values], ignore_index=True)
        df.to_csv(f'csv_file/{file_format}_{num_datasets}_{dimensions}.csv', index=False)
                                                        # concatenate df & mean-values vertically
                                                        # convert the dataframe back to csv file

    return total_dataset_create_time, total_dataset_open_time, error
