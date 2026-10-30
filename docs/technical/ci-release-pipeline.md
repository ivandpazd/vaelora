# CI, Export, and Release Pipeline

**Status:** Approved Stage 0 pipeline policy, resolved under issue #25. This document defines repeatable checks and release boundaries; it does not claim CI workflows, export presets, or signing credentials are already configured.

## Pipeline

```text
Pull request to dev or main; push to dev/main; manual CI dispatch
  ├─ Static checks: GDScript formatting + documentation whitespace
  ├─ Godot checks: editor import/parse + deterministic GUT suite
  └─ Non-production export smoke matrix: Windows / macOS / Linux / Android / Web
       └─ Upload per-target CI artifacts (14-day retention; no production signing)

Maintainer manually dispatches a release from main
  └─ Protected release environment approval
       └─ Signed release-candidate artifacts, if signing secrets are configured
            └─ Human-controlled publication; no automatic deployment
```

The initial pipeline uses no dependency or editor-cache restore. Godot import state is derived from the exact source and pinned engine; avoiding a cache keeps the first CI baseline simple and prevents stale imported resources from obscuring failures. CI artifacts are immutable per run; missing expected exports fail the job. The PR author owns diagnosis and correction of failed checks. The maintainer owns protected-environment approval, secret configuration, and release disposition.

## Required checks and triggers

- Run the same validation pipeline for feature PRs targeting `dev` and promotion PRs targeting `main`; also run after pushes to `dev` and `main` and on manual CI dispatch.
- Keep GitGuardian as the existing required repository check. Do not require the new CI check until the pipeline has completed successfully on both protected branches and its exact GitHub check name has been observed.
- Then require the aggregate check `Vaelora CI / Validate` on both `dev` and `main`. Keep prior branch protections unchanged while establishing this baseline.
- If a check is broken or renamed, restore the prior workflow/check name or have a maintainer remove only the stale CI requirement through the normal repository process. Never weaken PR, review-conversation, force-push, or deletion protections. Re-enable the exact check only after a successful run on the target branch.

## Local and CI commands

Run from the repository root with Godot **4.7.2 stable** (`4.7.2.stable.official.ed1daf0bf`). CI installs this exact editor version and its matching official export templates.

| Check | Local command | CI behavior |
|---|---|---|
| GDScript formatting | `gdformat --check game/content/ game/tests/` | Install the same pinned package and run `gdformat --check game/content/ game/tests/`; never format source in CI. |
| Documentation whitespace | `git diff --check <base-ref>...HEAD` | Run against the PR base SHA and candidate HEAD; any whitespace error fails validation. |
| Godot import and script parse | `godot --headless --editor --path game --quit` | Run with the pinned editor before GUT; preserve output and exit status. |
| Deterministic GUT suite | `godot --headless --path game --script res://addons/gut/gut_cmdln.gd -gdir=res://tests -gpost_run_script=res://tests/require_tests_hook.gd -gexit` | Run unchanged from repository root; zero tests, script errors, or failed assertions fail validation. |
| Export smoke | Use the five commands below | Run only when the matching preset and runner prerequisites are present; any failed export or missing file fails that target job. |

Install the GDScript formatter in an isolated Python virtual environment with `python3 -m pip install "gdtoolkit==4.5.0"`; it is pinned to stable 4.5.0. Update it only through reviewed tooling changes and keep local and CI versions identical. The listed paths are the current project-owned GDScript directories; extend the same check when new first-party script directories are added, and do not apply it to vendored `game/addons/gut/`. Godot import is not a substitute for GUT, and neither is platform runtime evidence.

## Export targets and non-production smoke commands

Export preset names are stable workflow identifiers. Presets use the project Compatibility renderer and CI uses debug exports for smoke testing. CI carries no production signing certificates or secrets; Godot/platform-required debug or ad-hoc signing is allowed only for non-production smoke artifacts. Godot's headless exporter requires the editor binary and matching export templates; Android additionally requires the documented Android SDK/JDK prerequisites. Output paths below are relative to `game/project.godot`, and the output directory must exist.

Create the ignored output directory before exporting: `mkdir -p game/builds`.

