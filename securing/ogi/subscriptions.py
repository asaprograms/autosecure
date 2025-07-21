def get_subscriptions(client, msadelegate):
    try:
        resp = client.get(
            "https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentTransactions",
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Authorization": f"MSADELEGATE1.0={msadelegate}",
            },
        )
        data = resp.json()
        subs = data.get("subscriptions", []) if isinstance(data, dict) else []
        if not subs:
            return "None"
        parts = []
        for s in subs:
            title = s.get("title") or "Unknown"
            freq = s.get("recurringFrequency") or "Unknown frequency"
            auto = s.get("autoRenew")
            autorenew = str(auto).lower() if auto is not None else "unknown"
            renewal = s.get("nextRenewalDate") or "No renewal date"
            parts.append(f"{title} - {freq} - autorenew: {autorenew} - {renewal}")
        return ", ".join(parts)
    except Exception:
        return None 