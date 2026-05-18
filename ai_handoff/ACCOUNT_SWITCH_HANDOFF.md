# Account Switch Handoff

Generated: 2026-05-18T13:35:25+08:00

## Can A New Codex Take Over?

Partly, but not from chat history alone.

A new Codex can take over from GitHub for the published handoff state, because `main` contains:

- `README.md`
- `.gitignore`
- `AGENTS.md`
- `ai_handoff/*`
- `scripts/validate_ai_handoff.py`

A new Codex cannot fully reconstruct all local project code from GitHub yet. The core project code, MATLAB files, scripts, tests, and some reports are still local untracked files in `D:\AI_for_wifi\AI_FOR_WIFI_2` and were intentionally not included in the first safe GitHub publish.

Local Codex chat logs exist, but they are not the primary handoff mechanism. They are large, account/tool-state dependent, and may not be automatically available to a different account. Use this file and the rest of `ai_handoff/` as the stable handoff.

## Start Here

For a new Codex on this machine:

```powershell
cd D:\AI_for_wifi\AI_FOR_WIFI_2
git status --short --branch
git log --oneline --decorate --graph --all --max-count=8
python scripts\validate_ai_handoff.py
```

Read in this order:

1. `AGENTS.md`
2. `ai_handoff/ACCOUNT_SWITCH_HANDOFF.md`
3. `ai_handoff/README_AI_HANDOFF.md`
4. `ai_handoff/LATEST_STATUS.md`
5. `ai_handoff/CURRENT_DECISIONS.md`
6. `ai_handoff/KNOWN_ISSUES.md`
7. `ai_handoff/NEXT_PLAN.md`

## One Page Project State

- GitHub currently contains the safe handoff/publishing layer, not the full local codebase.
- Local project root: `D:\AI_for_wifi\AI_FOR_WIFI_2`.
- Current direction: Action3P CQL / MDP-lite offline RL diagnostics.
- Latest completed run: `reports/runs/run_001_coverage_v0_action3p_reward_fullstep/`.
- Latest run size: `77760` candidate rows, `180` transitions, `432` actions.
- MATLAB status: original `coverage_v0` run performed simulation/replay; handoff/report-cleanup work did not rerun MATLAB.
- CQL status: loader/loss/interface smoke only; no formal CQL training or effectiveness result.
- Reward status: current `reward_final` is PHY/link diagnostic only, not real full-MAC reward evidence.
- GitHub publish status: initial safe handoff was pushed to `everglow246/AI_FOR_WIFI_2`; source publication still needs a separate whitelist review.

## Decisions Already Made

- Action3P has exactly three RL action fields: `mcs`, `target_apep_length_bytes`, and `tx_power_dbm`.
- HE-SU, 2Tx/2NSS, GI `1.6 us`, and fixed TxMode `he_su_2tx_2nss_fixed_csd_nonbf_nostbc` are fixed for the current formal path.
- Current action grid is `12 x 6 x 6 = 432`.
- Active scenarios are `S1-S6`; `S7` is reserved and must not enter current formal datasets or loader smoke.
- Formal state should use receiver-observed telemetry and controller memory only.
- Scenario labels, geometry, speed, positions, wall/corner losses, link-budget SNR, future reward, and candidate-best/sweep-best fields must not enter formal no-time RL state.
- Candidate rows are counterfactual sweep outcomes and are not formal CQL transitions.
- Formal transitions must come from one logged behavior action with `(state_t, action_t, reward, state_t1, done)`.
- Large/generated files stay out of GitHub and are recorded in `ARTIFACT_MANIFEST.json`.

## Do Not Repeat These Mistakes

- Do not rely on local chat history as the project source of truth.
- Do not run `git add .`.
- Do not force-push over GitHub `main`.
- Do not upload raw JSONL, NPZ datasets, MATLAB binary outputs, checkpoints, zip bundles, or `raw_steps.jsonl`.
- Do not treat loader/loss CQL smoke as algorithm performance.
- Do not treat `coverage_v0` as controlled_v1 speed-only causal evidence.
- Do not convert all candidate rows into CQL transitions with synthetic next states.
- Do not call `target_apep_length_bytes` full MAC aggregation time.
- Do not claim MATLAB simulation/replay as real AP measurement.
- Do not run large CQL training until controlled_v1 and reproducible smoke gates are clear.

## Codex Completed

- Created `ai_handoff/` as the GitHub-facing handoff entry.
- Added `scripts/validate_ai_handoff.py`.
- Added GitHub publishing guards in `.gitignore` and `AGENTS.md`.
- Published the first safe handoff commit to GitHub without uploading raw data or large artifacts.
- Added this account-switch handoff so a new Codex can restart from project files instead of chat logs.

