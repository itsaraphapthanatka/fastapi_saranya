from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.collection import Collection
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(
    prefix="/collection",
    tags=["collection"]
)

class CollectionCreate(BaseModel):
    name: str
    name_th: str = None 


@router.get("/")
def get_collections(db: Session = Depends(get_db)):
    collections = db.query(Collection).all()
    return collections

@router.post("/")
def create_collection(collection_create: CollectionCreate, db: Session = Depends(get_db)):
    collection = Collection(collec_name=collection_create.name, collec_name_th=collection_create.name_th)
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
def update_collection(collection_id: int, collection_update: CollectionCreate, db: Session = Depends(get_db)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    if collection_update.name:
        collection.collec_name = collection_update.name
    if collection_update.name_th:
        collection.collec_name_th = collection_update.name_th 
    
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
