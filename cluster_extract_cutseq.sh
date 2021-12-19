#!/bin/bash
#SBATCH -t 0-12:00
#SBATCH --mem=128000
#SBATCH --cpus-per-task=8
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jxzhu@ualberta.ca

module load python/3.8.10 #don't load versions, messes with imports/3.8.10
virtualenv --no-download ENV
source ENV/bin/activate

#don't do this it does bad things, pip install --no-index --upgrade pip
pip install biopython
pip install cloudpickle

module load nixpkgs/16.09
module load gcc/7.3.0
module load muscle/3.8.31

python3 ExtractCluster_CutSeq.py
deactivate
