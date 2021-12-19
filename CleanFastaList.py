from Bio import SeqIO

def open_reference(target):
    reference = {} 
    for record in SeqIO.parse(target, 'fasta'):
        reference[record.id] = record.seq
    return reference

def create_fasta(promotors, out_file): 
    with open(out_file, 'w') as file:
        for seq in promotors:
            file.write('>' + seq)
            file.write('\n')
            file.write(str(promotors[seq]))
            file.write('\n')

def main():   
    in_file = '/home/justinz/scratch/Cooke/hmmer_time/data/PLPR_verified.fasta'   
    out_file = '/home/justinz/scratch/Cooke/hmmer_time/data/fixed_PLPR_verified.fasta' 

    temp = open_reference(in_file) 
    create_fasta(temp, out_file)
    
if __name__ == "__main__":
    main() 
