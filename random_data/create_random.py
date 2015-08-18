
from random import randrange
from collections import Counter
import matplotlib.pyplot as plt
import colorsys


mw = 0.17979798,0.161616162,0.145454545,0.147474747,0.17979798,0.155555556,0.16969697,0.18989899,0.185858586,0.139393939
iw = 0.486868687,0.505050505,0.521212121,0.519191919,0.486868687,0.511111111,0.496969697,0.476767677,0.480808081,0.527272727
fw = 0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333
mm = 0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333,0.333333333
im = 0.525,0.533333333,0.488888889,0.505555556,0.466666667,0.519444444,0.494444444,0.536111111,0.530555556,0.55
fm = 0.141666667,0.133333333,0.177777778,0.161111111,0.2,0.147222222,0.172222222,0.130555556,0.136111111,0.116666667


PERCENT = 40
LENGTH = 10000

def create_rand(length=LENGTH, percent=PERCENT):
    mix = length*percent/100
    return sorted(range(length), key=lambda x:x+randrange(-mix, mix+1))

def count_properties(mp, fp):
    wcount = Counter()
    mcount = Counter()
    for m,f in zip(mp, fp):
        vector = create_rand()
        length = len(vector)
        wcount.update(vector[-int(length*f):])
        mcount.update(vector[:int(length*m)])
    return wcount, mcount

def count_persons(wcount, mcount):
    props = Counter()
    for i in xrange(LENGTH):
        props[(wcount[i],mcount[i])] += 1 
    return props


def bubble(label, count_data):
    x = []
    y = []
    sizes = []
    for k,v in count_data.iteritems():
        x.append(k[0])
        y.append(k[1])
        sizes.append(v)
    min_s = min(sizes)
    max_s = float(max(sizes)-min_s)
    colors = []
    for s in sizes:
        base = (s-min_s)/max_s
        color = colorsys.hsv_to_rgb((0.58+base*(1-0.58))%1, base**0.3, 0.5+base*0.5)
        colors.append(color)

    plt.figure(label)
    plt.scatter(x, y, s=sizes, marker='o', c=colors)


def create_data():    
    women = count_persons(*count_properties(mw, fw))
    men = count_persons(*count_properties(mm, fm))
    bubble("women percent=%d" % (PERCENT), women)
    #bubble("men", men)



create_data()
plt.show()
