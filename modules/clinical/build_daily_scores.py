import pandas as pd
from modules.core.clinical_engine import run_pars_engine


def build_daily_scores():

    df = pd.read_csv("daily_data.csv")

    results = []

    for _, row in df.iterrows():

        data = {
            "fev1_percent": row["FEV1"] * 40,
            "symptom_score": row["symptom"],

            "mef25": row["MEF25"],
            "mef50": row["MEF50"],
            "mef75": row["MEF50"],

            "pef_am": row["PEF_AM"],
            "pef_pm": row["PEF_PM"]
        }

        r = run_pars_engine(data)

        results.append({
            "date": row["date"],
            "remission_score": r["remission_score"],
            "small_airway_score": r["small_airway_score"],
            "pef_variability": r["pef_variability"]
        })

    score_df = pd.DataFrame(results)

    score_df.to_csv("daily_scores.csv", index=False)

    print("Daily clinical scores generated: daily_scores.csv")


if __name__ == "__main__":
    build_daily_scores()
