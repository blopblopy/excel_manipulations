import math
import random
from random import randrange
from collections import Counter
import colorsys
from itertools import combinations


import matplotlib.pyplot as plt
from scipy.stats import chisquare, pearsonr

mw = 0.17979798,0.161616162,0.145454545,0.147474747,0.17979798,0.155555556,0.16969697,0.18989899,0.185858586,0.139393939
iw = 0.486868687,0.505050505,0.521212121,0.519191919,0.486868687,0.511111111,0.496969697,0.476767677,0.480808081,0.527272727
fw = 0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333
mm = 0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333
im = 0.525,0.533333333,0.488888889,0.505555556,0.466666667,0.519444444,0.494444444,0.536111111,0.530555556,0.55
fm = 0.141666667,0.133333333,0.177777778,0.161111111,0.2,0.147222222,0.172222222,0.130555556,0.136111111,0.116666667

FEATURES = len(mw)
PERCENT = 40
LENGTH = 10000

random.seed(math.e)

def check_chi(length, percent):
    edges = xrange(length*percent/100, length*(100-percent)/100)
    vector = create_rand(percent, length)
    data = [(i-x) for i,x in enumerate(vector) if i in edges]
    count = Counter((min(x/100,percent-1) if x > 0 else max(-percent, x/100)) for x in data)
    return count, chisquare(count.values())[-1], max(data), min(data), sum(data), sum(abs(x) for x in data)/float(len(data))

def create_rand(percent, length=LENGTH):
    mix = length*percent/100
    return sorted(range(length), key=lambda x:x+randrange(-mix, mix+1))

def create_rand2(percent, length=LENGTH):
    #mix = sorted(range(length), key=lambda x:random.random())
    return [((100-percent)*i+percent*random.randrange(length))/100. for i in xrange(length)]


def count_properties(mp, fp, vectors):
    wcount = Counter()
    mcount = Counter()
    for m,f, vector in zip(mp, fp, vectors):
        vs = sorted(vector)
        length = len(vs)
        fb = vs[-int(length*f)]
        mb = vs[int(length*m)]
        wcount.update(i for i,x in enumerate(vector) if x > fb)
        mcount.update(i for i,x in enumerate(vector) if x < mb)
    return wcount, mcount

def count_persons(wcount, mcount):
    props = Counter()
    for i in xrange(LENGTH):
        props[(wcount[i],mcount[i])] += 1 
    return props


def color_from_size(sizes):
    min_s = min(sizes)
    max_s = float(max(sizes)-min_s)
    colors = []
    for s in sizes:
        base = (s-min_s)/max_s
        color = colorsys.hsv_to_rgb((0.58+base*(1-0.58))%1, base**0.3, 0.5+base*0.5)
        colors.append(color)
    return colors

def bubble(count_data, color='red'):
    x = []
    y = []
    sizes = []
    for k,v in count_data.iteritems():
        x.append(k[0])
        y.append(k[1])
        sizes.append(v)
    plt.scatter(x, y, s=sizes, edgecolors=color, facecolors='none')

def count_props(counter):
    l = LENGTH/100.
    return dict(
    womanly = counter[(FEATURES, 0)]/l,
    manly = counter[(0, FEATURES)]/l,
    intersex = counter[(0, 0)]/l,
    mixed = sum(v for k, v in counter.iteritems() if 0 not in k)/l
    )

def avg_correlation(vectors):
    length = len(vectors)
    n = length*(length-1)/2
    return {'average correlation':sum(pearsonr(v1, v2)[0] for v1, v2 in combinations(vectors, 2))/n}
        

def one_run(women_vectors, men_vectors, percent):
    women = count_persons(*count_properties(mw, fw, women_vectors))
    men = count_persons(*count_properties(mm, fm, men_vectors))
    title = "percent=%d" % percent
    plt.figure(title)
    bubble(women, 'r')
    bubble(men, 'g')
    print title
    print 'women:', count_props(women), avg_correlation(women_vectors)
    print 'men:', count_props(men), avg_correlation(men_vectors)
    print


def create_data():
    for percent in (0, 25, 33, 50, 100): # , 200, 1000):
        women_vectors = [create_rand(percent=percent) for i in xrange(FEATURES)]
        men_vectors = [create_rand(percent=percent) for i in xrange(FEATURES)]
        one_run(women_vectors, men_vectors, percent)


##        women_vectors = [create_rand2(percent=percent) for i in xrange(FEATURES)]
##        men_vectors = [create_rand2(percent=percent) for i in xrange(FEATURES)]
##        one_run(women_vectors, men_vectors, -percent)


##    women_vectors = [random.sample(range(LENGTH), LENGTH) for i in xrange(FEATURES)]
##    men_vectors = [random.sample(range(LENGTH), LENGTH) for i in xrange(FEATURES)]
##    one_run(women_vectors, men_vectors, -1)

    




create_data()
plt.show()
