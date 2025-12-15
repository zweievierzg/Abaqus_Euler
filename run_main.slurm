#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=08:00:00
#SBATCH --mem-per-cpu=4000
#SBATCH --tmp=50g

module load stack/2024-06 intel-oneapi-compilers/2023.2.0 abaqus/2023 libjpeg-turbo/3.0.0



# abaqus python main.py
abaqus cae noGUI=main.py

