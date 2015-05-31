#!/usr/bin/env python
# -*- coding: utf-8 -*-
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.text.run import Font
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt

document = docx.Document()
style = document.styles.add_style("hebrew", WD_STYLE_TYPE.PARAGRAPH)
style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
font = style.font
font.complex_script = True
font.name = "Arial Hebrew"
font.rtl = True 
font.size = Pt(12)


techen = u"שלום"
tichnun = u"סופ"

p = document.add_paragraph(style="hebrew")
r = p.add_run(u"תחום התכן:")
r.font.cs_bold = True
r = p.add_run(u" " + techen)

p = document.add_paragraph(style="hebrew")
r = p.add_run(u"שלב תכנון:")
r.font.cs_bold = True
r = p.add_run(u" " + tichnun)

document.save("pytest.docx")
