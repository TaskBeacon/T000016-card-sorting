# CHANGELOG

All notable development changes for `T000016-card-sorting` are documented here.

## [0.1.0] - 2026-02-17

### Added
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
