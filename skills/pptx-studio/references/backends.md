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

If the host permits local dependency installation and no preferred editor is available, a separate virtual environment with `python-pptx` can provide basic deck editing. For example, create `outputs/.venv` with `python -m venv outputs/.venv`, then use that environment's Python to install `python-pptx`. Use `outputs/.venv/Scripts/python.exe` on Windows or `outputs/.venv/bin/python` on macOS/Linux. Follow the host's own tool requirements when it supplies an authoring workflow.

The bundled planning and inspection helpers need no installation. `python-pptx`, PptxGenJS and renderers are optional host tools, not dependencies shipped with this skill. Check their actual installed APIs; do not assume SVG import, editable vectors, animation round-tripping or direct PPTX rendering are supported merely because basic editing works. Consult [python-pptx documentation](https://python-pptx.readthedocs.io/en/latest/) or [PptxGenJS documentation](https://gitbrent.github.io/PptxGenJS/) when using those backends.

## Minimum working path

Identify the source, operation, selected pages and final output path. Inspect the source and record the text/objects that scope requires preserving. Confirm an editing backend and separately a renderer before promising their results. Read the selected direction guides, make the scoped changes into a new file, run the bundled preflight, and inspect a direct rendering of that final file when available.

For a new deck, use supplied source material and an available font containing the required characters. For a scoped edit, retain the source dimensions and reference typography. Record the actual backend and renderer in verification evidence, including any rasterized icons or unsupported features. A renderer supplied by an editing library should be named explicitly; it is not proof of identical display in PowerPoint or WPS.

If editing is unavailable, complete an audit or concrete change plan and state that no edited PPTX was produced. If editing works but rendering does not, deliver the editable output with visual verification pending. A preview image alone does not satisfy a request for an editable presentation.
