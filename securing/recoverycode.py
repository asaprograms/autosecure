from utils.decode import decode


def generate_recovery_code(client, eni, apicanary=None):
    if apicanary is None:
        apicanary = client.cookies.get("canary")
    payload = {"encryptedNetId": eni}
    headers = {"canary": decode(apicanary) if apicanary else "", "Content-Type": "application/json"}
    resp = client.post(
        "https://account.live.com/API/Proofs/GenerateRecoveryCode",
        json=payload,
        headers=headers,
    )
    data = resp.json()
    return data.get("recoveryCode") if isinstance(data, dict) else "Failed" 