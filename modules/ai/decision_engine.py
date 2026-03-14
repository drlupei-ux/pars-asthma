def calculate_remission_probability(remission_score, sad_score, pef_variability):

    base = remission_score

    if sad_score < 50:
        base -= 10

    if pef_variability > 20:
        base -= 10

    probability = max(0, min(100, base))

    return probability


def medication_adjustment(remission_score, sad_score, pef_variability):

    if remission_score >= 90 and sad_score >= 60 and pef_variability < 10:
        return "Consider step-down therapy"

    if remission_score >= 70:
        return "Maintain current therapy"

    return "Step-up therapy recommended"


def ai_doctor_summary(remission_score, sad_score, pef_variability):

    if remission_score >= 90:
        stage = "Clinical remission"
    elif remission_score >= 70:
        stage = "Controlled asthma"
    else:
        stage = "Uncontrolled asthma"

    airway_status = "Normal airway" if sad_score >= 60 else "Small airway dysfunction"

    variability = "Stable airway" if pef_variability < 10 else "Airway instability"

    return f"{stage}. {airway_status}. {variability}."


def run_decision_engine(remission_score, sad_score, pef_variability):

    probability = calculate_remission_probability(
        remission_score,
        sad_score,
        pef_variability
    )

    medication = medication_adjustment(
        remission_score,
        sad_score,
        pef_variability
    )

    summary = ai_doctor_summary(
        remission_score,
        sad_score,
        pef_variability
    )

    return {
        "remission_probability": probability,
        "medication_recommendation": medication,
        "ai_summary": summary
    }
