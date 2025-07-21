import re


def leave_family(client):
    try:
        home_resp = client.get(
            "https://account.microsoft.com/family/home",
            headers={"X-Requested-With": "XMLHttpRequest"},
        )
        m = re.search(r'<input\s+name="__RequestVerificationToken"\s+type="hidden"\s+value="([^"]+)"', home_resp.text)
        if not m:
            return False
        token = m.group(1)
        roster_resp = client.get(
            "https://account.microsoft.com/family/api/roster",
            headers={"X-Requested-With": "XMLHttpRequest", "__RequestVerificationToken": token},
        )
        members = roster_resp.json().get("Members", [])
        puid = None
        for mbr in members:
            if mbr.get("IsSelf"):
                puid = mbr.get("Puid")
                break
        if not puid:
            return False
        delete_url = f"https://account.microsoft.com/family/api/member?removeSet=Msa:{puid}"
        client.delete(
            delete_url,
            headers={"X-Requested-With": "XMLHttpRequest", "__RequestVerificationToken": token},
        )
        return True
    except Exception:
        return False 