filename = ""
offset = 3
start_col = 1
end_col = 116

s = open(filename).read()
insert_position = len(s) - s.find("<pageMargins")
s[-insert_position:]
>>> def col_id(idx):
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
<conditionalFormatting sqref="%(col)s6:%(col)s143">
    <cfRule type="colorScale" priority="1">
      <colorScale>
        <cfvo type="min"/>
        <cfvo type="percentile" val="50"/>
        <cfvo type="max"/>
        <color rgb="FF008000"/>
        <color theme="0"/>
        <color rgb="FFFFFF00"/>
      </colorScale>
    </cfRule>
  </conditionalFormatting>"""
new_data = s[:-insert_position] + "\n".join(formatting % dict(col=col_id(i+offset)) for i in xrange(start_col,end_col+1)) + s[-insert_position:]
open(filename, 'w').write(new_data)

