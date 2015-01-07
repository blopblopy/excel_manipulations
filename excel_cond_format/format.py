#! /usr/bin/python

import sys

filename = sys.argv[1]
offset = 3
start_col = 2
end_col = 116
start_row = sys.argv[2]
end_row = sys.argv[3]


s = open(filename).read()
insert_position = len(s) - s.find("<pageMargins")
s[-insert_position:]
def col_id(idx):
    if idx < 1:
        raise ValueError("Index is too small")
    result = ""
    while True:
        if idx > 26:
            idx, r = divmod(idx - 1, 26)
            result = chr(r + ord('A')) + result
        else:
            return chr(idx + ord('A') - 1) + result

        
formatting = """
<conditionalFormatting sqref="%(col)s%(start_row)s:%(col)s%(end_row)s">
    <cfRule type="colorScale" priority="1">
      <colorScale>
        <cfvo type="min"/>
        <cfvo type="formula" val="$%(col)s$3"/>
        <cfvo type="max"/>
        <color rgb="FF008000"/>
        <color theme="0"/>
        <color rgb="FFFFFF00"/>
      </colorScale>
    </cfRule>
  </conditionalFormatting>"""
new_data = s[:-insert_position] + "\n".join(formatting % dict(start_row=start_row, end_row=end_row, col=col_id(i+offset)) for i in xrange(start_col,end_col+1)) + s[-insert_position:]
open(filename, 'w').write(new_data)

