from Bio import SeqIO

def open_reference(target):
    reference = {} 
    for record in SeqIO.parse(target, 'fasta'):
        reference[record.id] = record.seq
    return reference

def get_names(blast_output):
    cluster = []

    with open(blast_output, 'r') as file:
        reader = csv.reader(file, delimiter = '\t')
        for row in reader:
            temp = [row[0], row[1], row[8], row[9]]
            flat_cluster.append(temp)

    return cluster

def get_upstream(blast_results, genome, target_genes):
    upstream_bits = {}
    for target in target_genes:
        upstream = genome[target][ int(blast_results[2]-1) : int(blast_result[3]) ]
        upstream_bits[target] = upstream 

    return upstream_bits

def create_fasta(upstream_bits, hmmer_stash): #fix 
    name = str(key) + '.fasta'
    
    with open(hmmer_stash + name, 'w') as file:
        for value in values:
            file.write('>' + value)
            file.write('\n')
            file.write(str(genome[value]))
            file.write('\n')
       
def main():
    hmmer_stash = '/home/justinz/scratch/Cooke/blast/hmmer_profiles/'     
    genome_file = '/home/justinz/scratch/Cooke/blast/data/PG29-v5_1000plus.fa'   
    valid_genes = '/home/justinz/scratch/Cooke/blast/data/distance_validated_genes.fasta'
    blast_output = '/home/justinz/scratch/Cooke/blast/blast_result/SAL_Y1H_ORFS_vs_PG29.tab'  
    
    genome = open_reference(genome_file)
    target_genes = open_reference(valid_genes)
    blast_results = get_names(blast_output)     
    upstream_bits = get_upstream(blast_results, genome, target_genes)
    create_fasta(upstream_bits, hmmer_stash)

if __name__ == "__main__":
    main()
