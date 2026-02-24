def detect_intent(query):
    q = query.lower()

    if "emi" in q or "interest" in q:
        return "loan"
    elif "otp" in q or "qr" in q or "scam" in q or "fraud" in q:
        return "fraud"
    else:
        return "general"