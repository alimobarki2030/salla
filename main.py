from fastapi import FastAPI, Request

app = FastAPI()

# ✅ المسار الأساسي
@app.get("/")
async def root():
    return {"message": "✅ API is running"}

# ✅ مسار استيراد منتجات وهمية (بدون سلة)
@app.get("/import")
async def import_fake_products():
    return {
        "products": [
            {"id": 1, "name": "منتج تجريبي 1", "price": 100},
            {"id": 2, "name": "منتج تجريبي 2", "price": 200},
            {"id": 3, "name": "منتج تجريبي 3", "price": 300},
        ]
    }

# ✅ مسار عرض منتجات محفوظة (مباشر من قاعدة بيانات وهمية)
@app.get("/products")
async def list_fake_products():
    return {
        "products": [
            {"id": 1, "name": "منتج محفوظ 1", "price": 150},
            {"id": 2, "name": "منتج محفوظ 2", "price": 250}
        ]
    }

# ✅ Webhook لاستقبال أي بيانات
@app.post("/webhook/salla")
async def receive_webhook(request: Request):
    data = await request.json()
    print("📩 Webhook received:", data)
    return {"status": "received", "data": data}
