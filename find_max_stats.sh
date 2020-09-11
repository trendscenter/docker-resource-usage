#!/usr/bin/bash

filename=$1
container=$2

echo Maximum CPU used:
cat $filename | awk "{ if ($2 == $container) { print } }" | cut -d "," -f 3 | sort -nr | head -1

echo Maximum memory used:
cat $filename | awk "{ if ($2 == $container) { print } }" | cut -d "," -f 4 | cut -d "/" -f 1 | grep "GiB" | sort -r | head -1
