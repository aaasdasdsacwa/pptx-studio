# Layout recipes

Read when selecting or adapting a composition. These are adjustable starting layouts, not universal slide templates. Extract a supplied reference's dimensions, margins, typography, colors and line treatment first. Use the original object placements when only a local repair is authorized.

Coordinates below describe percentages of the usable content frame after the title and margins are reserved. Translate them to the actual slide size. Reading decks may need more space for qualifications than spoken decks.

## Timeline: stages or dated milestones

Use for an actual progression. A horizontal layout works well for roughly three to five short milestones; larger counts or longer explanations may need a vertical layout or several permitted pages.

- Place a baseline near the middle of the frame and distribute milestone centers across its width.
- Reserve the upper portion for stage/date labels and the lower portion for short descriptions. Keep the same label-to-marker spacing across stages.
- For n equally spaced stages, a useful starting center is `(i + 0.5) / n` of the usable width, with each label narrower than its spacing minus a gutter.
- Equally spaced markers communicate order. A proportional time axis needs real dates and spacing that matches elapsed time. Use stage names when dates are absent.
- If labels collide, try a vertical arrangement, wider labels or an authorized split before reducing type.

Example content: 需求确认, 原型设计, 联合验证, 上线交付. These are stages, not invented dates or measured durations. Preserve all original descriptions during layout-only work.

## Comparison: common criteria

Use aligned columns or an editable table when readers need to compare the same criteria. Two independent text piles make differences hard to inspect.

- For a two-option table, try 24% of the frame width for criteria and 38% for each option. Adjust for actual text rather than fixing those proportions.
- Put the same criterion on one row. Align units, qualifiers and label baselines. Use concise column headings and restrained divider lines.
- Use dashed internal dividers when requested or when they suit the reference. Header rules and table boundaries can retain their own treatment.
- Size each row for the largest wrapped cell, including cell margins and paragraph spacing. Keep one authoritative text layer inside each native cell.
- If a required row is dense, widen its columns, allow more row height, or split permitted rows while retaining headings. A font size reduction is the last adjustment.

Example criteria: 适用场景, 输入要求, 输出形式. A comparison need not imply that one option is universally better.

## Process: ordered actions and decisions

Use a process when sequence or branching is the point. A flat list can remain a list if order is incidental.

- For a short linear flow, reserve a common horizontal lane for node centers, with labels beneath or within nodes according to the reference. Leave dedicated gaps for connectors.
- Four short steps might start with nodes using about 18% of the frame each and the remaining width as outside and connector gaps. More words need fewer nodes per row.
- Route edges through open gaps and label decision branches close to their edge. Arrowheads communicate direction; visual proximity alone does not.
- Put responsible roles in swimlanes when ownership matters. Draw a return path only when the workflow actually returns.
- If branches cross repeatedly, change the orientation or separate subflows. Preserve the original decisions, conditions and termination rules.

Example sequence: 接收问题, 检索资料, 组织答案, 人工确认. Include 人工确认 only when the source actually requires it.

## Architecture: components and boundaries

Use for components and their dependencies. Keep organizational ownership separate from runtime call direction.

- Start with a few meaningful layers or zones, such as client, service and data. Shared vertical alignment helps readers match dependencies across layers.
- Place related components together; name boundaries when they represent deployment, trust or responsibility. Use containers for real boundaries rather than decoration.
- Draw only the edges needed to explain the stated relationship. Label ambiguous edges, and use arrows only when direction is known.
- Put a legend near the diagram only when different edge/shape types encode distinct meanings. Mark conceptual architecture as conceptual when no implementation evidence is supplied.
- If the graph becomes tangled, extract one interaction into a focused process slide while preserving an overview when scope permits.

Example: 客户端 calls 问答服务, which retrieves from 知识库. Do not infer data retention, security guarantees or performance from that structure.

## Adapt and verify

Choose the recipe from the relationship, fit it to the supplied reference, and place the real content before adding decoration. Check labels and connectors after rendering the actual final PPTX. For layout-only edits, compare the text before and after; for shared-theme changes, inspect affected pages outside the selected range too.
