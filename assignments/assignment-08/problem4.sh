#!/bin/bash

# Obfuscate fib-time.c with Tigress
tigress ...
   ...\
    --Transform=AddOpaque ... \
       --AddOpaqueKind= ... \
    --Transform=Measure= ... \
    ... \
    fib-time.c --out=fib-time-obf.c

# Compile 
gcc  fib-time-obf.c -o fib-time-obf.exe

# Run, printing the execution time
fib-time-obf.exe
