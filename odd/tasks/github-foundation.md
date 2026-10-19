# Vaelora GitHub and documentation foundation
Objective: complete the project's documentation hub and prepare GitHub collaboration conventions before gameplay implementation.
Branch: `docs/github-foundation` | Delivery: `feature-branch-chain` (all changes use `feature/<issue>-<slug>` branches; feature PRs target `dev`; `dev` is the only source for promotion to `main`) | Test runner: Markdown/link readback and Ruby YAML parse for GitHub form files.

## Specs

### S1 — Complete product and game design documentation
- Authorized scope: expand the repository's documentation so product intent, gameplay systems, world/civilizations, and unresolved design decisions are discoverable and cross-linked. Document approved decisions faithfully; mark undecided values as open instead of inventing them.
- User request (verbatim): “Además, tenemos que tener una documentación super completa de absolutamente todo y debe de estar también en el repositorio ya sea en una carpeta de docs o similar.”
- Acceptance: the `docs/` source of truth distinguishes confirmed requirements, proposals, and TBDs; every local Markdown link resolves.
- Checks: structural readback, link checks, compare against accepted design memories, no invented values.

### S2 — GitHub issue and pull-request templates
- Authorized scope: add GitHub YAML Issue Forms, including a dedicated project-foundation task form, issue chooser configuration, a pull-request template, and contributor instructions that standardize actionable reports and reviews without inventing repository labels or licenses.
- User request (verbatim): “Si, deberíamos preparar de forma muy profesional primero Github, para tener un sistema de issues, PRs, etc. La idea es tener el entorno preparado antes de empezar a desplegar.”
- Acceptance: forms are valid GitHub issue-form YAML; the project-foundation form captures context, scope, and acceptance criteria; template submission data is actionable; PR guidance explains expected evidence and review; templates are located in GitHub-supported paths.
- Checks: parse each YAML file and verify required form keys/relative links.

### S3 — Technical, production, and repository workflow guidance
- Authorized scope: document the proposed Godot architecture and production phases, plus Conventional Commits and the requested feature-branch → `dev` → `main` model, including branch naming, base branch, PR targets, issue closure, a required technical/documentation review of integrated `dev` before a separate promotion PR to `main`, and the bootstrap caveat for enabling templates on GitHub's default branch.
- User request (verbatim): “Quiero utilizar conventional-commits para git, y me gustaría tener un esquema main - dev (rama previa) - features”
- Acceptance: technical recommendations are distinct from approved game rules; workflow treats `main` as stable, `dev` as integration, and feature branches as short-lived branches based on `dev`; feature PRs target `dev`, the integrated `dev` state receives a technical and documentation review, and only a passing review leads to a separate `dev` → `main` PR; commit message examples follow Conventional Commits; remote ruleset status is documented accurately.
- Checks: verify examples and current local branch names; distinguish local setup from remote settings.

### S4 — General project README
- Authorized scope: make the root README the clear project home, with a complete but scannable explanation of the game, its scope, status, rules at a glance, documentation links, and contribution path.
- User request (verbatim): “Y todo asociado y bien explicado a nivel proyecto y videojuego en el README.md general.”
- Acceptance: the README makes the project understandable without duplicating the full specifications and all local links resolve.
- Checks: heading and link readback against the documentation tree.

### S5 — Proprietary rights notice
- Authorized scope: add a root `LICENSE` notice identifying the sole developer and reserving all rights to original Vaelora content, without claiming rights over third-party materials or overriding GitHub's Terms of Service.
- User request (verbatim): “Vale, lo primero es agregar licencia (no se puede utilizar por terceros)” and “El juego se va a llamar Vaelora, y el desarrollador único soy yo: Iván de Paz Delgado con email: ivandpazd@gmail.com”
- Acceptance: the notice states that no license is granted for third-party use of original project materials without written permission; identifies Iván de Paz Delgado and the supplied contact email; explicitly scopes third-party materials to their own licenses and acknowledges GitHub hosting terms.
- Checks: verify rights-holder spelling/email, plain-text readback, and `git diff --check`; do not present the text as legal advice.

### S6 — GitHub visibility and branch rulesets
- Authorized scope: configure the remote repository visibility and protective rules for the established `main` → `dev` workflow, then document the verified remote state in the repository readiness guide.
- User request (verbatim): “Vale, pues si es así, mejor lo dejamos público y remarcamos en la licencia el uso para poder aplicar las reglas”
- Acceptance: repository visibility and active `main`/`dev` rulesets are verified from GitHub; each ruleset requires pull requests, blocks deletion and force-pushes, and requires review-thread resolution without requiring unavailable CI checks or an additional reviewer.
- Checks: read back repository visibility and each ruleset by ID; document the published `dev` branch and the current promotion policy.

