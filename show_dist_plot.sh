#!/bin/bash
#SBATCH -t 0-00:20
#SBATCH --mem=8000
#SBATCH -c 4
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jxzhu@ualberta.ca
export OMP_NUM_THREADS=#SLURM_CPUS_PER_TASK

module load python/3.8.10
virtualenv --no-download ENV
source ENV/bin/activate

pip install matplotlib
pip install seaborn
pip install cloudpickle

python3 DistPlot.py
deactivate
