# Known Issues And Non-Claims

## Current Blockers

- controlled_v1 has not been rerun after the fixed geometry and stride-separated seed plan.
- coverage_v0 changes near geometry across speeds in several scenarios, so it is not speed-controlled.
- coverage_v0 did not observe full back-and-forth mobility coverage.
- Scenario 3 corner static-across-speed validation is reported as failed in the post-reward validator.
- Old CQL smoke lacks checkpoint, selected action ids, per-state Q values, and selected-action replay percentile metrics.
- Large CQL training should wait until controlled_v1 data and reproducible smoke outputs are available.

## Explicit Non-Claims

- No formal CQL performance has been proven.
- No offline RL effectiveness has been proven.
- Reward-best candidate is not CQL.
- CQL smoke is not deployment performance.
- coverage_v0 is not a controlled_v1 speed-only causal dataset.
- MATLAB simulation/replay is not real AP measurement.
- Candidate flat pairs are not RL trajectories.
- Candidate rows must not be converted into formal CQL transitions.
- Current `reward_final` is not a final full-MAC reward.

## GitHub Upload Limits

Do not upload these classes of files to GitHub:

- full raw JSONL candidate/episode data
- NPZ datasets
- model checkpoints
- MATLAB binary outputs
- downloaded zip bundles
- full `raw_steps.jsonl`

Record them in `ARTIFACT_MANIFEST.json` instead.
