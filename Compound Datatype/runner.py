import csv
import glob
import yaml 
import plot_test, read_test, write_test


def run_benchmark(config_file, file_formats, num_trials):
    
    #get configuration data from the configuration file
    with open(f'{config_file}', 'r') as file:
        config = yaml.safe_load(file)
        filename = config.get('FILE_NAME')
        num_properties = config.get('NUMBER_PROPERTIES')
        num_elements = config.get('NUMBER_ELEMENTS')

    #keep track of write data for compound HDF5 and CSV 
    write_dict = {} # file format --> write data
    for file_format in file_formats:
        write_list = [] # combine write data for all trials
        for i in range(num_trials):
            write_data = write_test.write(file_format, filename, num_properties, num_elements)
            write_list.append(write_data)
        write_dict[file_format] = write_list


    #keep track of read data for HDF5 and CSV, for 4 different approaches of reading respectively
    read_dict_0 = {} #read data property-wise
    read_dict_1 = {} #read data row-wise 
    read_dict_2 = {} #read data row-wise for all properties
    read_dict_3 = {} #read data row-wise for first half properties
    for file_format in file_formats:
        read_list_0 = [] # combine read data for all trials
        read_list_1 = []
        read_list_2 = []
        read_list_3 = []
        for i in range(num_trials):
            read_data = read_test.read_0(file_format,filename,num_properties,num_elements)
            read_list_0.append(read_data)
            read_data = read_test.read_1(file_format,filename,num_properties,num_elements)
            read_list_1.append(read_data)
            read_data = read_test.read_2(file_format,filename,num_properties,num_elements)
            read_list_2.append(read_data)
            read_data = read_test.read_3(file_format,filename,num_properties,num_elements)
            read_list_3.append(read_data)
        read_dict_0[file_format] = read_list_0
        read_dict_1[file_format] = read_list_1
        read_dict_2[file_format] = read_list_2
        read_dict_3[file_format] = read_list_3


    #push data from dictionaries to CSV files
    #write benchmark CSV file
    for file_format in file_formats:
        #open corresponding CSV files
        with open(f'csv_file/{file_format}_{num_properties}_{num_elements}_write.csv', 'w') as csv_file:
            #write the header
            writer = csv.writer(csv_file)
            writer.writerow(['CSV', 'Dataset Write Time', 'Alternative Time'])
            
            #write data associated with each file format
            write_benchmark = write_dict[file_format]
            
            #create a CSV writer
            #push data for each trial
            for i in range(num_trials):
                write_trial = list(range(2))
                if file_format == 'HDF5_compound':
                    write_trial[0] = write_benchmark[i][0]
                    write_trial[1] = 0.0
                else: 
                    write_trial[0] = write_benchmark[i][0]
                    write_trial[1] = write_benchmark[i][1]

                data_row = [f'Trial {i + 1}', write_trial[0], write_trial[1]]
                writer.writerow(data_row) 
            #close CSV file in the end
            csv_file.close()

    for file_format in file_formats:
        #open corresponding CSV files
        with open(f'csv_file/{file_format}_{num_properties}_{num_elements}_read.csv', 'w') as csv_file:
            #write the header
            writer = csv.writer(csv_file)
            writer.writerow(['CSV', 
                         'Dataset Read_0 Time', 
                         'Dataset Read_1 Time', 
                         'Dataset Read_2 Time',
                         'Dataset Read_3 Time'
                        ])
            
            #write data and read data associated with each file format
            read_benchmark_0 = read_dict_0[file_format]
            read_benchmark_1 = read_dict_1[file_format]
            read_benchmark_2 = read_dict_2[file_format]
            read_benchmark_3 = read_dict_3[file_format]

            #create a CSV writer
            #push data for each trial
            for i in range(num_trials):
                read_trial_0 = read_benchmark_0[i]
                read_trial_1 = read_benchmark_1[i]
                read_trial_2 = read_benchmark_2[i]
                read_trial_3 = read_benchmark_3[i]

                data_row = [f'Trial {i + 1}',  
                            read_trial_0,
                            read_trial_1,
                            read_trial_2,
                            read_trial_3
                            ]
                writer.writerow(data_row) 
            #close CSV file in the end
            csv_file.close()

    plot_test.plot(file_formats, num_properties, num_elements)
                                                            #plot final results 


def main(file_formats, num_trials):

    config_files = glob.glob('config/*.yaml')
    
    for config_file in config_files:
        run_benchmark(config_file,file_formats,num_trials)
                                                            #run benchmarks for every configuration file



if __name__ == '__main__':
    file_formats  = ['HDF5_compound','CSV']
                                                            # 3 file format to explore

    num_trials = 5
                                                            # Must be greater than 1

    main(file_formats, num_trials)
