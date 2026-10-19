# GitHub Readiness Checklist

This file records the local preparation and the verified GitHub configuration as of 2026-10-19.

## Prepared in the repository

- [x] Issue forms for bug reports, feature requests, and design decisions.
- [x] Issue chooser configuration.
- [x] Pull-request template.
- [x] Contributor and branch/commit/PR guidance.
- [x] Root repository hygiene for the planned Godot project: generated-file ignores, text line endings, and editor defaults.
- [x] Proprietary rights notice for original Vaelora materials in `LICENSE`.
- [x] README and `docs/` navigation.
- [x] Foundation files merged to the repository default branch and available to GitHub.
- [x] Required labels used by the current workflow exist: `status:approved`, `type:docs`, and `size:exception`.
- [ ] Broader label catalog and project board — optional; do not add them speculatively.

## Initial publication/bootstrap

The repository's default branch is `main`. GitHub reads issue-form and PR-template files from the default branch, as described in [GitHub's template documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates). The one-time foundation bootstrap is complete: the templates are on `main`, and `dev` is the published integration branch. Normal work now follows `feature/<issue>-<slug>` → `dev` → `main`.

## Verified repository settings

- Visibility: **public**.
- Default branch: `main`.
- `Protect main` ruleset (ID `25234621`): active; pull requests required; branch deletion and force-push blocked; review conversations must be resolved; zero outside approvals; no required CI checks yet.
- `Protect dev` ruleset (ID `25234622`): active with the same protections; the `dev` branch is published.
- Bypass actors: none configured.

GitHub's Terms of Service allow users to view and fork a public repository through GitHub's functionality. The proprietary notice reserves broader reuse rights but does not make public content private or remove GitHub's platform permissions. See [GitHub's licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

## Remaining repository setup

### Branches and rulesets

- [x] Keep `main` as the default/stable branch.
- [x] Create/publish `dev` from the approved foundation baseline.
- [x] Add a ruleset for `main`: require PRs, block force pushes and deletion, and require resolved review conversations.
- [x] Add a ruleset for `dev`: require PRs, block force pushes and deletion, and require resolved review conversations.
- [x] Preserve the two-stage review flow: feature PRs merge into `dev`; after technical and documentation review, promote `dev` to `main` with a separate PR.
- [x] Initially require zero outside approvals while this is a solo-maintainer project. Revisit when collaborators can independently review.
- [ ] Do not configure required status check names until the matching workflow has completed successfully; then select the exact job name.
- [ ] Allow only narrowly justified bypass actors. Avoid blanket administrator bypass for ordinary changes.

GitHub branch protections and rulesets are repository settings, not files in this checkout. Current GitHub documentation describes the available rules and PR requirements in [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) and [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

### Issues and project tracking

- [x] Confirm the default branch contains `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md`.
- [x] Create the labels required by the current issue/PR workflow before using them.
- [ ] Suggested minimal label groups: `type:bug`, `type:feature`, `type:design`, `type:docs`; `area:gameplay`, `area:tech`, `area:art`, `area:repo`; `priority:high`, `priority:normal`, `priority:low`; `status:needs-decision`, `status:blocked`.
- [ ] Consider a single GitHub Project board with `Backlog`, `Ready`, `In progress`, `Review`, and `Done` only after the issue backlog exists.
- [ ] Create milestones around deliverables, not arbitrary dates: repository foundation, design lock, two-civilization prototype, prototype validation, civilization expansion.
- [ ] Keep issue labels and project columns lightweight; use the issue body and links for detailed context.

The current issue forms do not assign labels automatically. Labels are applied deliberately during issue/PR triage so the repository does not silently depend on an incomplete catalog.

### Merge and release settings

- [x] Keep the configured merge methods available to the solo maintainer; use the repository PR title and merge method that preserve a reviewable Conventional Commit history.
- [ ] Add CI only after the Godot project skeleton and a real test/check command exist; then require the exact successful workflow check on `dev` and `main`.
- [ ] Decide whether final art assets need Git LFS after representative source files and expected asset sizes are known; do not add LFS rules or storage assumptions speculatively.
- [ ] Disable automatic deployment until platform exports, signing, and release checks are approved.
- [ ] Set release/version policy before the first packaged build.
- [x] Add a proprietary `LICENSE` notice for original Vaelora materials; third-party materials remain under their own terms.
- [ ] Add a `SECURITY.md`, code of conduct, or public support link only after choosing the appropriate project policy.

## Current verified state

- `main` is the public default branch and contains the issue forms, PR template, contributor guidance, and repository foundation.
- `dev` is published and protected by ruleset `25234622`; `main` is protected by ruleset `25234621`.
- PR #2 merged the foundation into `dev` as `0057a59ba9346a56bba90022adf9e52c5af79e2e`; issue [#1](https://github.com/ivandpazd/vaelora/issues/1) is closed.
- GitGuardian passed on PR #2. No Godot project or repository CI workflow exists yet, so no additional required CI checks are configured.
- The normal path is `feature/<issue>-<slug>` → `dev` → `main`. Feature PRs close their concrete issue; the promotion PR from `dev` to `main` does not require an intermediate issue.
- Optional labels, project-board columns, release automation, Git LFS, and packaged-build policy remain intentionally unconfigured until their need is demonstrated.
