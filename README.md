# Card Sorting Task (WCST-style)

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field                | Value                                        |
|----------------------|----------------------------------------------|
| Name                 | Card Sorting Task (WCST-style)               |
| Version              | v0.1.0-dev                                   |
| URL / Repository     | https://github.com/TaskBeacon/T000016-card-sorting |
| Short Description    | Rule-based card sorting task for cognitive flexibility and set-shifting |
| Created By           | TaskBeacon                                   |
| Date Updated         | 2026-02-17                                   |
| PsyFlow Version      | 0.1.9                                        |
| PsychoPy Version     | 2025.1.1                                     |
| Modality             | Behavior                                     |
| Language             | Chinese                                      |
| Voice Name           | zh-CN-YunyangNeural                          |

## 1. Task Overview

This task implements a WCST-style card sorting paradigm in which participants classify target cards according to a currently active rule (`color`, `shape`, or `number`). The rule changes by block, and each trial requires mapping the target card to one of four reference cards using keys `1-4`. The implementation supports `human`, `qa`, and `sim` modes, includes trigger emissions for all major phases, and logs trial-level behavioral outcomes with rule-specific controller state.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|------|-------------|
| 1. Parse runtime mode and config | `main.py` resolves mode (`human`, `qa`, `sim`) and loads the selected YAML profile into `TaskSettings`. |
| 2. Build participant context | Human mode opens `SubInfo` form; QA uses `subject_id=qa`; sim uses session participant ID. |
| 3. Initialize runtime | Window/keyboard are initialized; trigger runtime uses mock in QA/sim and configured driver in human mode. |
| 4. Load stimuli | `StimBank` preloads all configured stimuli (fixation, rule cue, card images, feedback, block break, goodbye). |
| 5. Initialize controller | `Controller.from_dict` reads controller config (`seed`, `enable_logging`) and prepares history tracking. |
| 6. Start experiment | Send `exp_onset` trigger and show instruction screen; wait for continue key. |
| 7. Enter block loop | For each of `total_blocks=3`, choose rule by index from `conditions=[color, shape, number]`. |
| 8. Optional countdown | Human mode shows a 3-second countdown before block start. |
| 9. Run `BlockUnit` | Block sends `block_onset`, generates sequential rule conditions, executes trial function, then sends `block_end`. |
| 10. Compute block summary | After each block, compute accuracy and score from block trial data. |
| 11. Show block break | Present formatted `block_break` text with block index, rule label, accuracy, and total score. |
| 12. Finalize | Show `good_bye` with final score, send `exp_end`, save CSV, close trigger runtime, and quit PsychoPy. |

### Trial-Level Flow

| Step | Description |
|------|-------------|
| 1. Sample trial | `run_trial.py` requests one trial spec from controller for current rule and allocates a trial ID. |
| 2. Cue phase | Show `rule_cue` for `cue_duration=0.4s`; emit rule-specific cue trigger (`color_cue_onset` / `shape_cue_onset` / `number_cue_onset`). |
| 3. Anticipation phase | Show fixation for `anticipation_duration=0.2s` with `anticipation_onset` trigger. |
| 4. Target phase | Draw target card plus four reference cards; open response window (`target_duration=2.0s`) for keys `1,2,3,4`; emit `target_onset`, `key_press`, and `no_response` as applicable. |
| 5. Response state writeback | Store response key, correctness (`hit`), correct key, and target features into trial data. |
| 6. Feedback phase | Update controller history and show either `feedback_correct` or `feedback_incorrect` for `feedback_duration=0.6s`; emit `feedback_onset`. |
| 7. ITI phase | Show fixation for `iti_duration=0.3s` with `iti_onset` trigger. |
| 8. Return trial record | Return fully populated trial dictionary to block-level collector. |

### Controller Logic

| Component | Description |
|-----------|-------------|
| Feature spaces | Fixed controller feature sets: 4 colors (`RED/GREEN/BLUE/YELLOW`), 4 shapes (`CIRCLE/TRIANGLE/STAR/SQUARE`), 4 numbers (`1-4`). |
| Trial generation | `sample_trial(rule)` shuffles feature indices and selects rule-dependent correct key (`1-4`) so each rule maps to one reference index. |
| Target image binding | Target image path is generated from sampled feature tuple and points to `assets/cards/targets/...png`. |
| Rule-wise history | `update(hit, rule)` appends performance per rule and optionally logs running rule accuracy. |
| Accuracy helpers | `rule_accuracy` and `overall_accuracy` provide summary metrics from accumulated history. |

### Other Logic

