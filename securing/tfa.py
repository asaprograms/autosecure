import re
import pyotp
import json


def setup_tfa(client):
    apicanary = client.cookies.get("apicanary")
    resp = client.get(
        "https://account.live.com/proofs/Add?uaid=b79c68e4a2f04965a2a9a4d694809ff0&mpsplit=2&apt=3&mkt=en-us",
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    secret_match = re.search(r"Secret key: <span class=\"dirltr bold\">([^<]+)<", resp.text)
    proof_match = re.search(r'<input type="hidden" id="ProofId" name="ProofId" value="([^"]+)"', resp.text)
    if not secret_match or not proof_match:
        return False
    key = secret_match.group(1).replace("&nbsp;", "")
    proof_id = proof_match.group(1)
    totp_code = pyotp.TOTP(key).now()
    payload = {"ProofId": proof_id, "TotpCode": totp_code}
    vr = client.post(
        "https://account.live.com/API/AddVerifyTotp",
        data=json.dumps(payload),
        headers={
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Canary": apicanary,
        },
    )
    if vr.json().get("apiCanary"):
        return key
    return False
