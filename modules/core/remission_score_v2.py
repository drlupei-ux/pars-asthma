def remission_score_v2(fev1_percent, symptom_score, sad_score):

    score = 0

    score += fev1_percent * 0.4
    score += (100 - symptom_score * 10) * 0.3
    score += sad_score * 0.3

    if score > 100:
        score = 100

    if score >= 90:
        stage = "Clinical Remission"

    elif score >= 70:
        stage = "Controlled"

    else:
        stage = "Uncontrolled"

    return score, stage
