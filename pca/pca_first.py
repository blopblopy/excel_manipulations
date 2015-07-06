import csv
from math import ceil
import random

import numpy as np
from sklearn import mixture
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
 

class BarData(object):
    def __init__(self, x, y, label):
        self.label = label
        self.x = x
        self.y = y

class Plot(object):
    def __init__(self, label, max_per_row=1):
        self.figure = plt.figure(label)
        self.count = 0
        self.max_per_row = max_per_row

    def add_subplot(self, **kwargs):
        self.count += 1
        dim = int(ceil(float(self.count)/self.max_per_row))
        # change former graphs
        for index, ax in enumerate(self.figure.axes, start=1):
            ax.change_geometry(self.max_per_row, dim, index)

        return self.figure.add_subplot(self.max_per_row, dim, self.count, **kwargs)


class FileData(object):
    WOMEN_SEX = "2"
    def __init__(self, filename):
        self.filename = filename
        self.figure = Plot(filename)
        self.bar_figure = Plot(filename + "-bars", 2)

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
        ax = self.figure.add_subplot(projection='3d')
        ax.set_title(label)
        for man_x,man_y,man_z in men:
            ax.scatter(man_x, man_y, man_z, c="g", marker="^")
        for woman_x,woman_y,woman_z in women:
            ax.scatter(woman_x, woman_y, woman_z, c="r", marker="o")

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
        max_x = [min(int(x) for data in datum for x in data.x)-10, max(int(x) for data in datum for x in data.x)+10]
        max_y = [0, max(int(y) for data in datum for y in data.y)*1.1]
        print max_x, max_y
        for data in datum:
            self.draw_bar(max_x, max_y, data)

        

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


def do_file(filename):
    f = FileData(filename)
    f.parse_file()
#    f.all_pcas()
#    f.whiten_pca()
#    f.draw_3d()
#    f.random_data()
#    f.random_label()
    f.draw_bars()
#    f.do_gmm()
#    f.do_svc()


#do_file("israeli_brain.csv")
do_file("VBM.csv")
plt.show()

# create f on f, m on m
# graph 3 components with colors
# create seperate groups using minimum/maximum data.
# understand what the components are

# PCA!
# check the number of men vs women that fit certain thresholds of scoring.

# understand what the score_samples calculates
# check jonathan's svd
# read about GMM - and some basic runs.

# give random sex and run same analysis on data
# bootstraping on group pca - men, women on each other. graph and show where the original data lays.

# moshe's separation! - validity against random data - bootstrap the data.

