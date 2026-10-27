"""Synthetic OOXML fixtures for read-only inspection, not render-quality fixtures."""
from html import escape
from pathlib import Path
import zipfile

P='http://schemas.openxmlformats.org/presentationml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL='http://schemas.openxmlformats.org/package/2006/relationships'
EMU=914400


def paragraphs(lines):
    if isinstance(lines,str):lines=[lines]
    return ''.join('<a:p><a:r><a:t>'+escape(line)+'</a:t></a:r></a:p>' for line in lines)


def shape(ident=2,text='Clean',x=1,y=1,w=3,h=.5,rotation=0):
    return f'''<p:sp><p:nvSpPr><p:cNvPr id="{ident}" name="Shape {ident}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm rot="{rotation}"><a:off x="{round(x*EMU)}" y="{round(y*EMU)}"/><a:ext cx="{round(w*EMU)}" cy="{round(h*EMU)}"/></a:xfrm></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/>{paragraphs(text)}</p:txBody></p:sp>'''


def table(ident=2,text=('现象：复现条件','预防：检查输入'),x=2,y=2,w=3,h=1.1):
    return f'''<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="{ident}" name="Comparison table"/><p:cNvGraphicFramePr/><p:nvPr/></p:nvGraphicFramePr><p:xfrm><a:off x="{round(x*EMU)}" y="{round(y*EMU)}"/><a:ext cx="{round(w*EMU)}" cy="{round(h*EMU)}"/></p:xfrm><a:graphic><a:graphicData uri="{A}/table"><a:tbl><a:tblPr/><a:tblGrid><a:gridCol w="{round(w*EMU)}"/></a:tblGrid><a:tr h="{round(h*EMU)}"><a:tc><a:txBody><a:bodyPr/><a:lstStyle/>{paragraphs(text)}</a:txBody><a:tcPr marL="91440" marR="91440" marT="45720" marB="45720"/></a:tc></a:tr></a:tbl></a:graphicData></a:graphic></p:graphicFrame>'''


def group(child):
    return f'''<p:grpSp><p:nvGrpSpPr><p:cNvPr id="8" name="Translated group"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="{7*EMU}" y="{EMU}"/><a:ext cx="{2*EMU}" cy="{2*EMU}"/><a:chOff x="0" y="0"/><a:chExt cx="{10*EMU}" cy="{10*EMU}"/></a:xfrm></p:grpSpPr>{child}</p:grpSp>'''


def slide(content):
    return f'''<p:sld xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name="Root"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>{content}</p:spTree></p:cSld></p:sld>'''


def make_deck(path:Path,contents=None,parts=None,extra=None):
    contents=contents if contents is not None else [shape()]
    parts=parts or [f'ppt/slides/slide{i+1}.xml' for i in range(len(contents))]
    sids=''.join(f'<p:sldId id="{256+i}" r:id="rId{i+1}"/>' for i in range(len(parts)))
    pres=f'<p:presentation xmlns:p="{P}" xmlns:r="{R}"><p:sldIdLst>{sids}</p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/></p:presentation>'
    rels=''.join(f'<Relationship Id="rId{i+1}" Type="{R}/slide" Target="{part[4:]}"/>' for i,part in enumerate(parts))
    entries={'[Content_Types].xml':'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>',
             '_rels/.rels':f'<Relationships xmlns="{REL}"><Relationship Id="root" Type="{R}/officeDocument" Target="ppt/presentation.xml"/></Relationships>',
             'ppt/presentation.xml':pres,
             'ppt/_rels/presentation.xml.rels':f'<Relationships xmlns="{REL}">{rels}</Relationships>'}
    entries.update({part:slide(content) for part,content in zip(parts,contents)})
    entries.update(extra or {})
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name,body in entries.items():z.writestr(name,body)
    return path
