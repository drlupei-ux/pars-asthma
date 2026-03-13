def pef_instability(pef_am, pef_pm):

    variability = abs(pef_am - pef_pm) / ((pef_am + pef_pm) / 2) * 100

    if variability < 10:
        level = "Stable airway"

    elif variability < 20:
        level = "Moderate variability"

    else:
        level = "High airway instability"

    return variability, level
