# Task Logic Audit: Card Sorting Task (WCST-style)

## 1. Paradigm Intent

- Task: `card-sorting` (WCST-style rule-based sorting).
- Primary construct: cognitive flexibility and rule maintenance/set-shifting.
- Manipulated factor: active sorting rule by block (`color`, `shape`, `number`).
- Dependent measures: response key, accuracy, RT, and block-wise performance.

## 2. Block/Trial Workflow

### Block Structure

- Human profile uses 3 blocks, one rule per block (`color -> shape -> number`).
- Conditions are generated with `BlockUnit.generate_conditions(...)` from rule labels.
- Concrete target-card features are sampled in `run_trial.py` using deterministic trial seeds for reproducibility.

### Trial State Machine

1. `rule_cue`: show current rule cue text and emit rule-specific cue trigger.
2. `pre_choice_fixation`: brief fixation period before choice.
3. `card_choice_response`: show target + four reference cards; collect key `1-4` or timeout.
4. `choice_feedback`: show correct/incorrect feedback.
5. `iti`: fixation inter-trial interval.

## 3. Condition Semantics

- Condition token is the active rule label: `color`, `shape`, or `number`.
- For each trial, runtime derives `target_color`, `target_shape`, `target_number`, and `correct_key` from the active rule.
- Trial record logs rule token and sampled features to make replay/audit deterministic.

## 4. Response and Scoring Rules

- Valid response keys: `1`, `2`, `3`, `4`.
- Correct key is determined by active rule and target-reference match.
- Accuracy: hit if key equals derived `correct_key`; miss on wrong key or timeout.
- Feedback uses correctness outcome; block summaries aggregate accuracy/score.

## 5. Stimulus Layout Plan

- Rule cue and fixation are center-aligned.
- Choice screen layout:
  - target card in upper-central area.
  - four reference cards in lower horizontal row, mapped left-to-right to keys `1-4`.
- Feedback text appears centered.

## 6. Trigger Plan

- Experiment: `exp_onset`, `exp_end`
- Block: `block_onset`, `block_end`
- Rule cue: `color_cue_onset`, `shape_cue_onset`, `number_cue_onset`
- Pre-choice fixation: `anticipation_onset`
- Choice: `target_onset`, `key_press`, `no_response`
- Feedback: `feedback_onset`
- ITI: `iti_onset`

## 7. Architecture Decisions (Auditability)

- Keep block generation simple (rule labels only) via standard `BlockUnit.generate_conditions(...)`.
- Keep trial-specific feature sampling in `run_trial.py` with deterministic seed-based generation.
- Avoid unnecessary controller abstraction because no adaptive scheduling/staircase is required.

## 8. Inference Log

- Exact timing constants are marked as `inferred` where source papers report paradigm structure but not fixed numeric values.
- Trigger code assignments are implementation-level and therefore documented as `inferred` mappings.
- Chinese participant-facing strings are localization choices and can be replaced via config without runtime code edits.
