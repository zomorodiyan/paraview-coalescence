#!/bin/bash

# Bash script to run LIGGGHTS with 18 MPI processes
# Usage: ./run_liggghts.sh

mpirun --oversubscribe -n 18 lmp_auto < in.256um_box
