def amcjwt(client) -> bool:
    try:
        d1 = client.get("https://account.microsoft.com/", allow_redirects=False)
        loc1 = d1.headers.get("location")
        if not loc1:
            return False
        d2 = client.get(loc1)
        loc2 = d2.headers.get("location")
        if not loc2:
            return False
        d3 = client.get(loc2)
        loc3 = d3.headers.get("location")
        if not loc3:
            return False
        client.get(loc3)
        return bool(client.cookies.get("AMCSecAuthJWT"))
    except Exception:
        return False 