# Stimulus Mapping

Task: `Card Sorting Task (WCST-style)`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `color` | `color_cue`, `color_target` | `W2093830143` | Methods section describes condition-specific cue-target structure and response phase. | `generated_reference_asset` | Cue label text for COLOR; target token for condition-specific response context. |
| `shape` | `shape_cue`, `shape_target` | `W2093830143` | Methods section describes condition-specific cue-target structure and response phase. | `generated_reference_asset` | Cue label text for SHAPE; target token for condition-specific response context. |
| `number` | `number_cue`, `number_target` | `W2093830143` | Methods section describes condition-specific cue-target structure and response phase. | `generated_reference_asset` | Cue label text for NUMBER; target token for condition-specific response context. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
