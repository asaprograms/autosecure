import json
import subprocess
import sys

class LunarError(Exception):
    pass

def get_lunar_cosmetics(access_token: str, timeout: float = 30.0):
    if not access_token:
        print("[lunar] missing access token", flush=True)
        raise LunarError("missing access token")
    print("[lunar] using lunarclient-websocket npm package", flush=True)
    try:
        result = subprocess.run([
            "node", "./lunarfetch.js", access_token
        ], capture_output=True, text=True, timeout=timeout)
        output = result.stdout.strip().split('\n')[-1]
        resp = json.loads(output)
        if not resp.get("success"):
            print(f"[lunar] error: {resp.get('error')}", flush=True)
            raise LunarError(resp.get("error", "no response"))
        print("[lunar] success", flush=True)
        return resp["data"]
    except Exception as e:
        print(f"[lunar] error: {e}", flush=True)
        raise LunarError(str(e)) 