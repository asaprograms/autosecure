def get_orders(client):
    try:
        resp = client.get(
            "https://account.microsoft.com/billing/orders/list?period=AllTime&orderTypeFilter=All&filterChangeCount=1&isInD365Orders=true&isPiDetailsRequired=true&timeZoneOffsetMinutes=-60",
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        data = resp.json()
        parsed = "None"
        if isinstance(data, dict):
            orders = data.get("orders", [])
            if isinstance(orders, list) and orders:
                details = []
                for order in orders:
                    order_id = order.get("orderId", "N/A")
                    date = order.get("localSubmittedDate", "N/A")
                    cost = order.get("localTotal", "N/A")
                    name = "N/A"
                    items = order.get("items", [])
                    if isinstance(items, list) and items:
                        name = items[0].get("localTitle", "N/A")
                    details.append(f"Order ID: {order_id}, Name: {name}, Cost: {cost}, Date: {date}")
                parsed = "\n\n".join(details)
        return parsed
    except Exception:
        return None 