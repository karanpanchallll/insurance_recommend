def calculate_risk_score(age, income, driving_record, smoker):
    score = 0
    # Age factor
    if age < 25:
        score += 2
    elif age > 60:
        score += 3
    else:
        score += 1

    # Income level factor
    if income < 30000:
        score += 2
    elif income < 60000:
        score += 1

    # Driving record
    if driving_record == "DUI":
        score += 3
    elif driving_record == "Accident":
        score += 2
    elif driving_record == "Major Violations":
        score += 4

    # Smoking
    if smoker == "Yes":
        score += 3

    # Risk interpretation
    if score <= 3:
        return "Low Risk"
    elif score <= 6:
        return "Medium Risk"
    else:
        return "High Risk"