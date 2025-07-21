import time


MAX_RETRIES = 3


def get_personal_info(client):
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            resp = client.get(
                "https://account.microsoft.com/profile/api/v1/personal-info",
                headers={"X-Requested-With": "XMLHttpRequest"},
            )
            data = resp.json()
            return {
                "og_email": data.get("signInEmail"),
                "first_name": data.get("firstName"),
                "last_name": data.get("lastName"),
                "dob": data.get("birthday"),
                "region": data.get("region"),
            }
        except Exception:
            attempt += 1
            if attempt < MAX_RETRIES:
                time.sleep(1)
    return None 