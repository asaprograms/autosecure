from urllib.parse import quote_plus


def get_amrp(client, token):
    payload = f"t={quote_plus(token)}"
    client.post(
        "https://account.live.com/proofs/Add?apt=2&wa=wsignin1.0",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        allow_redirects=False,
    )
    return bool(client.cookies.get("AMRPSSecAuth")) 