# Task Plot Review

## Evidence Match

- Pass: title and construct match the WCST-style card sorting task.
- Pass: Color, Shape, and Number rows match the configured rule blocks.
- Pass: phase order matches README and `src/run_trial.py`: Rule cue -> Anticipation -> Card choice -> Feedback -> ITI.
- Pass: timing labels match config: 400 ms cue, 200 ms anticipation, 2000 ms choice, 600 ms feedback, 300 ms ITI.
- Pass: card choice shows the target card above four reference cards and response keys 1-4.
- Pass: feedback shows correct and incorrect outcomes.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