## Tasks
- [x] T1 — S1: Complete product and game design documentation — inline — complete — commit: `2356f96`.
- [x] T2 — S2: Add GitHub issue/PR forms and contribution guidance — inline — complete — commit: `a13f246`; Ruby YAML parsing and `git diff --cached --check` passed.
- [x] T3 — S3: Add technical, production, and branch/commit guidance — inline — complete — commits: `4428367`, `aa6cbb9`; Markdown links passed.
- [x] T4 — S4: Complete general README and cross-document navigation — inline — complete — commit: `b3387a9`; local Markdown links validated.
- [x] T5 — S5: Add proprietary rights notice — inline — complete — commit: `9e26a33`; holder/contact and `git diff --check` verified; assessment: medium, under budget.
- [x] T6 — S3, S6: Configure and document public GitHub repository and main/dev rulesets — inline — complete — commit: `9e26a33`; rulesets `25234621` and `25234622` verified and documented; `main` and `dev` are published; assessment: medium, under budget.
- [x] T7 — S2: Add a dedicated project-foundation YAML issue form — inline — complete — commit: `986c6b8`; YAML structure and chooser config parsed, whitespace check passed; assessment: medium, under budget.
- [x] T8 — S2, S6: Publish the project-foundation form on protected `main` through a one-commit, user-scoped bootstrap bypass, then remove that bypass — inline — complete — remote commit `3d32821`; ruleset restored active with zero bypass actors; independent verification pending.
- [x] T9 — S6: Publish the integration and foundation branches to GitHub — inline — complete — remote refs `dev` and `docs/github-foundation` verified at their pushed commits; task record: `6d226ef`.
- [x] T10 — S2, S6: Create the foundation issue and complete the linked PR/merge path — inline — complete — issue `#1` closed after PR `#2`; PR `#2` merged into `dev` as `0057a59`; GitGuardian passed; `type:docs` and `size:exception` were applied.

