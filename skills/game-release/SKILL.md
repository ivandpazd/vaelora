---
name: game-release
description: "Trigger: export, build, platform, packaging, release, signing, CI, store submission, migration, performance. Validate deliverables without claiming unsupported targets."
license: Apache-2.0
metadata:
  author: "vaelora"
  version: "1.0"
---

## Activation Contract
Load for project bootstrap, exports, CI, packaging, signing, release readiness, platform validation, or delivery incidents.

## Stage Scope
Primary: stages 0 and 5; supports stages 2–4. Platform assumptions must be identified at foundation and proven before release claims.

## Hard Rules
- Confirm engine/export behavior from current official documentation before locking configuration.
- Keep credentials and signing material out of the repository and logs.
- Validate actual packaged builds on Android, Windows, macOS, Linux, and Web as applicable.
- Do not claim release readiness from a local export, editor run, or unverified store artifact.

## Decision Gates
- Build config: document target, reproducibility, artifact, and required checks.
- Platform failure: preserve logs, isolate adapter/config causes, and record supported scope.
- Release: require test battery, docs, versioning, provenance, and rollback evidence.

## Execution Steps
1. Identify target, source revision, environment, and acceptance gate.
2. Build in a reproducible isolated environment.
3. Validate launch, input, saves, performance, and packaging on the target.
4. Record artifacts and limitations; follow the branch promotion workflow.

## Output Contract
Return revision, target, build command, artifact identity, checks, environment, limitations, and release decision.

## References
- `docs/technical/architecture-proposal.md`
- `docs/project/development-workflow.md`
- `docs/production/production-plan.md`
