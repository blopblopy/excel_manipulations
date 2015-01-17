#! /usr/bin/python
import re, sys
import xml.dom.minidom as mdom

filename = sys.argv[1]

NEW_COLOR = {0:"FFFFFF00", 2:"FF008000"}

doc = mdom.parse(filename)
for cf in doc.getElementsByTagName("conditionalFormatting"):
    for i, element in enumerate(cf.getElementsByTagName("color")):
        attrs = element.attributes
        #print attrs
        if attrs.get('rgb', False):
            attrs['rgb'] = NEW_COLOR[i]

doc.writexml(open(filename, 'w'))



            
