#!/bin/bash
#SBATCH -c 16
#SBATCH --mem=24000
#SBATCH --time=05:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jxzhu@ualberta.ca
export OMP_NUM_THREADS=#SLURM_CPUS_PER_TASK

module load bowtie2/2.4.2

bowtie2 -f -a --sensitive-local --local -N 1 -t -p 16 -x Consolidated_PG29-v5 -U /home/justinz/scratch/Cooke/blast/data/S031-32_clones_SAL_and_Y1H_blast.fasta -S PG29-v5_S031-32_mapping.sam
