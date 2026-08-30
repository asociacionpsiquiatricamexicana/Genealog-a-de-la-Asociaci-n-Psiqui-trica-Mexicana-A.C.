# -*- coding: utf-8 -*-
"""Extrae el texto de cada pagina del PDF final via pypdfium2 y lo guarda como
lista de cadenas en mypages.json, en el formato que espera cmp.py."""
import json, sys
import pypdfium2 as pdfium

PDF = sys.argv[1] if len(sys.argv) > 1 else 'pdfs/APM60_Genealogia__final.pdf'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'mypages.json'

doc = pdfium.PdfDocument(PDF)
pages = []
for i in range(len(doc)):
    page = doc[i]
    textpage = page.get_textpage()
    txt = textpage.get_text_range()
    pages.append(txt)
    textpage.close()
    page.close()
doc.close()

json.dump(pages, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print(f'páginas extraídas: {len(pages)} -> {OUT}')
