# Example requests

These are conversation examples, not a separate web application or a promise of model-level evaluation.

## Choosing a direction

User: “我想把这份 PPT 做好一点，但还没确定从哪改。”

Expected behavior: inspect the source if available, briefly offer the seven selectable directions, and allow combined choices or a free-text goal. Ask about audience/use only if it changes the design decision.

## Icons only

User: “第 1–16 页多用图标，正文意思不变，其他页别动。”

Expected behavior: edit + icons, preserve scope and wording constraints, read the icon guide, distinguish meanings and states, and verify the final PPTX. Do not automatically add images, rewrite claims, or restyle the entire deck.

## Layout with a reference

User: “只优化第 5 页布局，按第 2 页的标题层级来，文字不要改。”

Expected behavior: layout edit of one page, inspect both pages, reuse the reference hierarchy, preserve the exact wording, and check affected geometry.

## Multiple directions

User: “选择图标和版式，把业务审核这一页变得更直观。”

Expected behavior: establish the actual sequence/relationship, choose accurate symbols, arrange the existing content, and keep decisions outside the chosen directions proportionate to the request.

## New presentation

User: “给新同事做一份 10 分钟系统入门 PPT，资料已经放在附件，选择内容、布局、风格。”

Expected behavior: build a supported storyline and editable deck from the material, without inventing metrics or feature screenshots.

## Image direction without a downloader

User: “给这几页加一些真实产品截图和官方 Logo。”

Expected behavior: use verified available assets/tools, disclose specific unavailable material, and keep custom capability illustrations distinguishable from official brand assets.

## Targeted repair

User: “第二页表格叠字了，第一页面已经确认，不要动。”

Expected behavior: inspect the latest source, locate content ownership, repair the redundant layer or layout cause, retain one authoritative table text layer, and preserve page 1.

## Read-only audit

User: “只检查第 1–8 页，告诉我哪里可能有重叠、内容不清楚或图标不对应。”

Expected behavior: audit with no source mutation; distinguish approximate geometric candidates, semantic review, and unverified native rendering.
