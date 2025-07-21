import re


def remove_devices(client):
    try:
        page_resp = client.get(
            "https://account.microsoft.com/devices?lang=en-US",
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        m = re.search(r'<input\s+name="__RequestVerificationToken"\s+type="hidden"\s+value="([^"]+)"', page_resp.text)
        if not m:
            return False
        token = m.group(1)
        summary = client.get(
            "https://account.microsoft.com/home/api/devices/devices-summary",
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        device_ids = [d.get("id") for d in summary.json().get("devices", []) if d.get("id")]
        for device_id in device_ids:
            form = f"deviceId={device_id}"
            client.post(
                "https://account.microsoft.com/devices/api/disclaim",
                data=form,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "__RequestVerificationToken": token,
                    "X-Requested-With": "XMLHttpRequest",
                },
            )
            client.put(
                "https://account.microsoft.com/devices/api/app-device/deauthorize",
                data=form,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "__RequestVerificationToken": token,
                    "X-Requested-With": "XMLHttpRequest",
                },
            )
            client.put(
                "https://account.microsoft.com/devices/api/offline-play/deauthorize",
                data=form,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "__RequestVerificationToken": token,
                    "X-Requested-With": "XMLHttpRequest",
                },
            )
        client.delete(
            "https://account.microsoft.com/devices/api/delete-settings",
            headers={"__RequestVerificationToken": token, "X-Requested-With": "XMLHttpRequest"},
        )
        return True
    except Exception:
        return False 