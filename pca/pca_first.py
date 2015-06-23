import csv
import numpy as np
from sklearn.decomposition import PCA

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random


def draw(men, women, filename):
    fig = plt.figure(filename)
    ax = fig.add_subplot(111, projection='3d')
    for man_x,man_y,man_z in men:
        ax.scatter(man_x, man_y, man_z, c="g", marker="^")
    for woman_x,woman_y,woman_z in women:
        ax.scatter(woman_x, woman_y, woman_z, c="r", marker="o")
        


def do_draw(men, women, filename):
    pca = PCA(3)
    together = []
    together.extend(men)
    together.extend(women)
    pca.fit(together)
    draw(pca.transform(men), pca.transform(women), filename)

def do_pca(pca, data):
    pca.fit(data)
    print(pca.explained_variance_ratio_)
    print(pca.n_components_)
    
def do_pcas(data, label):
    print ("======= START %s %d ======" % (label, len(data)))
    #mle_pca = PCA("mle")
    #do_pca(mle_pca, data)
    half_pca = PCA(0.75)
    do_pca(half_pca, data)
    print ("======= END %s ==========" % label)
    return half_pca
    

def score_against(base, other):
    pca = PCA(0.75)
    scores = (pca.fit(base).score_samples(other))
    return min(scores), max(scores)


def parse_file(filename):
    women = []
    men = []
    r = csv.reader(file(filename, "rU"))
    r.next()
    for line in r:
        sex = line[1]
        try:
            data = [float(x) for x in line[2:]]
        except:
            continue
        if sex == "2":
            women.append(data)
        else:
            men.append(data)
    
    together = np.array(women + men)
    women_data = np.array(women)
    men_data = np.array(men)
    return together, women, men


def random_data(filename, together):
    data_high = []
    data_low = []
    for element in np.transpose(together):
        so = sorted(element)
        high = so[:len(so)/2]
        low = so[len(so)/2:]
        random.shuffle(high)
        random.shuffle(low)
        data_high.append(high)
        data_low.append(low)

    data_high = np.transpose(data_high)
    data_low = np.transpose(data_low)

    print "RANDOM"
    print(score_against(data_high, data_low))
    print(score_against(data_low, data_high))
    do_draw(data_high, data_low, filename + " - RANDOM")
    
    
    


def do_file(filename):
    print "============ %s ===========" % filename

    together, women, men = parse_file(filename)

    do_pcas(together, "TOGETHER")
    do_pcas(women, "WOMEN")
    do_pcas(men, "MEN")

    do_draw(men, women, filename)

    random_data(filename, together)
    

    m_on_f = score_against(women, men)
    print m_on_f
    f_on_m = score_against(men, women)
    print f_on_m
    m_on_m = score_against(men, men)
    print m_on_m
    f_on_f = score_against(women, women)
    print f_on_f
    
    print
    print
    print


do_file("israeli_brain.csv")
do_file("VBM.csv")
plt.show()
# create f on f, m on m
# graph 3 components with colors
# create seperate groups using minimum/maximum data.
# understand what the components are

# PCA!
# understand what the score_samples calculates
# check the number of men vs women that fit certain thresholds of scoring.
# check jonathan's svd
# read about GMM - and some basic runs.   



