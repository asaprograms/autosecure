# grabbing ms rewards info from before secure

def get_rewards(client):
    try:
        resp = client.get(
            "https://account.microsoft.com/home/api/rewards/rewards-summary?lang=en-US&refd=account.live.com&refp=landing&mkt=EN-US&status=cancelled&res=acw_landing_page_cancelled",
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        data = resp.json()
        return {"mspoints": data.get("balance", 0) if isinstance(data, dict) else 0}
    except Exception:
        return {"mspoints": 0} 