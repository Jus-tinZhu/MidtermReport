#!/bin/bash
#SBATCH -t 0-05:00
#SBATCH --mem=16000
#SBATCH -c 4
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jxzhu@ualberta.ca
"export OMP_NUM_THREADS=#SLURM_CPUS_PER_TASK"

module load StdEnv/2020
module load gcc/9.3.0
module load blast+/2.12.0

makeblastdb -blastdb_version 5 -dbtype nucl -in '/home/justinz/scratch/Cooke/blast/data/PG29-v5_1000plus.fa' -parse_seqids -hash_index -out 'PG29-v5_BLASTdb'
