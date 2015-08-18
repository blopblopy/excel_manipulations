import csv
from math import ceil
import random

import numpy as np
from sklearn import mixture
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from scipy.stats import pointbiserialr
from scipy.stats import ttest_ind

def ttest(A, B):
    return ttest_ind(A, B, equal_var=False)

def pca_bin_corr(group1, group2):
    pca = PCA(3)
    together = np.concatenate((group1, group2))
    pca.fit(together)
    g1 = pca.transform(group1)
    g2 = pca.transform(group2)
    for i in range(3):
        print bin_corr(g1[:,i], g2[:,i])
    print
    

def bin_corr(group1, group2):
    bin = [0]* len(group1) + [1] *len(group2)
    return pointbiserialr(bin, np.concatenate((group1, group2)))

class BarData(object):
    def __init__(self, x, y, label):
        self.label = label
        self.x = x
        self.y = y


class BootResult(object):
    def __init__(self, w_w, w_m, m_m, m_w):
        self.w_w = w_w
        self.w_m = w_m
        self.m_m = m_m
        self.m_w = m_w

    def __str__(self):
        return "BootResult(%s, %s, %s, %s)" % (self.w_w, self.w_m, self.m_m, self.m_w)

class Plot(object):
    def __init__(self, label, max_per_row=1):
        self.figure = None
        self.label = label
        self.count = 0
        self.max_per_row = max_per_row

    def _init(self):
        if self.figure is None:
            self.figure = plt.figure(self.label)

    def add_subplot(self, **kwargs):
        self._init()
        self.count += 1
        dim = int(ceil(float(self.count)/self.max_per_row))
        # change former graphs
        for index, ax in enumerate(self.figure.axes, start=1):
            ax.change_geometry(dim, self.max_per_row, index)

        return self.figure.add_subplot(dim, self.max_per_row, self.count, **kwargs)


from collections import defaultdict
def parse_origin_file(filename):
    origins = defaultdict(lambda:{'f':[], 'm':[]})
    r = csv.reader(open(filename, "rU"))
    # remove header
    r.next()
    limit = 5
    for line in r:
        subject, sex, handedness, age, origin = [x.strip().lower() for x in line[:limit]]
        try:
            data = [float(x) for x in line[limit:]]
        except:
            continue
        origins[origin][sex].append(data)

    res = {}
    for origin, data in origins.iteritems():
        tmp = FileData(origin)
        tmp.create_data(data['f'], data['m'])
        res[origin] = tmp
    return res


class FileData(object):
    WOMEN_SEX = "2"
    def __init__(self, filename):
        self.filename = filename
        self.figure = Plot(filename)
        self.bar_figure = Plot(filename + "-bars", 2)
        self.boot_figure = Plot(filename + "-bootstraping", 2)

    def parse_file(self):
        women = []
        men = []
        r = csv.reader(open(self.filename, "rU"))
        # remove header
        r.next()
        for line in r:
            sex = line[1]
            try:
                data = [float(x) for x in line[2:]]
            except:
                continue
            if sex == FileData.WOMEN_SEX:
                women.append(data)
            else:
                men.append(data)
        self.create_data(women, men)

    def create_data(self, women, men):
        random.shuffle(women)
        random.shuffle(men)
        self.together = np.array(women + men)
        self.women = np.array(women)
        self.men = np.array(men)

    def do_pca(self, pca, data):
        pca.fit(data)
        print(pca.explained_variance_ratio_)
        print(pca.n_components_)

    def do_pcas(self, data, label):
        print ("======= START %s %d ======" % (label, len(data)))
        #mle_pca = PCA("mle")
        #do_pca(mle_pca, data)
        half_pca = PCA(0.75)
        self.do_pca(half_pca, data)
        print ("======= END %s ==========" % label)
        return half_pca

    def all_pcas(self):
        print "============ %s ===========" % self.filename
        self.do_pcas(self.together, "TOGETHER")
        self.do_pcas(self.women, "WOMEN")
        self.do_pcas(self.men, "MEN")

    def whiten_pca(self):
        whiten = PCA(0.75, whiten=True)
        self.do_pca(whiten, self.together)
        

    def pca3(self, together, men, women):
        pca = PCA(3)
        pca.fit(together)
        #print(pca.explained_variance_ratio_)
        #print(pca.mean_)
        #print(pca.components_)
        return pca.transform(men), pca.transform(women)

    def draw_3d(self):
        men, women = self.pca3(self.together, self.men, self.women)
        self.draw(men, women, "3D view")

    def draw_general_3d(self, men, women, label):
        together = []
        together.extend(men)
        together.extend(women)
        men3, women3 = self.pca3(together, men, women)
        self.draw(men3, women3, label)

    def draw(self, men, women, label):
