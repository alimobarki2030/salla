from fastapi import APIRouter, Header, HTTPException, Depends
import requests
from sqlalchemy.orm import Session
from database import get_db
from api.models import Product
from datetime import datetime

router = APIRouter()

@router.post("/salla/import-products")
def import_products_from_salla(access_token: str = Header(...), db: Session = Depends(get_db)):
    try:
        url = "https://api.salla.dev/admin/v2/products"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="فشل في جلب المنتجات من سلة")

        products = response.json().get("data", [])
        saved = 0
        for p in products:
            product_id = p.get("id")
            existing = db.query(Product).filter(Product.id == product_id).first()
            if existing:
                continue

            new_product = Product(
                id=product_id,
                keyword=p.get("name", ""),
                title=p.get("name", ""),
                description=p.get("description", ""),
                seo_title=p.get("name", ""),
                seo_url=p.get("slug", ""),
                meta_description=p.get("short_description", ""),
                status="pending",
                created_at=datetime.utcnow()
            )

            db.add(new_product)
            saved += 1

        db.commit()
        return {"message": f"تم حفظ {saved} منتج جديد بنجاح"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء الحفظ: {str(e)}")
