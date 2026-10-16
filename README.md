# Vaelora

**Vaelora** is a 2D, turn-based fantasy strategy game in preproduction. Build a civilization across a hexagonal world: found cities, claim and improve territory, choose what each city produces, research a shared technology tree, and compete for victory against an AI rival.

The game takes place on the continent of Vaelora, where generations of political disputes and neglected infrastructure weakened **the Trama**, an old network of roads and signal beacons. Rival civilizations now expand, develop their settlements, and contest the routes and resources that connect them.

> **Project status:** preproduction. The design and collaboration foundation is being documented before gameplay implementation. The initial complete prototype targets the human **Liga de Auren** and orc **Clanes de Brasal**. It must use final-quality visual assets; placeholder art is out of scope.

> **Rights:** Vaelora's original materials are proprietary; all rights are reserved by Iván de Paz Delgado. See [LICENSE](LICENSE). Because this repository is public, GitHub's Terms of Service still permit viewing and forking through GitHub; the notice does not grant broader reuse rights.

## At a glance

| Area | Current direction |
|---|---|
| Genre | Accessible turn-based strategy with city development, research, exploration, and tactical combat |
| Players | Local single-player against one AI opponent initially |
| Map | Procedurally generated, seeded, hexagonal, fixed-isometric 2D |
| Platforms | Android, Windows, macOS, Linux, and Web from the start |
| Engine | Godot with GDScript |
| Presentation | Landscape orientation; bright, luminous fantasy art |
| Prototype civilizations | Human Liga de Auren and orc Clanes de Brasal |
| Match types | Turn-limited score, total conquest, full-tree knowledge, and combined victory |

## What makes the game distinct

Vaelora keeps the board and turn structure readable while making cities active strategic centers rather than passive score markers. Each city develops from the resources and improvements in its assigned territory, grows up to level 6, and runs one production project at a time: a unit **or** a building. Civilization-wide research unlocks capabilities, while roads connect cities and improve movement and economic growth. Civilizations share most of their technology foundation but specialize in different ways.

## How a match works

1. Choose a civilization, match type, map type/size, and difficulty. The AI civilization and map seed are selected automatically.
2. Explore with units and manage fog of war; settle with settlers and assign tiles to cities.
3. Improve terrain with limited-use workers, connect cities with roads, and balance growth, income, production, and research.
4. Finish your turn; the AI then takes its turn separately. Production and research progress once per civilization turn.
5. Pursue the selected victory condition: outscore the rival at the turn limit, conquer the rival's cities, finish the whole knowledge tree, or whichever of conquest/research happens first.

## Project documentation

Start with the [documentation index](docs/README.md) for the complete map of project and game documents.

### Product and game

- [Product vision and scope](docs/product/vision-and-scope.md) — audience assumptions, product goals, constraints, and non-goals.
- [Game Design Document](docs/game-design/game-design-document.md) — the agreed gameplay baseline and links to deeper system specifications.
- [World and civilizations](docs/game-design/world-and-civilizations.md) — Vaelora, the Trama, and the planned civilization identities.
- [Open design decisions](docs/game-design/open-decisions.md) — implementation-blocking questions and balance values that still need decisions.

### Delivery and technology

- [Technical architecture proposal](docs/technical/architecture-proposal.md) — proposed Godot structure, simulation boundaries, saves, input, and platform validation.
- [Production plan](docs/production/production-plan.md) — phases, prototype scope, and the test gate before adding civilizations.
- [Development workflow](docs/project/development-workflow.md) — `main` → `dev` → feature branches, Conventional Commits, issues, and PRs.
- [GitHub readiness checklist](docs/project/github-readiness.md) — repository settings and setup steps that must be completed on GitHub.
- [Contributing guide](.github/CONTRIBUTING.md) — short entry point for contributors.

## Branch and review model

- `main` is the stable line.
- `dev` is the integration line.
- Short-lived `feature/<issue>-<slug>`, `fix/<issue>-<slug>`, and `docs/<issue>-<slug>` branches start from `dev` and merge back into `dev` by pull request.
- After feature PRs merge into `dev`, review the integrated branch for technical correctness and documentation quality; only then open a separate `dev` → `main` promotion PR.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

The repository is public, with active pull-request rulesets on `main` and `dev`; the `dev` branch itself has not yet been published. Issue forms and pull-request templates become active on GitHub only after their files reach the repository's default branch. See the [readiness checklist](docs/project/github-readiness.md) for the initial bootstrap and remaining settings.

## First prototype boundary

The first complete prototype is a two-civilization game, not a reduced rules demo: it should contain the agreed match modes and full initial gameplay systems for the human and orc civilizations. The remaining four planned civilizations are considered only after the prototype passes its final test battery. No online multiplayer, campaign progression, city renaming, or additional initial combat classes are currently in scope.

## Start here

- New to the project? Read the [product vision](docs/product/vision-and-scope.md), then the [Game Design Document](docs/game-design/game-design-document.md).
- Planning implementation? Review the [open decisions](docs/game-design/open-decisions.md) and [technical proposal](docs/technical/architecture-proposal.md).
- Preparing a contribution? Read the [development workflow](docs/project/development-workflow.md) and [GitHub readiness checklist](docs/project/github-readiness.md).
