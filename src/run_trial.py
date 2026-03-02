from __future__ import annotations

from functools import partial

from psyflow import StimUnit, next_trial_id, set_trial_context

from .utils import normalize_rule, sample_card_trial_spec


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one WCST-style card-sorting trial from a simple rule condition label."""
    trial_id = next_trial_id()
    rule = normalize_rule(str(condition))
    response_keys = [str(k) for k in settings.key_list]
    if len(response_keys) != 4:
        raise ValueError(f"T000016 requires task.key_list to define 4 response keys, got {response_keys!r}")
    if block_idx is None:
        raise ValueError("block_idx is required for deterministic trial generation in T000016.")

    block_seed = int(settings.block_seed[int(block_idx)])
    trial_seed = (block_seed * 1000) + int(trial_id)
    trial_spec = sample_card_trial_spec(rule, key_list=response_keys, seed=trial_seed)
    cond_id = str(trial_spec["condition_id"])

    trial_data = {"condition": rule, "condition_id": cond_id, "trial_seed": trial_seed}
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    # phase: rule_cue
    cue_stim_name = f"rule_cue_{rule}"
    cue = make_unit(unit_label="rule_cue").add_stim(stim_bank.get(cue_stim_name))
    set_trial_context(
        cue,
        trial_id=trial_id,
        phase="rule_cue",
        deadline_s=float(settings.cue_duration),
        valid_keys=[],
        block_id=block_id,
        condition_id=cond_id,
        task_factors={"rule": rule, "block_idx": block_idx, "stage": "rule_cue"},
        stim_id=cue_stim_name,
    )
    cue.show(
        duration=float(settings.cue_duration),
        onset_trigger=settings.triggers.get(f"{rule}_cue_onset"),
    ).to_dict(trial_data)

    # phase: pre_choice_fixation
    pre_choice_fixation = make_unit(unit_label="pre_choice_fixation").add_stim(stim_bank.get("fixation"))
    pre_choice_fixation_duration = float(settings.anticipation_duration)
    set_trial_context(
        pre_choice_fixation,
        trial_id=trial_id,
        phase="pre_choice_fixation",
        deadline_s=pre_choice_fixation_duration,
        valid_keys=[],
        block_id=block_id,
        condition_id=cond_id,
        task_factors={"rule": rule, "block_idx": block_idx, "stage": "pre_choice_fixation"},
        stim_id="fixation",
    )
    pre_choice_fixation.show(
        duration=pre_choice_fixation_duration,
        onset_trigger=settings.triggers.get("anticipation_onset"),
    ).to_dict(trial_data)

    # phase: card_choice_response
    choice_display = (
        make_unit(unit_label="card_choice_response")
        .add_stim(stim_bank.rebuild("target_card", image=trial_spec["target_image"]))
        .add_stim(stim_bank.get("ref_card_1"))
        .add_stim(stim_bank.get("ref_card_2"))
        .add_stim(stim_bank.get("ref_card_3"))
        .add_stim(stim_bank.get("ref_card_4"))
    )
    set_trial_context(
        choice_display,
        trial_id=trial_id,
        phase="card_choice_response",
        deadline_s=float(settings.target_duration),
        valid_keys=list(response_keys),
        block_id=block_id,
        condition_id=cond_id,
        task_factors={
            "rule": rule,
            "target_color": trial_spec["target_color"],
            "target_shape": trial_spec["target_shape"],
            "target_number": trial_spec["target_number"],
            "correct_key": trial_spec["correct_key"],
            "target_image": trial_spec["target_image"],
            "block_idx": block_idx,
            "stage": "card_choice_response",
        },
        stim_id="target_card",
    )
    choice_display.capture_response(
        keys=response_keys,
        correct_keys=[trial_spec["correct_key"]],
        duration=float(settings.target_duration),
        onset_trigger=settings.triggers.get("target_onset"),
        response_trigger=settings.triggers.get("key_press"),
        timeout_trigger=settings.triggers.get("no_response"),
    )

    response_key = choice_display.get_state("response", None)
    target_rt = choice_display.get_state("rt", None)
    hit = bool(choice_display.get_state("hit", False))
    choice_display.set_state(
        rule=rule,
        target_color=trial_spec["target_color"],
        target_shape=trial_spec["target_shape"],
        target_number=trial_spec["target_number"],
        correct_key=trial_spec["correct_key"],
        target_image=trial_spec["target_image"],
        response_key=response_key,
        trial_seed=trial_seed,
    ).to_dict(trial_data)

    # phase: choice_feedback
    feedback_name = "feedback_correct" if hit else "feedback_incorrect"
    feedback = make_unit(unit_label="choice_feedback").add_stim(stim_bank.get(feedback_name))
    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="choice_feedback",
        deadline_s=float(settings.feedback_duration),
        valid_keys=[],
        block_id=block_id,
        condition_id=cond_id,
        task_factors={
            "rule": rule,
            "correct_key": trial_spec["correct_key"],
            "response_key": response_key,
            "hit": hit,
            "block_idx": block_idx,
            "stage": "choice_feedback",
        },
        stim_id=feedback_name,
    )
    feedback.show(
        duration=float(settings.feedback_duration),
        onset_trigger=settings.triggers.get("feedback_onset"),
    )
    feedback.set_state(
        hit=hit,
        feedback_label="正确" if hit else "错误",
        delta=1 if hit else 0,
    ).to_dict(trial_data)

    # phase: iti
    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    iti_duration = float(settings.iti_duration)
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="iti",
        deadline_s=iti_duration,
        valid_keys=[],
        block_id=block_id,
        condition_id=cond_id,
        task_factors={"rule": rule, "block_idx": block_idx, "stage": "iti"},
        stim_id="fixation",
    )
    iti.show(
        duration=iti_duration,
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    trial_data.update(
        {
            "rule": rule,
            "target_correct_key": trial_spec["correct_key"],
            "target_response_key": response_key,
            "target_response": response_key,
            "target_hit": hit,
            "target_rt": target_rt,
            "hit": hit,
        }
    )
    return trial_data