#        ax = self.figure.add_subplot(projection='3d')
        bx = self.figure.add_subplot()

#        ax.set_title(label)
        bx.set_title(label + "-2d")
        for man_x,man_y,man_z in men:
#            ax.scatter(man_x, man_y, man_z, c="g", marker="^")
            bx.scatter(man_x, man_y, c="g", marker="^")
        for woman_x,woman_y,woman_z in women:
#            ax.scatter(woman_x, woman_y, woman_z, c="r", marker="o")
            bx.scatter(woman_x, woman_y, c="r", marker="o")


    def random_label(self):
        together = sorted(self.together, key=lambda x:random.random)
        men, women = self.pca3(self.together, together[::2], together[1::2])
        self.draw(men, women, "random label")

    def random_data(self):
        data_high = []
        data_low = []
        for element in np.transpose(self.together):
            so = sorted(element)
            high = so[:len(so)/2]
            low = so[len(so)/2:]
            random.shuffle(high)
            random.shuffle(low)
            data_high.append(high)
            data_low.append(low)

        data_high = np.transpose(data_high)
        data_low = np.transpose(data_low)

        self.draw_general_3d(data_high, data_low, "3D sorted RANDOM")

    def score_against(self, base, other):
        pca = PCA(0.75)
        scores = pca.fit(base).score_samples(other)
        return scores

    def score_against_avg(self, base, other):
        pca = PCA(0.75)
        return pca.fit(base).score(other)
        
    def bucketize(self, data, step = 10):
        from collections import OrderedDict
        from itertools import groupby
        data = sorted(data)
        data_len = float(len(data))/100
        d = OrderedDict(
           (x, len(list(g))/data_len) for x, g in groupby(data, lambda x: int(x/step)*step))
        return d.keys(), d.values()


    def bar_data(self, first, second, label):
        data = self.score_against(first, second)
        x, y = self.bucketize(data)
        return BarData(x, y, label)


    def draw_bar(self, xlim, ylim, bar_data):
        ax = self.bar_figure.add_subplot()
        ax.set_title(bar_data.label)
        ax.bar(bar_data.x, bar_data.y)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

    def draw_bars(self):
        datum = [
        self.bar_data(self.men, self.women, "women scored on men"),
        self.bar_data(self.men, self.men, "men scored on men"),

        self.bar_data(self.women, self.men, "men scored on women"),
        self.bar_data(self.women, self.women, "women scored on women")
        ]
        lower, upper = 190, 260
        
        
        max_x = [min(int(x) for data in datum for x in data.x)-10, max(int(x) for data in datum for x in data.x)+10]
        max_y = [0, max(int(y) for data in datum for y in data.y)*1.1]
        #print max_x, max_y
        for data in datum:
            self.draw_bar(max_x, max_y, data)
            print "###", self.filename, data.label, sum(y for x,y in zip(data.x, data.y) if not(lower <= x <= upper))

        

    def do_gmm(self):
        men_gmm = mixture.GMM(n_components=3, covariance_type="full")
        men_gmm.fit(self.men)
        print men_gmm.score(self.women)

    def do_svc(self):
        svc = SVC()
        men_train, men_test = np.array_split(self.men, [0.75*len(self.men)])
        women_train, women_test = np.array_split(self.women, [0.75*len(self.women)])
        svc.fit(
            np.concatenate((men_train, women_train)
                ),
            np.concatenate(
                [[1]*len(men_train), [2]*len(women_train)]
                )
            )
        print svc
        print svc.predict(women_test)
        print svc.predict(men_test)
        print svc.predict(men_train), len(men_train)
        print svc.predict(women_train), len(women_train)


    def bootstrap(self, runs = 30):
        self.plot_data(runs, self.bootstrap_once, "bootstrap")


    def plot_data(self, runs, random_data, label):
        actual = self.do_scoring(self.women, self.men)
        bootstraps = [random_data() for i in xrange(runs)]
        data = np.matrix([[boot.w_m, boot.m_w] for boot in bootstraps])
        plot = self.boot_figure.add_subplot()
        plot.set_title("%s - inter sex" % label)
        plot.set_xlabel("men on women")
        plot.set_ylabel("women on men")

        plot.scatter(data[:,0], data[:,1], color='b', marker='p')
        plot.scatter([actual.w_m], [actual.m_w], color='r', marker='*')


        data2 = np.matrix([[boot.w_w, boot.m_m] for boot in bootstraps])
        plot2 = self.boot_figure.add_subplot()
        plot2.set_title("%s - inner sex" % label)
        plot2.set_xlabel("women on women")
        plot2.set_ylabel("men on men")

        plot2.scatter(data2[:,0], data2[:,1], color='b', marker='p')
        plot2.scatter([actual.w_w], [actual.m_m], color='r', marker='*')
        
        
    def do_scoring(self, boot_women, boot_men):
        return BootResult(self.score_against_avg(boot_women, boot_women),
                          self.score_against_avg(boot_women, boot_men),
                          self.score_against_avg(boot_men, boot_men),
                          self.score_against_avg(boot_men, boot_women)
                          )

    def bootstrap_once(self):
        boot_women, boot_men = self.create_boot_data()
        return self.do_scoring(boot_women, boot_men)

    def create_boot_data(self):
        rows, cols = shape = self.together.shape
        data = np.zeros(shape=shape)
        for col in xrange(cols):
            data[:, col] = np.random.choice(self.together[:, col], size=rows)
        boot_women, boot_men = np.array_split(data, [len(self.women)])
        return boot_women, boot_men

    def pca_boot_data(self):
        boot_women, boot_men = self.create_boot_data()
        self.draw_general_3d(boot_women, boot_men, "booted data")
    

    def create_relabel(self):
        data = np.random.permutation(self.together)
        boot_women, boot_men = np.array_split(data, [len(self.women)])
        return boot_women, boot_men

    def relabel_once(self):
        boot_women, boot_men = self.create_relabel()
        return self.do_scoring(boot_women, boot_men)
        
    def relabel(self, runs=100):
        self.plot_data(runs, self.relabel_once, "relabel")

    def pca_relabel(self):
        boot_women, boot_men = self.create_relabel()
        self.draw_general_3d(boot_women, boot_men, "relabel data")

    def sex_pca_correlation(self):
        pca = PCA(10)
        pca.fit(self.women) #together)
        men = pca.transform(self.men)
        women = pca.transform(self.women)
        for index in xrange(3):
            print "index", index
            print bin_corr(men[:,index], women[:,index])
        print
        svc = SVC()
        men_test, men_train = np.array_split(men, [0.25*len(self.men)])
        women_test, women_train = np.array_split(women, [0.25*len(self.women)])
        svc.fit(
            np.concatenate((men_train, women_train)
                ),
            np.concatenate(
                [[0]*len(men_train), [1]*len(women_train)]
                )
            )
        print svc
        print svc.predict(women_test), len(women_test), sum(svc.predict(women_test))
        print svc.predict(men_test), len(men_test), sum(svc.predict(men_test))
        print svc.predict(women_train), len(women_train), sum(svc.predict(women_train))
        print svc.predict(men_train), len(men_train), sum(svc.predict(men_train))

    
    def first_index_plot(self):
        pca = PCA(1)
        pca.fit(self.together)
        men = pca.transform(self.men)
        women = pca.transform(self.women)
        total = []
        for man in men:
            total.append((man, dict(c="g", marker="^")))
        for woman in women:
            total.append((woman, dict(c="r", marker="v")))

        total.sort()
            
        ax = self.figure.add_subplot()
        for index, (y, props) in enumerate(total):
            ax.scatter([50*index],[y], lw=0.0, **props)
        ax.set_xlim([-100,len(total)*50+100])        

        
    def half_and_half(self):
        men_1, men_2 = np.array_split(self.men, [0.5*len(self.men)])
        women_1, women_2 = np.array_split(self.women, [0.5*len(self.women)])
        mm = self.bar_data(men_1, men_2, "inner men vs men")
        ww = self.bar_data(women_1, women_2, "inner women vs women")
        self.draw_bar([0, 250], [0, 35], mm)
        self.draw_bar([0, 250], [0, 35], ww)


        


