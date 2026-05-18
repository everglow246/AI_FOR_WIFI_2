# AI Handoff Entry Point

This directory is the GitHub-facing project handoff for external reviewers and ChatGPT. It summarizes the real local project state without requiring large generated artifacts.

## Read Order

1. `LATEST_STATUS.md` for the current truth boundary.
2. `CURRENT_DECISIONS.md` for Action3P, state, reward, and data rules.
3. `KNOWN_ISSUES.md` for blockers and non-claims.
4. `NEXT_PLAN.md` for the next safe work sequence.
5. `REPORTS_INDEX.json`, `RUNS_INDEX.json`, and `ARTIFACT_MANIFEST.json` for machine-readable pointers.

## Current Headline

- Current project: `D:\AI_for_wifi\AI_FOR_WIFI_2`
- Current algorithm direction: Action3P CQL / MDP-lite offline RL diagnostics.
- Latest completed run: `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/`
- Latest completed run status: historical calibration, reward/candidate diagnostic, and regression asset only.
- MATLAB status: the original coverage_v0 run performed MATLAB simulation/replay; the 2026-05-17 report cleanup did not rerun MATLAB.
- CQL status: loader/loss/interface smoke only; no formal CQL training or effectiveness result has been produced.
- Reward status: `reward_final = G_norm * (1 - PER) - 0.1 * T_norm` is a PHY/link diagnostic reward, not a real full-MAC reward or final performance claim.

## Most Important Local Reports

These reports are generated/local artifacts and may be ignored by Git unless intentionally unignored later.

- `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/run_manifest.json`
- `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/metadata.json`
- `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/coverage_v0_global_validator_post_reward.md`
- `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/coverage_v0_transition_dataset_report.md`
- `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/coverage_v0_cql_loader_smoke_report.md`
- `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/coverage_v0_policy_diagnostic_smoke_report.md`
- `reports/decisions/controlled_v1_plan.md`
- `reports/decisions/report_cleanup_summary_20260517.md`

## What To Do Next

Do not start large-scale CQL training yet. First implement and rerun controlled_v1 with fixed geometry and seed metadata, then run a reproducible CQL loader/smoke that saves checkpoint, selected action ids, Q summaries, and selected-action replay diagnostics.

## GitHub Boundary

Do not upload raw JSONL data, NPZ datasets, MATLAB outputs, model checkpoints, or full `raw_steps.jsonl` files. Large or generated artifacts are recorded in `ARTIFACT_MANIFEST.json` with hashes and upload status.
