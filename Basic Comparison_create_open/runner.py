import csv
import glob
import yaml 
import plot_test, read_test, write_test


def run_benchmark(config_file, file_formats, num_trials):
    
    #get configuration data from the configuration file
    with open(f'{config_file}', 'r') as file:
        config = yaml.safe_load(file)
        filename = config.get('FILE_NAME')
        num_datasets = config.get('NUMBER_DATASETS')
        dimensions = config.get('NUMBER_ELEMENTS')
                                                            

    #Create CSV templates for each file format
    for file_format in file_formats:
        with open(f'csv_file/{file_format}_{num_datasets}_{dimensions}.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([file_format, 'Dataset Create Time','Dataset Open Time'])
            csvfile.close()
    
    #keep track of write data for each file format
    create_dict = {} # file format --> write data
    for file_format in file_formats:
        create_list = [] # combine write data for all trials
        for i in range(num_trials):
            create_data = write_test.write(file_format, filename, num_datasets, dimensions)
            create_list.append(create_data)
        create_dict[file_format] = create_list
    
    #keep track of read data for each file format
    open_dict = {} # file format --> read data
    for file_format in file_formats:
        open_list = [] # combine read data for all trials
        for i in range(num_trials):
            open_data = read_test.read(file_format,filename,num_datasets,dimensions)
            open_list.append(open_data)
        open_dict[file_format] = open_list
    #push data from dictionaries to CSV files
    for file_format in file_formats:
        #open corresponding CSV files
        with open(f'csv_file/{file_format}_{num_datasets}_{dimensions}.csv', 'w') as csv_file:
            #write data and read data associated with each file format
            create_benchmark = create_dict[file_format]
            open_benchmark = open_dict[file_format]
            #create a CSV writer
            writer = csv.writer(csv_file)
            #push data for each trial
            for i in range(num_trials):
                create_trial = create_benchmark[i]
                open_trial = open_benchmark[i]
                data_row = [f'Trial {i + 1}', create_trial, open_trial]
                writer.writerow(data_row) 
            #close CSV file in the end
            csvfile.close()

    plot_test.plot(file_formats, num_datasets, dimensions)
                                                            #plot final results 


def main(file_formats, num_trials):

    config_files = glob.glob('config/*.yaml')
    
    for config_file in config_files:
        run_benchmark(config_file,file_formats,num_trials)
                                                            #run benchmarks for every configuration file



if __name__ == '__main__':
    file_formats = ['HDF5','netCDF4', 'Zarr']
                                                            # 3 file format to explore

    num_trials = 5  
                                                            # Must be greater than 1

    main(file_formats, num_trials)
