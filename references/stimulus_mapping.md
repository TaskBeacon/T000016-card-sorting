# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `color` | `rule_cue` | `rule_color` | Chinese rule cue text indicating color sorting rule | W2093830143 | Methods describe active rule cueing before sorting response | psychopy_builtin | config text stimulus | Localizable via config text |
| `shape` | `rule_cue` | `rule_shape` | Chinese rule cue text indicating shape sorting rule | W2093830143 | Methods describe active rule cueing before sorting response | psychopy_builtin | config text stimulus | Localizable via config text |
| `number` | `rule_cue` | `rule_number` | Chinese rule cue text indicating number sorting rule | W2093830143 | Methods describe active rule cueing before sorting response | psychopy_builtin | config text stimulus | Localizable via config text |
| `color` | `card_choice_response` | `target_card`, `ref_card_1..4` | One target card and four reference cards; participant chooses matching reference by rule | W2104402653 | WCST rule-matching response phase with four-choice mapping | generated_reference_asset | generated card primitives/assets | Correct key derived by active rule |
| `shape` | `card_choice_response` | `target_card`, `ref_card_1..4` | One target card and four reference cards; participant chooses matching reference by rule | W2104402653 | WCST rule-matching response phase with four-choice mapping | generated_reference_asset | generated card primitives/assets | Correct key derived by active rule |
| `number` | `card_choice_response` | `target_card`, `ref_card_1..4` | One target card and four reference cards; participant chooses matching reference by rule | W2104402653 | WCST rule-matching response phase with four-choice mapping | generated_reference_asset | generated card primitives/assets | Correct key derived by active rule |
| `all` | `pre_choice_fixation` | `fixation` | Center fixation cross prior to choice | W2067877506 | Standard fixation-preparation stage in computerized tasks | psychopy_builtin | config text stimulus | Shared across conditions |
| `all` | `choice_feedback` | `feedback_correct`, `feedback_incorrect` | Centered correctness feedback text | W2067877506 | Trial-level correctness feedback in computerized batteries | psychopy_builtin | config text stimuli | Shared across conditions |
| `all` | `iti` | `fixation` | Center fixation during ITI | W2067877506 | ITI stage between successive trials | psychopy_builtin | config text stimulus | Shared across conditions |
