import json
import re

from config import KEYS
from utils.solvecaptcha import solve_base64_2captcha, CaptchaError
from utils.namegen import random_first, random_last


def change_name(client, settings):
    r = client.get("https://account.microsoft.com/profile/", headers={"X-Requested-With": "XMLHttpRequest"})
    token_match = re.search(r'name="__RequestVerificationToken" type="hidden" value="(.*?)"', r.text)
    if not token_match:
        return None
    verification_token = token_match.group(1)
    captcha_resp = client.get(
        "https://account.microsoft.com/api/hip/challenge/visual",
        headers={"__RequestVerificationToken": verification_token, "X-Requested-With": "XMLHttpRequest"},
    )
    data = captcha_resp.json()
    if not data or "challengeSource" not in data:
        return None
    api_key = KEYS.get("2captcha") or KEYS.get("captcha")
    if not api_key:
        return None
    try:
        captcha_solution = solve_base64_2captcha(data["challengeSource"], api_key)
    except CaptchaError:
        return None

    first_name = settings.first_name or random_first()
    last_name = settings.last_name or random_last()

    payload = {
        "firstName": first_name,
        "lastName": last_name,
        "hipSolution": captcha_solution,
        "hipContext": {
            "challengeType": data["context"].get("challengeType"),
            "azureRegion": data["context"].get("azureRegion"),
            "challengeId": data["context"].get("challengeId"),
        },
    }

    headers = {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "__RequestVerificationToken": verification_token,
    }
    resp = client.put(
        "https://account.microsoft.com/profile/api/v1/edit-name/name",
        data=json.dumps(payload),
        headers=headers,
    )
    if resp.status_code == 200:
        return {"success": True, "new_first_name": first_name, "new_last_name": last_name}
    return {"success": False} 