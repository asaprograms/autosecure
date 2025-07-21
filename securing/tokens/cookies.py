import re
import time
from urllib.parse import unquote


def _decode(token: str) -> str:
    decoded = unquote(token)
    return re.sub(r"\\u([0-9A-Fa-f]{4})", lambda m: chr(int(m.group(1), 16)), decoded)


def get_cookies(client):
    canary = None
    apicanary = None
    max_retries = 3
    for _ in range(max_retries):
        time.sleep(1)
        try:
            resp = client.get(
                "https://account.live.com/password/reset",
                allow_redirects=False,
            )
            # rate limit check
            if resp.status_code == 429:
                continue
            text = resp.text
            a_match = re.search(r'"apiCanary"\s*:\s*"([^"]+)"', text)
            c_match = re.search(r'"sCanary"\s*:\s*"([^"]*)"', text)
            if c_match:
                canary = _decode(c_match.group(1))
                client.set_cookie("canary", canary)
            if a_match:
                apicanary = _decode(a_match.group(1))
                client.set_cookie("apicanary", apicanary)
            if canary or apicanary:
                break
        except Exception:
            continue
    amsc = client.cookies.get("amsc")
    return canary, apicanary, amsc 