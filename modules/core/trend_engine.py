import pandas as pd
import numpy as np


def calculate_trend(dataframe):

    """
    dataframe example columns:
    date
    remission_score
    small_airway_score
    pef_variability
    """

    trend = {}

    if len(dataframe) < 2:
        trend["trend"] = "insufficient data"
        return trend

    remission_trend = np.polyfit(
        range(len(dataframe)),
        dataframe["remission_score"],
        1
    )[0]

    airway_trend = np.polyfit(
        range(len(dataframe)),
        dataframe["small_airway_score"],
        1
    )[0]

    pef_trend = np.polyfit(
        range(len(dataframe)),
        dataframe["pef_variability"],
        1
    )[0]

    if remission_trend > 0:
        remission_status = "improving"
    else:
        remission_status = "declining"

    if airway_trend > 0:
        airway_status = "small airway improving"
    else:
        airway_status = "small airway worsening"

    if pef_trend > 0:
        pef_status = "airway instability increasing"
    else:
        pef_status = "airway stability improving"

    trend["remission_trend"] = remission_status
    trend["airway_trend"] = airway_status
    trend["pef_trend"] = pef_status

    return trend
