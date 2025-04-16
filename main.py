import os
import httpx
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv

from salla_import import router as import_router

# تحميل متغيرات البيئة
load_dotenv()

# تعريف التطبيق والموجه
app = FastAPI()
router = APIRouter()

# ربط الراوتر
app.include_router(import_router)

# الصفحة الرئيسية للتأكد أن الـ API شغالة
@app.get("/")
async def root():
    return {"message": "✅ API is running"}

# جلب التوكن من سلة
async def get_access_token():
    client_id = os.getenv("SALLA_CLIENT_ID")
    client_secret = os.getenv("SALLA_CLIENT_SECRET")

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
