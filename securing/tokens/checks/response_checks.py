def response_checks(body: str, client, canary: str, headers):
    if "Abuse" in body: # checks if account is locked, keyword "Abuse" of microsoft services
        return "locked"
    if "working to restore all services" in body: # checks if microsoft is down or being ratelimited
        return "down"
    if "family/child-consent" in body: # checks if it is a child account, very limited if so
        return "child_landing"
    if "Your account is missing some key info" in body: # checks for china info lock, only occurs on chinese originated microsoft accounts
        return "chinese_lock"
    return None 