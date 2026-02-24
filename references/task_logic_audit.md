# Task Logic Audit: Card Sorting Task (WCST-style)

## 1. Paradigm Intent

- Task: `card-sorting` (WCST-style rule-based sorting)
- Primary construct: rule maintenance and rule-specific stimulus-response mapping.
- Manipulated factor: active sorting rule by block (`color`, `shape`, `number`).
- Dependent measures: response key, accuracy, RT, block-wise accuracy/score.
- Key references: WCST-style card sorting implementations and standard rule-shift logic (see `references.yaml` / `references.md`).

## 2. Block and Trial Workflow

### Block Structure

- Blocks correspond to rule epochs.
- Human profile uses 3 blocks with fixed rule order from `task.conditions`: `color -> shape -> number`.
- Trials per block are generated through the basic `BlockUnit.generate_conditions(...)` path in `main.py`:
  - each block uses a single rule label from `task.conditions` (`color`, `shape`, `number`)
  - `BlockUnit` generates plain rule-label conditions for the block (e.g., repeated `color`)
  - detailed target features and correct key are sampled in `run_trial.py` from the rule label
  - sampling is deterministic from block seed plus trial ID (`trial_seed`) for reproducibility
- No adaptive RT-window controller is used.

### Trial State Machine

1. `rule_cue`
   - Stimulus: text cue showing current rule (`颜色 / 形状 / 数量`)
   - Trigger: rule-specific cue onset (`color_cue_onset` / `shape_cue_onset` / `number_cue_onset`)
   - Response: none
   - Transition: auto-advance after `timing.cue_duration`

2. `pre_choice_fixation`
   - Stimulus: fixation cross
   - Trigger: `anticipation_onset`
   - Response: none
   - Transition: auto-advance after `timing.anticipation_duration`

3. `card_choice_response`
   - Stimuli:
     - one target card (feature-combination card)
     - four reference cards
   - Trigger: `target_onset`
   - Response keys: `1, 2, 3, 4`
   - Response triggers:
     - key press -> `key_press`
     - timeout -> `no_response`
   - Correctness rule:
     - `correct_key` is determined by active rule and sampled target features
   - Transition: response or timeout, then advance

4. `choice_feedback`
   - Stimulus: `feedback_correct` or `feedback_incorrect`
   - Trigger: `feedback_onset`
   - Response: none
   - Transition: auto-advance after `timing.feedback_duration`

5. `iti`
   - Stimulus: fixation cross
   - Trigger: `iti_onset`
   - Response: none
   - Transition: auto-advance after `timing.iti_duration`

## 3. Trial Condition Semantics (Rule Label + Deterministic Trial Sampling)

Each block condition passed to `run_trial.py` is a simple rule label (`color`, `shape`, `number`). `run_trial.py` then deterministically generates the concrete trial spec and logs:

- `rule`
- `condition_id`
- `target_color`
- `target_shape`
- `target_number`
- `correct_key`
- `target_image`

This keeps block conditions simple and auditable while still making target-feature sampling reproducible via logged `trial_seed` and `condition_id`.

## 4. Response and Scoring Rules

- Valid response keys on choice screen: `task.key_list` from config (default `1-4`)
- Correct response defined by active rule:
  - `color` rule -> reference index matching target color
  - `shape` rule -> reference index matching target shape
  - `number` rule -> reference index matching target number
- Scoring:
  - hit -> `delta = 1`
  - miss/timeout -> `delta = 0`
- Block summary metrics:
  - accuracy from `target_hit`
  - score from `feedback_delta`

## 5. Stimulus Layout Plan

- `rule_cue`: centered text cue
- `pre_choice_fixation`: centered fixation
- `card_choice_response`:
  - target card centered upper area (`target_card`)
  - reference cards arranged in a horizontal row along lower screen (`ref_card_1..4`)
  - key mapping is positional (1-4 left to right)
- `choice_feedback`: centered correctness text
- `iti`: centered fixation

## 6. Trigger Plan

- Experiment: `exp_onset`, `exp_end`
- Block: `block_onset`, `block_end`
- Rule cue: `color_cue_onset`, `shape_cue_onset`, `number_cue_onset`
- Pre-choice fixation: `anticipation_onset`
- Card choice: `target_onset`, `key_press`, `no_response`
- Feedback: `feedback_onset`
- ITI: `iti_onset`

## 7. Architecture Notes (Auditability)

- `utils.py` is used only for lightweight rule normalization and target-feature sampling helpers.
- No unified task controller is required because this task has no adaptive timing or online difficulty adjustment.
- `main.py` uses standard `BlockUnit.generate_conditions(...)` for rule labels; `run_trial.py` resolves target features from the rule plus deterministic trial seed.
