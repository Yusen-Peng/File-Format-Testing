import csv
import glob
import os

import yaml

from unit_test import plot_test, read_test, write_test


def run_benchmark(config_file, file_formats, num_trials):
    #get configuration parameters
    with open(f'{config_file}', 'r') as file:
        config = yaml.safe_load(file)
        filename = config.get('FILE_NAME')
        num_datasets = config.get('NUMBER_DATASETS')
        dimensions = config.get('NUMBER_ELEMENTS')


    for file_format in file_formats:
        # Create a CSV file to store the data for a given file format
        csvfile = open(f'unit_test/csv_file/{file_format}_{num_datasets}_{dimensions}.csv', 'w')
        writer = csv.writer(csvfile)
        writer.writerow([file_format, 'Dataset Creation Time', 'Dataset Write Time', 'Dataset Open Time',
                         'Dataset Read Time'])

        # Run write and read benchmarks and write the times taken to the CSV file
        for i in range(num_trials):
            results_write = write_test.write(file_format, filename, num_datasets, dimensions)
            results_read = read_test.read(file_format, filename, num_datasets, dimensions)
            writer.writerow(['Trial {i + 1}', results_write[0], results_write[1], results_read[0], results_read[1]])
        csvfile.close()
    plot_test.plot(file_formats, num_datasets, dimensions)


def main(directories, file_formats, num_trials):

    config_files = glob.glob('unit_test/config/*.yaml')
    if not config_files:
        data = {
            'FILE_NAME': 'File_Name',
            'NUMBER_DATASETS': 0,
            'NUMBER_ELEMENTS': [0, 0, 0]  # Create dataset with dimensions provided by 'NUMBER_ELEMENTS'
        }
        with open('unit_test/config/sample_configuration.yaml', 'w') as file:
            yaml.safe_dump(data, file, sort_keys=False)
        print('A sample configuration file has been placed in the directory: unit_test/config/')
        exit(0)

    for config_file in config_files:
        run_benchmark(config_file, file_formats,num_trials)


if __name__ == '__main__':
    directories = ['config', 'csv_files', 'plot_files', 'files_1', 'files_2']

    #each file format and associated compressed format   
    file_formats = ['HDF5', 'HDF5_compressed', 'netCDF4', 'netCDF4_compressed', 'Zarr', 'Zarr_compressed']

    num_trials = 5
    main(directories, file_formats, num_trials)