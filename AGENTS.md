# AI FOR WIFI 2 / Action3P Agent Context

## User Constraints

1. Do not invent literature, page numbers, datasets, experiment results, or performance claims.
2. Do not casually delete files. When deleting generated artifacts, list the deleted files and the replacement artifact or validator.
3. When explaining code, start with overall logic, then explain variables and syntax details if needed.
4. Every code or document update must list all changed files and behavior changes.
5. Experiments must answer a hypothesis or support a decision. Do not run low-value ablation just to fill tables.
6. Keep the project lean: separate core architecture code, documentation, validators/tests, and generated reports/data.

## Current Project Scope

- Current project root: `D:\AI_for_wifi\AI_FOR_WIFI_2`
- Legacy project: `D:\AI_for_wifi\wifi_phase3`; inspect only when useful, do not modify the legacy mainline.
- Current algorithm direction: CQL / MDP-lite offline RL diagnostics, not a final contextual-bandit route.
- MATLAB results are simulation/replay only, not real AP measurements.

## Action3P Definition

Action3P has exactly three RL action fields:

- `mcs`
- `target_apep_length_bytes`
- `tx_power_dbm`

Fixed fields:

- HE-SU PPDU
- 2Tx / 2NSS
- GI = 1.6 us
- fixed TxMode = `he_su_2tx_2nss_fixed_csd_nonbf_nostbc`
- TxMode, NSS, and GI do not enter `action_id`.

`target_apep_length_bytes` is the payload-side AGGR proxy. Do not call it full MAC-layer aggregation time. `cfg_apep_length`, `cfg_psdu_length`, and `actual_tx_time_us` are MATLAB-derived or verification fields.

Default action grid for new formal smoke runs:

- `mcs = 0:11`
- `target_apep_length_bytes = [1500, 3000, 5000, 8000, 12000, 16000]`
- `tx_power_dbm = [5, 8, 11, 14, 17, 20]`
- default action space size is `12 x 6 x 6 = 432`.

Older 288-action or five-payload diagnostic artifacts may be read for provenance only. Do not use their action-grid conclusions as current formal-grid evidence without saying they are old diagnostics.

## S1-S6 Scenario Geometry

Current active scenarios are `S1-S6`. `S7_reserved = true`; S7 must not enter the current formal dataset, phasegate, or loader smoke.

Global defaults:

- Indoor AP-STA simulation/replay only, not real AP measurement.
- Near distance is sampled once per episode from `[3, 4, 5] m`.
- Mid distance is `10 m`.
- Speeds are `0.4 / 0.6 / 0.8 m/s`.
- Track length is `6 m`, with a `3 m` half-length around the scenario-specific origin.
- "Through wall" means the AP-STA signal path crosses a wall. It does not mean a human or STA may cross a wall.
- Distance, wall position, AP/STA/human position, speed, scenario label, LOS/NLOS flags, and losses are metadata/debug only and must not enter formal RL state.

Scenario definitions:

- `S1`: Near LOS, AP and STA static. Human moves parallel to the AP-STA LOS, starting at the STA projection point, with `d_human_offset_m = 1.0`; human must not enter the LOS main path.
- `S2`: Near LOS, AP and STA static. Human moves perpendicular to the AP-STA line through the midpoint; this constructs LOS blockage.
- `S3`: Near NLOS 90 degree corner. AP and STA are across the corner; human moves along the corner angle bisector. Corner/NLOS geometry is debug metadata only.
- `S4`: Mid NLOS through-wall. Corrected project rule: human moves on the STA side, not the AP side. The track is parallel to the NLOS main path, starts at the STA initial position's offset point, uses `d_human_offset_m = 1.0`, does not cross the wall, and does not enter the NLOS main path.
- `S5`: Near LOS handheld STA. AP is static; STA/carrier moves along the AP-STA line. The carrier is not modeled as an extra blockage object.
- `S6`: Mid NLOS through-wall handheld STA. AP is static; STA/carrier stays on the STA side and moves along the AP-STA line from the STA initial position. STA/carrier must not cross the wall.

## Fixed CSD Rules

