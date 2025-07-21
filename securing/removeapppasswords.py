from utils.decode import decode


def remove_app_passwords(client, apicanary=None):
    if apicanary is None:
        apicanary = client.cookies.get("canary")
    payload = {
        "uiflvr": 1001,
        "uaid": "da90e97a55cf431385e2dd217c6ba873",
        "scid": 100109,
        "hpgid": 201030,
    }
    resp = client.post(
        "https://account.live.com/API/Proofs/DeleteAppPassword",
        json=payload,
        headers={"canary": decode(apicanary) if apicanary else ""},
    )
    return resp.json() if resp.status_code == 200 else False 