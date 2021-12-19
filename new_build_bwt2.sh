#!/bin/bash
#SBATCH --account=def-jek4
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=8190mb
#SBATCH --time=04:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jxzhu@ualberta.ca

module load bowtie2/2.4.2

bowtie2-build -f --threads 16 /home/justinz/scratch/Cooke/bowtie2/ConsolidatedGenome.fasta Consolidated_PG29-v5
