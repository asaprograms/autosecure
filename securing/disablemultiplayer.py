def disable_multiplayer(client, xbl):
    if not xbl:
        return False
    if not xbl.startswith("XBL3.0 x="):
        xbl = f"XBL3.0 x={xbl}"
    headers = {
        "authorization": xbl,
        "ms-cv": "dona",
        "content-type": "application/json",
        "accept": "*/*",
        "dnt": "1",
        "origin": "https://www.xbox.com",
        "referer": "https://www.xbox.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "x-ms-api-version": "1.0",
    }
    data = {
        "setOnlineSafetySettings": [185, 254],
        "clearOnlineSafetySettings": [188, 190, 198, 199, 220, 255],
    }
    try:
        resp = client.post(
            "https://emerald.xboxservices.com/xboxcomfd/settings/privacyonlinesafety",
            json=data,
            headers=headers,
            timeout=10,
        )
        return resp.status_code == 200
    except Exception:
        return False 