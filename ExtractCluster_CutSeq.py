from Bio import SeqIO
from Bio import AlignIO
from Bio.Align.Applications import MuscleCommandline
from Bio.Phylo.TreeConstruction import DistanceCalculator
from io import StringIO
from itertools import repeat

import multiprocessing as mp
import os
import cloudpickle
import csv

def open_reference(target):
    reference = {} 
    for record in SeqIO.parse(target, 'fasta'):
        reference[record.id] = record.seq
    return reference

def extract_clusters(blast_result):
    flat_cluster = []
    dict_cluster = {}
    
    with open(blast_result, 'r') as file:
        reader = csv.reader(file, delimiter = '\t')
        for row in reader:
            temp = (row[0], row[1], row[8], row[9])
            flat_cluster.append(temp)

    current = flat_cluster[0][0]
    dict_list = []
    last = len(flat_cluster)-1

    for i in range(len(flat_cluster)): #does work?
        if flat_cluster[i][0] != current:
            dict_cluster[current] = dict_list
            current = flat_cluster[i][0]
            dict_list = []
        dict_list.append(flat_cluster[i][1:])

        if i == last:
            dict_cluster[current] = dict_list

    return dict_cluster

def get_upstream(target_genes, genome):
    upstream_bits = {}
    for target in target_genes:
        upstream = genome[ target[0] ][ int(target[1])-1 : int(target[2]) ]
        upstream_bits[ target[0] ] = upstream 

    return upstream_bits

def create_fasta(key, seqs, arabid_ref, fasta_stash): 
    name = str(key) + 'CutSeq.fasta'
    
    with open(fasta_stash + name, 'w') as file:
        for seq in seqs:
            file.write('>' + seq)
            file.write('\n')
            file.write(str(seqs[seq]))
            file.write('\n')
        
        for ref in arabid_ref:
            file.write('>' + str(ref))
            file.write('\n')
            file.write(str(arabid_ref[ref]))
            file.write('\n')
     
    return name

def get_stat(raw): #list within lists 
    flattened = []
    for i in range(len(raw)-1): 
        for j in range(i+1, len(raw)):
            flattened.append(raw[i][j]) 
    return flattened

def run_align_dist(filename):
    fasta_stash = '/home/justinz/scratch/Cooke/blast/fastadump/'
    align_dump = '/home/justinz/scratch/Cooke/blast/alignmentdump/' 
    values = {}
 
    try:
        cline = MuscleCommandline(input=( fasta_stash+filename ), out=( align_dump + filename[:-5] + 'aln' )) 
        cline()
    
        alignment = AlignIO.read(open(align_dump + filename[:-5] + 'aln'), 'fasta')
        calculator = DistanceCalculator('identity') 
        numbers = calculator.get_distance(alignment)    
        flattened = get_stat(list(numbers)) 
        values[ filename[:-6] ] = flattened         
        
        print(filename)
        print(numbers)

    except Exception as error:
        print(error)

    return values 

def main():
    fasta_stash = '/home/justinz/scratch/Cooke/blast/fastadump/'    
    align_dump = '/home/justinz/scratch/Cooke/blast/alignmentdump/'
    genome_file = '/home/justinz/scratch/Cooke/blast/data/PG29-v5_1000plus.fa'   
    arabid_file = '/home/justinz/scratch/Cooke/blast/data/Arabidopsis_SAL_Reference.txt'
    blast_result = '/home/justinz/scratch/Cooke/blast/blast_result/SAL_Y1H_ORFS_vs_PG29.tab'  
    
    genome = open_reference(genome_file)
    reference = open_reference(arabid_file)
    clusters = extract_clusters(blast_result)     
    
    filenames = []
    for cluster in clusters:
        upstream_bits = get_upstream(clusters[cluster], genome)
        filename = create_fasta(cluster, upstream_bits, reference, fasta_stash)
        filenames.append(filename)
    
    pool = mp.Pool(8)
    all_values = pool.map(run_align_dist, filenames) #map needs one iterable and only one
    pool.close()
    pool.join()

    super_dict = {}
    for entry in all_values:
        super_dict.update(entry)
    
    with open('/home/justinz/scratch/Cooke/blast/data/ClusterNumbersCutSeq', 'wb') as handle:
        cloudpickle.dump(super_dict, handle) 
    
if __name__ == "__main__":
    main()   
