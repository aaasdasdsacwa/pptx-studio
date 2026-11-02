# Design references and scope

Reviewed on 2026-10-29: [guizang-ppt-skill README](https://github.com/op7418/guizang-ppt-skill), [SKILL.md](https://github.com/op7418/guizang-ppt-skill/blob/main/SKILL.md), and [LICENSE](https://github.com/op7418/guizang-ppt-skill/blob/main/LICENSE).

The reference emphasizes HTML slide delivery with two visual systems. Its useful design lesson is to connect the brief, page plan, visual system, asset treatment, speaker support and verification as a complete authoring process. It is a reference for workflow thinking, not a claim that its runtime or templates are included here.

PPTX Studio independently implements purpose-aware presentation instructions and a brief-recording helper. This change does not copy the reference project's code, templates, text, runtime or visual assets. The referenced project identifies its license as AGPL-3.0; the existing license of this project remains unchanged.

## Choices for this project

- The audience's purpose and source material determine the storyline. The scenario examples remain open and combinable.
- Visual style is independent of purpose. User branding, arbitrary colors and references are accepted.
- Complete creation is the primary entry alongside scoped editing and audit. Icons remain optional.
- Editable PPTX remains the target for PPTX requests. No HTML presenter runtime, social-cover generator or format-conversion guarantee is implied by the reference.
- Clarifications are proportional to actual missing information. A complete brief proceeds to the deliverable without a mandatory extra approval gate.
- Authoring instructions, script tests, model-behavior evaluations and final-file visual evidence are reported separately. A broader scenario guide is not proof that all scenarios have been tested.
