import json


def disable_tfa(client, apicanary=None):
    if apicanary is None:
        apicanary = client.cookies.get("apicanary")
    payload = {
        "uiflvr": 1001,
        "uaid": "d61ce05e888d47a2a1563133c6a610d6",
        "scid": 100109,
        "hpgid": 201030,
    }
    headers = {"X-Requested-With": "XMLHttpRequest"}
    if apicanary:
        headers["canary"] = apicanary
    try:
        r = client.post(
            "https://account.live.com/API/Proofs/DisableTfa",
            data=json.dumps(payload),
            headers=headers,
        )
        return r.status_code == 200
    except Exception:
        return False 