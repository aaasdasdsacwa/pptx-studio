#!/usr/bin/env python3
"""Build an installable skill ZIP and a source ZIP from explicit public paths."""
from pathlib import Path
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]
NAME='pptx-studio'
SKILL=ROOT/'skills'/NAME
EXCLUDED={'__pycache__','.git','.test-output','.local-deps','dist'}
PUBLIC=['README.md','LICENSE','.gitignore','requirements-dev.txt','.github','skills','tests','tools','examples','evals']


def files(path):
    candidates=[path] if path.is_file() else sorted(path.rglob('*'))
    for p in candidates:
        if p.is_symlink():raise ValueError(f'Symlinks are not packaged: {p.relative_to(ROOT)}')
        if p.is_file() and not set(p.relative_to(ROOT).parts)&EXCLUDED and p.suffix not in {'.pyc','.pyo'}:
            yield p


def build():
    dest=ROOT/'dist';dest.mkdir(exist_ok=True)
    skill_zip=dest/(NAME+'-skill.zip');source_zip=dest/(NAME+'-source.zip')
    with zipfile.ZipFile(skill_zip,'w',zipfile.ZIP_DEFLATED) as z:
        for p in files(SKILL):z.write(p,str(Path(NAME)/p.relative_to(SKILL)))
    with zipfile.ZipFile(source_zip,'w',zipfile.ZIP_DEFLATED) as z:
        for item in PUBLIC:
            for p in files(ROOT/item):z.write(p,str(Path(NAME)/p.relative_to(ROOT)))
    result=[]
    for path in [skill_zip,source_zip]:
        with zipfile.ZipFile(path) as z:
            if z.testzip() is not None:raise ValueError(f'Invalid ZIP: {path}')
            result.append({'file':str(path.relative_to(ROOT)),'entries':len(z.namelist()),'bytes':path.stat().st_size})
    print(json.dumps(result,indent=2))


if __name__=='__main__':build()
