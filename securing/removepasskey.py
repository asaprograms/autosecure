def remove_passkey(client, apicanary, credential_id):
    if apicanary is None:
        apicanary = client.cookies.get("canary")
    payload = {
        "credentialId": credential_id,
        "uiflvr": 1001,
        "uaid": "e352464a3aa44879a8b2173b34b568df",
        "scid": 100109,
        "hpgid": 201030,
    }
    resp = client.post(
        "https://account.live.com/API/Proofs/RemovePasskey",
        json=payload,
        headers={"canary": apicanary},
    )
    return resp.json() if resp.status_code == 200 else False 