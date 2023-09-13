import pandas as pd
import glob
import yaml

def file_format_timing(file_format, num_datasets, dimensions, num_trials):
    timing = 0.0
    #grab data from CSV files
    df = pd.read_csv(f'timer_csv/{file_format}_{num_datasets}_{dimensions}.csv')
    avg_file, avg_per_create, avg_per_random, avg_per_write = df.iloc[-1, 1: ]
    
    #calculate the total time
    timing += avg_file * num_trials
    timing += avg_per_create * num_datasets * num_trials
    timing += avg_per_random * num_datasets * num_trials
    timing += avg_per_write * num_datasets * num_trials
    return timing

if __name__ == '__main__':
    file_formats = ['HDF5', 'netCDF4', 'Zarr']
    num_trials = 5
    config_files = glob.glob('config/*.yaml')
    for config_file in config_files:
        #grab configuration data
        with open(f'{config_file}', 'r') as file:
            config = yaml.safe_load(file)
            filename = config.get('FILE_NAME')
            num_datasets = config.get('NUMBER_DATASETS')
            dimensions = config.get('NUMBER_ELEMENTS')

            total_time = 0.0
            for file_format in file_formats:
                total_time += file_format_timing(file_format, num_datasets, dimensions, num_trials)
            print((int)(total_time)) 
