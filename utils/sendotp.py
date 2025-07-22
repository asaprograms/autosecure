# sending one time login code to email/security email for an email

import requests

_API_URL = "https://login.live.com/GetOneTimeCode.srf"
_DEFAULT_COOKIE = "MSPRequ=id=N&lt=1710339166&co=1; uaid=c91a322ee1b4429680ea8f66c093a0; MSCC=197.120.88.59-EG; MSPOK=$uuid-146ab8a8-c9d0-4bb1-aa27-547da7d29c2e; OParams=11O.DtGQ6hN13OJzMvlgcsbk3K1MJr*X68!Ot3yO3k6RSI06blohFE2hyzV47ZO5tLXE6D0m99QK34YAxLCQDz3U1Nwyqy2Ov*hJkMvLwJXKbYUIjSGgHieTerUPAdR6FgtL0BzQq8XqFSgSdvzmclJqKpzC0GvHtf*jA5WjBZyVV5OSII6OIjJzM8v256KIa95Jzj14D1QDiteTtl5yjezcl!ntryM4c*L*FOCgYxrA8MD9oya8pFHntdG4l5NgaUHkKencTODUnk6EbqD0Scud3qYyArpTBs7ryxY7AUWiqHf1tEwSAEzpGdVVlnooi!h0*w$$; MicrosoftApplicationsTelemetryDeviceId=8d42cd67-e191-4485-b99f-61acde87e85c; ai_session=xgIvNnBy7/HaB8dU2XGZWs|1710339167277|1710339167277; MSFPC=GUID=254359f779a247ddb178d133b367ad82&HASH=2543&LV=202403&V=4&LU=1710339171328"
_DEFAULT_FLOWTOKEN = "-DvTDvmRgphmpW9oJRrYLB1YGD*aPHnUeOf3zvwQABaxrG8WwdFr6jD12imzrE3D2AhdfsKbazoW5G0AvCvO9Thz!9VzxnGUlAbtWqwft34nll3cx2ge2pRYsrK5Sq6BtZbObPlJ2tDiwu3gRDgBjzFldYn*rt9By5D!6QUKFoC8pFtKS949tDFokpG0BpT07ig$$"

def sendotp(primary_email: str, secdata: str) -> bool:
    sess = requests.Session()
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": _DEFAULT_COOKIE}
    data = {"login": primary_email, "flowtoken": _DEFAULT_FLOWTOKEN, "purpose": "eOTT_OtcLogin", "channel": "Email", "AltEmailE": secdata}
    try:
        resp = sess.post(_API_URL, headers=headers, data=data, timeout=30)
        resp.raise_for_status()
    except requests.RequestException:
        return False
    try:
        payload = resp.json()
    except ValueError:
        return False
    return payload.get("State") == 201 