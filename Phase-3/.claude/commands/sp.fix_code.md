---
description: Analyze, diagnose, and fix code bugs or inconsistencies while ensuring cross-file compatibility and reliability.
---

## Fix Purpose

**CRITICAL CONCEPT**: Fixing code is a surgical operation that requires 100% certainty about the root cause. A "fix" that only silences a symptom while breaking other files is a failure.

## User Input

```text
$ARGUMENTS
```

## Execution Steps

1. **Environmental Audit**:

   - Run `.specify/scripts/bash/check-prerequisites.sh --json` from repo root to load the active feature context.
   - Use `find` and `grep` to locate the failure point (e.g., specific file, line number, or error message).
   - Read the relevant code block plus 50 lines above and below for context.

2. **Root Cause Analysis (RCA)**:

   - Identify WHY the bug exists (race condition, null pointer, syntax error, logic flaw).
   - Check the `history/prompts/` logs for recent changes that might have introduced the bug.
   - Cross-reference with `spec.md` and `plan.md` to ensure the fix doesn't violate established business rules.

3. **Compatibility Trace (The "Blast Radius")**:

   - **MANDATORY**: Search for all usages of any modified function, class, or data structure.
   - Check for:
     - Broken imports
     - Type mismatches
     - Changed API response shapes
     - Database schema inconsistencies (if applicable)

4. **Remediation & Verification Plan**:

   - Propose the code fix.
   - **Verification Requirement**: Each fix MUST be verified. Plan the following:
     - Test execution command (e.g., `npm test`, `pytest`).
     - Manual check steps (e.g., "Reload dashboard and verify task counts").
     - **Verification Script**: If no automated test exists, you MUST run a one-liner script (e.g., `node -e '...'` or `python -c '...'`) to dry-run the logic. This ensures the fix is compatible and works fine with other file code.

5. **Implementation**:

   - Apply the edits accurately.
   - Use `ls` or `dir` to ensure no temporary files or `__pycache__` artifacts are left behind.
   - Update `tasks.md` to reflect the bug fix if it's a significant diversion from the original plan.

6. **Confidence Check**:
   - Re-run the verification plan from step 4.
   - Verify that all related files (identified in step 3) still compile/execute correctly.
   - **Final compatibility check**: Explicitly verify that the fix is compatible and works fine with other file code in the feature directory.

## Output Report

- **Diagnosis**: Concise explanation of the bug and its cause.
- **Fixed Files**: List of modified artifacts.
- **Verification Result**: Summary of tests run and proof of success.
- **Compatibility Note**: Confirmation that neighbor files are unaffected and the fix works fine with other file code.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1. Determine Stage

   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2. Generate Title and Determine Routing:

   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3. Create and Fill PHR (Shell first; fallback agent‑native)

   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4. Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.