## Codex Not Completed

- Full local source code has not been reviewed or published to GitHub.
- controlled_v1 generator patch has not been completed in this handoff step.
- controlled_v1 MATLAB rerun has not been performed.
- `reward_final` has not been recomputed for a new controlled_v1 run.
- Formal CQL training has not been run.
- Reproducible CQL smoke with saved checkpoint, selected action ids, Q summaries, and replay percentile diagnostics is still missing.

## Core Logic Snapshot

Reward:

- Current formula: `reward_final = G_norm * (1 - PER) - 0.1 * T_norm`.
- `G_norm` and `T_norm` must use calibration-derived constants.
- This is a PHY/link diagnostic reward using goodput, PER, and HE-SU airtime proxy.
- It is not a final full-MAC reward and does not include real queue latency, real retry count, ACK/backoff/retransmission-inclusive airtime, switch penalty, or standalone power penalty.

Data collection:

- Current logged behavior policy for the reward-fullstep path is `stratified_random_legal`.
- Candidate sweeps are side-channel diagnostics for sweep-best, regret, reward ranking, and coverage.
- Formal CQL datasets must be built from logged behavior transitions only.
- The formal no-time profile must avoid geometry/time/speed/debug leakage.

CQL smoke:

- Existing CQL status is loader/loss/interface smoke only.
- Existing smoke is useful for interface sanity, not performance.
- Next smoke must save enough replay artifacts to audit selected actions and Q summaries.

`coverage_v0`:

- Reusable as historical calibration, reward/candidate diagnostic, regression asset, and CQL loader/interface historical asset.
- Not valid for controlled_v1 speed-only causal conclusions, final best-action claims, formal CQL performance proof, offline RL effectiveness proof, or strict controlled geometry comparison.

`controlled_v1`:

- Next formal dataset direction.
- Must fix geometry, full back-and-forth trajectory phase, and stride-separated seed metadata before rerun.
- Must rerun all 18 `(S1-S6, speed 0.4/0.6/0.8)` shards only after generator changes and validators are ready.

## Current GitHub State

- GitHub repo: `https://github.com/everglow246/AI_FOR_WIFI_2`
- Local branch: `main`
- Remote branch: `origin/main`
- Published baseline before this account-switch handoff update: `2d1e9ad`
- To confirm the current handoff commit after publishing, run `git log -1 --oneline`.
- Commit `e7812de`: added GitHub handoff and publishing guards.
- Commit `2d69e52`: remote initial README.
- Commit `2d1e9ad`: merged remote README into the local handoff branch without force-push.

The first push preserved the existing remote `README.md`; no force push was used.

## Local State Not Yet Published

The following local project areas are still untracked and need a separate review before any future commit:

- `ai_for_wifi2/`
- `matlab/`
- many `scripts/*.py`
- `tests/`
- `grill-with-docs/`
- one Chinese-titled Markdown execution document shown by `git status --short`
- `5.17-run1-deep-research-report.md`

Do not run `git add .`. Future commits should use an explicit whitelist after checking `.gitignore` and `scripts/validate_ai_handoff.py`.

## Local Chat Record Pointers

Optional local provenance only:

- session index: `%USERPROFILE%\.codex\session_index.jsonl`
- recent handoff session: `%USERPROFILE%\.codex\sessions\2026\05\17\rollout-2026-05-17T20-59-32-019e3605-373d-7950-b3ad-a9452c089944.jsonl`
- local logs database: `%USERPROFILE%\.codex\logs_2.sqlite`

These files are not committed to the project and should not be treated as portable project documentation. Prefer project files and GitHub handoff documents.

## Do Not Do

- Do not force push.
- Do not run `git add .`.
- Do not upload raw JSONL, NPZ datasets, MATLAB binary outputs, checkpoints, zip bundles, or `raw_steps.jsonl`.
- Do not rerun MATLAB as part of account-switch handoff.
- Do not train CQL as part of account-switch handoff.
- Do not claim CQL performance from loader/loss smoke.
- Do not treat `coverage_v0` as controlled_v1 speed-only causal evidence.

## Next Safe Step

Create a feature branch for reviewing and publishing the actual source code:

```powershell
git checkout main
git pull --ff-only
git checkout -b feature/codex-source-whitelist
```

Then inspect and stage only source/docs/tests that are safe for GitHub. Keep generated data and large artifacts out of GitHub.
