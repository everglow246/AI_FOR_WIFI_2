# Latest Status

Generated: 2026-05-18T13:35:25+08:00

## Current State

- GitHub handoff files were prepared for a first safe GitHub commit.
- GitHub connector login observed in this session: `everglow246`.
- Target GitHub repository exists: `everglow246/AI_FOR_WIFI_2`, default branch `main`.
- GitHub `main` was pushed successfully and contains the first safe handoff commit plus the preserved remote README.
- Current local and remote handoff commit: `2d1e9ad`.
- Current source tree contains Action3P Python, MATLAB, scripts, validators, tests, and decision documents.
- Current generated report/data layout uses `reports/runs/`, `reports/decisions/`, and `reports/archive/`.
- `scripts/validate_ai_handoff.py` now exists as a lightweight pre-push validator for handoff completeness and path integrity.
- Latest handoff validation before account-switch update: PASS with `D:\AI_for_wifi\.venvs\wifi_phase3\Scripts\python.exe scripts\validate_ai_handoff.py`.
- Account-switch handoff exists at `ai_handoff/ACCOUNT_SWITCH_HANDOFF.md`.

## Latest Completed Run

- run_id: `run_001_coverage_v0_action3p_reward_fullstep`
- local path: `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/`
- original created_at: `2026-05-15T21:07:35+08:00`
- original MATLAB simulation/replay: yes, according to `run_manifest.json`
- report cleanup reran MATLAB: no
- report cleanup retrained CQL: no
- report cleanup recomputed reward: no
- scenarios: `S1-S6`
- speeds: `0.4`, `0.6`, `0.8` m/s
- action_count: `432`
- candidate rows: `77760`
- transition count: `180`
- behavior policy: `stratified_random_legal`
- candidate mode: `full_per_step`
- packets_per_action: `20`

## What Is Complete

- Action3P code and configuration exist for the three RL action fields: `mcs`, `target_apep_length_bytes`, and `tx_power_dbm`.
- Fixed-CSD formal gate fields are present in current coverage_v0 reports, with fixed profile `he_su_2tx_2nss_fixed_csd_nonbf_nostbc`.
- The post-reward validator report passed core integrity checks but still issued coverage_v0 warnings.
- A transition dataset was built with `180` transitions, `23` state features, action space size `432`, and zero invalid actions in the dataset report.
- CQL loader/loss smoke ran and passed as an interface check.

## What Is Not Complete

- No formal CQL training result exists.
- No CQL effectiveness or deployment performance claim exists.
- No controlled_v1 MATLAB rerun has been completed after the controlled geometry/seed plan.
- coverage_v0 is not valid for speed-only causal conclusions.
- Current reward remains a PHY/link diagnostic reward, not a final full-MAC reward.
- The prior CQL smoke did not save checkpoint, selected action ids, per-state Q values, or selected-action replay percentile tables.

## Current Data Reuse Boundary

coverage_v0 may be reused for:

- historical calibration
- reward/candidate diagnostics
- regression tests
- CQL loader/interface smoke as a historical asset

coverage_v0 must not be used for:

- controlled_v1 speed-only causal conclusions
- final all-scenario best-action records
- formal CQL performance proof
- offline RL effectiveness proof
- strict controlled geometry comparison
- full plus/minus 3 m back-and-forth validation

## Latest Report Pointers

- Latest completed run manifest: `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/run_manifest.json`
- Latest run metadata: `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/metadata.json`
- Latest post-reward validator: `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/coverage_v0_global_validator_post_reward.md`
- Latest transition dataset report: `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/coverage_v0_transition_dataset_report.md`
- Latest CQL smoke report: `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/coverage_v0_cql_loader_smoke_report.md`
- Latest policy diagnostic smoke report: `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/coverage_v0_policy_diagnostic_smoke_report.md`

## Safe To Proceed?

Not safe for large-scale CQL training yet. Next blockers are controlled_v1 MATLAB rerun, controlled geometry validation, seed metadata validation, and a reproducible CQL smoke that saves the missing replay artifacts.

For GitHub publishing, the first safe handoff commit was pushed. Future source publication still needs a separate whitelist review. No MATLAB rerun, CQL training, new experiment data generation, or large-file upload is part of the account-switch handoff step.

For account switching, a new Codex should start from `ai_handoff/ACCOUNT_SWITCH_HANDOFF.md`. It should not rely on old local chat logs as the primary project state.
