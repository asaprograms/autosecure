import json


def make_primary(client, apicanary: str, alias_name: str) -> bool:
    url = "https://account.live.com/API/MakePrimary"
    payload = {
        "aliasName": alias_name,
        "emailChecked": True,
        "removeOldPrimary": True,
        "uiflvr": 1001,
        "uaid": "abd2ca2a346c43c198c9ca7e4255f3bc",
        "scid": 100141,
        "hpgid": 200176,
    }
    try:
        resp = client.post(
            url,
            data=json.dumps(payload),
            headers={"canary": apicanary, "Content-Type": "application/json"},
            timeout=25,
        )
        data = resp.json()
        if "error" in data:
            code = str(data["error"].get("code"))
            if code == "500":
                return True
            return False
        return True
    except Exception as e:
        msg = str(e)
        if "socket hang up" in msg or "500" in msg:
            return True
        return False 