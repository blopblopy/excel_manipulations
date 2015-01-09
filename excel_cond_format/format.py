#! /usr/bin/python

import sys

def col2int(s):
    return sum(26**i*(ord(c) - ord('A') +1) for i,c in enumerate(reversed(s)))

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

def main():
    filename = sys.argv[1]
    start_col = col2int(sys.argv[2])
    end_col = col2int(sys.argv[3])
    start_row = sys.argv[4]
    end_row = sys.argv[5]

    s = open(filename).read()
    insert_position = len(s) - s.find("<pageMargins")
    
    conditional_formatting =  "\n".join(formatting % dict(start_row=start_row, end_row=end_row, col=col_id(i))
                                        for i in xrange(start_col, end_col+1))

    new_data = s[:-insert_position] + conditional_formatting + s[-insert_position:]
    open(filename, 'w').write(new_data)


if __name__ == "__main__":
    main()

