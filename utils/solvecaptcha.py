# 2captcha solving flow

import time
import requests

class CaptchaError(Exception):
    pass

def solve_base64_2captcha(base64_img: str, api_key: str, timeout: int = 90) -> str:
    body = base64_img.split(',', 1)[-1]
    resp = requests.post(
        'https://2captcha.com/in.php',
        data={'key': api_key, 'method': 'base64', 'body': body, 'json': 1},
        timeout=30,
    ).json()
    if resp.get('status') != 1:
        raise CaptchaError(resp.get('request', 'submit failed'))
    cap_id = resp['request']
    start = time.time()
    while time.time() - start < timeout:
        time.sleep(5)
        res = requests.get(
            'https://2captcha.com/res.php',
            params={'key': api_key, 'action': 'get', 'id': cap_id, 'json': 1},
            timeout=30,
        ).json()
        if res.get('status') == 1:
            return res['request'].replace(' ', '')
        if res.get('request') not in ('CAPCHA_NOT_READY', '0'):
            raise CaptchaError(res.get('request', 'error'))
    raise CaptchaError('timeout') 