from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.standardProduct import StandardProduct
from datetime import datetime

router = APIRouter(
    prefix="/standard_product",
    tags=["standard_product"]
)

@router.get("/")
def get_standard_products(db: Session = Depends(get_db)):
    standard_products = db.query(StandardProduct).all()
    return standard_products

@router.post("/")
def create_standard_product(name: str, db: Session = Depends(get_db)):
    standard_product = StandardProduct(standname=name)
    db.add(standard_product)
    db.commit()
    db.refresh(standard_product)
    return standard_product

@router.get("/{standard_product_id}")
def get_standard_product(standard_product_id: int, db: Session = Depends(get_db)):
    standard_product = db.query(StandardProduct).filter(StandardProduct.id == standard_product_id).first()
    if not standard_product:
        raise HTTPException(status_code=404, detail="Standard Product not found")
    return standard_product

@router.put("/{standard_product_id}")
def update_standard_product(standard_product_id: int, name: str = None, db: Session = Depends(get_db)):
    standard_product = db.query(StandardProduct).filter(StandardProduct.id == standard_product_id).first()
    if not standard_product:
        raise HTTPException(status_code=404, detail="Standard Product not found")
    
    if name:
        standard_product.standname = name
    
    db.commit()
    db.refresh(standard_product)
    return standard_product

@router.delete("/{standard_product_id}")
def delete_standard_product(standard_product_id: int, db: Session = Depends(get_db)):
    standard_product = db.query(StandardProduct).filter(StandardProduct.id == standard_product_id).first()
    if not standard_product:
        raise HTTPException(status_code=404, detail="Standard Product not found")
    
    db.delete(standard_product)
    db.commit()
    return {"detail": "Standard Product deleted successfully"}