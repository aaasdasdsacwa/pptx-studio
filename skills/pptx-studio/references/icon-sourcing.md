# Icon sourcing and selection

Read when the icons direction needs new assets, more visual variety, or a correction to an ambiguous symbol. Treat the examples as search starting points, not a fixed visual vocabulary.

## Find usable assets

Start with approved assets in the deck or a locally installed icon package. If retrieval is available, search the source library rather than downloading an untraceable icon collage.

- [Lucide](https://lucide.dev/icons/) provides outline icons. Check its [license](https://lucide.dev/license), including notices for icons derived from Feather. It is useful for a consistent set of capability symbols.
- [Tabler Icons](https://docs.tabler.io/icons) provides outline and filled families. Its [source repository](https://github.com/tabler/tabler-icons) contains the icon files and license. Choose one family for peer concepts.
- For product identity, prefer the product's own brand resources. [Simple Icons](https://github.com/simple-icons/simple-icons#disclaimer) can help locate brand artwork, but verify the individual icon's source and brand guidelines. Availability in a collection does not make the artwork an official endorsement or establish all trademark permissions.

These are optional sources, not required integrations. Search terms and file names vary by version; inspect actual artwork before choosing it. When shipping downloaded source files, retain their applicable notices alongside the assets. Record family, icon name, source URL or installed package version, license/notice, recoloring, and intended meaning in notes or an asset list.

## Translate meaning into search terms

Identify the object, action and state in the slide. Search two or three concrete nouns or verbs; abstract slide titles alone often retrieve generic art.

- 客服问答: `headset`, `messages`, `help`. A headset suggests human support; a dialogue suggests an exchange. Retain a short label if the human/automated distinction matters.
- 资料检索: `search document`, `file search`. A bare magnifying glass may mean zoom rather than retrieval.
- 会话记忆: `history`, `notebook`, `archive`. A chip suggests compute and is a weak match for recall.
- 审核通过: `clipboard check`, `approval`. A check needs a review object; use different states for pending, rejected and approved.
- 人工接管: `user handoff`, `user check`, `headset`. A connected robot pair suggests cooperation between agents rather than a transfer to a person.
- 受限查询: `database lock`, `shield database`. A lock alone hides the information object and the constraint may need a short label.
- 断链: `unlink`, `link off`. A connected chain communicates the opposite state.

For each changed concept, keep an internal record such as:

```text
Slide 3 / 会话记忆
Meaning: retrieve earlier conversation records
Candidate: history or notebook
Rejected: chip, because it suggests compute
Family/style: chosen deck family, same stroke and optical size as peers
Label: preserve 会话记忆
```

## Add variety without losing coherence

Choose outline, filled, or restrained duotone from the reference deck and viewing size. Vary the meaningful silhouette and composition before mixing families. Keep the same concept recognizable across pages; introduce a different motif when the meaning differs.

A long response can become a labeled sequence of dialogue, lookup and confirmation when those steps actually exist. A product name can sit beside its verified logo. An abstract caveat often needs text rather than an extra symbol. More icons is not a quota.

Normalize optical size rather than only bounding-box dimensions. Check stroke visibility at presentation size, proximity to the matching label, and positive/negative state. Prefer SVG or editable groups supported by the destination. If the backend rasterizes the icon, disclose the editability limit; keep surrounding labels and diagrams editable.
