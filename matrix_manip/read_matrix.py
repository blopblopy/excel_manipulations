#! /usr/bin/python

from os.path import basename
from csv import DictWriter
from collections import OrderedDict

from zurich_subject_mapping import MAPPING

class DataMatrix(object):
    def __init__(self, subject, f):
        self.subject = subject
        self.data = []
        for line in f:
            self.data.append(line.strip().split(" "))

    def get_data(self):
        data = OrderedDict(subject=self.subject, sex=MAPPING[self.subject])
        for row, line in enumerate(self.data, 1):
            for col, value in enumerate(line[row:], row+1):
                data["%s,%s" % (row, col)] = value
        return data

def main(files):
    datum = []
    for filename in files:
        subject = basename(filename).partition('_')[0]
        with open(filename) as f:
            datum.append(DataMatrix(subject, f).get_data())

    with open("Zurich_white_matter.csv","wb") as outputfile:
        csvoutput = DictWriter(outputfile, datum[0].keys())
        csvoutput.writeheader()
        csvoutput.writerows(datum)
    
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])





        
