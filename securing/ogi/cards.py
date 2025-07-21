
def get_cards(client, msadelegate):
    try:
        resp = client.get(
            "https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentInstrumentsEx?status=active,removed&language=en-US&partner=northstarweb",
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Authorization": f"MSADELEGATE1.0={msadelegate}",
            },
        )
        cards_data = resp.json()
        if isinstance(cards_data, list) and cards_data:
            real_cards = [
                f"{card['paymentMethod']['display']['name']} - {card['creationDateTime']}"
                for card in cards_data
                if card.get("creationDateTime")
                and card.get("paymentMethod", {}).get("display", {}).get("name")
            ]
            return "\n".join(real_cards) if real_cards else "None"
        return "None"
    except Exception:
        return None 