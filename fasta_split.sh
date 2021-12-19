#!/bin/bash
#SBATCH -t 0-00:10
#SBATCH --mem=8000
#SBATCH --cpus-per-task=4
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jxzhu@ualberta.ca

module load python/3.8.10 #don't load versions, messes with imports/3.8.10
virtualenv --no-download ENV
source ENV/bin/activate

#don't do this it does bad things, pip install --no-index --upgrade pip
pip install biopython

python3 SplitFastaFile.py
deactivate