## Log
- L12 (2026-10-16): “Vale, pues si es así, mejor lo dejamos público y remarcamos en la licencia el uso para poder aplicar las reglas”
- L13 (2026-10-16): “El juego se va a llamar Vaelora, y el desarrollador único soy yo: Iván de Paz Delgado con email: ivandpazd@gmail.com”
- L14: The remote repository is public; active `Protect main` and `Protect dev` rulesets were verified as IDs `25234621` and `25234622`. `dev` is not yet present on the remote. A proprietary rights notice is the remaining local work; exact holder identity is now confirmed.
- L15: Added a proprietary rights notice naming Iván de Paz Delgado and the supplied email. It reserves reuse rights in original Vaelora materials while explicitly preserving applicable law, GitHub's public-repository terms, and third-party licenses. Updated the README and readiness/workflow guides to reflect verified remote settings. An independent legal review remains advisable because the repository is public and the notice is not legal advice.
- L16: Local links passed for all three changed Markdown files; focused holder/contact/GitHub-terms assertions and `git diff --check` passed. Commit `9e26a33` assessed as medium risk, `under_budget`; no native review was due. The candidate excludes unrelated pre-existing untracked editor configuration files.
- L17: Task-record commit `ea25263` assessed as passive, no review due.
- L18 (2026-10-18): “Si, perfecto” — confirmation to prepare a dedicated YAML form for project-foundation issues and resolve its publication to `main`.
- L19: Current GitHub `main` has no `.github/ISSUE_TEMPLATE` directory while two active rulesets require PRs; the form must first be added to a feature branch, then published through an authorized bootstrap path. No bypass of `main` protection is assumed.
- L20: Added `.github/ISSUE_TEMPLATE/project_foundation.yml` with required context, scope, and acceptance criteria plus optional dependencies/references. YAML parsing and `git diff --check` passed. Commit `986c6b8` assessed medium, `under_budget`; native review was not due. The Engram mirror remains pending because the runtime did not register a session identity; no agent-attributed memory write was attempted.
- L21: Pushed `dev` and `docs/github-foundation` to `origin`; both remote branch creations succeeded. The new issue form is on `docs/github-foundation` but is not yet available on GitHub's default branch. PR creation remains blocked until a valid approved issue can be created and the form is published to `main`.
- L22: `git ls-remote` confirmed remote `dev` at `37324d6f62d1f24b7d2ce946a73e370d345fdc5e` and `docs/github-foundation` at `6d226efbfb5d34ece14110bac0f863cc50ad6ab3`; task-record commit `6d226ef` assessed passive, no review due.
- L23 (2026-10-18): “ok pues haz el trabajo, la idea es que tu puedas crear un listado grande de issues sin mi autorización, crear ramas, asociar Prs a issues.. y hacer merge”. The user delegates issue creation, branch creation, PR association, and merging for this project without per-operation confirmation.
- L24 (2026-10-18): “permito crear un desarrollo de más de 400 líneas para este caso ya que es un comienzo de proyecto”. The initial foundation PR may exceed the 400-line review budget under this explicit project-start exception; document the rationale and apply the required exception label.
- L25: Published `.github/ISSUE_TEMPLATE/project_foundation.yml` to `main` in one commit (`3d32821`) using a temporary bypass restricted to the authenticated user; the bypass was removed immediately. Read-back confirmed the file blob and `Protect main` active with zero bypass actors. GitHub's REST ruleset API supports user-scoped bypass actors and audited `always` mode (see GitHub REST ruleset documentation). Independent verification pending.
- L26: Created `https://github.com/ivandpazd/vaelora/issues/1` from the now-active Project foundation task form after an open-and-closed duplicate search returned no matches. Target-host read-back confirmed title, body, open state, and no labels (`confirmed`).
- L27: The user authorized autonomous creation of project issues, branches, PR association, and merge. Issue `#1` still needs the protected `status:approved` action and the exact `Closes` versus `Refs` choice required by the PR workflow before a PR can be created; no labels or PRs have been added yet.
- L28 (2026-10-18): Independent verification passed the published bootstrap. Corrected stale current-state statements: `dev` exists, the foundation form is on `main`, and issue `#1` is open; PR creation and merge remain unfinished.
- L29 (2026-10-18): The user explicitly authorized creating and applying `status:approved` to issue `#1`. Created the repository label (`0e8a16`); the single issue-label attempt was rejected by GitHub with `403 Resource not accessible by integration`. Target-host read-back confirmed issue `#1` remains open with no labels. No retry was made; integration write access is required before continuing.
- L30 (2026-10-19): PR `#2` merged the foundation into `dev` as `0057a59`; GitGuardian passed; issue `#1` was closed explicitly because GitHub does not auto-close a `Closes #1` reference when the target branch is non-default `dev`. The repository now uses only `feature/<issue>-<slug>` branches for changes into `dev`; `main` accepts only promotion PRs from `dev`, with no intermediate issue.
- L9 (2026-10-16): “Vale, la idea es crear siempre PR de la feature a dev, después ir a la rama dev, hacer una valoración técnica y de documentación, y si todo está correcto se debe crear otra PR de dev a main”
- L10: Reopened only T3 to make the post-merge `dev` technical/documentation review and the separate `dev` → `main` promotion PR explicit; no other task or game rule changed.
- L11: Verified the local Markdown links and whitespace check; 14 Markdown files scanned with zero broken local links. T3 follow-up assessment: medium risk, `under_budget`, no review due.
- L8: T4 completed in `b3387a9`; the root README now acts as project overview and navigation hub. Final RDD assessment: passive, no review due. No GitHub remote settings, issues, branches, or PRs were changed.
- L7: T3 completed in `4428367`, documenting the Godot architecture proposal, production phases, local branch/PR workflow, Conventional Commits, and GitHub settings checklist. Assessment: medium risk, `under_budget`, no review due.
- L6: T1 and T2 completed locally. T2 commit `a13f246` adds three issue forms, chooser configuration, PR template, and contributor guidance; YAML parsing passed. RDD assessment for T2: medium risk, `under_budget`, no review due.
- L1 (2026-10-16): “Si, deberíamos preparar de forma muy profesional primero Github, para tener un sistema de issues, PRs, etc. La idea es tener el entorno preparado antes de empezar a desplegar. Además, tenemos que tener una documentación super completa de absolutamente todo y debe de estar también en el repositorio ya sea en una carpeta de docs o similar. Y todo asociado y bien explicado a nivel proyecto y videojuego en el README.md general. Quiero utilizar conventional-commits para git, y me gustaría tener un esquema main - dev (rama previa) - features”
- L2: User confirmed full authority to work in the local Vaelora repository using the connected GitHub session. Repository-specific remote operations remain limited by explicit delivery rules; this task will prepare local files and branches, not push or open a PR.
- L3: Local `dev` was created at the prior documentation work; current feature branch `feature/github-foundation` is based on `dev`. Plan selects `feature-branch-chain`, directly reflecting the requested `main` → `dev` → features flow.
- L4: Official GitHub documentation says issue forms live in `.github/ISSUE_TEMPLATE` and become available only after reaching the repository default branch. Keep `main` as the stable default; document an initial bootstrap path because later feature PRs target `dev`.
- L5: Evidence: [GitHub issue and PR template docs](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates) state templates must be on the default branch; [GitHub ruleset docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) cover PR and required-check settings; [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) defines commit structure.
