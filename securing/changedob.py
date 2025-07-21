import json
import random
import re
from datetime import datetime


def change_dob(client, settings):
    try:
        r = client.get("https://account.microsoft.com/profile?lang=en-US", headers={"X-Requested-With": "XMLHttpRequest"})
    except Exception as e:
        return {"success": False, "error": str(e)}
    m = re.search(r'name="__RequestVerificationToken" type="hidden" value="(.*?)"', r.text)
    if not m:
        return {"success": False, "error": "token"}
    token = m.group(1)
    now = datetime.utcnow().year
    day = settings.dob_day if settings.dob_day else str(random.randint(1, 28)).zfill(2)
    month = settings.dob_month if settings.dob_month else str(random.randint(1, 12)).zfill(2)
    year = settings.dob_year if settings.dob_year else str(random.randint(now - 70, now - 20))
    country = settings.region if settings.region else random.choice(["US", "CA", "GB", "AU", "DE", "FR", "JP", "IN", "GP"])
    payload = {
        "structuredBirthdate": {"day": day, "month": month, "year": year},
        "country": country,
        "isConfirmedToConvertToMinor": False,
    }
    try:
        resp = client.post(
            "https://account.microsoft.com/profile/api/v1/personal-info/msa-profile",
            data=json.dumps(payload),
            headers={
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "__RequestVerificationToken": token,
            },
        )
        if resp.status_code == 200:
            return {"success": True, "new_dob": f"{day}-{month}-{year}", "new_region": country}
        return {"success": False}
    except Exception as e:
        return {"success": False, "error": str(e)} 