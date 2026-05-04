#!/bin/bash

# Simple Ping Sweeper
# Usage: ./ping_sweep.sh 192.168.1

if [ "$1" == "" ]
then
    echo "Usage: ./ping_sweep.sh [network]"
    echo "Example: ./ping_sweep.sh 192.168.1"
else
    echo "Scanning network $1.0/24..."
    for ip in `seq 1 254`; do
        ping -c 1 $1.$ip | grep "64 bytes" | cut -d " " -f 4 | tr -d ":" &
    done
    wait
    echo "Scan complete."
fi
