import json
import re
import time
from urllib.parse import unquote, quote_plus
import logging

RESET_URL = "https://account.live.com/ResetPassword.aspx?wreply=https://login.live.com/oauth20_authorize.srf&mn={email}"
VERIFY_URL = "https://account.live.com/API/Recovery/VerifyRecoveryCode"
RECOVER_URL = "https://account.live.com/API/Recovery/RecoverUser"

INVALID_ACCOUNT_PATTERNS = [
    "Try entering your Microsoft account again.",
    "We don't recognize this one.",
    "account doesn't exist",
    "Microsoft account doesn't exist",
    "doesn't exist"
]

def _extract_server_data(html: str):
    m = re.search(r"var\s+ServerData\s*=\s*(\{.*?\})(?:;|\n)", html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None

def recovery_code_secure(client, email: str, recovery_code: str, security_email: str, password: str):
    reset_url = RESET_URL.format(email=quote_plus(email))
    server_data = None
    max_server_retries = 3
    # Step 1: Initial request and ServerData extraction with retries
    for attempt in range(max_server_retries):
        resp = client.get(reset_url)
        data = resp.text
        if any(pat.lower() in data.lower() for pat in INVALID_ACCOUNT_PATTERNS):
            logging.warning(f"[recovery_code_secure] Account does not exist for {email}")
            return {"error": "1300"}
        server_data = _extract_server_data(data)
        if server_data:
            break
        time.sleep(1)
    if not server_data:
        logging.error("[recovery_code_secure] Failed to extract ServerData after retries.")
        return None

    # Step 2: Retry for missing tokens (sRecoveryToken/apiCanary)
    max_token_retries = 5
    token_retry_count = 0
    while not (server_data.get("sRecoveryToken") and server_data.get("apiCanary")) and token_retry_count < max_token_retries:
        token_retry_count += 1
        time.sleep(token_retry_count)  # progressive backoff
        resp = client.get(reset_url)
        data = resp.text
        new_data = _extract_server_data(data)
        if new_data:
            server_data = new_data
    if not (server_data.get("sRecoveryToken") and server_data.get("apiCanary")):
        logging.error(f"[recovery_code_secure] Missing tokens after {max_token_retries} retries.")
        return None

    s_recovery_token = server_data.get("sRecoveryToken")
    api_canary = server_data.get("apiCanary")
    uaid = server_data.get("sUnauthSessionID", "")

    # Step 3: Verify Recovery Code
    verify_payload = {
        "recoveryCode": recovery_code,
        "scid": 100103,
        "token": unquote(s_recovery_token),
        "uaid": uaid,
        "uiflvr": 1001,
        "code": recovery_code,
    }
    verify_resp = client.post(
        VERIFY_URL,
        json=verify_payload,
        headers={"Content-Type": "application/json; charset=utf-8", "canary": api_canary},
    ).json()
    if not verify_resp or not verify_resp.get("token"):
        if verify_resp.get("error", {}).get("code") == "1300":
            return {"error": "1300"}
        logging.error(f"[recovery_code_secure] No token in verify response: {verify_resp}")
        return None

    # Step 4: Recover User with retries
    recover_payload = {
        "contactEmail": security_email,
        "contactEpid": "",
        "password": password,
        "passwordExpiryEnabled": 0,
        "publicKey": "25CE4D96CB3A09A69CD847C69FC6D40AF4A4DE12",
        "token": unquote(verify_resp["token"]),
    }
    max_recover_attempts = 3
    recovery_response = None
    for attempt in range(1, max_recover_attempts + 1):
        try:
            recover_resp = client.post(
                RECOVER_URL,
                json=recover_payload,
                headers={"Content-Type": "application/json; charset=utf-8", "Canary": api_canary},
            ).json()
            if recover_resp.get("error", {}).get("code") == "6001":
                return {"error": "6001"}
            if recover_resp.get("recoveryCode"):
                recovery_response = recover_resp
                break
            if attempt < max_recover_attempts:
                time.sleep(attempt * 2)  # progressive delay: 2s, 4s, ...
        except Exception as e:
            logging.error(f"[recovery_code_secure] RecoverUser exception on attempt {attempt}: {e}")
            if attempt < max_recover_attempts:
                time.sleep(attempt * 2)
    if not recovery_response:
        logging.error(f"[recovery_code_secure] RecoverUser failed after {max_recover_attempts} attempts.")
        return None
    return {
        "email": email,
        "recoveryCode": recovery_response["recoveryCode"],
        "security_email": security_email,
        "password": password,
    } 