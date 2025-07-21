import requests
from typing import Optional

ENTITLEMENTS_URL = "https://api.minecraftservices.com/entitlements/license?requestId=c24114ab-1814-4d5c-9b1f-e8825edaec1f"

def get_method(ssid: str) -> Optional[str]:
    if not ssid:
        return None
    try:
        r = requests.get(ENTITLEMENTS_URL, headers={"Authorization": f"Bearer {ssid}"}, timeout=10)
        if r.status_code >= 500:
            return None
        for i in r.json().get("items", []):
            if i.get("name") in {"product_minecraft", "game_minecraft"}:
                s = i.get("source")
                if s == "GAMEPASS":
                    return "Gamepass"
                if s in {"PURCHASE", "MC_PURCHASE"}:
                    return "True"
                return "Failed"
    except Exception:
        return None
    return None 