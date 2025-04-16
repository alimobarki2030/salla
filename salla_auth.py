import os
import httpx

async def get_access_token():
    url = "https://accounts.salla.sa/oauth2/token"
    client_id = os.getenv("SALLA_CLIENT_ID")
    client_secret = os.getenv("SALLA_CLIENT_SECRET")

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=payload, headers=headers)
        print("🔍 Salla response text:", response.text)
        response.raise_for_status()
        return response.json().get("access_token")

