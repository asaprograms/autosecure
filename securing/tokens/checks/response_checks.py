def response_checks(body: str, client, canary: str, headers):
    if "Abuse" in body:
        return "locked"
    if "working to restore all services" in body:
        return "down"
    if "family/child-consent" in body:
        return "child_landing"
    if "Your account is missing some key info" in body:
        return "chinese_lock"
    return None 