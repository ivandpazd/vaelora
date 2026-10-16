# Vaelora GitHub and documentation foundation
Objective: complete the project's documentation hub and prepare GitHub collaboration conventions before gameplay implementation.
Branch: `feature/github-foundation` | Delivery: `feature-branch-chain` (feature PRs target `dev`; `dev` is the integration path to `main`) | Test runner: Markdown/link readback and Ruby YAML parse for GitHub form files.

## Specs

### S1 — Complete product and game design documentation
- Authorized scope: expand the repository's documentation so product intent, gameplay systems, world/civilizations, and unresolved design decisions are discoverable and cross-linked. Document approved decisions faithfully; mark undecided values as open instead of inventing them.
- User request (verbatim): “Además, tenemos que tener una documentación super completa de absolutamente todo y debe de estar también en el repositorio ya sea en una carpeta de docs o similar.”
- Acceptance: the `docs/` source of truth distinguishes confirmed requirements, proposals, and TBDs; every local Markdown link resolves.
- Checks: structural readback, link checks, compare against accepted design memories, no invented values.

### S2 — GitHub issue and pull-request templates
- Authorized scope: add GitHub YAML Issue Forms, issue chooser configuration, a pull-request template, and contributor instructions that standardize actionable reports and reviews without inventing repository labels or licenses.
- User request (verbatim): “Si, deberíamos preparar de forma muy profesional primero Github, para tener un sistema de issues, PRs, etc. La idea es tener el entorno preparado antes de empezar a desplegar.”
- Acceptance: forms are valid GitHub issue-form YAML; template submission data is actionable; PR guidance explains expected evidence and review; templates are located in GitHub-supported paths.
- Checks: parse each YAML file and verify required form keys/relative links.

### S3 — Technical, production, and repository workflow guidance
- Authorized scope: document the proposed Godot architecture and production phases, plus Conventional Commits and the requested `main` → `dev` → feature-branch model, including branch naming, base branch, PR targets, release integration, and the bootstrap caveat for enabling templates on GitHub's default branch.
- User request (verbatim): “Quiero utilizar conventional-commits para git, y me gustaría tener un esquema main - dev (rama previa) - features”
- Acceptance: technical recommendations are distinct from approved game rules; workflow treats `main` as stable, `dev` as integration, and feature branches as short-lived branches based on `dev`; commit message examples follow Conventional Commits; GitHub-only branch rules are presented as a setup checklist, not falsely claimed as configured.
- Checks: verify examples and current local branch names; distinguish local setup from remote settings.

### S4 — General project README
- Authorized scope: make the root README the clear project home, with a complete but scannable explanation of the game, its scope, status, rules at a glance, documentation links, and contribution path.
- User request (verbatim): “Y todo asociado y bien explicado a nivel proyecto y videojuego en el README.md general.”
- Acceptance: the README makes the project understandable without duplicating the full specifications and all local links resolve.
- Checks: heading and link readback against the documentation tree.

## Tasks
- [x] T1 — S1: Complete product and game design documentation — inline — complete — commit: `2356f96`.
- [x] T2 — S2: Add GitHub issue/PR forms and contribution guidance — inline — complete — commit: `a13f246`; Ruby YAML parsing and `git diff --cached --check` passed.
- [x] T3 — S3: Add technical, production, and branch/commit guidance — inline — complete — commit: `4428367`; Markdown link check passed.
- [x] T4 — S4: Complete general README and cross-document navigation — inline — complete — commit: pending.

## Log
- L7: T3 completed in `4428367`, documenting the Godot architecture proposal, production phases, local branch/PR workflow, Conventional Commits, and GitHub settings checklist. Assessment: medium risk, `under_budget`, no review due.
- L6: T1 and T2 completed locally. T2 commit `a13f246` adds three issue forms, chooser configuration, PR template, and contributor guidance; YAML parsing passed. RDD assessment for T2: medium risk, `under_budget`, no review due.
- L1 (2026-10-16): “Si, deberíamos preparar de forma muy profesional primero Github, para tener un sistema de issues, PRs, etc. La idea es tener el entorno preparado antes de empezar a desplegar. Además, tenemos que tener una documentación super completa de absolutamente todo y debe de estar también en el repositorio ya sea en una carpeta de docs o similar. Y todo asociado y bien explicado a nivel proyecto y videojuego en el README.md general. Quiero utilizar conventional-commits para git, y me gustaría tener un esquema main - dev (rama previa) - features”
- L2: User confirmed full authority to work in the local Vaelora repository using the connected GitHub session. Repository-specific remote operations remain limited by explicit delivery rules; this task will prepare local files and branches, not push or open a PR.
- L3: Local `dev` was created at the prior documentation work; current feature branch `feature/github-foundation` is based on `dev`. Plan selects `feature-branch-chain`, directly reflecting the requested `main` → `dev` → features flow.
- L4: Official GitHub documentation says issue forms live in `.github/ISSUE_TEMPLATE` and become available only after reaching the repository default branch. Keep `main` as the stable default; document an initial bootstrap path because later feature PRs target `dev`.
- L5: Evidence: [GitHub issue and PR template docs](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates) state templates must be on the default branch; [GitHub ruleset docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) cover PR and required-check settings; [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) defines commit structure.
