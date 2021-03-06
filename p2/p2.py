#p2.py
from datetime import datetime
import numpy as np
from numpy import genfromtxt
import csv
from matplotlib import pyplot as plt
from scipy.sparse import csc_matrix
from scipy.sparse import csr_matrix
import scipy.spatial.distance


def main():
    #similarity_metrics3(l2)

    article_matrix = read_csvs3()
    reduced_matrix = dimensionality_reduction(d=25, mat=article_matrix)
    #part_1d2(article_matrix)
    part_1d2(reduced_matrix)

    #part_2b(reduced_matrix, article_matrix)



#Makes a scatter plot between article 3 and all other articles in both matricies
def part_2b(reduced_matrix, original_matrix):
    x_coords = []
    y_coords = []
    for i in range(1000):
        #Compute distance from article_3 to each of the matricies
        x_coords.append(cosine(original_matrix[2, :], original_matrix[i, :]))
        y_coords.append(cosine(reduced_matrix[2, :], reduced_matrix[i, :]))

    #Plot scatter of all the 
    plt.scatter(x_coords,y_coords)
    plt.show()


#takes our N x K matrix, and converts it to a (N x D) matrix by using a D x K matrix of random projections
def dimensionality_reduction(d=10, mat=None):
    n, k = mat.shape
    random_matrix = np.random.normal(0, 1, (d, k))
    new_matrix = np.zeros((n, d))
    for i in range(n):
        new_matrix[i , :] = (random_matrix.dot(mat[i , :]))
    new_matrix *= 1.0/(np.sqrt(d)) #From the lecture notes, not necessarily the handout
    return new_matrix


#Trying again with the giant matrix
def part_1d2(article_matrix):
    similarity_data = np.zeros((20,20))
    start = datetime.now()

    for i in range(20):
        for x in range(50):
            article_a = i*50 + x
            most_similar = -1
            winning_group = -1
            #print article_a
            start2 = datetime.now()

            for j in range(20):
                if(j != i):
                    for y in range(50):
                        article_b = j*50 + y
                        
                        similarity = cosine(article_matrix[article_a, :], article_matrix[article_b, :])
                        
                        if(similarity > most_similar):
                            most_similar = similarity
                            winning_group = j
            #At the end of the article, add similarity info
            similarity_data[i, winning_group] += 1
    print "This took : ", datetime.now()-start, " seconds"

    groups = get_group_names()
    plot_heatmat(similarity_data, groups, groups)


#Uses the giant matrix form and some hard coding, sorryyy
def similarity_metrics3(sim_metric):
    article_matrix = read_csvs3()
    similarity_data = np.zeros((20,20))
    start = datetime.now()
    for i in range(20):
        for x in range(50):
            article_a = i*50 + x
            print article_a
            for j in range(20):
                for y in range(50):
                    article_b = j*50 + y
                    similarity_data[i, j] += sim_metric(article_matrix[article_a, :], article_matrix[article_b, :])
    print "This took ", datetime.now() - start, " seconds"
    groups = get_group_names()
    #print datetime.now().time()
    similarity_data /= 1000
    plot_heatmat(similarity_data, groups, groups)
    #print similarity_data
    #print similarity_data / 1000



#Plots a heatmap given a numpy array of data and labels
#http://stackoverflow.com/questions/14391959/heatmap-in-matplotlib-with-pcolor
def plot_heatmat(data, row_labels, col_labels):
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(data, cmap=plt.cm.Blues, alpha=0.8)
    # put the major ticks at the middle of each cell
    ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)
    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    #More stuff from the stackoverflow...
    ax.set_xticklabels(row_labels, minor=False, rotation = 70)
    ax.set_yticklabels(col_labels, minor=False, rotation = 10)

    cbar = plt.colorbar(heatmap)

    cbar.ax.get_yaxis().set_ticks([])
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('Most Similar                                    Least Similar', rotation=270)

    plt.show()



def get_avg_similarity(a_articles, b_articles, words_in_articles, sim_metric):
    total_similarity = 0.0
    count = 0.0
    for article_a in a_articles:
        for article_b in b_articles:
            similarity = sim_metric(words_in_articles[article_a], words_in_articles[article_b])
            count += 1.0
            total_similarity += similarity
            #print similarity
            #raw_input("")
    return total_similarity/count


#Simple function that reads CSV of group names
def get_group_names():
    groups = []
    group_file = open('p2_dataset/groups.csv', 'rb')
    for line in group_file.readlines():
        groups.append(line.strip())
    return groups


#Use the numpy stuff, vectorized code, no loops
#into each of these functions, pass 2 vectors (np arrays)
def jaccard(x,y):
    return np.sum(np.minimum(x,y))/np.sum(np.maximum(x,y))

def l2(x,y):
    return -np.sqrt(np.sum((x - y)**2))

def cosine(x,y):
    return np.sum(x*y)/(np.sum(np.abs(x)) * np.sum(np.abs(y))) 




#numpy 1000 x 61100 matrix
def read_csvs3():
    data = genfromtxt('p2_dataset/data50.csv', delimiter=' ')
    matrix = np.zeros((1000,61100))
    counter = 0
    prev_article_id = 1
    for article_id, word_id, count in data:
        if(article_id != prev_article_id):
            counter += 1
        matrix[counter, word_id] = count
        prev_article_id = article_id
    return matrix



if __name__ == "__main__":
    main()


