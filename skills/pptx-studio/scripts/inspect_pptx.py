#!/usr/bin/env python3
"""Read-only PPTX structural preflight. This is not a rendering engine."""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import unicodedata
import zipfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree as ET

from plan import parse_slides, output_is_input

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'}
EMU = 914400
MAX_XML_BYTES = 8 * 1024 * 1024


class InspectionError(ValueError):
    pass


def xml(z: zipfile.ZipFile, name: str) -> ET.Element:
    try:
        info = z.getinfo(name)
        if info.file_size > MAX_XML_BYTES:
            raise InspectionError(f'XML part exceeds {MAX_XML_BYTES} bytes: {name}')
        raw = z.read(name)
        if b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():
            raise InspectionError(f'DTD/entity declarations are unsupported: {name}')
        return ET.fromstring(raw)
    except (KeyError, ET.ParseError, zipfile.BadZipFile) as exc:
        raise InspectionError(f'Cannot read XML part {name}: {exc}') from exc


def relationship_part(part: str) -> str:
    return posixpath.join(posixpath.dirname(part), '_rels', posixpath.basename(part) + '.rels')


def resolve_target(part: str, target: str) -> str:
    target = unquote(target.split('#', 1)[0]).replace('\\', '/')
    if not target:
        return part
    if target.startswith('/'):
        return posixpath.normpath(target.lstrip('/'))
    return posixpath.normpath(posixpath.join(posixpath.dirname(part), target))


def relationship_owner(name: str) -> str:
    if name == '_rels/.rels':
        return ''
    directory, base = posixpath.split(name)
    return posixpath.join(posixpath.dirname(directory), base[:-5])


def integer(el: ET.Element | None, key: str, default: int = 0) -> int:
    return int(el.get(key, default)) if el is not None else default


def normalize(text: str) -> str:
    return ' '.join(unicodedata.normalize('NFKC', text).split()).casefold()


def paragraphs(body: ET.Element | None) -> tuple[str, ...]:
    if body is None:
        return ()
    result = []
    for p in body.findall('a:p', NS):
        pieces = []
        for node in p.iter():
            if node.tag == '{' + NS['a'] + '}t':
                pieces.append(node.text or '')
            elif node.tag == '{' + NS['a'] + '}br':
                pieces.append('\n')
        if ''.join(pieces).strip():
            result.append(''.join(pieces))
    return tuple(result)


@dataclass(frozen=True)
class Obj:
    id: str
    name: str
    kind: str
    box: tuple[float, float, float, float]
    paragraphs: tuple[str, ...] = ()
    rotated: bool = False

    @property
    def text(self) -> str:
        return '\n'.join(self.paragraphs)

    def public(self) -> dict:
        return {'id': self.id, 'name': self.name, 'kind': self.kind,
                'box_inches': [round(v / EMU, 4) for v in self.box],
                'text': self.text, 'rotation_unverified': self.rotated}


def mapped_box(x: float, y: float, w: float, h: float, tr: tuple) -> tuple:
    sx, sy, ox, oy = tr
    x1, x2 = x * sx + ox, (x + w) * sx + ox
    y1, y2 = y * sy + oy, (y + h) * sy + oy
    return min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)