- CSD means cyclic shift diversity.
- Do not set `SpatialMapping='CSD'`; MATLAB `wlanHESUConfig` does not expose CSD as a `SpatialMapping` enum.
- Do not use `PreHECyclicShifts=-75` as evidence for 2Tx HE CSD.
- Current fixed CSD implementation uses `SpatialMapping='Custom'` plus per-subcarrier `SpatialMappingMatrix`.
- `he_csd_shift_ns=-400` is the current group setting and is used in code, but still needs standard/documentation review before publication.
- Formal fixed-CSD data must satisfy:
  - `tx_mode_profile=he_su_2tx_2nss_fixed_csd_nonbf_nostbc`
  - `csd_config_status=configured`
  - `csd_phase_equivalence_status=pass`
  - `csd_decode_status=pass`
  - `csd_formal_gate_status=pass`
- `csd_audit_status` alone is a legacy summary, not a formal admission gate.
- In trajectory data, `csd_decode_status=pass` means the fixed-CSD waveform/receiver chain completed and produced valid PER/goodput/SNR telemetry. It does not mean every packet decoded successfully; PER=1 is a valid bad-action outcome.
- Old Direct artifacts are legacy diagnostic only and must not be used as formal fixed-CSD training data.

## State And SNR Rules

Formal CQL state should use receiver-observed telemetry only:

- `last_rx_observed_snr_db`
- `snr_ewma_db`
- `noise_estimate_ewma`
- `csi_mean_ewma`
- `csi_std_ewma`
- `csi_p10_ewma`
- controller memory such as last action, PER/goodput/reward EWMA, retry/power/cooldown/switch proxies

Do not put these into formal state:

- distance / AP/STA position / human position
- wall loss / blockage loss / corner loss / NLOS labels
- `reference_snr_db`
- `sim_link_budget_snr_db`
- `estimated_snr_db` unless proven receiver-observed
- `step_idx`, `time_s`, `speed_mps`, `speed_index` for the formal no-time profile

Preferred formal smoke profile: `s_ap_observable_controller_no_time`.

Formal state may include receiver-observed/controller-memory fields such as `last_rx_observed_snr_db`, `snr_ewma_db`, `noise_estimate_ewma`, `csi_mean_ewma`, `csi_std_ewma`, `csi_p10_ewma`, historical PER/goodput/reward/latency-airtime EWMAs, last action, switch/cooldown/retry/power proxies, and legal action masks.

Formal state must not include scenario id/name, speed, step/time, distance, AP/STA/human/wall position, LOS/NLOS labels, blocked flags, wall/blockage/corner losses, `reference_snr_db`, `sim_link_budget_snr_db`, `snr_injection_debug_db`, candidate-best/sweep-best/oracle action, future reward, or next outcome.

## Candidate And Transition Boundary

- Candidate rows are counterfactual sweep outcomes at one state. They do not have action-specific `state_t1`.
- Use candidates for sweep-best diagnostics, regret, ranking, Q-regression sanity, and BC labels.
- Formal CQL transitions must come from one actually selected behavior action and contain `state_t`, `action_t`, reward, `state_t1`, and `done`.
- Do not convert all candidates into formal CQL transitions with synthetic next states.
- CQL loader reads `state_features_pre_action` and `next_state_features` from the NPZ dataset, not raw debug arrays.

Current formal behavior policy is `stratified_random_legal`:

- MATLAB simulation/replay returns outcomes for a given state/scenario/action.
- The actual logged behavior action must be selected by `stratified_random_legal`, not by sweep-best.
- The policy samples legal actions with balanced marginal coverage across MCS, payload, and tx power as much as the small run allows.
- Candidate sweeps remain a side channel for reward diagnostics, sweep-best upper bound, regret, and coverage analysis only.
- `sweep_best`, `behavior_mixed_v1`, and `first_full_then_sparse` are legacy/diagnostic only for the current reward-fullstep formal path.
- Current reward-fullstep collection uses one scenario-speed shard per `(S1-S6, 0.4/0.6/0.8)` pair, `packets_per_action=20`, `candidate_mode=full_per_step`, and `selection_policy=stratified_random_legal`.

