import base64
import json
import re

from ..xboxloginlink import get_xbox_login_link

TOKEN_RE = re.compile(r"accessToken=([A-Za-z0-9_\-]+)")


def _find_token_in_url(url: str):
    m = TOKEN_RE.search(url)
    return m.group(1) if m else None


def get_xbl(client, msaauth: str):
    current = get_xbox_login_link(client)
    token = None
    for _ in range(20):
        token = _find_token_in_url(current)
        if token:
            break
        resp = client.get(current, allow_redirects=False, headers={"Cookie": f"__Host-MSAAUTH={msaauth}"})
        if 300 <= resp.status_code < 400:
            next_url = resp.headers.get("Location")
            if not next_url:
                return None
            if "/verify" in next_url:
                return "verify"
            current = next_url
            continue
        body_token = _find_token_in_url(resp.text)
        if body_token:
            token = body_token
            break
        return None
    if not token:
        return None
    while len(token) % 4:
        token += "="
    try:
        decoded = base64.b64decode(token).decode()
        data = json.loads(decoded)
    except Exception:
        return None
    if not isinstance(data, list) or not data:
        return None
    uhs = data[0].get("Item2", {}).get("DisplayClaims", {}).get("xui", [{}])[0].get("uhs")
    xsts = ""
    gtg = None
    for item in data:
        if item.get("Item1") == "rp://api.minecraftservices.com/":
            xsts = item.get("Item2", {}).get("Token", "")
        elif item.get("Item1") == "http://xboxlive.com":
            xui = item.get("Item2", {}).get("DisplayClaims", {}).get("xui", [{}])[0]
            gtg = xui.get("gtg")
    if not (uhs and xsts and gtg):
        return None
    return {"xbl": f"XBL3.0 x={uhs};{xsts}", "gtg": gtg} 