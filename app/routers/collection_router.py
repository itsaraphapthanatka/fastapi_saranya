from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.collection import Collection
from datetime import datetime

router = APIRouter(
    prefix="/collection",
    tags=["collection"]
)

@router.get("/")
def get_collections(db: Session = Depends(get_db)):
    collections = db.query(Collection).all()
    return collections

@router.post("/")
def create_collection(name: str, name_th: str = None, db: Session = Depends(get_db)):
    collection = Collection(collec_name=name, collec_name_th=name_th)
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection

@router.get("/{collection_id}")
def get_collection(collection_id: int, db: Session = Depends(get_db)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

@router.put("/{collection_id}")
def update_collection(collection_id: int, name: str = None, name_th: str = None, db: Session = Depends(get_db)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    if name:
        collection.collec_name = name
    if name_th:
        collection.collec_name_th = name_th 
    
    db.commit()
    db.refresh(collection)
    return collection

@router.delete("/{collection_id}")
def delete_collection(collection_id: int, db: Session = Depends(get_db)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    db.delete(collection)
    db.commit()
    return {"detail": "Collection deleted successfully"}
