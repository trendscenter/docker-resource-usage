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
