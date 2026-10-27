---
name: pptx-studio
description: Create, improve, or inspect PowerPoint PPTX presentations by the user's chosen directions, including content, layout, icons, images, charts, visual style, and targeted repairs. Use when a user wants to make slides, improve an existing deck, choose an improvement direction, or check presentation problems.
license: MIT
---

# PPTX Studio

Turn the user's chosen improvement directions into an editable presentation. Communicate in the user's language. Keep the skill portable: use the presentation tools available in the current environment rather than requiring a particular connector, model, or paid service.

## Establish the task

Identify the operation: **create**, **edit**, or **audit**. Audit means report findings without changing the presentation; an explicit request to fix a problem is edit with the repair direction.

Resolve these inputs from the request and existing context: source or topic, target slides, chosen directions, presentation audience/use, and any reference/template. Inspect an available source immediately. Ask only for missing information that materially changes the result.

Honor explicit choices. “Add icons to slides 5–8, leave the wording alone” already selects edit, icons, and slides 5–8; proceed without displaying a menu. For a narrowly requested repair, preserve the remaining work.

If the user wants help selecting an improvement direction, offer this short menu in their language, allowing multiple choices or free text:

1. Content and storyline — 内容与逻辑
2. Layout and relationships — 版式与构图
3. Icons and semantic diagrams — 图标增强
4. Images and screenshots — 图片与配图
5. Charts and data — 数据图表
6. Visual style — 视觉风格
7. Targeted repairs — 问题修复

Read the catalog at [references/directions.json](references/directions.json) for canonical IDs and the corresponding guides. `scripts/plan.py --list` displays the same catalog. These are conversation choices, not a required graphical interface. Use a question tool when available and ordinary conversation otherwise.

For an unspecified new presentation, collect the topic, audience, and source material; content, layout, and style are a reasonable starting combination. For “improve everything,” state the improvements the source actually needs rather than adding every visual category by default.

## Execute selected directions

Read **only the selected guides**:

- Content restructuring or a new storyline: [references/content.md](references/content.md).
- Layout changes, timelines, architecture, or comparisons: [references/layout.md](references/layout.md).
- Icon additions, replacements, or semantic review: [references/icons.md](references/icons.md).
- Photos, illustrations, screenshots, or visual evidence: [references/images.md](references/images.md).
- Quantitative charts or comparison tables: [references/charts.md](references/charts.md).
- Aesthetic restyling or template following: [references/style.md](references/style.md).
- Overlap, overflow, broken assets, or formatting faults: [references/repair.md](references/repair.md).

Combine compatible directions in one pass. Establish content and facts first when selected, choose visual representations next, then place and style them. An icons-only request does not authorize rewriting the argument or replacing the whole template. A layout-only request preserves wording unless the user also selects content editing.

For mechanical file editing or missing tooling, consult [references/backends.md](references/backends.md). The bundled scripts inspect decks and record explicit selections; they do not autonomously generate or aesthetically evaluate a finished presentation.

## Verify and deliver

Read [references/verification.md](references/verification.md) for every created or changed presentation, and for audit requests. Use `scripts/inspect_pptx.py` as a read-only structural preflight when a local PPTX is available. It detects some geometric and package problems; it never certifies visual correctness.

Preserve source facts, user changes, and the selected slide scope. Keep intended text, tables, charts, and icons editable where the backend permits it. Prefer a new output file unless overwriting was requested.

Check the **final PPTX** in the target application or by directly rendering that file. Treat independently drawn mockups as design previews, not evidence that the PPTX has been rendered. If native rendering is unavailable, deliver the editable file with that specific verification limitation stated.

Report the output path, the directions actually applied, and any unresolved material issue. For audit-only requests, deliver findings with page/object locations and proposed fixes. Keep private source slides, logos, screenshots, credentials, and customer data out of reusable/public skill assets unless the user explicitly authorizes including them.
