# File Format Comparison Benchmark

Scientific data is often stored in files because of the simplicity they provide in managing, transferring, and sharing
data. These files are typically structured in a specific arrangement and contain metadata to understand the structure
the data is stored in. There are numerous file formats in use in various scientific domains that provide abstractions
for storing and retrieving data. With the abundance of file formats aiming to store large amounts of scientific data
quickly and easily,
a question that arises is, "Which scientific file format is best for a general use case?"
In this study, we compiled a set of benchmarks for common file operations, i.e., create, open, read, write, and close,
and used the results of these benchmarks to compare three popular formats: `HDF5`, `netCDF4`, and `Zarr`.


## How to Run
1. Install the requirements found in the `requirements.txt` file.
2. Run the `runner.py` file. If no configuration files are found in the `datasets_test/configuration_files/` directory,
   a configuration file will be generated. Otherwise, the benchmark will be run with all `.yaml` configuration files
   found in the directory. The benchmark will test each file format 5 times, but this can be
   modified by changing the `num_trials` variable in the `runner.py` file.

## Section 1: Small Scale Testing
This benchmark compares the time taken to create a dataset, write data to a dataset, and finally open that dataset at a
later time and read its contents. This can be categorized into two types of operations: the writing operation and the
reading operation.Additionally, this benchmark uses a configuration-based system in which the user is able to specify the testing
parameters such as the number of datasets to create within the file and the dimensions of the array that will be written
to each dataset by editing a `YAML` configuration file.After the benchmark is done, the program then stores the times 
taken across multiple trials in a CSV file and plots its data with [matplotlib.pyplot](https://github.com/matplotlib/matplotlib) 
to allow the user to make a definitive comparison between the file formats being tested.

## Section 2: netCDF4 Optimization
In theory, netCDF4 generally writes faster if all datasets are created before being written, compared to the case where
each dataset is written immediately after being created. Thereby, the loop structure is changed from single loop (each
dataset is written immediately after being created) to separate loop (all datasets are created before being written). In the
experiment, two plots are made to validate the optimization above.

## Section 3: Comparison with CSV 
Developed benchmarks to compare CSV file I/O performance with HDF5, netCDF4, and Zarr. The ”write all, read all” approach in the runner.py python file is used to eliminate any caching effect. In other words, ”write all, read all” means to finish writing the random data into datasets associated with all file formats (HDF5, netCDF4, zarr) before reading them. This helps avoid any caching effect when reading files. In terms of implementation details, dictionary and list in Python are applied. Specifically, one dictionary is created for every single I/Ooperation: create, write, open, read. These dictionaries are mapping each file format to its performance data list of the corresponding I/O operation. These data lists keep track of the performance measurements from all of repeated trials. In this experiment, the number of repeated trials is 5. Dictionaries for create, write, open, read benchmarks are utilized to store and transfer performance data to csv files later for plotting.

## Section 4: Large Scale Testing - Basic Comparison
Same setyp as small-scale testing, but with much larger data size configuration.

## Section 5: Scale Element Comparison - Basic Comparison
Developed benchmarks to generate plots in 4 different scale element comparison. In order to identify the performance trend or pattern with different scales of increasing number of elements, the scale element comparison section is added to this benchmark project. The number of elements is increasing in four different scales, whereas the number of datasets is fixed. The scale element comparison is applied to both basic comparison (comparison among HDF5, netCDF4, and zarr) and compression comparison (HDF5, netCDF4, zarr, and corresponding compressed versions). In terms of the implementaion details, various data structures like dictionary and list in
Python are applied. Basically, one single dictionary called database is created to map each individual file format to its data list, which stores the average time and
standard deviation of create, write, open, read performance. When it comes to matplotlib.pyplot plotting process, the performance data including average time and standard deviation will be retrieved by its file format and eventually visualize the performance comparison. 

## Section 6: Large Scale Testing - Compression Comparison
Developed benchmarks to test the Blosc_zstd compression effect on flle I/O performance among HDF5, netCDF4, and Zarr. In this benchmark project, the effect of compression on file common I/O operation performance is investigated. Specifically, blosc compression is used to compress HDF5, netCDF4, and Zarr files and the performance of compressed file formats is measured and compared with uncompressed versions of corresponding file formats. In terms of implementation details, compressed HDF5, compressed netCDF4, compressed zarr are treated as different individual data models to facilitate the process of developing code. A total of 6 csv files are created to keep track of common I/O operation performance to prepare for plotting. matplotlib.pyplot is utilized to visualize file I/O operation performance of HDF5, netCDF4, Zarr, and corresponding compressed versions of them on a single bar plot.

## Section 7: Scale Element Comparison - Compression Comparison
Scale element comparison in the context of Blosc_zstd compression. Refer to Section 5 for implementation details.   

## Section 8: Compound Datatype Comparison
Developed benchmarks to compare compound datatype HDF5 file I/O performance with CSV file format. Compared four different approaches of reading benchmark performance. 
The compound datatype in HDF5 is a similar data model to csv files. In this benchmark project, the performance of write/read operations are measured for both HDF5 compound datatype and csv files. Specifically, in the write benchmark for HDF5 compound datatype, the random data are written into one single compound dataset by properties; However, in the case of csv files, random data could be written either by columns or by rows. Accordingly, both writing approaches are considered and implemented respectively. To write random data by columns, the dataframe in pandas is utilized to populate data into columns. In order to write data by rows, on the other hand, the csv.writer in csv module is used to write data in a row-wise fashion. In the read benchmark for compound datatype, four different reading approaches are proposed and implemented respectively: read data by columns; read data by rows; read the entire dataset; read data by the first half of rows. All reading approaches are implemented by dataframe and df.iloc function in pandas library.

## extra Python files
### log scale conversion
`log_conversion` is a Python file that converts plots into log scale in y direction. This helps visualization when the performance difference between file formats is extremely large.
### write timer
`write_timing` is a Python file that measures the time of multiple code chunks in the write process and stores data to a folder of csv files. 
