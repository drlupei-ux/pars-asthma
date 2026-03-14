from modules.core.remission_score_v2 import calculate_remission_score
from modules.core.sad_score import calculate_sad_score
from modules.core.pef_instability import calculate_pef_instability
from modules.core.exacerbation_risk import calculate_exacerbation_risk


def run_pars_engine(data):

    remission_score = calculate_remission_score(
        data["fev1_percent"],
        data["symptom_score"]
    )

    sad_score = calculate_sad_score(
        data["mef25"],
        data["mef50"],
        data["mef75"]
    )

    pef_variability = calculate_pef_instability(
        data["pef_am"],
        data["pef_pm"]
    )

    exacerbation_risk = calculate_exacerbation_risk(
        remission_score,
        sad_score,
        pef_variability
    )

    return {
        "remission_score": remission_score,
        "small_airway_score": sad_score,
        "pef_variability": pef_variability,
        "exacerbation_risk": exacerbation_risk
    }
