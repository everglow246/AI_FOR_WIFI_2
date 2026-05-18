# Codex Changelog

## 2026-05-18 - Add account-switch handoff

Changed files:

- `ai_handoff/ACCOUNT_SWITCH_HANDOFF.md`
- `ai_handoff/README_AI_HANDOFF.md`
- `ai_handoff/LATEST_STATUS.md`
- `ai_handoff/CODEX_CHANGELOG.md`
- `ai_handoff/NEXT_PLAN.md`
- `ai_handoff/REPORTS_INDEX.json`
- `ai_handoff/ARTIFACT_MANIFEST.json`
- `scripts/validate_ai_handoff.py`

Behavior/documentation changes:

- Added a dedicated handoff for a new Codex account.
- Expanded the account-switch handoff with project state, decisions, mistakes to avoid, completed/unfinished Codex work, next steps, and core reward/data/CQL/coverage_v0/controlled_v1 logic.
- Recorded that GitHub `main` is pushed at `2d1e9ad`, but actual project source code remains local and untracked.
- Recorded local chat provenance paths as optional only, not as the stable project handoff.
- Added `ACCOUNT_SWITCH_HANDOFF.md` to the validator's required file list and marker checks.

No MATLAB rerun, CQL training, experimental data generation, large-file upload, or raw data upload was performed.

## 2026-05-18 - Prepare first safe GitHub publish

Changed files:

- `AGENTS.md`
- `scripts/validate_ai_handoff.py`
- `ai_handoff/LATEST_STATUS.md`
- `ai_handoff/CODEX_CHANGELOG.md`
- `ai_handoff/NEXT_PLAN.md`

Behavior/documentation changes:

- Added the branch workflow rule: stable branch is `main`; future Codex implementation work should use `feature/codex-<short-task-name>`.
- Fixed the handoff validator missing-artifact sentinel to ASCII-safe `"\u672a\u751f\u6210"`.
- Recorded that the target GitHub repository `everglow246/AI_FOR_WIFI_2` exists and that first publish should include only handoff and publishing guard files.

Validation before commit:

- `D:\AI_for_wifi\.venvs\wifi_phase3\Scripts\python.exe -m py_compile scripts\validate_ai_handoff.py`
- `D:\AI_for_wifi\.venvs\wifi_phase3\Scripts\python.exe scripts\validate_ai_handoff.py`
- `git diff --cached --name-only`

Validation result:

- `scripts/validate_ai_handoff.py`: PASS
- `py_compile`: PASS
- staged-file whitelist check: PASS

No MATLAB rerun, CQL training, experimental data generation, or large-file upload was performed.

## 2026-05-17 - Add handoff validation script and publish guards

Changed files:

- `scripts/validate_ai_handoff.py`
- `.gitignore`
- `ai_handoff/LATEST_STATUS.md`
- `ai_handoff/CODEX_CHANGELOG.md`
- `ai_handoff/REPORTS_INDEX.json`
- `ai_handoff/ARTIFACT_MANIFEST.json`
- `ai_handoff/NEXT_PLAN.md`

Behavior/documentation changes:

- Added a local validation script for `ai_handoff/` required files, JSON parsing, indexed path existence, forbidden large/binary handoff files, and latest run/report/blocker markers.
- Strengthened `.gitignore` for `raw_steps.jsonl`, NPZ datasets, PyTorch checkpoints, checkpoint directories, raw candidate/episode JSONL files, and MATLAB binary/runtime artifacts.
- Recorded that GitHub publishing is still blocked by missing `origin` remote.
- Ran `D:\AI_for_wifi\.venvs\wifi_phase3\Scripts\python.exe scripts\validate_ai_handoff.py`; result: PASS.

No MATLAB rerun, CQL training, experimental data generation, GitHub push, or large-file upload was performed.

## 2026-05-17 - Add GitHub handoff directory

Changed files:

- `ai_handoff/README_AI_HANDOFF.md`
- `ai_handoff/LATEST_STATUS.md`
- `ai_handoff/CODEX_CHANGELOG.md`
- `ai_handoff/CURRENT_DECISIONS.md`
- `ai_handoff/KNOWN_ISSUES.md`
- `ai_handoff/NEXT_PLAN.md`
- `ai_handoff/REPORTS_INDEX.json`
- `ai_handoff/RUNS_INDEX.json`
- `ai_handoff/ARTIFACT_MANIFEST.json`
- `AGENTS.md`
- `.gitignore`

Behavior/documentation changes:

- Added a GitHub-facing handoff entry point for reviewers and ChatGPT.
- Recorded the current project status without claiming formal CQL performance.
- Recorded that coverage_v0 is a historical calibration, reward/candidate diagnostic, and regression asset only.
- Recorded that the 2026-05-17 cleanup did not rerun MATLAB, retrain CQL, or recompute reward.
- Added a maintenance rule requiring future Codex tasks to update handoff status and indexes.
- Added `.gitignore` protection so raw JSONL, NPZ, checkpoint, MATLAB, zip, and `raw_steps.jsonl` artifacts are not copied into `ai_handoff/`.

Commands used for this handoff:

- `git status --short --branch`
- `git remote -v`
- `Get-Content` on current reports and decision documents
- `Get-FileHash -Algorithm SHA256` on indexed artifacts
- JSONL line counting with .NET `System.IO.File.ReadLines`
- NPZ shape inspection for `coverage_v0_transition_dataset.npz`

No MATLAB rerun, CQL training, data regeneration, or GitHub push was performed.

## Maintenance Rule

After every future Codex task that changes code, reports, data artifacts, decisions, or project status, update these together:

- `LATEST_STATUS.md`
- `CODEX_CHANGELOG.md`
- `REPORTS_INDEX.json`
- `ARTIFACT_MANIFEST.json`
- `NEXT_PLAN.md`
