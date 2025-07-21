import re


def get_addresses(client):
    try:
        first = client.get(
            "https://account.microsoft.com/billing/addresses",
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        m = re.search(r'<input\s+name="__RequestVerificationToken"\s+type="hidden"\s+value="([^"]+)"', first.text, re.I)
        if not m:
            return None
        token = m.group(1)
        second = client.get(
            "https://account.microsoft.com/billing/api/shipping/address-list",
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "__RequestVerificationToken": token,
            },
        )
        data = second.json()
        addrs = data.get("addresses", [])
        lines = []
        for a in addrs:
            addr = a.get("address", {})
            vals = [
                addr.get("countryId", ""),
                addr.get("line1", ""),
                addr.get("line2", ""),
                addr.get("line3", ""),
                addr.get("state", ""),
                addr.get("city", ""),
                addr.get("zip", ""),
            ]
            lines.append(", ".join(vals))
        return "\n".join(lines) if lines else "None"
    except Exception:
        return None 