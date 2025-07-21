from urllib.parse import urlencode


def remove_alias(client, canary: str, name: str) -> bool:
    url = "https://account.live.com/names/manage"
    payload = {
        "canary": canary,
        "action": "RemoveAlias",
        "aliasName": name,
        "displayName": name,
    }
    try:
        resp = client.post(
            url,
            data=urlencode(payload),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            allow_redirects=False,
        )
        return "Note_AssociatedIdRemoved" in resp.text
    except Exception:
        return False 