def do_file(filename):
    f = FileData(filename)
    f.parse_file()
#    f.all_pcas()
#    f.whiten_pca()
#    f.draw_3d()
#    f.random_data()
#    f.random_label()
#    f.draw_bars()
#    f.do_gmm()
#    f.do_svc()
#    f.bootstrap()
#    f.pca_boot_data()
#    f.relabel()
#    f.pca_relabel()
#    f.sex_pca_correlation()
#    f.first_index_plot()
#    f.half_and_half()
    return f


israeli = do_file("israeli_brain.csv")
vbm = do_file("VBM.csv")
#israeli.half_and_half()
#vbm.half_and_half()
israeli.draw_bars()
#vbm.draw_bars()
#vbm.draw_bar([0,250], [0,35], vbm.bar_data(vbm.men, israeli.men, "men - israeli on vbm"))
#vbm.draw_bar([0,250], [0,35], vbm.bar_data(vbm.women, israeli.women, "women - israeli on vbm"))


#israeli.draw_general_3d(israeli.together, vbm.together, "israeli vs european")
#israeli.draw_general_3d(israeli.men, vbm.men, "men - israeli vs european")
#israeli.draw_general_3d(israeli.women, vbm.women, "women - israeli vs european")

#pca_bin_corr(israeli.together, vbm.together)
#pca_bin_corr(israeli.men, vbm.men)
#pca_bin_corr(israeli.women, vbm.women)

