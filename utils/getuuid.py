import time
from typing import Optional
import requests

API_URL = "https://api.minetools.eu/uuid/{username}"

def get_uuid(username: str, retry_count: int = 0, max_retries: int = 3) -> Optional[str]:
    base_delay = 1.0  # seconds

    # basic validation
    if not isinstance(username, str):
        return None
    username = username.strip()
    if not (3 <= len(username) <= 16):
        return None

    url = API_URL.format(username=requests.utils.quote(username))

    try:
        r = requests.get(url, timeout=10)
    except requests.RequestException:
        return None

    # rate-limit handling
    if r.status_code == 429 and retry_count < max_retries:
        time.sleep(base_delay * (2 ** retry_count))
        return get_uuid(username, retry_count + 1, max_retries)

    if r.status_code == 200:
        d = r.json()
        if d.get("status") == "OK" and d.get("id"):
            return d["id"]

    if r.status_code == 429 and retry_count >= max_retries:
        return None
    return None 