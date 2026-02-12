
import numpy as np

def predict_visa(age, visa_type, applied_month,
                 financial_status, experience,
                 education_level, previous_rejections):

    score = (
        experience * 2 +
        education_level * 3 +
        financial_status * 3 -
        previous_rejections * 4
    )

    if age < 40:
        score += 2

    if visa_type == "Work":
        score += 3
    elif visa_type == "Student":
        score += 2

    if applied_month in [6,7,8]:
        score -= 2

    if score > 12:
        status = "Approved"
        processing = np.random.randint(10, 25)
    else:
        status = "Rejected"
        processing = np.random.randint(30, 60)

    confidence = min(max(int((score + 20) * 2), 10), 95)

    return status, int(processing), confidence