| Component | Description |
|-----------|-------------|
| Scoring | Feedback state sets `delta=1` for correct and `delta=0` otherwise; block and final scores sum these deltas. |
| Rule labels | Rule names are mapped to Chinese labels (`颜色/形状/数量`) for participant-facing cue and break screens. |
| Trial context plumbing | Every major stage (`cue`, `anticipation`, `target`, `feedback`, `iti`) calls `set_trial_context(...)` for responder/simulation compatibility and auditability. |

### Runtime Context Phases
| Phase Label | Meaning |
|---|---|
| `rule_cue` | rule cue stage in `src/run_trial.py` responder context. |
| `pre_choice_fixation` | pre choice fixation stage in `src/run_trial.py` responder context. |
| `card_choice_response` | card choice response stage in `src/run_trial.py` responder context. |
| `choice_feedback` | choice feedback stage in `src/run_trial.py` responder context. |

## 3. Configuration Summary

All settings are defined in `config/config.yaml`.

### a. Subject Info

| Field | Meaning |
|-------|---------|
| subject_id | Required participant ID, integer, 3 digits, constrained to 101-999. |

### b. Window Settings

| Parameter | Value |
|-----------|-------|
| size | `[1280, 720]` |
| units | `pix` |
| screen | `0` |
| bg_color | `black` |
| fullscreen | `false` |
| monitor_width_cm | `35.5` |
| monitor_distance_cm | `60` |

### c. Stimuli

| Name | Type | Description |
|------|------|-------------|
| fixation | text | Center `+` shown in anticipation and ITI. |
| instruction_text | text | Chinese task instruction with key mapping (`1-4`) and start prompt. |
| rule_cue | text | Rule cue text (`当前规则：{rule_label}`) shown at trial start. |
| target_card | image | Target card image placeholder (overridden per trial with sampled target image). |
| ref_card_1 | image | Reference card #1 (left-most response option). |
| ref_card_2 | image | Reference card #2. |
| ref_card_3 | image | Reference card #3. |
| ref_card_4 | image | Reference card #4 (right-most response option). |
| feedback_correct | text | Positive feedback (`正确`). |
| feedback_incorrect | text | Error feedback (`错误`). |
| block_break | text | Inter-block summary with rule label, accuracy, and score. |
| good_bye | text | Final completion screen with total score. |

### d. Timing

| Phase | Duration |
|-------|----------|
| cue | `0.4 s` |
| anticipation | `0.2 s` |
| target response window | `2.0 s` |
| feedback | `0.6 s` |
| iti | `0.3 s` |

### e. Triggers

| Event | Code |
|-------|------|
| exp_onset | 98 |
| exp_end | 99 |
| block_onset | 100 |
| block_end | 101 |
| color_cue_onset | 20 |
| shape_cue_onset | 21 |
| number_cue_onset | 22 |
| anticipation_onset | 25 |
| target_onset | 30 |
| key_press | 40 |
| no_response | 41 |
| feedback_onset | 50 |
| iti_onset | 60 |

### f. Adaptive Controller

| Parameter | Value |
|-----------|-------|
| seed | `2026` |
| enable_logging | `true` |
| random source | Python `random.Random(seed)` |
| rule types | `color`, `shape`, `number` |
| response space | keys `1-4` |
| adaptation style | No staircase; deterministic rule-based trial sampling with performance history tracking |

## 4. Methods (for academic publication)

Participants completed a rule-based card sorting task designed to probe set-shifting and cognitive flexibility. Before the task started, instructions explained that each trial required classifying a target card using one of four response keys (`1-4`) corresponding to four reference cards displayed at the bottom of the screen. The active rule was provided by a cue at the beginning of each trial and changed across blocks (`color`, `shape`, `number`). Trials were organized into three blocks with 32 trials each (96 total trials), with one rule per block.

Each trial began with a rule cue (0.4 s), followed by a short anticipation fixation (0.2 s). The target card and reference cards were then displayed, and participants had up to 2.0 s to respond. Responses were evaluated against the controller-defined correct key based on the active rule. Feedback was shown for 0.6 s as either correct or incorrect, followed by a 0.3 s inter-trial fixation interval. Event triggers were emitted at experiment, block, and phase transitions to support synchronization and downstream analysis.

A controller sampled trial feature combinations (color, shape, number) and computed rule-specific correct responses, while maintaining per-rule performance histories. Block-level summaries reported rule label, accuracy, and accumulated score. This structure supports reproducible behavioral measurement of rule maintenance, rule switching across blocks, and response accuracy under explicit rule constraints.
