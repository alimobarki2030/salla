# ملف salla_auth.py
import httpx

CLIENT_ID = "b78e56f5-b7e9-4cc0-aa8b-f4ad0171ea6a"
CLIENT_SECRET = "7baa9bc331f264ded27d5858ab3504cc"
TOKEN_URL = "https://accounts.salla.sa/oauth2/token"

async def get_access_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        return response.json()["access_token"]