#pca_bin_corr(israeli.men, israeli.women)
#pca_bin_corr(vbm.men, vbm.women)

alpha = 0.0005

#print "vbm vs israel", sum(x>alpha for x in ttest(israeli.together, vbm.together)[-1])


origins = parse_origin_file("VBM_origin.csv")

chosen = "beijing_zang,cambridge_buckner".split(",")
def run_against_israel():
    for choice in chosen:
        choice_data = origins[choice]
        title = "israeli vs %s=%d/%d/%d" % (choice, len(choice_data.together), len(choice_data.women), len(choice_data.men))
        #choice_data.draw_general_3d(israeli.together, choice_data.together, title)
        #choice_data.draw_general_3d(israeli.men, choice_data.men, "men - %s" % title)
        #choice_data.draw_general_3d(israeli.women, choice_data.women, "women - %s" % title)
        choice_data.draw_bar([0,250], [0,35], choice_data.bar_data(choice_data.men, israeli.men, "men - %s" % title))
        choice_data.draw_bar([0,250], [0,35], choice_data.bar_data(choice_data.women, israeli.women, "women - %s" % title))
        choice_data.draw_bars()
        print 'men - ' + title, sum(x>alpha for x in ttest(israeli.men, choice_data.men)[-1])
        print 'women - ' + title, sum(x>alpha for x in ttest(israeli.women, choice_data.women)[-1])

run_against_israel()


from itertools import permutations
def run_on_each_other():
    for c1, c2 in permutations(chosen, 2):
        title = "%(c1)s vs %(c2)s" % vars()
        c1data, c2data = origins[c1], origins[c2]
        n1m, n1w = len(c1data.men), len(c1data.women)
        n2m, n2w = len(c2data.men), len(c2data.women) 

        graph = FileData(title)
        graph.draw_bar([0,250], [0,35], graph.bar_data(c1data.men, c2data.men, "men - %(n1m)d/%(n2m)d" % vars()))
        graph.draw_bar([0,250], [0,35], graph.bar_data(c1data.women, c2data.women, "women - %(n1w)d/%(n2w)d" % vars()))
        print "men - " + title, sum(x>alpha for x in ttest(c1data.men, c2data.men)[-1])
        print "women - " + title, sum(x>alpha for x in ttest(c1data.women, c2data.women)[-1])


#run_on_each_other()



plt.show()





# create f on f, m on m - done
# graph 3 components with colors - done
# create seperate groups using minimum/maximum data. - done


# understand what the components are
# understand what the score_samples calculates
# check jonathan's svd
# read about GMM - and some basic runs.

# give random sex and run same analysis on data - done
# bootstrapping on group pca - men, women on each other. graph and show where the original data lay. - done

# moshe's separation! - validity against random data - bootstrap the data.

# check correlation between second pca and sex - done, index 0 is super significant

# pca for women/men only check correlation with sex - still correlated.
# random european data and see correlation - so it seems like it's the same thing as before. interesting!
# correlations between european/israeli - there is evidence for difference
# randomize test/train on pca'd svm - done, no extremely different results.

# take the database origins from zohar.
# T test for means - means are not similiar! =O - let's try ANOVA israel vs cambidge vs bejing
# check the number of men vs women that fit certain thresholds of scoring.


# Amir - unsupervised non-linear dimension reduction
# estimate the difference in the pca components
# check the middle group distribution
 

 
