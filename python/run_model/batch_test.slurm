#!/bin/sh


#SBATCH --job-name="EU_test"
#SBATCH --qos=short
#SBATCH --account=vewa
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=20
#SBATCH --partition=compute

export OMP_NUM_THREADS=20
srun --exclusive --cpu-bind=cores python3 test.py