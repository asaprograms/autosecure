# grabbing linked applications from before secure, such as prismlauncher

def get_applications(client):
    try:
        resp = client.get(
            "https://account.microsoft.com/privacy/api/app-consent/applications",
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        return resp.json()
    except Exception:
        return None 