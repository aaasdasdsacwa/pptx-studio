# Behavioral evaluation

`scenarios.json` lists requests and acceptance criteria for Agent trials. Its status describes those manual scenarios, not the Python test suite and not an independently measured benchmark. The public showcase is a separate, agent-executed demonstration; see its evidence in the installed skill's `examples` directory.

## Run a case

Use a clean temporary project and install only `skills/pptx-studio`. Provide a source deck with synthetic or redistributable content and the case's request. Let the Agent use the actual tools available in that environment. Do not provide a proposed solution as part of the task prompt.

Retain the source and final files, exact request, chosen directions and slide range, editing backend, renderer, source/final hashes, structural report, and final-file previews. For read-only cases, compare the source hash before and after. For limited-scope cases, compare text and untouched objects/parts as appropriate to the backend. Record unsupported round-tripping instead of claiming byte preservation from a whole-file save.

Inspect the actual final deck for icon meaning, source facts, text retention, overlaps and reference match. A Python test of `build_plan()` does not establish that an Agent followed the user's natural-language scope. A structurally valid PPTX does not establish visual quality.

## Useful first trials

For complete generation, sample different purposes rather than treating one successful deck as universal coverage. Include a decision report, a lesson with practice, a research defense, a photo-led story and a mixed/unlisted purpose from `scenarios.json`. Vary audience, delivery setting and visual style independently. Also test whether a complete brief proceeds without a redundant module-selection or outline-approval step.

1. Icons only: change the ambiguous repeated symbols, preserve every text label and its placement, and leave other slides alone.
2. Reference layout: rearrange a stage list into a timeline while retaining all supplied descriptions and avoiding invented dates.
3. Table repair: remove a confirmed redundant overlay, retain the native cell text once, and preserve the rest of the deck.

The bundled showcase combines these in one three-slide source for convenient comparison. Separate single-direction trials are still needed to measure scope preservation independently.

The broader generation scenarios are currently manual cases, not completed independent evaluations. Record their actual results separately from the existing three-slide editing demonstration.

## Record results honestly

Use per-case results such as `passed`, `failed`, `blocked`, or `not_run`, and distinguish `agent_self_review`, `independent_agent_review`, and `human_review`. Name the model/client only when known. Record tool versions and evidence paths rather than assigning a quality score from a structural scanner. Mark unavailable native rendering or untested clients explicitly. Update a result only after rerunning the relevant case and inspecting the output.
