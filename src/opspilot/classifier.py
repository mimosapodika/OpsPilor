def classify_ticket(description):

    text = description.lower()

    if any(word in text for word in [
        "password", "hacked", "suspicious", "phishing", "virus"
    ]):
        category = "SECURITY"

    elif any(word in text for word in [
        "internet", "wifi", "network", "router"
    ]):
        category = "NETWORK"

    elif any(word in text for word in [
        "keyboard", "laptop", "monitor", "mouse", "hardware"
    ]):
        category = "HARDWARE"

    else:
        category = "SOFTWARE"

    if any(word in text for word in [
        "entire office", "all employees", "company-wide", "completely stopped"
    ]):
        priority = "CRITICAL"

    elif any(word in text for word in [
        "urgent", "cannot work", "not working", "unavailable"
    ]):
        priority = "HIGH"

    elif any(word in text for word in [
        "slow", "sometimes", "intermittent"
    ]):
        priority = "MEDIUM"

    else:
        priority = "LOW"

    return {
        "category": category,
        "priority": priority
    }