# Development Workflow

## Branch model

The project uses a three-level flow: **`main` → `dev` → short-lived feature branches**.

| Branch | Role | Receives changes from |
|---|---|---|
| `main` | Stable, reviewed project state; release candidates and tagged releases originate here | PRs from `dev` |
| `dev` | Integration branch for the next development cycle | PRs from `feature/*`, `fix/*`, and `docs/*` |
| `feature/<issue>-<slug>` | New game behavior/content for one issue | Starts from and returns to `dev` |
| `fix/<issue>-<slug>` | A scoped correction | Starts from and returns to `dev` |
| `docs/<issue>-<slug>` | Documentation-only work | Starts from and returns to `dev` |
| `hotfix/<issue>-<slug>` | Urgent correction to a released `main` build | Starts from `main`; after the main PR, back-merge to `dev` |

Examples: `feature/42-city-growth`, `fix/58-road-movement`, `docs/31-combat-rules`. Use lowercase kebab-case and include the issue number whenever an issue exists.

### Change flow

1. Open or select an issue and confirm its acceptance criteria.
2. Create a short-lived branch from `dev` (or from `main` for an urgent release hotfix).
3. Commit a coherent work unit using Conventional Commits.
4. Open a PR to `dev`; link the issue, describe player-visible behavior, and provide tests/screenshots/platform evidence as relevant.
5. Address review feedback and verify the final candidate.
6. Merge approved feature PRs into `dev`.
7. After each feature PR is merged, review the integrated `dev` state for technical correctness and documentation quality before promoting it. Use the [integration review gate](#integration-review-gate).
8. Only when that review passes, open a separate release/integration PR from `dev` to `main`; review the complete promotion diff and release checklist before merging it.
9. If the integration review finds a problem, keep `main` unchanged. Create a corrective branch from `dev`, send its PR to `dev`, merge it after review, and repeat the integration review.
10. Back-merge urgent hotfixes from `main` to `dev` so the fix is not lost in ongoing work.

GitHub Issue Forms and PR templates are stored in `.github/`. GitHub only displays these templates after they are committed to the repository's default branch; use the initial bootstrap release path in the [GitHub readiness checklist](github-readiness.md).

## Conventional Commits

Every commit message follows:

```text
<type>[optional scope][!]: <description>

[optional body]
[optional footer(s)]
```

Use a concise, imperative description and lowercase type/scope. Recommended types:

| Type | Use |
|---|---|
| `feat` | Player-visible gameplay feature or content |
| `fix` | Bug correction |
| `docs` | Documentation-only change |
| `test` | Test additions or corrections |
| `refactor` | Internal restructuring without behavior change |
| `perf` | Performance improvement |
| `build` | Build/export configuration or tooling |
| `ci` | Continuous integration workflow |
| `chore` | Repository maintenance |
| `revert` | Reverts a prior commit |

Examples:

```text
feat(city): add gradual territory growth
fix(combat): keep a winning defender on its tile
docs(game-design): clarify city capture rules
build(android): configure landscape export preset
chore(repo): add issue and pull request templates
```

For breaking changes, add `!` before the colon or a `BREAKING CHANGE: <description>` footer. Use `Refs: #123` for work that should not close an issue; use `Closes #123` only when the PR completes that issue. Do not add Co-Authored-By or AI attribution to commits.

The Conventional Commits format is documented at [conventionalcommits.org](https://www.conventionalcommits.org/en/v1.0.0/). The exact project-approved type catalog is the table above; new types should be added here before broad use.

## Issues

Use the matching issue form for bugs, feature proposals, or unresolved design decisions. Before opening a new issue, search for an existing open or closed issue covering the same behavior. An issue should include:

- One problem, decision, or outcome.
- Context and motivation, without prescribing unrelated implementation.
- Observable acceptance criteria.
- Dependencies or affected systems where known.
- A clear open question where a product decision is still required.

Do not use issues to silently approve TBD game rules. A design proposal remains open until the user accepts it and the canonical docs are updated.

## Pull requests

- Feature/fix/docs PRs target `dev`; release/integration PRs target `main`.
- Use the repository PR template. Link issues and state whether the change closes or only references them.
- Explain the player-facing outcome and what is intentionally out of scope.
- Include focused automated tests and complete relevant checks; passive documentation changes need structural/link validation.
- For game behavior, include a manual test scenario and affected platform/export coverage. For visual changes, include screenshots or a short capture when practical.
- Update the relevant docs in the same work unit as behavior or content changes.
- Keep each PR reviewable. Split independent work by behavior or system rather than by file type.
- Resolve review conversations and ensure required checks pass before merge.
- Use the repository's configured merge method; until it is set, do not assume squash/rebase/merge policy.

## Integration review gate

Every feature/fix/docs PR is reviewed and merged into `dev` first. Then evaluate the resulting integrated `dev` branch before opening a `dev` → `main` PR:

- **Technical review:** check the change against the intended architecture and game rules; run the focused tests and the applicable project checks/builds; inspect platform impact and any known limitations.
- **Documentation review:** confirm the README and relevant design/technical docs match the behavior, links work, unresolved decisions remain explicit, and the PR provides enough context to maintain the change.
- **Decision:** record the outcome. If either review finds a blocker, fix it through another PR to `dev` and repeat the gate. Do not promote a known-bad integration state.
- **Promotion PR:** after both reviews pass, create a distinct PR from `dev` to `main`. Include the promoted change range, review outcome, test/build evidence, and release notes or a concise change summary. Merge only after this PR's checks and final diff review pass.

This gate is a required human review step. The remote repository currently has active `main` and `dev` rulesets that require PRs, block force-pushes and deletion, and require resolved review conversations. No CI checks are required yet because the Godot project and its test workflow are not in place.

## Initial solo-maintainer policy

The repository currently has one known owner. Require pull requests for `main` and `dev`, but do not require an approval from another person until an independent reviewer exists; an impossible approval rule would block the owner. Add required status checks after a stable CI workflow exists and its exact job name has passed on the target branch. Keep force-push and branch deletion disabled for `main`; protect `dev` against accidental force-push as well.

## Releases

Release versioning, release notes, signing, store submission, and version-number policy are open until the first executable build. Do not create a release or claim platform support from a local export alone; test the actual packaged build on each declared target.
