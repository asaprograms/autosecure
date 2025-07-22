def get_ssid(client, xbl: str):
    if not xbl:
        return None
    try:
        resp = client.post(
            "https://api.minecraftservices.com/authentication/login_with_xbox", # site to grab minecraft ssid, 24h validity
            json={"identityToken": xbl, "ensureLegacyEnabled": True},
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=10,
        )
        if resp.status_code == 200:
            return resp.json().get("access_token")
        return None
    except Exception:
        return None 