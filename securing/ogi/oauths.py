# grabbing consented apps from before secure

def get_oauths(client):
    try:
        resp = client.get(
            "https://account.microsoft.com/privacy/api/app-consent/applications",
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        data = resp.json()
        apps = "None"
        if isinstance(data, dict):
            applications = data.get("applications", [])
            if isinstance(applications, list) and applications:
                apps = "; ".join([app.get("name", "Unnamed Application") for app in applications])
        return apps
    except Exception:
        return None 