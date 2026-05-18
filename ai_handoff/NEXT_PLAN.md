# Next Plan

## Immediate Safe Work

1. New account Codex should read `ai_handoff/ACCOUNT_SWITCH_HANDOFF.md`.
2. Create `feature/codex-source-whitelist` to review local untracked source code for future GitHub publication.
3. Do not stage generated data or reports; use explicit whitelists only.
4. Implement controlled_v1 generator changes for fixed geometry, full back-and-forth trajectory phase, and stride-separated seed metadata only after source publication is clean.
5. Rerun all 18 controlled_v1 shards only after the generator patch is in place.
6. Validate controlled_v1 for scenario geometry, no S7 leakage, fixed-CSD formal gates, seed uniqueness, candidate/transition boundary, and no-time state leakage.
7. Recompute or confirm `reward_final` with calibration constants from the controlled_v1 calibration split.
8. Build the transition dataset from logged behavior actions only.
9. Run a reproducible CQL loader/loss smoke that saves checkpoint, selected action ids, Q summaries, and selected-action replay metrics.

## Do Not Do Yet

- Do not run large-scale CQL training.
- Do not claim CQL effectiveness from the existing smoke.
- Do not use coverage_v0 for controlled speed-only conclusions.
- Do not upload raw JSONL, NPZ, MATLAB binary outputs, or checkpoints to GitHub.
- Do not add low-value ablations only to fill a table.

## Decision Gates

Proceed past smoke only when:

- controlled_v1 geometry and seed metadata pass validators
- `reward_final` exists and is finite for all required rows
- candidate rows remain separate from transition tuples
- CQL smoke writes reproducibility artifacts
- selected-action replay diagnostics can be reconstructed from saved outputs

## GitHub Publishing Step

GitHub connector access is available as `everglow246`. The first safe handoff publish has already been pushed to `everglow246/AI_FOR_WIFI_2` on `main`. The next GitHub publishing step should be a separate `feature/codex-source-whitelist` review for local source/docs/tests, using explicit staging only and running the handoff validator before push.
