# General decision issues — Vaelora
Objective: resolve and document issues #22, #23, #17, #18, #28, and #27 on one feature branch.
Branch: `feature/22-23-17-18-28-27-general-decisions`; delivery: one feature PR to `dev`; test runner: GUT 9.7.1 for behavior changes, structural checks for passive decision documentation.

## Specs

### S1 — Issue #22 device-parity decision
- **Authorized scope:** Record the user's confirmed interaction and display decisions in the canonical design and architecture documents; do not change authoritative gameplay rules.
- **Selected contract:** Shared presentation with adaptive input/device profiles, not duplicated screens; landscape only, 4:3–21:9; compact logical viewport 960×540 at 16:9 or 720×540 at 4:3, standard 1280×720, wide 1920×1080; validate at 200% UI scale; keep interactive controls, text, focus and confirmations inside platform safe areas while the map may extend beneath cutouts; known-illegal actions are not offered; rejection feedback is contextual and non-modal, preserves focus/selection and authoritative state, and explains the reason using text plus redundant visual feedback.
- **Preserved existing contract:** Shared action vocabulary and validated command path, existing device bindings, focus order, 48 logical-pixel targets, and 100–200% scaling remain unchanged.
- **Acceptance:** GDD, architecture proposal, decision register, and Stage 1 gate consistently state the selected contract and measurable viewport/safe-area/rejection checks without claiming implementation or platform conformance.
- **Checks:** Markdown/link consistency and `git diff --check`; no runtime test applies unless authorized behavior code is actually in scope.

### S2 — Issue #23 save/persistence decision
- **Authorized scope:** Record the user's confirmed persistence contract in canonical design, architecture, and QA documentation; do not introduce a production save system beyond the approved Stage 1 decision scope.
- **Selected contract:** Current schema plus two prior schemas load through explicit sequential migrations; older schemas remain preserved but are not auto-loaded. `schema_version` is a positive integer incremented only for persisted format changes requiring migration; `game_build` is independent. Envelope metadata is separate from authoritative payload; exclude scene nodes and transient presentation/input state. SHA-256 hexadecimal covers canonical JSON for the complete envelope except the checksum field and detects corruption, not deliberate tampering. Stable slot IDs are `manual_1`, `manual_2`, `manual_3`, `autosave`, and `autosave_backup`. Manual overwrite requires confirmation. Stage writes in the same directory, flush, reopen and validate before atomic replacement; rotate backup only from a valid autosave; on any failure preserve the last valid autosave and backup. A corrupt save and active match remain unchanged; offer the backup only when autosave validation fails, never silently. Migrate older saves in memory and do not rewrite the source until an explicit save or later autosave. Reject newer schemas without changing the save or active match. Web uses local `user://` persistence without cross-device/cloud or browser-data-recovery promises; report write failures and preserve the last valid save. Test every supported source schema and migration step through public load, including state correctness and preservation on failure.
- **Acceptance:** GDD, architecture proposal, decision register, QA strategy, and Stage 1 gate agree on envelope, compatibility, write/recovery, platform limits, and observable migration tests; no unsupported durability or tamper-resistance claims.
- **Checks:** Markdown/link consistency and `git diff --check`; no runtime test applies unless authorized behavior code is actually in scope.

### S3 — Issue #17
- **Scope and acceptance:** Pending independent issue review and user-confirmed decision; do not infer requirements.

### S4 — Issue #18
- **Scope and acceptance:** Pending independent issue review and user-confirmed decision; do not infer requirements.

### S5 — Issue #28
- **Scope and acceptance:** Pending independent issue review and user-confirmed decision; do not infer requirements.

### S6 — Issue #27
- **Scope and acceptance:** Pending independent issue review and user-confirmed decision; do not infer requirements.

## Tasks
- T1 — S1; route: inline; status: documentation complete; commit: pending.
- T2 — S2; route: inline; status: documentation complete; commit: pending.
- T3 — S3; route: inline after decision; status: pending user decisions; commit: pending.
- T4 — S4; route: inline after decision; status: pending user decisions; commit: pending.
- T5 — S5; route: inline after decision; status: pending user decisions; commit: pending.
- T6 — S6; route: inline after decision; status: pending user decisions; commit: pending.

## Log

- L1 — User request: “Ahora creo que podríamos trabajar en la 22, 23, 17, 18, 28 y 27 issues todas en una misma rama. Será una rama de decisión general. Así completaríamos todo. Se permitirá un size:exception en el código. Para ello, preguntame todo lo que necesites de cada una de las decisiones de forma independiente para confirmar todo y que quede totalmente definido de forma profesional según nuestras skills personalizadas para el proceso, tú y yo.”
- L2 — User authorized writing the complete repository files/code for each decision issue immediately after it is fully defined, then continuing with the next issue's questions. Issues #22 and #23 are fully defined; #17, #18, #28, and #27 remain pending their independent decision conversations.
- L3 — User authorized fetching `dev` from `origin` using the configured Git credential session. Local `dev` was behind `origin/dev`; created this feature branch from fetched `origin/dev` commit `19f1d66`.
- L4 — Updated the canonical GDD, open-decision register, architecture proposal, production plan, and testing strategy for #22/#23. `git diff --check` passed; a relative-link check passed for all five changed Markdown documents. No runtime test or gameplay code applies at the Stage 1 decision-documentation boundary; dependent behavior remains gated for later stages.
