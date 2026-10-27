# Verification and delivery

Use the checks relevant to the chosen operation and scope. Findings from a scanner are evidence to inspect, not automatic fixes or a complete quality score.

## Structural preflight

`scripts/inspect_pptx.py` is read-only and uses no third-party Python packages. It follows presentation slide order and inspects selected slides for duplicate object IDs, possible repeated text layers, candidate text collisions, and object bounds. Package checks also report invalid XML and missing internal relationship targets.

```sh
python scripts/inspect_pptx.py input.pptx --slides 2 --output preflight.json
```

An error produces exit code 1, input/selection failures produce 2, and warning-only reports produce 0 unless `--strict` is set. The JSON report always records visual verification as `not_checked`. Refer to the script's `--help` for options.

Geometry is approximate. Rotated objects, SmartArt, font substitution, animations, intentional overlap, and application-specific text layout need human/model inspection of a direct rendering. Repeated labels in separate cells are valid. A text box and an identical table paragraph in the same area are a candidate duplicate; confirm which layer owns the intended content before removal.

## Content and semantic checks

Check selected slides against the request: facts/units, scope, retained user changes, icon-to-label meaning, negative states, connector direction, and source attribution. Review images for relevance, correct crops, and legibility. Do not promote an unsupported improvement claim because the new slide looks persuasive.

## Final-file visual checks

Open or directly render the actual final PPTX. Check edited pages at the intended use size, then review the deck overview for consistency. For shared-theme/assets changes, inspect affected unselected pages too.

Check table row growth, text wrapping, icon/label spacing, line/label collisions, stacking, clipping, contrast, missing images, and unexpected font changes. Keep previews separate from production objects: rendering a preview must not append duplicate text boxes to the editable deck. Check IDs for uniqueness after inserting grouped shapes.

If a defect is found, fix the relevant artifact and rerun the check that revealed it. Limit further checks to changed areas and unresolved concerns.

## Delivery

Provide the requested editable file (or an audit report), a compact change summary, and actual verification status. If previews are supplied, state whether they were exported directly from the final PPTX or are design mockups. Do not label structural-only inspection as “visually verified.” Avoid bundling customer/source material into public examples.
