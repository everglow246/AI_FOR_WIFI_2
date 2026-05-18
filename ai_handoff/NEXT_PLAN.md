# Next Plan

## Immediate Safe Work

1. Finish the first GitHub publish with only `.gitignore`, `AGENTS.md`, `ai_handoff/*`, and `scripts/validate_ai_handoff.py`.
2. Confirm `main` is pushed to `everglow246/AI_FOR_WIFI_2`.
3. For the next implementation task, create `feature/codex-<short-task-name>` from `main`.
4. Implement controlled_v1 generator changes for fixed geometry, full back-and-forth trajectory phase, and stride-separated seed metadata.
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

GitHub connector access is available as `everglow246`. Target repository `everglow246/AI_FOR_WIFI_2` exists and is suitable for the first handoff publish. Configure `origin` as `https://github.com/everglow246/AI_FOR_WIFI_2.git`, rename the first local branch to `main`, and push only after the handoff validator and staged-file whitelist checks pass.
