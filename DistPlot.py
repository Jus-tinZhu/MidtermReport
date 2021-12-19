import cloudpickle
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as stat

def get_file():
    with open ('/home/justinz/scratch/Cooke/blast/data/ClusterNumbersCutSeq', 'rb') as file: #get file name
        source_dict = cloudpickle.load(file)
    return source_dict

def raw_dist(data):
    mean = stat.mean(data)
    stdev = stat.stdev(data)

    median = stat.median(data)
    quantiles = stat.quantiles(data, n=10)
    quantiles.pop(4)

    sns.displot(data, bins=30) 
   
    plt.axvline(mean, color='r')
    plt.axvline(mean-stdev, color = 'r')
    plt.axvline(mean+stdev, color = 'r')

    plt.axvline(median, color='m')
    for number in quantiles:
        plt.axvline(number, color='g')

    plt.savefig('/home/justinz/scratch/Cooke/blast/data/distance_plot_cutseq.png')

    print('mean: ' + str(mean))
    print('stdev: ' + str(stdev))
    print('median: ' + str(median))
    print('quantiles excluding median: ' + str(quantiles))
    
def main():
    source_dict = get_file()
    
    raw_data = []
    for value in source_dict.values():
        raw_data.extend(value)

    raw_dist(raw_data)

if __name__ == "__main__":
    main()
