# GitHub Readiness Checklist

This file distinguishes repository content already prepared locally from settings that still need to be applied on GitHub. It is not a claim that the remote repository is configured.

## Prepared in the repository

- [x] Issue forms for bug reports, feature requests, and design decisions.
- [x] Issue chooser configuration.
- [x] Pull-request template.
- [x] Contributor and branch/commit/PR guidance.
- [x] README and `docs/` navigation.
- [ ] Files merged to the repository default branch — required before GitHub presents the issue forms and PR template.
- [ ] GitHub labels and project board — proposed vocabulary is below; do not assign labels that have not been created.

## Initial publication/bootstrap

The repository's default branch is `main`. GitHub reads issue-form and PR-template files from the default branch, not from an arbitrary feature branch, as described in [GitHub's template documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates). Therefore the initial foundation needs a one-time bootstrap path: review and merge the project-foundation changes to `main`, then create or fast-forward `dev` from that stable baseline. After bootstrap, ordinary feature PRs target `dev`, and release/integration PRs target `main`.

If the initial foundation is first merged into `dev`, the forms will not be available until the later `dev` → `main` PR is merged. This delay is expected and does not require changing the default branch to `dev`.

## Repository settings to apply

### Branches and rulesets

- [ ] Keep `main` as the default/stable branch.
- [ ] Create/publish `dev` from the approved foundation baseline.
- [ ] Add a ruleset for `main`: require PRs, block force pushes and deletion, require resolved review conversations, and require passing CI once a stable CI check exists.
- [ ] Add a ruleset for `dev`: require PRs from feature branches and block force pushes/deletion; require CI once available.
- [ ] Initially require zero outside approvals while this is a solo-maintainer project. Revisit when collaborators can independently review.
- [ ] Do not configure required status check names until the matching workflow has completed successfully; then select the exact job name.
- [ ] Allow only narrowly justified bypass actors. Avoid blanket administrator bypass for ordinary changes.

GitHub branch protections and rulesets are repository settings, not files in this checkout. Current GitHub documentation describes the available rules and PR requirements in [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) and [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

### Issues and project tracking

- [ ] Confirm the default branch contains `.github/ISSUE_TEMPLATE/` and `.github/PULL_REQUEST_TEMPLATE.md`.
- [ ] Create agreed labels before any form is configured to apply labels automatically.
- [ ] Suggested minimal label groups: `type:bug`, `type:feature`, `type:design`, `type:docs`; `area:gameplay`, `area:tech`, `area:art`, `area:repo`; `priority:high`, `priority:normal`, `priority:low`; `status:needs-decision`, `status:blocked`.
- [ ] Consider a single GitHub Project board with `Backlog`, `Ready`, `In progress`, `Review`, and `Done` only after the issue backlog exists.
- [ ] Create milestones around deliverables, not arbitrary dates: repository foundation, design lock, two-civilization prototype, prototype validation, civilization expansion.
- [ ] Keep issue labels and project columns lightweight; use the issue body and links for detailed context.

The issue forms currently do not assign labels because the remote label catalog has not been reviewed or created.

### Merge and release settings

- [ ] Select one merge method after deciding how Conventional Commits should appear in the stable history. Squash merge makes the PR title become the main-branch commit subject; if selected, require Conventional Commit PR titles.
- [ ] Disable automatic deployment until platform exports, signing, and release checks are approved.
- [ ] Set release/version policy before the first packaged build.
- [ ] Add a `SECURITY.md`, license, code of conduct, or public support link only after choosing the appropriate project policy; none is invented by this foundation.

## Not performed yet

The local feature branch has not been pushed; no issue or PR has been created; no remote branch, label, project board, ruleset, default-branch setting, or merge policy has been changed. These require the initial changes to be reviewed and deliberately published.
