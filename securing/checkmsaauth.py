LOGIN_URL = (
    "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=21&ct=1708978285&rver=7.5.2156.0&wp=SA_20MIN&"
    "wreply=https://account.live.com/proofs/Add?apt=2&uaid=0637740e739c48f6bf118445d579a786&lc=1033&id=38936&mkt=en-US&"
    "uaid=0637740e739c48f6bf118445d579a786"
)


def check_msaauth(client, msaauth: str):
    try:
        client.set_cookie("__Host-MSAAUTH", msaauth)
        resp = client.get(
            LOGIN_URL,
            allow_redirects=False,
        )
        body = resp.text or ""
        if "Abuse" in body:
            return "locked"
        if "working to restore all services" in body:
            return "down"
        new_token = client.cookies.get("__Host-MSAAUTH")
        return new_token if new_token else msaauth
    except Exception:
        return msaauth