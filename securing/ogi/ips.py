import re
from typing import List, Union


def get_ips(client) -> Union[List[str], bool]:
    apicanary = client.cookies.get("apicanary")
    amrp = client.cookies.get("AMRPSSecAuth")
    amsc = client.cookies.get("amsc")
    if not all([apicanary, amrp, amsc]):
        return False
    headers = {
        "canary": apicanary,
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }
    try:
        resp = client.get("https://account.live.com/Activity", headers=headers)
    except Exception:
        return False
    text = resp.text
    ipv4_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    ips = ipv4_pattern.findall(text)
    if not ips:
        return False
    ignored = {"2.2.2.6", "2.2.3.6"}
    unique = [ip for ip in sorted(set(ips)) if ip not in ignored]
    return unique if unique else False 