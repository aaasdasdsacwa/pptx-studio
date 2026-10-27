# Presentation backends and capability checks

Inventory the current environment before choosing a backend. Separate three capabilities: editing PPTX, fetching/generating assets, and rendering the final PPTX. Availability of one does not imply the others.

## Local PPTX

Use a suitable installed library, such as python-pptx or PptxGenJS, for supported editable objects. Inspect its installed API/help or official documentation when needed. Preserve complex features the chosen library cannot round-trip reliably; for a constrained edit, targeted OOXML replacement can preserve untouched parts when relationships and IDs are handled correctly.

PPTX is an OOXML ZIP package. Resolve slide order from presentation relationships, account for groups and shared assets, and preserve relationship targets. Saving an entire file through a different application may rewrite unselected XML; choose preservation checks proportional to the user's requirement rather than asserting byte identity without measuring it.

Read-only helpers:

```sh
python scripts/plan.py --list
python scripts/inspect_pptx.py input.pptx --slides 1-8 --output preflight.json
```

Run these paths relative to the installed skill directory, or resolve absolute paths from its location. Both helpers use only the Python 3.10+ standard library. A presentation-writing backend remains necessary to create or change a PPTX.

## Rendering

Use an available target application or installed renderer that opens the final PPTX itself. Record the application/renderer and file/version inspected. WPS, PowerPoint, and LibreOffice can differ in font metrics and layout; target-application inspection is especially useful when the user reports a mismatch.

When no direct renderer is available, finish independent authorized edits and structural checks, then disclose that native visual verification remains unavailable. An HTML/Pillow redraw, a generated mockup, or successful ZIP parsing does not substitute for this check.

## Asset tools

Use available connectors or search/image tools for retrieval, and generation tools for requested illustrations. No particular tool names are mandatory. Keep asset attribution and public/private boundaries intact. A missing download tool does not authorize fabricating an official brand asset.

## Optional Python backend

If the host permits local dependency installation, a separate virtual environment with `python-pptx` can provide basic deck editing. The repository's `requirements-dev.txt` describes optional validation/demo dependencies. Do not assume the current interpreter has them or silently alter a user's global environment.
