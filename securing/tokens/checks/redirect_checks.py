def redirect_checks(redirect_url: str, client, headers):
    if redirect_url.startswith("https://account.microsoft.com/family/child-consent/child-landing"): # child account
        return "child_landing"
    if "/identity/confirm" in redirect_url:
        return "phone_locked"
    if redirect_url.startswith("https://account.live.com/pipl/accrue"): # chinese lock
        pipl_url = "https://account.live.com/API/ChinaPIPLAccrual"
        payload = {
            "uiflvr": 1001,
            "uaid": "a75fa1b72aab4213824fd77f4a8d97df",
            "scid": 100232,
            "hpgid": 201087,
        }
        try:
            client.post(
                pipl_url,
                json=payload,
                headers={"Content-Type": "application/json", **headers},
            )
        except Exception:
            pass
        return None
    if redirect_url.startswith("https://account.live.com/recover"): # password is flagged with a required reset
        return "password_flagged"
    return None 