## Reward Component Audit

Current reward-final policy is PHY/link diagnostic only, not a real full-MAC measurement.

Reward normalization constants must be generated from calibration/train candidate rows and reported with their source. Do not hard-code unexplained constants such as `G_ref=1200` or `T_ref=5000`. Current required calibration is:

- `G_ref = np.percentile(calibration_candidate_goodput_mbps, 95, method="linear")`
- `T_min_ref = min(calibration_candidate_actual_tx_time_us)`
- `T_ref = np.percentile(calibration_candidate_actual_tx_time_us, 95, method="linear")`
- fail if `G_ref <= 0` or `T_ref <= T_min_ref`; do not silently fallback.

Current reward-final candidates are V1/V2 goodput/PER/airtime only:

- Primary current reward-final is `V1 = G_norm * (1 - PER) - 0.1 * T_norm`.
- `lambda_air=0.2` is a reranking comparison unless explicitly promoted later.
- General `V1 = G_norm * (1 - PER) - lambda_air * T_norm`
- `V2 = lambda_g * G_norm - lambda_per * PER - lambda_air * T_norm`
- `G_norm = clip(goodput_mbps / G_ref, 0, 1)`
- `T_norm = clip((actual_tx_time_us - T_min_ref) / (T_ref - T_min_ref), 0, 1)`
- `reward_final` must be postprocessed from calibration constants and must exist before validator, evaluator, dataset builder, or CQL smoke runs. If `reward_final` is missing or non-finite, fail.
- `outcome_t.reward`, `mdp_reward`, and `phy_reward_raw` are legacy diagnostic fields only. Do not use them for best-action selection, ranking, diversity checks, dataset rewards, or CQL counterfactual evaluation.
- If formal state includes `last_reward` or `reward_ewma`, those fields must be recomputed from `reward_final`; legacy MATLAB reward must not enter formal state memory.

- `goodput`: MATLAB PHY/link-level estimate of successful payload over simulated action time; allowed in reward. Only historical EWMA may enter formal state.
- `PER`: packet error rate over `packets_per_action`; allowed in reward. Only historical EWMA may enter formal state.
- `power`: action `tx_power_dbm` diagnostic only for current reward-final; no standalone power penalty.
- `airtime`: `actual_tx_time_us` / PPDU-duration proxy; not ACK/backoff/retransmission-inclusive MAC airtime.
- `switch`: diagnostic only; not a physical measurement and not in current reward-final.
- `retry`: diagnostic only; PER/payload-based `retry_debt_proxy`, not a real retransmission loop or real retry count, and not in current reward-final.
- `latency/service_deficit/cooldown`: diagnostic only; not real MAC/queue delay unless future code implements such a queue, and not in current reward-final.

Reports must output each reward component's formula, unit, source type, whether it comes from MATLAB PHY, whether it is true MAC simulation, whether it is allowed in reward, and whether it may enter formal state.

## Artifact Layout

New reward-fullstep runs should write under `reports/runs/YYYYMMDD_HHMMSS_action3p_reward_fullstep_<diff7>/`.

- Each shard writes to its own subdirectory such as `shard_000_S1_speed04/`.
- Merged raw artifacts use `merged_episodes.jsonl`, `merged_candidates.jsonl`, `merged_results.json`, and `merged_manifest.json`.
- Postprocessed formal reward artifacts use `episodes_reward_final.jsonl` and `candidates_reward_final.jsonl`.
- Current cleanup policy is isolation-first: do not delete or move legacy files unless explicitly requested; write `cleanup_report.md` with `file path | reason | replacement`.

## Current Progress Snapshot

- Git has been initialized in `D:\AI_for_wifi\AI_FOR_WIFI_2`.
- `.gitignore` keeps generated data/reports out of version control by default, while preserving consolidated Markdown audits.
- Fixed-CSD capability audit passes:
  - real HE occupied subcarriers are used
  - matrix dimensions are `996 x 2 x 2` for CBW80 2Tx/2NSS
  - fitted delay is effectively `-400 ns`
  - waveform hash changes versus control
  - decode smoke passes
