def grade(task, actions, steps):
    score = 0.0
    expected = task["expected_action"]

    # Correct final action
    if actions and actions[-1].action_type == expected:
        score += 0.5

    # Correct action appeared anywhere
    if any(a.action_type == expected for a in actions):
        score += 0.2

    # Efficiency scoring
    if steps == 1:
        score += 0.3
    elif steps == 2:
        score += 0.2
    elif steps == 3:
        score += 0.1

    # Penalize repetition
    unique_actions = set(a.action_type for a in actions)
    if len(unique_actions) == 1 and len(actions) > 1:
        score -= 0.2

    return max(0.0, min(score, 1.0))