#!/usr/bin/env python3
"""Validate the bundled skill's metadata, pointers and Python syntax."""
from __future__ import annotations

import json
from pathlib import Path
import py_compile
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/pptx-studio'
sys.path.insert(0,str(SKILL/'scripts'))
from plan import load_catalog


def frontmatter(text: str) -> tuple[dict,str]:
    match=re.match(r'^---\r?\n(.*?)\r?\n---(?:\r?\n|$)',text,re.S)
    if not match:raise ValueError('Missing YAML frontmatter')
    try:
        import yaml
    except ImportError:
        # A narrow fallback for this package's flat, string-valued metadata.
        # Other YAML constructs require the optional PyYAML development dependency.
        data={}
        for line in match[1].splitlines():
            if not line.strip() or line.lstrip().startswith('#'):continue
            found=re.fullmatch(r'([a-z][a-z0-9_-]*):\s*(\S.*)',line)
            if not found:raise ValueError('Install requirements-dev.txt for non-flat YAML metadata')
            key,value=found.groups()
            if key in data:raise ValueError(f'Duplicate metadata key: {key}')
            data[key]=json.loads(value) if value.startswith('"') else value
    else:
        data=yaml.safe_load(match[1])
    if not isinstance(data,dict):raise ValueError('Metadata must be a dictionary')
    return data,text[match.end():]


def main() -> int:
    errors=[]
    try:
        text=(SKILL/'SKILL.md').read_text(encoding='utf-8')
        data,body=frontmatter(text)
        name=data.get('name','');description=data.get('description','')
        if not isinstance(name,str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name) or len(name)>64 or name!=SKILL.name:
            errors.append('Skill name must match its directory and use lower-case hyphenated words')
        if not isinstance(description,str) or not 1<=len(description.strip())<=1024 or '<' in description or '>' in description:
            errors.append('Description must be a nonempty string up to 1024 characters')
        if '[TODO:' in text:errors.append('Unfinished scaffold in SKILL.md')
        for source in [SKILL/'SKILL.md',*list((SKILL/'references').glob('*.md'))]:
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',source.read_text(encoding='utf-8-sig')):
                if re.match(r'[a-z]+://',target) or target.startswith('#'):continue
                resolved=(source.parent/target.split('#',1)[0]).resolve()
                if not resolved.is_relative_to(SKILL.resolve()) or not resolved.is_file():
                    errors.append(f'Broken or escaping reference in {source.name}: {target}')
        catalog=load_catalog()
        ui=(SKILL/'agents/openai.yaml').read_text(encoding='utf-8-sig')
        short=re.search(r'^  short_description: (".*")$',ui,re.M)
        prompt=re.search(r'^  default_prompt: (".*")$',ui,re.M)
        if not short or not 25<=len(json.loads(short[1]))<=64:errors.append('UI short description must have 25–64 characters')
        if not prompt or '$'+name not in json.loads(prompt[1]):errors.append('UI prompt must mention the skill name')
        for p in [*(SKILL/'scripts').glob('*.py'),*list((ROOT/'tests').glob('*.py'))]:
            py_compile.compile(str(p),doraise=True)
        scenarios=json.loads((ROOT/'evals/scenarios.json').read_text(encoding='utf-8-sig'))
        if scenarios['status']!='manual_scenarios_not_model_evaluated':errors.append('Behavior evaluation status must be explicit')
        valid_ids={item['id'] for item in catalog['directions']}
        for case in scenarios['scenarios']:
            if set(case.get('expected_directions',[]))-valid_ids:errors.append(f'Invalid direction in scenario {case["id"]}')
        if (ROOT/'LICENSE').read_bytes()!=(SKILL/'LICENSE.txt').read_bytes():errors.append('Packaged license differs from repository license')
    except Exception as exc:
        errors.append(str(exc))
    if errors:
        print('\n'.join('ERROR: '+e for e in errors));return 1
    print(f'Validated {name}: {len(catalog["directions"])} directions; metadata, local references, scenarios and script syntax are valid.')
    print('This is package validation, not a model-behavior or final-PPTX visual evaluation.')
    return 0


if __name__=='__main__':raise SystemExit(main())