- Latest phasegate prefix: `action3p_fixed_csd_speed_mcs_phasegate_seedfix2`.
- Latest phasegate scope:
  - 7 scenarios
  - 3 speeds: 0.4 / 0.6 / 0.8 m/s
  - 1 episode per scenario-speed
  - 3 steps per episode
  - 12 MCS candidates with fixed payload 1500 and power 17
  - 63 transitions / 756 candidate outcomes
- Latest phasegate gates:
  - duplicate candidate seeds = 0
  - fixed-CSD formal gate passed
  - S5-S7 STA mobility check passed
  - formal no-time dataset passed
  - CQL loader smoke passed with finite loss and invalid action rate 0
- MCS diagnostic:
  - MCS 0-4 still has decision value in this small probe
  - low-MCS best ratio = 0.365079
  - mean regret from removing MCS 0-4 = 0.679308
  - do not prune MCS 0-4 yet

## Important Recent Fixes

- Candidate seed formula was reduced to stay within MATLAB `rng` range `[0, 2^32)` while preserving uniqueness by shard/scenario/speed/episode/step/action.
- `csd_decode_status` semantics were corrected so high-MCS PER=1 remains a legal bad-action outcome instead of causing fixed-CSD gate failure.
- `s_ap_observable_controller_no_time` hard-fail checks were added for time/speed/debug-state leakage.

## Current Limitations

- `EnvironmentalSpeed` support is proven only for new audit-enabled runs from `action3p_speed_capability_smoke_v1`: `wlanTGaxChannel.EnvironmentalSpeed` exists and explicit channel speed changes receiver-side SNR/CSI telemetry in MATLAB simulation/replay.
- Old `action3p_fixed_csd_speed_mcs_phasegate_seedfix2` artifacts must not be reinterpreted as Doppler/mobile-channel data; their speed coverage was generated before the explicit channel speed handoff was added.
- Latest old phasegate fixed payload and power, so it is not evidence for the current 432-action formal grid.
- The three-parameter diagnostic using five payload values was diagnostic only and found reward/payload-grid concerns. It is not the current default action grid.
- CQL smoke is only loader/loss/interface validation. It is not an algorithm performance result.
- Larger CQL training should wait until payload/power grid and speed channel capability are checked.

## Common Commands

Run tests:

```powershell
cd D:\AI_for_wifi\AI_FOR_WIFI_2
& "D:\AI_for_wifi\.venvs\wifi_phase3\Scripts\python.exe" -m pytest tests -q
```

Run MATLAB through MATLAB Engine fallback, not `matlab.exe -batch`.

Useful environment:

```powershell
$env:MATLAB_PATH='D:\MATLAB'
$env:MATLAB_PREFDIR='D:\AI_for_wifi\matlab_pref'
$env:MATLAB_STARTUP_OPTIONS='-nodesktop -nosplash'
$env:MATLAB_ENGINE_START_DIR='D:\AI_for_wifi\matlab-mcp'
$env:TEMP='D:\AI_for_wifi\tmp'
$env:TMP='D:\AI_for_wifi\tmp'
```

Run the latest style of phasegate checks by reusing existing scripts:

```powershell
& "D:\AI_for_wifi\.venvs\wifi_phase3\Scripts\python.exe" scripts\validate_action3p_medium_artifacts.py ...
& "D:\AI_for_wifi\.venvs\wifi_phase3\Scripts\python.exe" scripts\build_action3p_transition_dataset.py --feature-profile s_ap_observable_controller_no_time ...
& "D:\AI_for_wifi\.venvs\wifi_phase3\Scripts\python.exe" scripts\audit_action3p_phasegate_diagnostics.py ...
& "D:\AI_for_wifi\.venvs\wifi_phase3\Scripts\python.exe" scripts\train_action3p_cql_smoke.py ...
```

## Next Recommended Work

Do not continue large CQL training or expand data scale before these are done:

1. Run `EnvironmentalSpeed` / speed capability smoke. If unsupported or ineffective, report that speed is scripted geometry/STA movement only.
2. Run a bounded payload/power small-grid diagnostic under fixed CSD.
3. Generate an artifact path manifest for each run prefix.
4. Do not run large-scale CQL training. CQL is loader/loss smoke only until speed and payload/power gates are clear.

