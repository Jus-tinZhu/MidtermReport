from Bio import SeqIO
from io import StringIO

def open_reference(target):
    reference = {} 
    for record in SeqIO.parse(target, 'fasta'):
        reference[record.id] = record.seq
    return reference

def split_fasta(in_fasta, split_number):
    if split_number <= len(in_fasta) and type(split_number) == int:
        assert "split number issues"

    splits = []
    for i in range(split_number):
        temp = {}
        counter = 0
        
        for entry in in_fasta:
            if counter%split_number == i:
                temp[entry] = in_fasta[entry]
            counter += 1
        splits.append(temp)

    return splits

def create_fasta(splits, filename):  
    for i in range(len(splits)):
        with open(filename + str(i) + ".fasta", 'w') as file:
            for contig in splits[i]:
                file.write('>' + contig)
                file.write('\n')
                file.write(str(splits[i][contig]))
                file.write('\n')

def main():
    in_file = '/home/justinz/scratch/Cooke/hmmer_time/data/AlignmentsUpstream.fasta'     
    out_file_base = '/home/justinz/scratch/Cooke/bowtie2/choppedAlignmentsUpstream/AlignmentsUpstream'
    split_number = 4

    in_fasta = open_reference(in_file)
    splits = split_fasta(in_fasta, split_number)     
    create_fasta(splits, out_file_base) 
     
if __name__ == "__main__":
    main()   
