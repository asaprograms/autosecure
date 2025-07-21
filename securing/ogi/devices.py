def get_devices(client):
    try:
        resp = client.get(
            "https://account.microsoft.com/home/api/devices/devices-summary",
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        data = resp.json()
        devices = data.get("devices", []) if isinstance(data, dict) else []
        if devices:
            models = [d.get("model", "Unnamed Device") for d in devices]
            return ", ".join(models)
        return "None"
    except Exception:
        return None 