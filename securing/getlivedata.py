import re

LOGIN_URL = "https://login.live.com"
LINK_RE = re.compile(r"https://login\.live\.com/ppsecure/post\.srf\?contextid=[0-9a-zA-Z]+&opid=[0-9a-zA-Z]+&bk=[a-zA-Z0-9]+&uaid=[0-9a-zA-Z]+&pid=0")
PPFT_RE = re.compile(r'value="([^"]+)"')


def get_live_data(client):
    resp = client.post(LOGIN_URL, data=None)
    html = resp.text
    link_match = LINK_RE.search(html)
    ppft_match = PPFT_RE.search(html)
    login_link = link_match.group(0) if link_match else "https://login.live.com/ppsecure/post.srf"
    ppft = ppft_match.group(1) if ppft_match else "null"
    return {"loginLink": login_link, "ppft": ppft} 