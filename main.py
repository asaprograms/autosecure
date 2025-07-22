# autosecure/main.py
from fastapi import FastAPI
from securing.secure import secure as _secure

app = FastAPI(title="asas/catjams autosecure api")

@app.post("/secure")
async def secure_account(method: str, token: str):
    client = HttpClient()
    result = await _secure(client, token, settings)
    return asdict(result)