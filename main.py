import os
import httpx
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv

from salla_import import router as import_router
from salla import router as webhook_router

load_dotenv()

app = FastAPI()
router = APIRouter()

@app.get("/")
async def root():
    return {"message": "✅ API is running"}

client_id = os.getenv("SALLA_CLIENT_ID")
client_secret = os.getenv("SALLA_CLIENT_SECRET")

# ✅ دالة لجلب التوكن
async def get_access_token():
    url = "https://accounts.salla.sa/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=payload)
        response.raise_for_status()
        return response.json().get("access_token")

# ✅ التأكد من وجود التوكن
async def ensure_token():
    if not hasattr(app.state, "access_token") or not app.state.access_token:
        app.state.access_token = await get_access_token()

# ✅ نقطة اختبار الاتصال
@app.get("/products")
async def get_products():
    await ensure_token()
    token = app.state.access_token

    url = "https://api.salla.dev/admin/v2/products"
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": f"Salla API error: {response.status_code}"}

        return response.json()

# ✅ تضمين الراوترات
app.include_router(import_router, prefix="/salla")
app.include_router(webhook_router, prefix="/webhook")
