import csv
import glob
import yaml 
import plot_test, read_test, write_test


def run_benchmark(config_file, file_formats, num_trials):

    with open(f'{config_file}', 'r') as file:
        config = yaml.safe_load(file)
        filename = config.get('FILE_NAME')
        num_datasets = config.get('NUMBER_DATASETS')
        dimensions = config.get('NUMBER_ELEMENTS')
                                                            # get configuration data from the configuration file

    for file_format in file_formats:
        
        csvfile = open(f'csv_file/{file_format}_{num_datasets}_{dimensions}.csv', 'w')
        writer = csv.writer(csvfile)
        writer.writerow([file_format, 'Dataset Write Time','Dataset Read Time'])
        for i in range(num_trials):
            results_write = write_test.write(file_format, filename, num_datasets, dimensions)
            results_read = read_test.read(file_format, filename, num_datasets, dimensions)
            writer.writerow([f'Trial {i + 1}', results_write, results_read])
        csvfile.close()
                                                            #Create a CSV file to store the data for a given file format

    plot_test.plot(file_formats, num_datasets, dimensions)
                                                            #plot final results 


def main(file_formats, num_trials):

    config_files = glob.glob('config/*.yaml')
    
    for config_file in config_files:
        run_benchmark(config_file,file_formats,num_trials)
                                                            #run benchmarks for every configuration file



if __name__ == '__main__':
    file_formats = ['CSV','HDF5','netCDF4','Zarr']
                                                            # 4 file format to explore

    num_trials = 5  
                                                            # Must be greater than 1

    main(file_formats, num_trials)
