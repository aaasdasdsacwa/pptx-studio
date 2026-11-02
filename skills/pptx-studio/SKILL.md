---
name: pptx-studio
description: Create complete editable PowerPoint presentations from topics, outlines, documents, data or existing decks; adapt storyline, visuals and delivery to the audience and purpose. Also revise, restyle or audit selected slides. Use for business, education, research, sales, public talks, creative presentations and other PPTX tasks.
license: MIT
---

# PPTX Studio

Produce a presentation suited to the user's purpose, audience, material and delivery setting. Handle complete creation, transformation of source material, revision and read-only review. Communicate in the user's language. Use the presentation tools available in the current environment rather than requiring a particular connector, model or paid service.

Prior examples demonstrate individual capabilities. They do not establish the default topic, industry, visual style, outline or slide count for a new request. Icons are one optional visual tool; a deck may be better served by photography, charts, text, illustrations, tables or diagrams.

## Establish the task

Identify the operation: **create**, **edit**, or **audit**. Audit means report findings without changing the presentation; an explicit request to fix a problem is edit with the repair direction.

Resolve the brief from the request and existing context: intended outcome, audience and prior knowledge, source material, delivery setting, duration or slide count, language, reference/brand/style, required content and output format. These are independent choices: a research talk can be highly visual; a product deck can be a detailed reading document. Inspect supplied material before asking for information it already contains. Ask only for gaps that materially change the work, preferably in a compact group.

Use a supplied topic, outline, article, Word/PDF document, data, images, screenshots or existing deck as inputs. Distinguish supported facts from proposals and examples. When the brief is sufficient, continue to a complete deliverable without requiring another outline-approval step unless the user requested staged collaboration.

Honor the requested output. Deliver editable PPTX for a PPTX request; a browser presentation, PDF or image preview is an additional or alternate format only when requested. Verify the backend's capabilities before promising interactivity, animations or conversion fidelity.

Honor explicit choices. “Add icons to slides 5–8, leave the wording alone” already selects edit, icons, and slides 5–8; proceed without displaying a menu. For a narrowly requested repair, preserve the remaining work.

## Create a complete presentation

For creation or substantial rebuilding, read [references/generation.md](references/generation.md). It covers source synthesis, storyline, per-slide planning, visual system, asset placement and speaker notes. When the purpose needs specialized treatment, consult the matching section of [references/scenarios.md](references/scenarios.md); these are adaptable approaches, not an exhaustive menu or mandatory outlines.

Derive the structure from what the audience needs to understand, decide, learn or experience. Plan slide roles and visual rhythm before producing pages. Adapt or invent a suitable composition rather than applying a prior example throughout the deck. Respect an explicit total slide count, including any cover and closing pages.

Choose the modules needed for the task. Complete creation ordinarily needs content, layout and style, plus charts, images or other capabilities where the material benefits from them. Users do not need to select technical modules before asking for a new deck.

## Improve selected aspects

If the user wants help selecting an improvement direction, offer this short menu in their language, allowing multiple choices or free text. The menu describes optional capabilities, not the full range of presentation scenarios:

1. Content and storyline — 内容与逻辑
2. Layout and relationships — 版式与构图
3. Icons and semantic diagrams — 图标增强
4. Images and screenshots — 图片与配图
5. Charts and data — 数据图表
6. Visual style — 视觉风格
7. Targeted repairs — 问题修复

Read the catalog at [references/directions.json](references/directions.json) for canonical IDs and the corresponding guides. `scripts/plan.py --list` displays the same catalog. These are conversation choices, not a required graphical interface. Use a question tool when available and ordinary conversation otherwise.

For “improve everything,” diagnose what the source needs rather than inserting every visual category. A free-text requirement outside the menu remains valid; use its intent to choose the work and consult relevant guides.

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

Resolve bundled script and reference paths from this skill's installed location, not from the user's project working directory. Installation and standalone usage are documented in [README.md](README.md); read that only when setup help is needed.

## Verify and deliver

Read [references/verification.md](references/verification.md) for every created or changed presentation, and for audit requests. Use `scripts/inspect_pptx.py` as a read-only structural preflight when a local PPTX is available. It detects some geometric and package problems; it never certifies visual correctness.

Preserve source facts, user changes, and the selected slide scope. Keep intended text, tables, charts, and icons editable where the backend permits it. Prefer a new output file unless overwriting was requested.

Check the **final PPTX** in the target application or by directly rendering that file. Treat independently drawn mockups as design previews, not evidence that the PPTX has been rendered. If native rendering is unavailable, deliver the editable file with that specific verification limitation stated.

Report the output path, the directions actually applied, and any unresolved material issue. For audit-only requests, deliver findings with page/object locations and proposed fixes. Keep private source slides, logos, screenshots, credentials, and customer data out of reusable/public skill assets unless the user explicitly authorizes including them.
