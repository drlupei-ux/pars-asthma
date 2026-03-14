def calculate_sad_score(mef25, mef50, mef75):

    score = (mef25 + mef50 + mef75) / 3

    if score >= 60:
        return 80
    elif score >= 40:
        return 60
    else:
        return 30
