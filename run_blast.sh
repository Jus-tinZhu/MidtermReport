#!/bin/bash
#SBATCH -t 0-00:30
#SBATCH --mem=16000
#SBATCH -c 8
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jxzhu@ualberta.ca

module load StdEnv/2020
module load gcc/9.3.0
module load blast+/2.12.0

blastn -outfmt "6" -num_threads 8 -export_search_strategy /home/justinz/scratch/Cooke/blast/search_strategy.txt -query /home/justinz/scratch/Cooke/blast/data/S031-32_clones_SAL_and_Y1H_blast.fasta -db /home/justinz/scratch/Cooke/blast/database/PG29-v5_BLASTdb -out /home/justinz/scratch/Cooke/blast/SAL_Y1H_ORFS_vs_PG29.tab 
