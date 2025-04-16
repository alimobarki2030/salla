import httpx
from salla_auth import get_access_token

API_URL = "https://api.salla.dev/admin/v2/products"

async def fetch_products_from_salla():
    token = await get_access_token()
    async with httpx.AsyncClient() as client:
        response = await client.get(
            API_URL,
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()


# إضافة هذا في ملف main.py
from fastapi import FastAPI
from salla_import import fetch_products_from_salla

app = FastAPI()

@app.get("/")
def root():
    return {"message": "✅ API is running"}

@app.get("/import")
async def import_products():
    return await fetch_products_from_salla()
