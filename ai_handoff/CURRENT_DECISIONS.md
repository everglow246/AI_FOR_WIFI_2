# Current Decisions

## Project Direction

- Current project root: `D:\AI_for_wifi\AI_FOR_WIFI_2`
- Legacy project: `D:\AI_for_wifi\wifi_phase3`; inspect only when needed and do not modify legacy mainline.
- Current direction is CQL / MDP-lite offline RL diagnostics.
- MATLAB outputs are simulation/replay artifacts, not real AP measurements.

## Action3P Contract

The RL action has exactly three fields:

- `mcs`
- `target_apep_length_bytes`
- `tx_power_dbm`

Fixed fields:

- HE-SU PPDU
- 2Tx / 2NSS
- GI = 1.6 us
- fixed TxMode = `he_su_2tx_2nss_fixed_csd_nonbf_nostbc`

Default current action grid:

- `mcs = 0:11`
- `target_apep_length_bytes = [1500, 3000, 5000, 8000, 12000, 16000]`
- `tx_power_dbm = [5, 8, 11, 14, 17, 20]`
- total actions: `432`

`target_apep_length_bytes` is a payload-side AGGR proxy. It is not full MAC-layer aggregation time.

## Scenario Set

- Current active scenarios: `S1-S6`
- `S7_reserved = true`; S7 must not enter current formal datasets, phasegates, or loader smoke.
- Speeds: `0.4`, `0.6`, `0.8` m/s.
- Distance, wall position, AP/STA/human position, speed, scenario labels, LOS/NLOS flags, and losses are debug metadata only and must not enter formal RL state.

## Fixed CSD

- CSD means cyclic shift diversity.
- Do not set `SpatialMapping='CSD'`; MATLAB `wlanHESUConfig` does not expose that enum.
- Current implementation uses `SpatialMapping='Custom'` plus per-subcarrier `SpatialMappingMatrix`.
- `he_csd_shift_ns=-400` is the current group setting in code, but still needs standard/documentation review before publication.
- Formal fixed-CSD data must satisfy `tx_mode_profile`, `csd_config_status`, `csd_phase_equivalence_status`, `csd_decode_status`, and `csd_formal_gate_status`.
- `csd_decode_status=pass` means the fixed-CSD waveform/receiver chain completed and produced valid telemetry; PER=1 can still be a valid bad-action outcome.

## State And Candidate Boundary

- Formal state should use receiver-observed telemetry and controller memory.
- Formal no-time profile should not include scenario id/name, speed, step/time, distance, positions, LOS/NLOS labels, wall/blockage/corner losses, reference/link-budget SNR, candidate-best/sweep-best fields, future reward, or next outcome.
- Candidate rows are counterfactual sweep outcomes at one state and do not have action-specific `state_t1`.
- Formal CQL transitions must come from one actually selected behavior action and contain `(state_t, action_t, reward, state_t1, done)`.
- Do not convert all candidates into formal CQL transitions.

## Reward Decision

Current mainline postprocessed reward:

```text
reward_final = G_norm * (1 - PER) - 0.1 * T_norm
```

Reward constants must come from calibration candidates, not unexplained hard-coded values.

Current reward is PHY/link diagnostic only:

- `goodput`: MATLAB PHY/link-level estimate
- `PER`: MATLAB PHY/link-level packet decode outcome
- `airtime`: MATLAB HE-SU waveform duration proxy

Not current reward terms:

- standalone power penalty
- switch penalty
- real retry count
- real queue latency
- real MAC backoff/ACK/retransmission-inclusive airtime

## Report Layout

- Active run reports: `reports/runs/`
- Decision documents: `reports/decisions/`
- Superseded or failed material: `reports/archive/`
- GitHub summary handoff: `ai_handoff/`