def objects(tree: ET.Element) -> tuple[list[Obj], set[str]]:
    found: list[Obj] = []
    unsupported: set[str] = set()

    def walk(parent: ET.Element, tr=(1.0, 1.0, 0.0, 0.0), inherited_rotation=False) -> None:
        for node in parent:
            tag = node.tag.rsplit('}', 1)[-1]
            if tag not in {'sp', 'pic', 'cxnSp', 'graphicFrame', 'grpSp'}:
                continue
            nv = node.find('.//p:cNvPr', NS)
            ident = nv.get('id', '?') if nv is not None else '?'
            name = nv.get('name', '') if nv is not None else ''
            if tag == 'grpSp':
                xf = node.find('p:grpSpPr/a:xfrm', NS)
            elif tag == 'graphicFrame':
                xf = node.find('p:xfrm', NS)
            else:
                xf = node.find('p:spPr/a:xfrm', NS)
            if xf is None:
                unsupported.add('objects_without_explicit_geometry')
                continue
            off, ext = xf.find('a:off', NS), xf.find('a:ext', NS)
            x, y, w, h = integer(off, 'x'), integer(off, 'y'), integer(ext, 'cx'), integer(ext, 'cy')
            rotated = inherited_rotation or integer(xf, 'rot') % 21600000 != 0
            if tag == 'grpSp':
                co, ce = xf.find('a:chOff', NS), xf.find('a:chExt', NS)
                cw, ch = integer(ce, 'cx', w), integer(ce, 'cy', h)
                if not cw or not ch:
                    unsupported.add('groups_with_zero_coordinate_extent')
                    continue
                ax, ay = w / cw, h / ch
                cx, cy = integer(co, 'x'), integer(co, 'y')
                dx, dy = x - ax * cx, y - ay * cy
                if xf.get('flipH') in {'1', 'true'}:
                    dx, ax = x + w + ax * cx, -ax
                if xf.get('flipV') in {'1', 'true'}:
                    dy, ay = y + h + ay * cy, -ay
                sx, sy, ox, oy = tr
                walk(node, (sx * ax, sy * ay, ox + sx * dx, oy + sy * dy), rotated)
                continue
            box = mapped_box(x, y, w, h, tr)
            if tag == 'graphicFrame':
                tbl = node.find('a:graphic/a:graphicData/a:tbl', NS)
                if tbl is None:
                    unsupported.add('charts_smartart_or_other_graphic_frames')
                    found.append(Obj(ident, name, 'graphic-frame', box, rotated=rotated))
                    continue
                cols = [integer(c, 'w') for c in tbl.findall('a:tblGrid/a:gridCol', NS)]
                rows = tbl.findall('a:tr', NS)
                row_heights = [integer(r, 'h') for r in rows]
                found.append(Obj(ident, name, 'table', box, rotated=rotated))
                for ri, row in enumerate(rows):
                    for ci, cell in enumerate(row.findall('a:tc', NS)):
                        if ci >= len(cols) or cell.get('hMerge') in {'1', 'true'} or cell.get('vMerge') in {'1', 'true'}:
                            continue
                        text = paragraphs(cell.find('a:txBody', NS))
                        if not text:
                            continue
                        col_span, row_span = integer(cell, 'gridSpan', 1), integer(cell, 'rowSpan', 1)
                        tw, th = sum(cols[ci:ci + col_span]), sum(row_heights[ri:ri + row_span])
                        tc = cell.find('a:tcPr', NS)
                        ml, mr = integer(tc, 'marL', 91440), integer(tc, 'marR', 91440)
                        mt, mb = integer(tc, 'marT', 45720), integer(tc, 'marB', 45720)
                        inner = mapped_box(x + sum(cols[:ci]) + ml, y + sum(row_heights[:ri]) + mt,
                                           max(0, tw - ml - mr), max(0, th - mt - mb), tr)
                        found.append(Obj(f'{ident}:r{ri+1}c{ci+1}', f'{name} [{ri+1},{ci+1}]',
                                         'table-cell', inner, text, rotated))
                continue
            found.append(Obj(ident, name, tag, box, paragraphs(node.find('p:txBody', NS)), rotated))

    root = tree.find('p:cSld/p:spTree', NS)
    if root is not None:
        walk(root)
    return found, unsupported


def intersection_ratio(a: Obj, b: Obj) -> float:
    ax, ay, aw, ah = a.box
    bx, by, bw, bh = b.box
    area = min(aw * ah, bw * bh)
    if area <= 0:
        return 0.0
    cross = max(0, min(ax + aw, bx + bw) - max(ax, bx)) * max(0, min(ay + ah, by + bh) - max(ay, by))
    return cross / area


def relationship_uses(tree: ET.Element) -> dict[str, set[str]]:
    """Collect referenced relationship IDs and their nearest slide object IDs."""
    uses: dict[str, set[str]] = {}
    relationship_attributes = {'{' + NS['r'] + '}' + key for key in ('id', 'embed', 'link')}
    object_tags = {'{' + NS['p'] + '}' + key
                   for key in ('sp', 'pic', 'cxnSp', 'graphicFrame', 'grpSp')}

    def walk(node: ET.Element, owner: str | None = None) -> None:
        if node.tag in object_tags:
            nv = node.find('.//p:cNvPr', NS)
            if nv is not None:
                owner = nv.get('id')
        for attribute, rid in node.attrib.items():
            if attribute in relationship_attributes:
                owners = uses.setdefault(rid, set())
                if owner is not None:
                    owners.add(owner)
        for child in node:
            walk(child, owner)

    walk(tree)
    return uses