## Reporting Contract

Every new run must use a unique `run_id` or artifact prefix. The prefix should include task name, date/time, and a git/diff/config hash when possible. Do not silently overwrite same-name `action3p_*` artifacts. If overwriting is intentional, record `replaced_by` and reason.

## GitHub Handoff Maintenance

The GitHub-facing handoff lives in `ai_handoff/`. After every Codex task that changes code, documentation, reports, run artifacts, or project decisions, update these files together:

- `ai_handoff/LATEST_STATUS.md`
- `ai_handoff/CODEX_CHANGELOG.md`
- `ai_handoff/REPORTS_INDEX.json`
- `ai_handoff/ARTIFACT_MANIFEST.json`
- `ai_handoff/NEXT_PLAN.md`

Do not copy raw JSONL data, NPZ datasets, MATLAB outputs, model checkpoints, or `raw_steps.jsonl` into `ai_handoff/`; record them in `ARTIFACT_MANIFEST.json` with path, type, sha256, sample count, generated time, upload status, and why they are not uploaded.

## Branch Workflow Rule

Use `main` as the stable branch. If the current local branch is `master` and the repository has not made its first commit yet, rename it with `git branch -M main` before the first push.

`main` should contain only validated code, documentation, and stable handoff updates. Do not run large MATLAB experiments, large CQL training, or risky refactors directly on `main`.

Before Codex starts implementation work after the initial GitHub handoff, create a feature branch from `main`:

```powershell
git checkout main
git pull --ff-only
git checkout -b feature/codex-<short-task-name>
```

Commit code changes, experiment script changes, validator changes, report updates, and `ai_handoff/` maintenance on `feature/*` branches. Before any feature branch is merged or pushed for review, update `ai_handoff/`, run `python scripts/validate_ai_handoff.py`, report `git status`, current branch, commit hash, whether MATLAB was rerun, whether CQL was trained, and whether new experiment data was generated.

Never commit raw JSONL, NPZ datasets, MATLAB binaries, checkpoints, zip bundles, or `raw_steps.jsonl` to `main` or `feature/*`.

Every work session must end with explicit absolute paths for:

- `changed_files`
- `deleted_files`
- `generated_reports`
- `generated_data`
- `exact_commands`
- `next_blockers`

Do not write only a prefix such as `action3p_fixed_csd_speed_mcs_phasegate_seedfix2_*`.
List concrete paths, for example:

- `D:\AI_for_wifi\AI_FOR_WIFI_2\reports\xxx.json`
- `D:\AI_for_wifi\AI_FOR_WIFI_2\reports\xxx.md`
- `D:\AI_for_wifi\AI_FOR_WIFI_2\data\xxx.jsonl`
- `D:\AI_for_wifi\AI_FOR_WIFI_2\data\xxx.npz`

Encoding clarification: if an expected artifact was not generated, write `未生成` explicitly. If a named report only exists as a section in a consolidated report, list that consolidated report path and section instead of silently substituting it.

After every run, explicitly answer:

- Whether it is safe to proceed to the next stage.
- If not safe, what the blockers are.
- Which conclusions are smoke/interface checks rather than performance results.

Acceptance targets are currently reporting targets, not proven results:

- Compared with the current action-grid sweep-best upper bound, throughput gap should eventually be `< 10%`.
- Repeated downlink throughput fluctuation should eventually be `< 5%`.
- Single-parameter convergence/update response target is `< 100 ms`.
- N-parameter response-time growth should not exceed `N x` single-parameter time.
- After significant channel change, parameter response target is `< 100 ms`.
- Model memory target is `< 10 MB`.
- Offline RL training time is excluded from the `100 ms` response targets.

If an expected artifact was not generated, write `未生成` explicitly. Do not substitute a consolidated audit for a missing standalone report.

If a report is mentioned by name, Codex must either provide its exact absolute path or explicitly write `未生成`. A consolidated report cannot silently replace a promised standalone report; if the information only exists inside a consolidated report, list the consolidated report path and section separately.
