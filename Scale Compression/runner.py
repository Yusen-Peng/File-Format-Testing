import csv
import glob
import yaml 
import giant_plot, read_test, write_test, average_test


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
            writer.writerow([file_format, 'Dataset Create Time','Dataset Write Time','Dataset Open Time','Dataset Read Time'])
            csvfile.close()
    
    #keep track of write data for each file format
    create_dict = {}
    write_dict = {} # file format --> write data
    for file_format in file_formats:
        create_list = []
        write_list = [] # combine write data for all trials
        for i in range(num_trials):
            create_data, write_data = write_test.write(file_format, filename, num_datasets, dimensions)
            create_list.append(create_data)
            write_list.append(write_data)
        create_dict[file_format] = create_list
        write_dict[file_format] = write_list
    
    #keep track of read data for each file format
    open_dict = {}
    read_dict = {} # file format --> read data
    for file_format in file_formats:
        open_list = []
        read_list = [] # combine read data for all trials
        for i in range(num_trials):
            open_data, read_data = read_test.read(file_format,filename,num_datasets,dimensions)
            open_list.append(open_data)
            read_list.append(read_data)
        open_dict[file_format] = open_list
        read_dict[file_format] = read_list

    #push data from dictionaries to CSV files
    for file_format in file_formats:
        #open corresponding CSV files
        with open(f'csv_file/{file_format}_{num_datasets}_{dimensions}.csv', 'a') as csv_file:
            #write data and read data associated with each file format
            create_benchmark = create_dict[file_format]
            write_benchmark = write_dict[file_format]
            open_benchmark = open_dict[file_format]
            read_benchmark = read_dict[file_format]
            #create a CSV writer
            writer = csv.writer(csv_file)
            #push data for each trial
            for i in range(num_trials):
                create_trial = create_benchmark[i]
                write_trial = write_benchmark[i]
                open_trial = open_benchmark[i]
                read_trial = read_benchmark[i]
                data_row = [f'Trial {i + 1}', create_trial, write_trial, open_trial, read_trial]
                writer.writerow(data_row) 
            #close CSV file in the end
            csvfile.close()

    #evaluate average and standard error
    #update to CSV tracker files 
    average_test.average(file_formats, num_datasets, dimensions)


def main(file_formats, num_trials):

    config_files = glob.glob('config_test/*.yaml')
    
    for config_file in config_files:
        run_benchmark(config_file,file_formats,num_trials)
                                                            #run benchmarks for every configuration file
    giant_plot.plot(file_formats, config_files)


if __name__ == '__main__':
    file_formats = ['HDF5', 'HDF5_compressed', 'netCDF4', 'netCDF4_compressed', 'Zarr', 'Zarr_compressed']
                                                            # 3 file format to explore

    num_trials = 5  
                                                            # Must be greater than 1

    main(file_formats, num_trials)
