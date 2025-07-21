import re


def amc(client) -> bool:
    try:
        step1 = client.get("https://account.microsoft.com", allow_redirects=False)
        amc_link = step1.headers.get("location")
        if not amc_link:
            return False
        step2 = client.get(amc_link)
        match = re.search(r'<input\s+type="hidden"\s+name="t"\s+id="t"\s+value="([^"]+)"', step2.text)
        if not match:
            return False
        t_value = match.group(1)
        post_url = (
            "https://account.microsoft.com/auth/complete-silent-signin?ru=https://account.microsoft.com/"
            "auth/complete-silent-signin?ru=https%3A%2F%2Faccount.microsoft.com%2F&wa=wsignin1.0&refd=login.live.com&wa=wsignin1.0"
        )
        client.post(post_url, data=f"t={t_value}", headers={"X-Requested-With": "XMLHttpRequest"})
        return bool(client.cookies.get("AMCSecAuth"))
    except Exception:
        return False 