def calculate_pef_instability(pef_am, pef_pm):

    variability = abs(pef_am - pef_pm) / ((pef_am + pef_pm) / 2) * 100

    return round(variability,1)
