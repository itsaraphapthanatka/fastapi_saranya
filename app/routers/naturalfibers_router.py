from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.naturalfibers import NaturalFibers
from pydantic import BaseModel
from typing import List
import os
import shutil

router = APIRouter(
    prefix="/naturalfibers",
    tags=["naturalfibers"]
)

# -----------------------
# Pydantic Model
# -----------------------
class ReorderPayload(BaseModel):
    order: List[int]


# -----------------------
# CRUD
# -----------------------
@router.get("/")
def get_natural_fiber(db: Session = Depends(get_db)):    
    return db.query(NaturalFibers).order_by(NaturalFibers.position.asc()).all()


@router.post("/")
def create_natural_fiber(img: str, db: Session = Depends(get_db)):
    exp = NaturalFibers(img=img)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


# -----------------------
# Reorder API (แก้ 422)
# -----------------------
@router.put("/reorder")
def reorder_natural_fiber(payload: ReorderPayload, db: Session = Depends(get_db)):

    # payload.order เป็น List[int] ที่ validate แล้ว
    order_list = payload.order

    for index, exp_id in enumerate(order_list):
        exp = db.query(NaturalFibers).filter(NaturalFibers.id == exp_id).first()
        if not exp:
            raise HTTPException(404, f"NaturalFibers ID {exp_id} not found")

        exp.position = index

    db.commit()
    return {"detail": "ok"}


@router.get("/{id}")
def get_natural_fiber(id: int, db: Session = Depends(get_db)):
    exp = db.query(NaturalFibers).filter(NaturalFibers.id == id).first()
    if not exp:
        raise HTTPException(404, "NaturalFibers not found")
    return exp


@router.put("/{id}")
def update_natural_fiber(id: int, img: str = None, db: Session = Depends(get_db)):
    exp = db.query(NaturalFibers).filter(NaturalFibers.id == id).first()
    if not exp:
        raise HTTPException(404, "NaturalFibers not found")

    if img:
        exp.img = img

    db.commit()
    db.refresh(exp)
    return exp


@router.delete("/{id}")
def delete_natural_fiber(id: int, db: Session = Depends(get_db)):
    exp = db.query(NaturalFibers).filter(NaturalFibers.id == id).first()
    if not exp:
        raise HTTPException(404, "NaturalFibers not found")

    db.delete(exp)
    db.commit()
    return {"detail": "NaturalFibers deleted successfully"}


# -----------------------
# File Upload
# -----------------------
@router.post("/upload-image/")
def upload_natural_fiber_image(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    upload_dir = os.path.join(os.getcwd(), "app", "static", "NaturalFibers")
    os.makedirs(upload_dir, exist_ok=True)

    file_location = os.path.join(upload_dir, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"/static/NaturalFibers/{file.filename}"
    max_position = db.query(func.max(NaturalFibers.position)).scalar() or 0
    exp = NaturalFibers(img=image_url, position=max_position + 1)
    db.add(exp)
    db.commit()
    db.refresh(exp)

    return exp


