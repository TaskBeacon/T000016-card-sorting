from functools import partial

from psyflow import StimUnit, set_trial_context


RESPONSE_KEYS = ["1", "2", "3", "4"]
RULE_LABEL_ZH = {
    "color": "颜色",
    "shape": "形状",
    "number": "数量",
}


def _next_trial_id(controller) -> int:
    histories = getattr(controller, "histories", {}) or {}
    done = 0
    for items in histories.values():
        try:
            done += len(items)
        except Exception:
            continue
    return int(done) + 1


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run a single card-sorting trial under a rule condition."""
    rule = str(condition)
    trial_id = _next_trial_id(controller)
    trial_spec = controller.sample_trial(rule)

    trial_data = {"condition": rule}
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    # phase: rule_cue
    cue = make_unit(unit_label="cue").add_stim(
        stim_bank.get_and_format("rule_cue", rule_label=RULE_LABEL_ZH.get(rule, rule))
    )
    set_trial_context(
        cue,
        trial_id=trial_id,
        phase="rule_cue",
        deadline_s=float(settings.cue_duration),
        valid_keys=RESPONSE_KEYS,
        block_id=block_id,
        condition_id=rule,
        task_factors={"rule": rule, "block_idx": block_idx, "stage": "rule_cue"},
        stim_id="rule_cue",
    )
    cue.show(
        duration=settings.cue_duration,
        onset_trigger=settings.triggers.get(f"{rule}_cue_onset"),
    ).to_dict(trial_data)

    # phase: pre_choice_fixation
    anticipation_duration = float(getattr(settings, "anticipation_duration", 0.2))
    anticipation = make_unit(unit_label="anticipation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        anticipation,
        trial_id=trial_id,
        phase="pre_choice_fixation",
        deadline_s=anticipation_duration,
        valid_keys=[],
        block_id=block_id,
        condition_id=rule,
        task_factors={"rule": rule, "block_idx": block_idx, "stage": "pre_choice_fixation"},
        stim_id="fixation",
    )
    anticipation.show(
        duration=anticipation_duration,
        onset_trigger=settings.triggers.get("anticipation_onset"),
    )

    # phase: card_choice_response
    target = (
        make_unit(unit_label="target")
        .add_stim(stim_bank.rebuild("target_card", image=trial_spec["target_image"]))
        .add_stim(stim_bank.get("ref_card_1"))
        .add_stim(stim_bank.get("ref_card_2"))
        .add_stim(stim_bank.get("ref_card_3"))
        .add_stim(stim_bank.get("ref_card_4"))
    )
    set_trial_context(
        target,
        trial_id=trial_id,
        phase="card_choice_response",
        deadline_s=float(settings.target_duration),
        valid_keys=list(RESPONSE_KEYS),
        block_id=block_id,
        condition_id=rule,
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
        stim_id=trial_spec["target_image"],
    )
    target.capture_response(
        keys=RESPONSE_KEYS,
        correct_keys=[trial_spec["correct_key"]],
        duration=settings.target_duration,
        onset_trigger=settings.triggers.get("target_onset"),
        response_trigger=settings.triggers.get("key_press"),
        timeout_trigger=settings.triggers.get("no_response"),
    )

    response_key = target.get_state("response", None)
    hit = bool(target.get_state("hit", False))
    target.set_state(
        rule=rule,
        target_color=trial_spec["target_color"],
        target_shape=trial_spec["target_shape"],
        target_number=trial_spec["target_number"],
        correct_key=trial_spec["correct_key"],
        target_image=trial_spec["target_image"],
        response_key=response_key,
    ).to_dict(trial_data)

    # phase: choice_feedback
    controller.update(hit, rule)
    fb_name = "feedback_correct" if hit else "feedback_incorrect"
    feedback = make_unit(unit_label="feedback").add_stim(stim_bank.get(fb_name))
    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="choice_feedback",
        deadline_s=float(settings.feedback_duration),
        valid_keys=[],
        block_id=block_id,
        condition_id=rule,
        task_factors={
            "rule": rule,
            "correct_key": trial_spec["correct_key"],
            "response_key": response_key,
            "hit": hit,
            "block_idx": block_idx,
            "stage": "choice_feedback",
        },
        stim_id=fb_name,
    )
    feedback.show(
        duration=settings.feedback_duration,
        onset_trigger=settings.triggers.get("feedback_onset"),
    )
    feedback.set_state(
        hit=hit,
        feedback_label="正确" if hit else "错误",
        delta=1 if hit else 0,
    ).to_dict(trial_data)

    # outcome display
    make_unit(unit_label="iti").add_stim(stim_bank.get("fixation")).show(
        duration=settings.iti_duration,
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    return trial_data
