def calculate_remission_score(fev1_percent, symptom_score):

    score = 0

    score += fev1_percent * 0.6
    score += (10 - symptom_score) * 4

    return min(100, round(score,1))
