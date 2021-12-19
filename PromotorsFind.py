from Bio import SeqIO
from io import StringIO
import csv
import pysam

def open_reference(target):
    reference = {} 
    for record in SeqIO.parse(target, 'fasta'):
        reference[record.id] = record.seq
    return reference

def open_bam(target):
    alignments = []
    bamfile = pysam.AlignmentFile(target, 'rb')

    for read in bamfile.fetch():
        temp = (read.reference_name, read.reference_start, read.reference_end, read.is_reverse) 
        alignments.append(temp)

    bamfile.close()
    return alignments

def extract_clusters(flat_cluster):
    dict_cluster = {}
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

def combine_reads_coords(reads):
    '''
    [0] = start
    [1] = end
    [2] = is reverse
    ''' 
    direction = reads[0][2]
    maxi = reads[0][1]
    mini = reads[0][0]
    
    for i in range(len(reads)):
        if reads[i][0] < mini:
            mini = reads[i][0]
        if reads[i][1] > maxi:
            maxi = reads[i][1]
        if reads[i][2] != direction:
            assert "something wrong with reads direction"

    return (mini, maxi, direction)

def reads_by_direction(alignment):
    direction = alignment[0][2]
    by_direction = []
    temp = []

    for i in range(len(alignment)): #group by direction
        if alignment[i][2] != direction:
            by_direction.append(temp)
            temp = []
            direction = alignment[i][2]
        
        temp.append(alignment[i])
        if i == len(alignment)-1:
            by_direction.append(temp)
    
    coords_dir = []
    for i in range(len(by_direction)):
        coords = combine_reads_coords(by_direction[i]) #get boundary coords
        coords_dir.append(coords)   
    
    return coords_dir

def make_bounds(dir_groups):# something wrong in here 
    boundaries = [] 
    length = len(dir_groups)
    print('\n')
    print(dir_groups)

    for i in range(length):
        coords = dir_groups[i]

        if coords[2] == False: # direction positive
            if i == 0: 
                left_bound = None # means alignment edge
                right_bound = coords[0]-1
            elif i > 0 : #either next group over or last group
                coords_prev = dir_groups[i-1]
                left_bound = coords_prev[1]+1
                right_bound = coords[0]-1
            else:
                assert "boundary issues"
            boundaries.append( (left_bound, right_bound, coords[2]) )

        elif coords[2] == True:  #something wrong in here
            if i == length-1:
                left_bound = coords[1]+1
                right_bound = None
            elif i < length-1:
                coords_next = dir_groups[i+1]
                left_bound = coords[1]+1
                right_bound = coords_next[0]-1
            else:
                assert "boundary issues"
            boundaries.append( (left_bound, right_bound, coords[2]) )
        
        else:
            assert "no bool for dir"
        print(boundaries)
    return boundaries

def cut_genome(contig_cuts, contig): #edge case catching
    cuts = {}
    '''
    info [0] = left coord
    info [1] = right coord
    info [2] = is_reverse, bool
    '''

    for info in contig_cuts:
        temp_list = list(info)

        if temp_list[0] == None: #edge case for bounds
            temp_list[0] = 0
        if temp_list[1] == None:
            temp_list[1] = len(contig)-1
        if (temp_list[1] - temp_list[0]) <= 0:
            assert " zero length contig"

        if temp_list[2] == False:
            cut_contig = contig[ temp_list[0]:(temp_list[1]+1) ]
        elif temp_list[2] == True:
            cut_contig = contig[ temp_list[0]:(temp_list[1]+1):-1] #have to reverse the sequence 
        else:
            assert "invalid direction while cutting"

        temp_tuple = tuple(temp_list)
        if temp_tuple not in contig_cuts: #add to dict
            cuts[temp_tuple] = cut_contig
        else:
            assert "duplicate gene cuts"
    
    return cuts

def create_fasta(promotors, out_file): 
    with open(out_file, 'w') as file:
        for contig in promotors:
            for cut in promotors[contig]:  #figuring dict syntax
                file.write('>' + str(contig) + " start" + str(cut[0]) + " end" + str(cut[1]) + " is_reverse" + str(cut[2]))
                file.write('\n')
                file.write(str(promotors[contig][cut]))
                file.write('\n')

def main():   
    bam_file = '/home/justinz/scratch/Cooke/bowtie2/data/PG29-v5_S031-32_mapping_sorted.bam'   
    genome_file = '/home/justinz/scratch/Cooke/bowtie2/data/ConsolidatedGenome.fasta'
    out_file = '/home/justinz/scratch/Cooke/hmmer_time/data/AlignmentsUpstream.fasta' 
    promotors = {}

    genome = open_reference(genome_file)
    raw_alignments = open_bam(bam_file)
    by_contig = extract_clusters(raw_alignments)

    for contig in by_contig: #something in this loop messing up the dicts?
        coords_dir_group = reads_by_direction(by_contig[contig]) 
        boundaries = make_bounds(coords_dir_group)
        contig_cuts = cut_genome(boundaries, genome[contig])
        promotors[contig] = contig_cuts #print?

    create_fasta(promotors, out_file) 

if __name__ == "__main__":
    main()   
