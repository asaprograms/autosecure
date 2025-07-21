import re
from .checks.redirect_checks import redirect_checks
from .checks.response_checks import response_checks
from .checks.token_parser import token_parser


LOGIN_URL = (
    "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=21&ct=1708978285&rver=7.5.2156.0&wp=SA_20MIN&"
    "wreply=https://account.live.com/proofs/Add?apt=2&uaid=0637740e739c48f6bf118445d579a786&lc=1033&id=38936&mkt=en-US&"
    "uaid=0637740e739c48f6bf118445d579a786"
)


def get_t(client, canary: str):
    headers = {"X-Requested-With": "XMLHttpRequest"}

    for _ in range(3):
        resp = client.get(LOGIN_URL, headers=headers, allow_redirects=False)

        # handle redirect
        if 300 <= resp.status_code < 400 and resp.headers.get("Location"):
            result = redirect_checks(resp.headers["Location"], client, headers)
            if result:
                return result
            continue

        # check body indicators
        body = resp.text
        res_chk = response_checks(body, client, canary, headers)
        if res_chk:
            return res_chk

        # token parse
        token = token_parser(body)
        if token:
            return token

    return None 