#!/usr/bin/env python3
# md→docx 迷你转换器（无第三方依赖，stdlib zipfile 直写 OOXML）
import re, sys, zipfile

esc = lambda s: s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def runs(text, bold_default=False):
    # 处理 **bold** 与行内代码 `x`
    parts = re.split(r'(\*\*[^*]+\*\*|`[^`]+`)', text)
    out = []
    for p in parts:
        if not p: continue
        if p.startswith('**') and p.endswith('**'):
            out.append(f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{esc(p[2:-2])}</w:t></w:r>')
        elif p.startswith('`') and p.endswith('`'):
            out.append(f'<w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/></w:rPr><w:t xml:space="preserve">{esc(p[1:-1])}</w:t></w:r>')
        else:
            b = '<w:b/>' if bold_default else ''
            out.append(f'<w:r><w:rPr>{b}</w:rPr><w:t xml:space="preserve">{esc(p)}</w:t></w:r>')
    return ''.join(out)

def para(text, style=None, indent=0, bold=False):
    ppr = ''
    if style: ppr += f'<w:pStyle w:val="{style}"/>'
    if indent: ppr += f'<w:ind w:left="{indent}"/>'
    if ppr: ppr = f'<w:pPr>{ppr}</w:pPr>'
    return f'<w:p>{ppr}{runs(text, bold)}</w:p>'

def table(rows):
    xml = ['<w:tbl><w:tblPr><w:tblBorders>' +
           ''.join(f'<w:{e} w:val="single" w:sz="4"/>' for e in ('top','left','bottom','right','insideH','insideV')) +
           '</w:tblBorders></w:tblPr>']
    for i, r in enumerate(rows):
        xml.append('<w:tr>')
        for cell in r:
            xml.append(f'<w:tc><w:tcPr><w:tcW w:w="2400" w:type="dxa"/></w:tcPr>{para(cell, bold=(i==0))}</w:tc>')
        xml.append('</w:tr>')
    xml.append('</w:tbl>')
    return ''.join(xml)

def md_to_body(md):
    lines = md.split('\n'); out = []; i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if ln.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-{2,}:?', c or '---') for c in cells):
                    rows.append(cells)
                i += 1
            out.append(table(rows)); continue
        if m := re.match(r'^(#{1,4})\s+(.*)', ln):
            lvl = len(m.group(1)); out.append(para(m.group(2), style=f'Heading{min(lvl,3)}')); i += 1; continue
        if re.match(r'^\s*---+\s*$', ln) and ln.strip():
            out.append(para('─'*36)); i += 1; continue
        if m := re.match(r'^>\s?(.*)', ln):
            out.append(para(m.group(1), indent=360)); i += 1; continue
        if m := re.match(r'^\s*[-*]\s+(.*)', ln):
            out.append(para('· ' + m.group(1), indent=360)); i += 1; continue
        if m := re.match(r'^\s*(\d+)[).、]\s+(.*)', ln):
            out.append(para(f'{m.group(1)}. {m.group(2)}', indent=360)); i += 1; continue
        if ln.strip() == '':
            out.append('<w:p/>'); i += 1; continue
        out.append(para(ln)); i += 1
    return ''.join(out)

def make_docx(md_path, docx_path):
    md = open(md_path, encoding='utf-8').read()
    body = md_to_body(md)
    doc = DOC_TPL.replace('%%BODY%%', body)
    with zipfile.ZipFile(docx_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CT); z.writestr('_rels/.rels', RELS)
        z.writestr('word/document.xml', doc); z.writestr('word/styles.xml', STYLES)

CT = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>'
RELS = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
STYLES = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:eastAsia="宋体" w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="21"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="200" w:after="100"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="160" w:after="80"/></w:pPr><w:rPr><w:b/><w:sz w:val="23"/></w:rPr></w:style></w:styles>'
DOC_TPL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>%%BODY%%<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:bottom="1134" w:left="1418" w:right="1418"/></w:sectPr></w:body></w:document>'

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    make_docx(src, dst); print(f'OK {dst}')
