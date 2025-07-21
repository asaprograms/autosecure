def get_family(client):
    try:
        resp = client.get(
            "https://account.microsoft.com/home/api/family/family-summary",
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        data = resp.json()
        members = data.get("members", []) if isinstance(data, dict) else []
        if not members:
            return "None"
        formatted = []
        for m in members:
            name = m.get("displayName") or "Unknown"
            relation = "child" if m.get("isChild") else "parent"
            formatted.append(f"{name}, {relation}")
        return ", ".join(formatted)
    except Exception:
        return None 