| Preset | Target | CI artifact | Smoke command |
|---|---|---|---|
| `Windows Desktop` | Windows x86_64 | `builds/vaelora-windows-{sha}.exe` | `godot --headless --path game --export-debug "Windows Desktop" "builds/vaelora-windows-{sha}.exe"` |
| `macOS Universal` | macOS universal application archive; no Developer ID signing/notarization in CI | `builds/vaelora-macos-{sha}.zip` | `godot --headless --path game --export-debug "macOS Universal" "builds/vaelora-macos-{sha}.zip"` |
| `Linux/X11` | Linux x86_64 | `builds/vaelora-linux-{sha}.x86_64` | `godot --headless --path game --export-debug "Linux/X11" "builds/vaelora-linux-{sha}.x86_64"` |
| `Android APK` | Android arm64 APK using only the non-production debug keystore | `builds/vaelora-android-{sha}.apk` | `godot --headless --path game --export-debug "Android APK" "builds/vaelora-android-{sha}.apk"` |
| `Web` | WebAssembly/WebGL 2.0 browser export | `builds/vaelora-web-{sha}.zip` | `godot --headless --path game --export-debug "Web" "builds/vaelora-web-{sha}.zip"` |

`{sha}` is the full checked-out commit SHA. CI names each artifact `vaelora-{target}-{sha}`, retains it for **14 days**, and fails if expected output is absent. Do not upload signing material, editor caches, or hidden files. A successful export proves packaging only; the Stage 2 platform smoke matrix in the production plan remains required.

## Signing, versioning, and release approval

- PR and branch CI uses debug exports only. It has no production signing secrets and cannot publish a release or deploy. Platform-required debug/ad-hoc signatures are confined to disposable non-production smoke artifacts.
- A release is explicitly started by a maintainer from `main` using `workflow_dispatch`, with a `vMAJOR.MINOR.PATCH` tag identifying the reviewed source. Version increments follow Semantic Versioning; no automated version bump or mutable `latest` artifact is produced.
- The release job waits on a GitHub protected environment named `release-approval`. A maintainer's environment approval is required before the job can read environment-scoped signing secrets. Workflow approval is not permission to publish to a store or deploy.
- Release signing credentials stay only in protected CI environment secrets. Never commit certificates, keystores, passwords, provisioning profiles, or signing identities. Configure only credentials for targets actually being signed. An absent secret fails closed for that signed target; it must not silently fall back to debug/ad-hoc output as a release.
- Signed candidate artifact names are `vaelora-{target}-{version}-{sha}`. Retain approved, published release files as GitHub release assets; keep temporary candidates for at most 14 days. Publication and store deployment remain separate, explicit maintainer actions and are not automated.
- No production secrets are needed for local checks, PR CI, or debug/ad-hoc export smoke tests.

## Platform and release limits

Export success does not certify launch, input, save durability, performance, accessibility, browser behavior, signing validity, or store acceptance. Record target/device/browser and build-specific runtime evidence under the Stage 2 and Stage 4 gates. Keep platform-specific export prerequisites and limitations visible in workflow logs; never claim platform support from an editor run or export alone.

Godot 4.7 documents that macOS exports without code signing/notarization are blocked by Gatekeeper, and that Google Play uploads require a non-debug keystore. CI therefore produces test artifacts only: macOS exports are not Developer ID signed or notarized, and Android uses only its non-production debug keystore. These outputs are not install/release evidence. See [Godot's macOS export guidance](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_for_macos.html) and [Android export guidance](https://docs.godotengine.org/en/4.7/tutorials/export/exporting_for_android.html).

## References

- [Automated Testing Strategy](testing-strategy.md)
- [Technical Architecture Proposal — Cross-platform validation](architecture-proposal.md#cross-platform-validation)
- [Production Plan — Stage 2 platform smoke matrix](../production/production-plan.md#2-godot-foundation-and-vertical-slice)
- [Godot 4.7 command-line tutorial](https://docs.godotengine.org/en/4.7/tutorials/editor/command_line_tutorial.html)
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [GitHub Actions artifact retention](https://github.com/actions/upload-artifact/tree/v4#usage)
