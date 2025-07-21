from urllib.parse import quote_plus
import re

from .getlivedata import get_live_data


OTP_RE = re.compile(r"^\d{6,7}$")


def login(client, email: str, otp_id: str, code: str, ppft: str | None = None):
    if not OTP_RE.fullmatch(code):
        return None
    if ppft is None:
        live = get_live_data(client)
        ppft = live.get("ppft")
    payload = (
        f"login={quote_plus(email)}&loginfmt={quote_plus(email)}&type=27&SentProofIDE={quote_plus(otp_id)}&"\
        f"otc={quote_plus(code)}&PPFT={quote_plus(ppft)}"
    )
    client.post(
        "https://login.live.com/ppsecure/post.srf",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        allow_redirects=True,
    )
    return client.cookies.get("__Host-MSAAUTH") 