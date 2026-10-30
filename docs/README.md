# Vaelora Documentation

This directory is the project's documentation hub. The root [README](../README.md) is the concise project home; these documents hold the detailed, reviewable source of truth.

## Reading path

1. [Product vision and scope](product/vision-and-scope.md) — what Vaelora is and what the first complete prototype includes.
2. [Game Design Document](game-design/game-design-document.md) — confirmed match and gameplay rules.
3. [World and civilizations](game-design/world-and-civilizations.md) — setting tone, history, and faction concepts.
4. [Open design decisions](game-design/open-decisions.md) — values and rules that must be resolved before they can be implemented.
5. [Technical architecture proposal](technical/architecture-proposal.md) — a proposed implementation structure and cross-platform validation plan.
6. [Automated testing strategy](technical/testing-strategy.md) — selected GUT runner, deterministic fixtures, and test boundaries.
7. [CI, export, and release pipeline](technical/ci-release-pipeline.md) — approved CI checks, unsigned exports, release signing, versioning, and approval boundaries.
8. [Production plan](production/production-plan.md) — sequencing, prototype acceptance, and the civilization expansion gate.
9. [Development workflow](project/development-workflow.md) — branch model, commits, issues, and pull requests.
10. [GitHub readiness](project/github-readiness.md) — remote settings and activation checklist.

## Source-of-truth rules

- **Confirmed** means the user has accepted the direction in the design conversation.
- **Proposal** means a technical or production recommendation that still needs validation; it is not a settled gameplay rule.
- **Open** means a decision, number, or constraint is not yet defined. Do not silently fill it in during implementation.
- When a new decision changes a confirmed rule, update the relevant source document and issue/PR references together.
- Prefer one canonical detailed section plus links over copying long, potentially divergent specifications into several documents.

## GitHub contribution references

- [Development workflow](project/development-workflow.md)
- [GitHub readiness checklist](project/github-readiness.md)
- [Issue form chooser](../.github/ISSUE_TEMPLATE/config.yml)
- [Pull request template](../.github/PULL_REQUEST_TEMPLATE.md)
