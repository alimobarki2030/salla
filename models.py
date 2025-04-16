from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String)
    title = Column(String)
    description = Column(String)
    seo_title = Column(String)
    seo_url = Column(String)
    meta_description = Column(String)
    status = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

