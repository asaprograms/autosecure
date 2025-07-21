import re
import time
from urllib.parse import urlencode


def remove_oauth_apps(client) -> int:
    manage_url = "https://account.live.com/consent/Manage?guat=1"
    try:
        manage_resp = client.get(manage_url, headers={"X-Requested-With": "XMLHttpRequest"}, allow_redirects=True)
    except Exception:
        return 0
    client_ids = re.findall(r'data-clientId="([^"]+)"', manage_resp.text)
    if not client_ids:
        return 0
    removed = 0
    for cid in client_ids:
        try:
            edit_url = f"https://account.live.com/consent/Edit?client_id={cid}"
            edit_resp = client.get(edit_url, headers={"X-Requested-With": "XMLHttpRequest"}, allow_redirects=True)
            canary_match = re.search(r'name="canary"\s+value="([^"]+)"', edit_resp.text)
            uaid_match = re.search(r'action="[^"]*[?&]uaid=([^"&]+)', edit_resp.text)
            if not canary_match or not uaid_match:
                continue
            canary_val = canary_match.group(1)
            uaid_val = uaid_match.group(1)
            remove_url = f"https://account.live.com/consent/Edit?client_id={cid}&uaid={uaid_val}"
            client.post(
                remove_url,
                data=urlencode({"canary": canary_val}),
                headers={
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                allow_redirects=True,
            )
            time.sleep(1)
            verify_resp = client.get(manage_url, headers={"X-Requested-With": "XMLHttpRequest"}, allow_redirects=True)
            if f'data-clientId="{cid}"' not in verify_resp.text:
                removed += 1
        except Exception:
            continue
    return removed
