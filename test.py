import asyncio
from utils.httpclient import HttpClient
from securing.secure import secure as _secure
from dataclasses import asdict
import json
from settings import settings

# paste your MSAAUTH token below
msaauth = ""

client = HttpClient()
result = asyncio.run(_secure(client, msaauth, settings))

print(json.dumps(asdict(result), indent=2, ensure_ascii=False)) 