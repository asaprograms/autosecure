import json


def remove_proof(client, apicanary, proof_id):
    if apicanary is None:
        apicanary = client.cookies.get("canary")
    url = "https://account.live.com/API/Proofs/DeleteProof"
    payload = {
        "proofId": proof_id,
        "uiflvr": 1001,
        "uaid": "da90e97a55cf431385e2dd217c6ba873",
        "scid": 100109,
        "hpgid": 201030,
    }
    try:
        resp = client.post(url, data=json.dumps(payload), headers={"canary": api_canary, "Content-Type": "application/json"})
        return resp.json()
    except Exception:
        return False 