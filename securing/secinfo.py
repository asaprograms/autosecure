import json
import re


def get_security_info(client):
    resp = client.get(
        "https://account.live.com/proofs/Manage/additional",
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    m = re.search(r"var\s+t0\s*=\s*({.*?});", resp.text, re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except Exception:
            return None
    return None 