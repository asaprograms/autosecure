import re
import urllib.parse


def enable_tfa(client):
    try:
        first = client.get(
            "https://account.live.com/proofs/EnableTfa?mkt=en-us",
            headers={"User-Agent": client.user_agent},
        )
        match = re.search(r"rvtkn=([^\"]+)", first.text)
        if not match:
            return False
        rvtkn = match.group(1)
        final_url = (
            "https://account.live.com/proofs/EnableTfa?mkt=en-us&uaid=eb19fd46532e4139a1dc2aedc2b881e4&"
            + "rvtkn="
            + urllib.parse.quote(rvtkn, safe="")
        )
        client.get(final_url, headers={"User-Agent": client.user_agent})
        return True
    except Exception:
        return False 