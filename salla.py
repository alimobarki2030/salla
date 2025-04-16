from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Product
from datetime import datetime

router = APIRouter()

@router.post("/webhook/salla")
async def handle_salla_webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    new_product = Product(
        id=data.get("id"),
        keyword=data.get("keyword"),
        title=data.get("title"),
        description=data.get("description"),
        seo_title=data.get("seo_title"),
        seo_url=data.get("seo_url"),
        meta_description=data.get("meta_description"),
        status=data.get("status", "pending"),
        created_at=datetime.utcnow()
    )

    db.add(new_product)
    db.commit()

    return {"message": "✅ تم حفظ المنتج من Webhook سلة"}
