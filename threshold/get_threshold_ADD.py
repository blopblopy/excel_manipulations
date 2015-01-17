#! /usr/bin/python

import sys
from collections import Counter, defaultdict
from csv import DictReader


def get_threshold_percent(mdata, fdata):
    mnums = float(sum(mdata.values()))
    fnums = float(sum(fdata.values()))
    msortedkeys = sorted(mdata.keys())
    fsortedkeys = sorted(fdata.keys())
    m_index = 0
    f_index = 0
    mrunning_sum = 0
    frunning_sum = 0
    for f_index, fvalue in enumerate(fsortedkeys):
        frunning_sum += fdata[fvalue]
        while fvalue >= msortedkeys[m_index]:
            mrunning_sum += mdata[msortedkeys[m_index]]
            m_index += 1
        if (mrunning_sum/mnums) >= (1-frunning_sum/fnums):
            break
    return fvalue, (mrunning_sum/mnums), (1-frunning_sum/fnums)

def get_threshold_from_percent(one_sex_histogram, from_right=False, percent=0.1):
        if from_right:
                percent = 1 - percent
        total = float(sum(one_sex_histogram.values()))
        running_total = 0
        last_k = 0
        last_percent = 0
        for k, v in sorted(one_sex_histogram.iteritems()):
                running_total += v
                current_percent = running_total/total
                if current_percent >= percent:
                        chosen_k = k
                        if current_percent - percent > percent - last_percent:
                                chosen_k = last_k
                        return chosen_k, {last_k:last_percent, k:current_percent}
                last_k = k
                last_percent = current_percent
        
        
        

                
def exp(data):
    nums = .0
    sum = 0
    for k,v in data.iteritems():
        nums += v
        sum += k*v
    return sum/nums


def print_threshold(f1, f2, attrib, mdata, fdata):
    mexp, fexp = exp(mdata), exp(fdata)
    if fexp <= mexp:
        threshold, mpercent, fpercent = get_threshold_percent(mdata, fdata)
        f1.write("{attrib}: below {threshold} is 'female'. {mpercent} male is 'female', {fpercent} female is 'male'\n".format(**vars()))
        f2.write("{attrib}, {threshold}, female\n".format(**vars()))
    else:
        threshold, fpercent, mpercent = get_threshold_percent(fdata, mdata)
        f1.write("{attrib}: below {threshold} is 'male'. {fpercent} female is 'male', {mpercent} male is 'female'\n".format(**vars()))
        f2.write("{attrib}, {threshold}, male\n".format(**vars()))
        
def main_behavioral():
    FILE = sys.argv[1] 
    SEX_ATTRIBUTE = 'bio_sex'
    MALE, FEMALE = '1', '2'
    NOT_ATTRIBUTE = '', SEX_ATTRIBUTE
    
    data = DictReader(open(FILE))

    attrib_dict = defaultdict(lambda : defaultdict(Counter))


    for subject in data:
        sex = subject[SEX_ATTRIBUTE]
        for attribute, value in subject.iteritems():
            if attribute in NOT_ATTRIBUTE:
                continue
            if value != '':
                attrib_dict[attribute][sex][float(value)] += 1

    f = file("attrib_threshold_ADD.txt", 'wt')
    f2 = file("attrib_threshold_ADD_xsl.txt", 'wt')
    for attribute, histogram in attrib_dict.iteritems():
        try:
            print_threshold(f, f2, attribute, histogram[MALE], histogram[FEMALE])
        except:
            print "Failed", attribute
    f2.close()
    f.close()

def parse_file(attrib_dict, sex, file_name):    
    for subject in DictReader(open(file_name)):
        if subject['BIO_SEX'] != sex:
            continue
        for attribute, value in subject.iteritems():
            if value != '':
                attrib_dict[attribute][sex][float(value)] += 1

def main_brain():
    FEMALE_FILE = sys.argv[1] 
    MALE_FILE = sys.argv[1]
    MALE, FEMALE = '1', '2'

    attrib_dict = defaultdict(lambda : defaultdict(Counter))
    parse_file(attrib_dict, MALE, MALE_FILE) 
    parse_file(attrib_dict, FEMALE, FEMALE_FILE)
    
    f1 = file("attrib_threshold_ADD.txt", 'wt')
    f2 = file("attrib_threshold_ADD_xsl.txt", 'wt')
    for k,v in attrib_dict.iteritems():
        print_threshold(f1, f2, k, v[MALE], v[FEMALE])
    f1.close()
    f2.close()


def print_extreme_threshold(f1, f2, attrib, mdata, fdata):
    mexp, fexp = exp(mdata), exp(fdata)
    if fexp <= mexp:
        fthreshold, fdict = get_threshold_from_percent(fdata)
        mthreshold, mdict = get_threshold_from_percent(mdata, from_right=True)
        f1.write("{attrib}: female extreme is below {fthreshold:.2f}, male extreme is above {mthreshold:.2f} ({fdict}, {mdict}).\n".format(**vars()))
        f2.write("{attrib},{fthreshold},0,{mthreshold},1\n".format(**vars()))
    else:
        fthreshold, fdict = get_threshold_from_percent(fdata, from_right=True)
        mthreshold, mdict = get_threshold_from_percent(mdata)
        f1.write("{attrib}: female extreme is above {fthreshold:.2f}, male extreme is below {mthreshold:.2f} ({fdict}, {mdict}).\n".format(**vars()))
        f2.write("{attrib},{fthreshold},1,{mthreshold},0\n".format(**vars()))


def main_extremelly_sex_typed():
    FEMALE_FILE = r''
    MALE_FILE = r''
    MALE, FEMALE = '1', '2'

    attrib_dict = defaultdict(lambda : defaultdict(Counter))
    parse_file(attrib_dict, MALE, MALE_FILE) 
    parse_file(attrib_dict, FEMALE, FEMALE_FILE)
    
    f1 = file("whole_area_extreme_typed.txt", 'wt')
    f2 = file("whole_area_extreme_typed_csv.txt", 'wt')
    f2.write("attribute,female threshold, 1=above is female, male threshold, 0=below is male\n")
    for k,v in attrib_dict.iteritems():
                print_extreme_threshold(f1, f2, k, v[MALE], v[FEMALE])
    f1.close()
    f2.close()
        


if __name__ == "__main__":
    #main_brain()
    #main_extremelly_sex_typed()
    main_behavioral()
    #if i want to run behavioral, change main_brain()
    #to run the script: double click on it. remeber to change file locations 
            
