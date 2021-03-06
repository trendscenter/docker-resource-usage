# Docker Resource Usage
Plots resource usage by a Docker container

## Usage
Before you start a Docker container, run the included script in a Terminal window on Mac OS to log docker stats to a file:

`$ ./log_docker_stats.sh /path/to/file`

where `/path/to/file` is the path to the file you want to save the data to. Credit to this [post](https://github.com/moby/moby/issues/22618) for that command. Once the process is finished, hit `ctrl+c` to stop the recording.

This command will create a file that looks like this:

CONTAINER ID        NAME                    CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS     
367f4a14014d        objective_banach        149.33%             2.014GiB / 15.65GiB   12.87%              60.8kB / 11.5kB     195MB / 0B          23
cb5fe1ddbcc2        reminders_pgbackups_1   0.00%               1.551MiB / 15.65GiB   0.01%               2kB / 0B            20MB / 0B           6
CONTAINER ID        NAME                    CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
367f4a14014d        objective_banach        113.53%             2.023GiB / 15.65GiB   12.93%              60.8kB / 11.5kB     195MB / 0B          23
cb5fe1ddbcc2        reminders_pgbackups_1   0.00%               1.551MiB / 15.65GiB   0.01%               2kB / 0B            20MB / 0B           6
...

The file will continue like that until the command is canceled.

This script takes that file as input and produces plots of the resource usage.

`python plot_usage.py /path/to/file`

This script will create cleaned data files and plots and save them in a local `results` folder.


## TODO
- Add MEM %, NET I/O, BLOCK I/O
- Write a script that includes recording, parsing, and plotting of docker stats
- Add timestamps to logs
