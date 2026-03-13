def sad_score(mef25, mef50, mef75, fef25, fef50, fef75):

    values = [mef25, mef50, mef75, fef25, fef50, fef75]

    score = sum(values) / len(values)

    if score >= 60:
        status = "Normal small airway function"

    elif score >= 40:
        status = "Mild small airway dysfunction"

    else:
        status = "Severe small airway dysfunction"

    return score, status
