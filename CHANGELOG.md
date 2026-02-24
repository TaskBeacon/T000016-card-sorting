# CHANGELOG

All notable development changes for `T000016-card-sorting` are documented here.

## [Unreleased]

### Added
- Added `references/task_logic_audit.md` for literature-first, auditable trial/state-machine documentation.

### Changed
- Refactored `src/run_trial.py` to use `psyflow`'s native `next_trial_id()` and removed legacy internal `_next_trial_id` boilerplate.
- Refactored task architecture to remove the mandatory task `Controller` pattern for `T000016`.
- Simplified card trial generation: `BlockUnit` now generates plain rule-label conditions and `run_trial.py` deterministically samples target features using utility helpers.
- Updated `main.py` to use the standard `BlockUnit.generate_conditions(...)` path and a MID-style single-flow structure.
- Updated responder phase routing to use canonical phase `card_choice_response`.

### Fixed
- Standardized ITI responder-context phase label to `iti` in `src/run_trial.py`.

## [0.1.0] - 2026-02-17
- Added new WCST-style card sorting task scaffold under PsyFlow/TAPS standards.
- Added mode-aware runtime (`human|qa|sim`) in `main.py`.
- Added split configs:
  - `config/config.yaml`
  - `config/config_qa.yaml`
  - `config/config_scripted_sim.yaml`
  - `config/config_sampler_sim.yaml`
- Added trial context plumbing (`set_trial_context`) in `src/run_trial.py`.
- Added task controller/trial generator in `src/utils.py`.
- Added sampler responder in `responders/task_sampler.py`.
- Added literature/reference artifacts in `references/`.
- Added generated card image stimuli (4 reference cards + 64 target cards) in `assets/cards/`.

### Changed
- Reframed template MID-style logic to card-sorting rule-based flow.
- Updated task metadata (`taskbeacon.yaml`, README) for new task identity.

### Fixed
- Added explicit `anticipation` trial context stage for responder/contract alignment.

### Verified
- `python -m psyflow.validate <task_path>`
- `psyflow-qa <task_path> --config config/config_qa.yaml --no-maturity-update`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`
