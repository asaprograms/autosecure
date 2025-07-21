def get_msadelegate(client):
    try:
        resp = client.get(
            "https://account.microsoft.com/auth/acquire-onbehalf-of-token?scopes=pidl",
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        data = resp.json()
        if isinstance(data, list) and data:
            token_data = data[0]
            if token_data.get("isSuccess") and token_data.get("token"):
                return token_data["token"]
        return None
    except Exception:
        return None 