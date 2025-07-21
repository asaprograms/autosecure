import re


def get_aliases(client):
    resp = client.get("https://account.live.com/names/manage")
    emails = re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)", resp.text)
    aliases = list({email.lower() for email in emails})
    match = re.search(r'<input type="hidden" id="canary" name="canary" value="([^"]+)" \/>', resp.text)
    canary2 = match.group(1) if match else None
    if canary2:
        client.set_cookie("canary", canary2)
    return aliases, canary2 