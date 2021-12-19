#!/bin/bash
#SBATCH -t 0-00:30
#SBATCH --mem=16000
#SBATCH -c 8
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jxzhu@ualberta.ca

module load StdEnv/2020
module load hmmer/3.2.1

nhmmer /home/justinz/scratch/Cooke/hmmer_time/hmmer_profiles/hmmer_query.hmm /home/justinz/scratch/Cooke/hmmer_time/data/fixed_PLPR_verified.fasta 
