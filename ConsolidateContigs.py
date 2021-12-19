from Bio import SeqIO
from io import StringIO
import csv

def open_reference(target):
    reference = {} 
    for record in SeqIO.parse(target, 'fasta'):
        reference[record.id] = record.seq
    return reference

def open_list(target):
    with open(target, 'r') as file:
        reference = file.readlines()
    
    for i in range(len(reference)):
        reference[i] = reference[i].rstrip('\n')

    print(len(reference))
    print(reference)
    return reference

def consolidate_genome(genome, contigs):
    consolidated = {}
    for contig in contigs:
        consolidated[contig] = genome[contig]

    print(len(consolidated))
    return consolidated

def create_fasta(contigs, filename):  
    with open(filename, 'w') as file:
        for contig in contigs:
            file.write('>' + contig)
            file.write('\n')
            file.write(str(contigs[contig]))
            file.write('\n')

def main():
    genome_file = '/home/justinz/scratch/Cooke/blast/data/PG29-v5_1000plus.fa'   
    unique_contigs = '/home/justinz/scratch/Cooke/bowtie2/All_Unique_Contigs.txt'  
    filename = '/home/justinz/scratch/Cooke/bowtie2/ConsolidatedGenome.fasta'

    genome = open_reference(genome_file)
    condensed = open_list(unique_contigs)     
    consolidated = consolidate_genome(genome, condensed) 
    create_fasta(consolidated, filename)
     
if __name__ == "__main__":
    main()   
