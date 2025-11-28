from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.internationnal import Internationnal
from pydantic import BaseModel
from typing import List
import os
import shutil

router = APIRouter(
    prefix="/internationnal",
    tags=["internationnal_standards"]
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
def get_internationnal_standards(db: Session = Depends(get_db)):
    return db.query(Internationnal).order_by(Internationnal.position.asc()).all()


@router.post("/")
def create_Internationnal(img: str, db: Session = Depends(get_db)):
    exp = Internationnal(img=img)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


# -----------------------
# Reorder API (แก้ 422)
# -----------------------
@router.put("/reorder")
def reorder_Internationnal(payload: ReorderPayload, db: Session = Depends(get_db)):

    # payload.order เป็น List[int] ที่ validate แล้ว
    order_list = payload.order

    for index, exp_id in enumerate(order_list):
        exp = db.query(Internationnal).filter(Internationnal.id == exp_id).first()
        if not exp:
            raise HTTPException(404, f"Internationnal ID {exp_id} not found")

        exp.position = index

    db.commit()
    return {"detail": "ok"}


@router.get("/{Internationnal_id}")
def get_Internationnal(Internationnal_id: int, db: Session = Depends(get_db)):
    exp = db.query(Internationnal).filter(Internationnal.id == Internationnal_id).first()
    if not exp:
        raise HTTPException(404, "Internationnal not found")
    return exp


@router.put("/{Internationnal_id}")
def update_Internationnal(Internationnal_id: int, img: str = None, db: Session = Depends(get_db)):
    exp = db.query(Internationnal).filter(Internationnal.id == Internationnal_id).first()
    if not exp:
        raise HTTPException(404, "Internationnal not found")

    if img:
        exp.img = img

    db.commit()
    db.refresh(exp)
    return exp


@router.delete("/{Internationnal_id}")
def delete_Internationnal(Internationnal_id: int, db: Session = Depends(get_db)):
    exp = db.query(Internationnal).filter(Internationnal.id == Internationnal_id).first()
    if not exp:
        raise HTTPException(404, "Internationnal not found")

    db.delete(exp)
    db.commit()
    return {"detail": "Internationnal deleted successfully"}


# -----------------------
# File Upload
# -----------------------
@router.post("/upload-image/")
def upload_Internationnal_image(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    upload_dir = os.path.join(os.getcwd(), "app", "static", "Internationnal")
    os.makedirs(upload_dir, exist_ok=True)

    file_location = os.path.join(upload_dir, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"/static/Internationnal/{file.filename}"
    max_position = db.query(func.max(Internationnal.position)).scalar() or 0
    exp = Internationnal(img=image_url, position=max_position + 1)
    db.add(exp)
    db.commit()
    db.refresh(exp)

    return exp
