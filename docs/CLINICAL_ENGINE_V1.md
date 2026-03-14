# PARS Clinical Engine v1.0

## Remission Score Algorithm

Inputs
- FEV1 percent predicted
- Symptom score

Score calculation

Remission Score = 0.6 * FEV1% + 4 * (10 - symptom_score)

Clinical interpretation

>= 90  Clinical remission  
70–89  Controlled asthma  
< 70   Uncontrolled asthma

---

## Small Airway Dysfunction Score

Inputs
- MEF25
- MEF50
- MEF75

Score

Small Airway Score = average(MEF25, MEF50, MEF75)

Clinical interpretation

>= 60  Normal  
40–59  Mild small airway dysfunction  
< 40   Significant small airway disease

---

## PEF Instability Index

Inputs
- Morning PEF
- Evening PEF

Calculation

PEF variability = |PEF_AM − PEF_PM| / mean(PEF) * 100

Clinical interpretation

< 10%   Stable airway  
10–20%  Moderate variability  
> 20%   High instability

---

## Exacerbation Risk Score

Risk factors

- Remission Score < 70
- Small Airway Score < 60
- PEF variability > 20

Risk level

0–1 factors  Low risk  
2 factors    Moderate risk  
3 factors    High risk