def inspect(path: Path, selection: str | None = None) -> dict:
    findings: list[dict] = []

    def add(code: str, severity: str, message: str, page=None, ids=None) -> None:
        item = {'code': code, 'severity': severity, 'message': message}
        if page is not None:
            item['page'] = page
        if ids:
            item['object_ids'] = ids
        findings.append(item)

    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        name_set = set(names)
        if len(names) != len(name_set):
            add('duplicate_package_entries', 'error', 'The ZIP package has repeated entry names.')
        main = 'ppt/presentation.xml'
        if '_rels/.rels' in name_set:
            for rel in xml(z, '_rels/.rels'):
                if rel.get('Type', '').endswith('/officeDocument') and rel.get('TargetMode') != 'External':
                    main = resolve_target('', rel.get('Target', ''))
                    break
        presentation = xml(z, main)
        if presentation.tag != '{' + NS['p'] + '}presentation':
            raise InspectionError('Unsupported presentation namespace; this scanner handles transitional PPTX.')
        presrels = {rel.get('Id'): rel for rel in xml(z, relationship_part(main))}
        slide_parts = []
        for sid in presentation.findall('p:sldIdLst/p:sldId', NS):
            rid = sid.get('{' + NS['r'] + '}id')
            rel = presrels.get(rid)
            if rel is None or rel.get('TargetMode') == 'External':
                raise InspectionError(f'Missing/internal slide relationship required: {rid}')
            slide_parts.append(resolve_target(main, rel.get('Target', '')))
        if not slide_parts:
            raise InspectionError('The presentation contains no slides.')
        selection_list = parse_slides(selection, len(slide_parts))
        pages = selection_list or list(range(1, len(slide_parts) + 1))
        size = presentation.find('p:sldSz', NS)
        width, height = integer(size, 'cx'), integer(size, 'cy')
        if width <= 0 or height <= 0:
            raise InspectionError('Missing or invalid slide dimensions.')
        relationship_ids: dict[str, set[str] | None] = {}
        for name in names:
            if not name.endswith('.rels'):
                continue
            try:
                relationships = xml(z, name)
            except InspectionError as exc:
                add('invalid_relationship_xml', 'error', str(exc))
                relationship_ids[relationship_owner(name)] = None
                continue
            owner = relationship_owner(name)
            relationship_ids[owner] = {rel.get('Id', '') for rel in relationships}
            for rel in relationships:
                if rel.get('TargetMode') == 'External':
                    continue
                target = rel.get('Target', '')
                resolved = resolve_target(owner, target)
                if resolved.startswith('../') or resolved == '..':
                    add('escaping_relationship_target', 'error', f'{name}: {target}')
                elif resolved and resolved not in name_set:
                    add('missing_relationship_target', 'error', f'{name}: {target}')
        slides = []
        for page in pages:
            part = slide_parts[page - 1]
            tree = xml(z, part)
            available_ids = relationship_ids.get(part, set())
            # An invalid .rels already has an error; avoid redundant missing-ID claims.
            if available_ids is not None:
                for rid, owners in relationship_uses(tree).items():
                    if not rid or rid not in available_ids:
                        add('missing_relationship_id', 'error',
                            f'{part} references undefined relationship ID {rid!r}.',
                            page, sorted(owners))
            counts: dict[str, int] = {}
            for nv in tree.findall('.//p:cNvPr', NS):
                key = nv.get('id', '?')
                counts[key] = counts.get(key, 0) + 1
            duplicates = [key for key, count in counts.items() if count > 1]
            if duplicates:
                add('duplicate_shape_ids', 'error', 'Object IDs are repeated within the slide.', page, duplicates)
            objs, unsupported = objects(tree)
            for obj in objs:
                if obj.rotated:
                    unsupported.add('rotated_geometry')
                    continue
                x, y, w, h = obj.box
                if min(x, y) < -EMU * .02 or x + w > width + EMU * .02 or y + h > height + EMU * .02:
                    add('object_out_of_bounds', 'warning', f'{obj.name} extends beyond the slide.', page, [obj.id])
            texts = [o for o in objs if o.text.strip() and not o.rotated]
            for i, left in enumerate(texts):
                for right in texts[i + 1:]:
                    overlap = intersection_ratio(left, right)
                    if overlap < .12:
                        continue
                    common = {normalize(p) for p in left.paragraphs if len(normalize(p)) >= 2} & \
                             {normalize(p) for p in right.paragraphs if len(normalize(p)) >= 2}
                    if overlap >= .8 and common:
                        add('possible_duplicate_text_layers', 'error',
                            'Matching text overlaps; confirm the intended content owner before deleting a layer.',
                            page, [left.id, right.id])
                    else:
                        add('possible_text_overlap', 'warning',
                            'Text object bounds intersect; inspect the actual rendered slide.', page, [left.id, right.id])
            if unsupported:
                add('geometry_or_feature_unverified', 'info', ', '.join(sorted(unsupported)), page)
            slides.append({'page': page, 'part': part, 'objects': [o.public() for o in objs],
                           'unsupported_features': sorted(unsupported)})
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return {'schema_version': 1, 'source': str(path), 'source_sha256': digest.hexdigest(),
            'summary': {'slides_total': len(slide_parts), 'slides_inspected': len(pages),
                        **{f'{level}_count': sum(f['severity'] == level for f in findings)
                           for level in ['error', 'warning', 'info']}},
            'visual_verification': {'status': 'not_checked',
                                    'reason': 'Structural preflight only; the final PPTX has not been rendered by this script.'},
            'limitations': ['Approximate bounds are not ink/text-layout measurements.',
                            'Masters, inherited placeholders, animations and notes are not visually evaluated.',
                            'The report includes source text; review it before sharing publicly.'],
            'findings': findings, 'slides': slides}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pptx', type=Path)
    parser.add_argument('--slides', help='One-based selected pages such as 1-4,7 or all')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--strict', action='store_true', help='Also return 1 for warning-only reports')
    args = parser.parse_args()
    try:
        report = inspect(args.pptx, args.slides)
        encoded = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
        if args.output:
            if output_is_input(args.output, args.pptx):
                raise InspectionError('The report path must differ from the input PPTX.')
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(encoded, encoding='utf-8')
        else:
            print(encoded, end='')
        summary = report['summary']
        return int(summary['error_count'] > 0 or (args.strict and summary['warning_count'] > 0))
    except (InspectionError, OSError, ValueError, zipfile.BadZipFile) as exc:
        parser.exit(2, f'Inspection failed: {exc}\n')
    return 2


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
