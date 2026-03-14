# PARS Clinical Engine v1.0
# Central entry point for all clinical algorithms

from remission_score_v2 import remission_score_v2
from sad_score import sad_score
from pef_instability import pef_instability
from exacerbation_risk import exacerbation_risk


def run_pars_engine(data):

    # ---------- Small airway score ----------
    sad_value, sad_status = sad_score(
        data["mef25"],
        data["mef50"],
        data["mef75"],
        data["fef25"],
        data["fef50"],
        data["fef75"]
    )

    # ---------- Remission score ----------
    remission_value, remission_stage = remission_score_v2(
        data["fev1_percent"],
        data["symptom_score"],
        sad_value
    )

    # ---------- PEF instability ----------
    pef_value, pef_level = pef_instability(
        data["pef_am"],
        data["pef_pm"]
    )

    # ---------- Exacerbation risk ----------
    risk_value, risk_level = exacerbation_risk(
        remission_value,
        sad_value,
        pef_value
    )

    result = {

        "remission_score": remission_value,
        "remission_stage": remission_stage,

        "small_airway_score": sad_value,
        "small_airway_status": sad_status,

        "pef_variability": pef_value,
        "pef_level": pef_level,

        "exacerbation_risk_score": risk_value,
        "exacerbation_risk_level": risk_level
    }

    return result
