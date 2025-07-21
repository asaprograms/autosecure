class ChangeIgnError(Exception):
    pass


def change_ign(client, ssid: str, new_name: str, *, timeout: float = 10.0) -> int:
    if not client or not ssid or not new_name:
        raise ChangeIgnError("client, ssid and new_name are required")
    url = f"https://api.minecraftservices.com/minecraft/profile/name/{new_name}"
    resp = client.put(
        url,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {ssid}"},
        timeout=timeout,
    )
    if 200 <= resp.status_code < 300:
        return resp.status_code
    raise ChangeIgnError(f"status {resp.status_code}: {resp.text}") 