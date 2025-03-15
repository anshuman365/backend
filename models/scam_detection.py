def detect_scam(description):
    scam_keywords = ["guaranteed", "free money", "lottery", "click here"]
    return any(word in description.lower() for word in scam_keywords)