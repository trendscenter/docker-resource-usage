#!/bin/bash
# Logs docker stats to file with path provided by first argument

if [ $# -gt 0 ]
then
    while true; do docker stats --no-stream | tee -a $1; sleep 1; done
else
    echo "File path to save logs must be provided as first argument."
fi
