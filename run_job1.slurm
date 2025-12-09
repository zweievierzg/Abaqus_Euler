#!/bin/bash
#SBATCH --job-name=abaqus_job1
#SBATCH --output=abaqus_job1.out
#SBATCH --error=abaqus_job1.err
#SBATCH --ntasks=4
#SBATCH --time=02:00:00
#SBATCH --mem=4G

# Load the Abaqus module (adjust version as needed)
module load abaqus/2023

# Run the Abaqus job
abaqus job=Job-1 input=Job-1.inp cpus=$SLURM_NTASKS interactive
