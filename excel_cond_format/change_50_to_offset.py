import re, sys
import xml.dom.minidom as mdom

DIGIT_PATT = re.compile(r"([A-Z]{1,2})")

filename = sys.argv[1]

s = mdom.parse(filename)
for cf in doc.getElementsByTagName("conditionalFormatting"):
    col = DIGIT_PATT.match(cf.attributes['sqref'].nodeValue).group(1)
    for element in cf.getElementsByTagName("cfvo"):
        attrs = element.attributes
        if attrs['type'] == 'percentile':
            attrs['type'] = 'formula'
            attrs['val'] = '$%(col)s$3' % dict(col=col)

s.writexml(open(filename, 'w'))



            
