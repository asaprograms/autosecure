def sign_out(client):
    amrp = client.cookies.get("AMRPSSecAuth")
    amsc = client.cookies.get("amsc")
    if not amrp or not amsc:
        return False
    resp = client.post(
        "https://account.live.com/API/Proofs/DeleteDevices",
        json={},
        headers={"Content-Type": "application/json"},
    )
    return resp.status_code == 200 