import time


def get_profile(client, ssid: str, max_retries: int = 3):
    attempt = 0
    rate_retries = 0
    max_rate = 3
    while attempt < max_retries:
        try:
            resp = client.get(
                "https://api.minecraftservices.com/minecraft/profile",
                headers={"Authorization": f"Bearer {ssid}"},
                allow_redirects=True,
            )
            status = resp.status_code
            print(f"status: {status}")
            if status == 200:
                data = resp.json()
                return data if data.get("name") else "Doesn't own MC"
            if status in (400, 401, 403):
                return "Failed"
            if status in (404):
                return "Doesn't own MC"
            if status == 429:
                rate_retries += 1
                if rate_retries >= max_rate:
                    return "Failed"
                time.sleep(3)
                continue
        except Exception:
            pass
        attempt += 1
        if attempt < max_retries:
            time.sleep(1)
    return "Failed" 