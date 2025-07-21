def get_capes(client, ssid: str) -> str:
    try:
        resp = client.get(
            "https://api.minecraftservices.com/minecraft/profile",
            headers={"Authorization": f"Bearer {ssid}"},
            timeout=5,
        )
        data = resp.json()
        capes = []
        for cape in data.get("capes", []):
            alias = cape.get("alias")
            if alias:
                capes.append(alias)
        return ", ".join(capes)
    except Exception:
        return "" 