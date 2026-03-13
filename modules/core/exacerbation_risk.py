def exacerbation_risk(remission_score, sad_score, pef_variability):

    risk = 0

    if remission_score < 70:
        risk += 2

    if sad_score < 40:
        risk += 2

    if pef_variability > 20:
        risk += 2

    if risk <= 1:
        level = "Low risk"

    elif risk <= 3:
        level = "Moderate risk"

    else:
        level = "High exacerbation risk"

    return risk, level
