import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def average(file_formats, num_datasets, dimensions):
    # Calculate the average value in each column of the provided CSV file.
    # Append it to the file if not already appended.
    # Return these average times to be plotted.
    total_dataset_create_time = []
    total_dataset_write_time = []
    total_dataset_open_time = []
    total_dataset_read_time = []
    error = []
    for file_format in file_formats:
        df = pd.read_csv(f'csv_file/{file_format}_{num_datasets}_{dimensions}.csv')
        dataset_create_time, dataset_write_time, dataset_open_time, dataset_read_time = df.iloc[:, 1:].mean(axis=0)
        create_deviation, write_deviation, open_deviation, read_deviation = df.iloc[:, 1:].std(axis=0)
        total_dataset_create_time.append(dataset_create_time)
        total_dataset_write_time.append(dataset_write_time)
        total_dataset_open_time.append(dataset_open_time)
        total_dataset_read_time.append(dataset_read_time)
        error.append([create_deviation, write_deviation, open_deviation, read_deviation])

        average_values = pd.DataFrame({
            file_format: 'Average',
            'Dataset Create Time': [dataset_create_time],
            'Dataset Write Time': [dataset_write_time],
            'Dataset Open Time': [dataset_open_time],
            'Dataset Read Time': [dataset_read_time]
        })

        standard_error = pd.DataFrame({
            file_format: 'standard error',
            'Dataset Create Time': [create_deviation],
            'Dataset Write Time': [write_deviation],
            'Dataset Open Time': [open_deviation],
            'Dataset Read Time': [read_deviation]
        })

        df = pd.concat([df, average_values, standard_error], ignore_index=True)
        df.to_csv(f'csv_file/{file_format}_{num_datasets}_{dimensions}.csv', index=False)