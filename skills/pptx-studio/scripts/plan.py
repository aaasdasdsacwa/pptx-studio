#!/usr/bin/env python3
"""List capabilities or record a PPTX Studio brief and explicit task scope."""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'references' / 'directions.json'


def load_catalog(path: Path = CATALOG) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    ids: set[str] = set()
    for item in data['directions']:
        key = item['id']
        if not re.fullmatch(r'[a-z][a-z0-9-]*', key) or key in ids:
            raise ValueError(f'Invalid or repeated direction ID: {key}')
        ids.add(key)
        guide = (path.parent / item['guide']).resolve()
        if guide.parent != path.parent.resolve() or not guide.is_file():
            raise ValueError(f'Missing or unsafe direction guide: {item["guide"]}')
    return data


def parse_slides(value: str | None, slide_count: int | None = None) -> list[int] | None:
    """Return one-based selected pages; None means all. Never clamp invalid pages."""
    if slide_count is not None and slide_count < 1:
        raise ValueError('slide_count must be positive')
    if value is None or value.strip().lower() == 'all':
        return None
    pages: set[int] = set()
    for part in value.split(','):
        match = re.fullmatch(r'\s*([1-9]\d*)(?:\s*-\s*([1-9]\d*))?\s*', part)
        if not match:
            raise ValueError(f'Invalid slide selection: {part!r}; use 1-4,7 or all')
        first = int(match.group(1))
        last = int(match.group(2) or first)
        if last < first:
            raise ValueError('Slide ranges must be ascending')
        if last > 100000:
            raise ValueError('Slide selection exceeds the supported range')
        if slide_count is not None and last > slide_count:
            raise ValueError(f'Slide {last} exceeds slide count {slide_count}')
        pages.update(range(first, last + 1))
    if not pages:
        raise ValueError('Select at least one slide')
    return sorted(pages)


def build_plan(operation: str, directions: list[str] | None = None, *,
               source: str | None = None, topic: str | None = None,
               slides: str | None = None, slide_count: int | None = None,
               use: str = 'unspecified', purpose: str | None = None,
               audience: str | None = None, style_hint: str | None = None,
               duration_minutes: float | None = None,
               target_slide_count: int | None = None) -> dict[str, Any]:
    catalog = load_catalog()
    if operation not in catalog['operations']:
        raise ValueError(f'Unknown operation: {operation}')
    if use not in {'talk', 'read', 'unspecified'}:
        raise ValueError(f'Unknown presentation use: {use}')
    if operation in {'edit', 'audit'} and not source:
        raise ValueError('An edit or audit plan needs a source PPTX path')
    if operation == 'create' and not (topic and topic.strip()) and not source:
        raise ValueError('A create plan needs a topic or source material')
    if duration_minutes is not None and (not math.isfinite(duration_minutes) or duration_minutes <= 0):
        raise ValueError('duration_minutes must be finite and positive')
    if target_slide_count is not None and (isinstance(target_slide_count, bool) or
            not isinstance(target_slide_count, int) or target_slide_count < 1):
        raise ValueError('target_slide_count must be a positive integer (total output pages)')
    brief: dict[str, Any] = {}
    for key, value in [('purpose', purpose), ('audience', audience), ('style_hint', style_hint)]:
        if value is not None:
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f'{key} must be nonempty text when provided')
            brief[key] = value.strip()
    if duration_minutes is not None:
        brief['duration_minutes'] = duration_minutes
    if target_slide_count is not None:
        brief['target_slide_count'] = target_slide_count
    if directions is None:
        directions = ['content', 'layout', 'style'] if operation == 'create' else []
    if operation == 'edit' and not directions:
        raise ValueError('Select at least one improvement direction for editing')
    aliases = {str(item[field]).casefold(): item['id']
               for item in catalog['directions']
               for field in ('id', 'label_zh', 'label_en')}
    chosen: list[str] = []
    for arg in directions:
        for name in arg.split(','):
            try:
                canonical = aliases[name.strip().casefold()]
            except KeyError as exc:
                raise ValueError(f'Unknown direction: {name!r}') from exc
            if canonical not in chosen:
                chosen.append(canonical)
    pages = parse_slides(slides, slide_count)
    by_id = {item['id']: item for item in catalog['directions']}
    return {
        'schema_version': 2,
        'operation': operation,
        'directions': chosen,
        'inputs': {key: val for key, val in {'source': source, 'topic': topic}.items() if val},
        'scope': {'slides': pages if pages is not None else 'all', 'slide_count': slide_count},
        'presentation_use': use,
        'brief': brief,
        'references': (['references/generation.md'] if operation == 'create' else []) +
                      [f'references/{by_id[key]["guide"]}' for key in chosen] +
                      ['references/verification.md'],
        'visual_verification': 'not_checked',
    }


def output_is_input(output: Path, source: Path) -> bool:
    if output.resolve() == source.resolve():
        return True
    return output.exists() and source.exists() and output.samefile(source)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='Show the selectable direction catalog')
    parser.add_argument('--operation', choices=['create', 'edit', 'audit'])
    parser.add_argument('--directions', nargs='+', help='IDs, Chinese labels, or English labels; selections are explicit')
    parser.add_argument('--source', help='Source material path, recorded without reading or modifying it')
    parser.add_argument('--topic')
    parser.add_argument('--slides', help='One-based pages such as 1-4,7, or all')
    parser.add_argument('--slide-count', type=int)
    parser.add_argument('--use', choices=['talk', 'read', 'unspecified'], default='unspecified')
    parser.add_argument('--purpose', help='Free-text intended outcome; not restricted to a scenario list')
    parser.add_argument('--audience', help='Audience and prior knowledge')
    parser.add_argument('--style-hint', help='User style or brand preference, independent of purpose')
    parser.add_argument('--duration-minutes', type=float, help='Planned delivery duration; no automatic slide-count formula')
    parser.add_argument('--target-slide-count', type=int, help='Total output pages, including any cover; differs from source --slide-count')
    parser.add_argument('--output', type=Path, help='Write a plan JSON; otherwise print it')
    args = parser.parse_args()
    try:
        if args.list:
            print(json.dumps(load_catalog(), ensure_ascii=False, indent=2))
            return 0
        if not args.operation:
            parser.error('--operation is required unless --list is used')
        plan = build_plan(args.operation, args.directions, source=args.source, topic=args.topic,
                          slides=args.slides, slide_count=args.slide_count, use=args.use,
                          purpose=args.purpose, audience=args.audience, style_hint=args.style_hint,
                          duration_minutes=args.duration_minutes, target_slide_count=args.target_slide_count)
        encoded = json.dumps(plan, ensure_ascii=False, indent=2) + '\n'
        if args.output:
            if args.source and output_is_input(args.output, Path(args.source)):
                raise ValueError('The plan output must differ from the source material')
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(encoded, encoding='utf-8')
        else:
            print(encoded, end='')
        return 0
    except (OSError, ValueError, KeyError) as exc:
        parser.error(str(exc))
    return 2


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
