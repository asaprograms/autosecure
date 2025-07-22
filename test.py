import asyncio
from utils.httpclient import HttpClient
from securing.secure import secure as _secure
from dataclasses import asdict
import json
from settings import settings

# paste ONE msaauth into the quotes, this is for a manual secure, NERD! set up your own damn bot integration or wait for s'anod :/
msaauth = ""

client = HttpClient()
result = asyncio.run(_secure(client, msaauth, settings))

print(json.dumps(asdict(result), indent=2, ensure_ascii=False)) 