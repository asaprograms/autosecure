import os
import re
from pathlib import Path
import requests


def change_pfp(client, settings=None):
    try:
        r = client.get("https://account.microsoft.com/profile/edit-picture", headers={"X-Requested-With": "XMLHttpRequest"})
    except Exception:
        return None
    m = re.search(r'name="__RequestVerificationToken" type="hidden" value="(.*?)"', r.text)
    if not m:
        return None
    token = m.group(1)
    img_path = Path(__file__).with_suffix("").parent / "image.jpg"
    tmp_path = None
    pfp_url = settings.pfp_url

    if pfp_url:
        try:
            resp = requests.get(pfp_url, timeout=10)
            ct = resp.headers.get("content-type", "")
            if resp.status_code == 200 and ct.startswith("image/"):
                ext = ".jpg"
                if "png" in ct:
                    ext = ".png"
                tmp_path = Path(__file__).with_suffix("").parent / f"downloaded_pfp{ext}"
                tmp_path.write_bytes(resp.content)
                img_path = tmp_path
        except Exception:
            pass
    if not img_path.exists():
        return None

    if not pfp_url:
        dona_img = Path(__file__).resolve().parents[1] / "resources" / "dona.png"
        if dona_img.exists():
            img_path = dona_img

    files = {"pictureFile": (img_path.name, open(img_path, "rb"), "application/octet-stream")}
    headers = {"X-Requested-With": "XMLHttpRequest", "__RequestVerificationToken": token}
    try:
        resp = client.post("https://account.microsoft.com/profile/api/v1/personal-info/profile-picture", files=files, headers=headers)
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()
        return {"success": True} if resp.status_code == 200 else {"success": False}
    except Exception:
        return None 