from urllib.parse import urlencode


def add_alias(client, name: str, canary: str) -> bool:
    url = "https://account.live.com/AddAssocId"
    payload = {
        "canary": canary,
        "PostOption": "NONE",
        "SingleDomain": "outlook.com",
        "UpSell": "",
        "AddAssocIdOptions": "LIVE",
        "AssociatedIdLive": name,
    }
    try:
        resp = client.post(url, data=urlencode(payload), headers={"Content-Type": "application/x-www-form-urlencoded"}, allow_redirects=False)
        return bool(resp.text and "alias=" in resp.text)
    except Exception:
        return False 