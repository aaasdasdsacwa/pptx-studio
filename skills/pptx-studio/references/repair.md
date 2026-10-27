# Targeted repairs

Inspect the user's latest file, not an earlier generated version. Locate the reported page and objects before changing them. Reproduce or establish the fault through the best available evidence: the target application, a direct rendering, and structural inspection.

Typical causes include duplicate text layers, text-box overflow, cell margins/paragraph spacing, group transforms, hidden/stacked objects, altered fonts, broken relationships, and unintended image crops. Treat scanner overlap warnings as candidates, not authorization to delete objects.

For a table/text overlap, determine which object owns the intended content. A table with body text plus identical overlaid text boxes often has two authoritative layers. Remove a redundant layer only after confirming its text, position, and role. Repeated labels in different non-overlapping cells are normal.

Change the smallest relevant part and preserve unrelated slides and the user's intervening edits. Keep a recoverable input. Verify the affected page and any shared resource changed by the fix.

If a generator caused the error and its source is in scope, correct that cause as well: preview drawing should not mutate the production slide; shape IDs remain unique; group coordinates use their actual transforms. Otherwise repair the artifact and report the source-side limitation.

Completion: the identified fault is corrected, required content is retained once, and the verification result distinguishes structural checks from actual rendering.
