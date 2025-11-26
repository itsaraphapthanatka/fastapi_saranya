from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.collectionImage import CollectionImage
from datetime import datetime
from datetime import datetime
from fastapi import UploadFile, File, Form
import os
import shutil
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/collection_image",
    tags=["collection_image"]
)

class ReorderPayload(BaseModel):
    orderIds: List[int]


@router.get("/{collection_id}")
def get_collection_images(collection_id: int, db: Session = Depends(get_db)):
    collection_images = db.query(CollectionImage).filter(CollectionImage.collection_id == collection_id).all()
    if not collection_images:
        raise HTTPException(status_code=404, detail="Collection Images not found")
    return collection_images

@router.post("/")
def create_collection_image(collection_id: int,file: UploadFile = File(...), db: Session = Depends(get_db)):
    upload_dir = os.path.join(os.getcwd(), "app", "static", "collectionImg")
    os.makedirs(upload_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    filename = f"{timestamp}_{os.path.basename(file.filename)}"
    dest_path = os.path.join(upload_dir, filename)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = f"/static/collectionImg/{filename}"
    max_position = db.query(func.max(CollectionImage.id)).scalar() or 0
    collection_image = CollectionImage(collection_id=collection_id, collection_img=img, position=max_position + 1)
    db.add(collection_image)
    db.commit()
    db.refresh(collection_image)
    return collection_image

@router.get("/{collection_image_id}")
def get_collection_image(collection_image_id: int, collection_image_collection_id: int, db: Session = Depends(get_db)):
    collection_image = db.query(CollectionImage).filter(CollectionImage.id == collection_image_id, CollectionImage.collection_id == collection_image_collection_id).first()
    if not collection_image:
        raise HTTPException(status_code=404, detail="Collection Image not found")
    return collection_image

@router.put("/reorder")
def reorder_collection_images(payload: ReorderPayload, collection_id: int, db: Session = Depends(get_db)):
    for position, image_id in enumerate(payload.orderIds):
        collection_image = db.query(CollectionImage).filter(CollectionImage.id == image_id, CollectionImage.collection_id == collection_id).first()
        if collection_image:
            collection_image.position = position
    db.commit()
    return {"detail": "ok"}

@router.put("/{collection_image_id}")
def update_collection_image(collection_image_id: int, img: str = None, db: Session = Depends(get_db)):
    collection_image = db.query(CollectionImage).filter(CollectionImage.id == collection_image_id).first()
    if not collection_image:
        raise HTTPException(status_code=404, detail="Collection Image not found")
    
    if img:
        collection_image.img = img
    
    db.commit()
    db.refresh(collection_image)
    return collection_image

@router.delete("/{collection_image_id}")
def delete_collection_image(collection_image_id: int, db: Session = Depends(get_db)):
    collection_image = db.query(CollectionImage).filter(CollectionImage.id == collection_image_id).first()
    if not collection_image:
        raise HTTPException(status_code=404, detail="Collection Image not found")
    
    db.delete(collection_image)
    db.commit()
    return {"detail": "Collection Image deleted successfully"}
