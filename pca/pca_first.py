import csv
import numpy as np
from sklearn.decomposition import PCA


        

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

def do_file(filename):
    print "============ %s ===========" % filename

    together, women, men = parse_file(filename)

    do_pcas(together, "TOGETHER")
    do_pcas(women, "WOMEN")
    do_pcas(men, "MEN")

    m_on_f = score_against(women, men)
    print m_on_f
    f_on_m = score_against(men, women)
    print f_on_m
    m_on_m = score_against(men, men)
    print m_on_m
    
    print
    print
    print


do_file("israeli_brain.csv")
do_file("VBM.csv")
# create f on f, m on m
# graph 3 components with colors
# create seperate groups using minimum/maximum data.
# understand what the components are


