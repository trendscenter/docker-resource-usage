"""
# Docker Resource Usage
Plots resource usage by a Docker container

## Usage
Before you start a Docker container, run this command in a Terminal window:

`while true; do docker stats --no-stream | tee -a stats.txt; sleep 1; done`

This command will create a file that looks like this:

CONTAINER ID        NAME                    CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS     
367f4a14014d        objective_banach        149.33%             2.014GiB / 15.65GiB   12.87%              60.8kB / 11.5kB     195MB / 0B          23
cb5fe1ddbcc2        reminders_pgbackups_1   0.00%               1.551MiB / 15.65GiB   0.01%               2kB / 0B            20MB / 0B           6
CONTAINER ID        NAME                    CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
367f4a14014d        objective_banach        113.53%             2.023GiB / 15.65GiB   12.93%              60.8kB / 11.5kB     195MB / 0B          23
cb5fe1ddbcc2        reminders_pgbackups_1   0.00%               1.551MiB / 15.65GiB   0.01%               2kB / 0B            20MB / 0B           6
...

It will keep repeating like that until the command is canceled.

This script takes that file as input and produces plots of the resource usage contained therein.

`python plot_usage.py /path/to/file`

It will create cleaned data files and plots in a local `results` folder.

## TODO
Add MEM %, NET I/O, BLOCK I/O

"""

import os
import sys
from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt
import logging


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Constants
MB = 'MiB'
GB = 'GiB'
HDR_CHECK_STR = 'CONTAINER'
CONTAINER_HDR = 'CONTAINERID'
NAME_HDR = 'NAME'
MEM_HDR = 'MEMUSAGE/LIMIT'
NAME_HDR = 'NAME'
MEM_USAGE_HDR = 'MEM USAGE (' + MB + ')'
MEM_LIMIT_HDR = 'MEM LIMIT (' + MB + ')'
CPU_HDR = 'CPU%'
RESULTS_FOLDER = 'results'
CLEAN_FNAME_SUFFIX = '_clean'


def read_data(file_path):
    """ Reads data from file """
    with open(file_path, 'r') as the_file:
        lines = the_file.readlines()
    return lines


def clean_data(dirty_data):
    """ Cleans data and returns it as a pandas DataFrame """
    single_header = remove_extra_headers(dirty_data)
    df = read_list_of_strings_to_df(single_header)
    log.debug('Single Header DF')
    log.debug(df)
    df = parse_mem_usage(df)
    df[CPU_HDR] = df[CPU_HDR].apply(cpu_str2num)
    return df


def read_list_of_strings_to_df(list_of_strings):
    return pd.read_csv(StringIO(''.join(list_of_strings)), sep='\s+')


def remove_extra_headers(dirty_data):
    """ Removes extra header lines from list of strings """
    cleaned_data = list()
    header = despace(dirty_data[0])
    cleaned_data.append(header)
    for line in dirty_data:
        if HDR_CHECK_STR not in line:
            cleaned_data.append(despace(line))
    return cleaned_data


def despace(line):
    """ 
    Removes single spaces from column names in string.
    e.g., "CONTAINER ID   NAME" -> "CONTAINERID    NAME"    
    This is done so that pandas can read space-delimited files without 
    separating headers with names containing spaces.
    """
    parts = line.split(' ')
    parts = [p if p else ' ' for p in parts]
    return ''.join(parts)


def parse_mem_usage(df):
    """ Parses memory usage column and splits it into two columns.
    Memory usage column will have strings of format 'x.xxxGiB/y.yyyGIB',
    where x.xxx is the memory usage, and y.yyy is the memory limit.  
    """
    mem_usage = df[MEM_HDR].str.split('/', n=1, expand=True)
    log.debug('Mem usage: ')
    log.debug(mem_usage)
    df[MEM_USAGE_HDR] = mem_usage[0].apply(mem_str2num)
    df[MEM_LIMIT_HDR] = mem_usage[1].apply(mem_str2num)
    return df


def mem_str2num(mem_str):
    """
    Returns memory string as numeric value in MB.
    Expects form of '1.234MiB' or '1.234GiB'
    """
    val = float(mem_str[:-3])
    units = mem_str[-3:]
    if units == GB:
        val *= 1000
    return val
        
    
def cpu_str2num(cpu_str):
    """ 
    Parses a string containing CPU % utilization and returns a float.
    e.g., "14.5%" -> 14.5
    """
    return float(cpu_str[:-1])


def plot_data(data, results_path):
    """ Plots data and saves plots to file """
    for name in data[NAME_HDR].unique():
        container_data = data[data[NAME_HDR] == name]
        
        f = plt.figure()
        ax = plt.plot(container_data[MEM_USAGE_HDR])
        plt.xlabel('Seconds')
        plt.ylabel(MB)
        plt.title('Memory consumption for ' + name)
        save_path = os.path.join(results_path, name + '_memory.png')
        plt.savefig(save_path)
        log.info('Saved memory consumption for ' + name + ' to ' + save_path)
        plt.close()

        f = plt.figure()
        ax = plt.plot(container_data[CPU_HDR])
        plt.xlabel('Seconds')
        plt.ylabel(CPU_HDR)
        plt.title('CPU Utilization for ' + name)
        save_path = os.path.join(results_path, name + '_cpu.png')
        plt.savefig(save_path)
        log.info('Saved CPU utilization for ' + name + ' to ' + save_path)
        plt.close()


def create_results_path():
    """ Creates path to save results """
    results_path = os.path.join(os.getcwd(), RESULTS_FOLDER)
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    return results_path


def save_cleaned_data(cleaned_data, file_path, results_path):
    """ Saves cleaned data to file """
    file_name = os.path.basename(file_path)
    fname, ext = os.path.splitext(file_name)
    cleaned_file_name = fname + CLEAN_FNAME_SUFFIX + ext
    cleaned_results_path = os.path.join(results_path, cleaned_file_name)
    cleaned_data.to_csv(cleaned_results_path, index=False)
    log.info('Saved cleaned data to ' + cleaned_results_path)


def main(file_path):
    raw_data = read_data(file_path)
    cleaned_data = clean_data(raw_data)
    results_path = create_results_path()    
    save_cleaned_data(cleaned_data, file_path, results_path)
    plot_data(cleaned_data, results_path)


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except IndexError as e:
        log.error('You must provide path to data as first argument')
        
