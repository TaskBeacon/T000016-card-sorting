# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| task_name | `task.task_name` | `eeg_card_sorting` | W2093830143 | WCST-style computerized set-shifting protocol in Methods | inferred | Task slug for runtime outputs |
| total_blocks | `task.total_blocks` | `3` | W2131168315 | Blocked rule-set switching structure | inferred | One block per active rule |
| trial_per_block | `task.trial_per_block` | `32` | W2067877506 | Computerized neurocognitive scanning trialized administration | inferred | Total 96 trials |
| conditions | `task.conditions` | `['color','shape','number']` | W2104402653 | Set-shifting among rule dimensions | inferred | Canonical WCST dimensions |
| key_list | `task.key_list` | `['1','2','3','4']` | W2067877506 | 4-option response interface in computerized battery | inferred | Maps to four reference cards |
| cue_duration | `timing.cue_duration` | `0.4` | W2093830143 | Trial epochs include brief rule cue before choice | inferred | Rule cue display |
| target_duration | `timing.target_duration` | `2.0` | W2067877506 | Timed forced-choice response window | inferred | Choice timeout window |
| feedback_duration | `timing.feedback_duration` | `0.6` | W2104402653 | Trial-wise correctness feedback stage | inferred | Correct/incorrect display |
| iti_duration | `timing.iti_duration` | `0.3` | W2067877506 | Short ITI in rapid computerized battery | inferred | Fixed ITI |
| trig_rule_color | `triggers.map.color_cue_onset` | `20` | W2093830143 | Cue onset event coding by trial phase | inferred | Rule-specific cue trigger |
| trig_rule_shape | `triggers.map.shape_cue_onset` | `21` | W2093830143 | Cue onset event coding by trial phase | inferred | Rule-specific cue trigger |
| trig_rule_number | `triggers.map.number_cue_onset` | `22` | W2093830143 | Cue onset event coding by trial phase | inferred | Rule-specific cue trigger |
| trig_target_onset | `triggers.map.target_onset` | `30` | W2067877506 | Stimulus onset marking for response epoch | inferred | Choice screen onset |
| trig_key_press | `triggers.map.key_press` | `40` | W2067877506 | Response event marker | inferred | Any valid response |
| trig_no_response | `triggers.map.no_response` | `41` | W2067877506 | Omission event marker | inferred | Timeout/no key |
| trig_feedback | `triggers.map.feedback_onset` | `50` | W2104402653 | Feedback stage onset | inferred | Correctness feedback |
| trig_iti | `triggers.map.iti_onset` | `60` | W2067877506 | Inter-trial interval onset marker | inferred | ITI stage |
| trig_block_onset | `triggers.map.block_onset` | `100` | W2093830143 | Block-level segmentation for analysis | inferred | Start of rule block |
| trig_block_end | `triggers.map.block_end` | `101` | W2093830143 | Block-level segmentation for analysis | inferred | End of rule block |
