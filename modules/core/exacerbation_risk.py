def calculate_exacerbation_risk(remission_score, sad_score, pef_variability):

    risk = 0

    if remission_score < 70:
        risk += 2

    if sad_score < 60:
        risk += 2

    if pef_variability > 20:
        risk += 2

    if risk >= 4:
        return "High"
    elif risk >= 2:
        return "Moderate"
    else:
        return "Low"
