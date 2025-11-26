from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.experience import Experience
from pydantic import BaseModel
from typing import List
import os
import shutil

router = APIRouter(
    prefix="/experience",
    tags=["experience"]
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
def get_experiences(db: Session = Depends(get_db)):
    return db.query(Experience).order_by(Experience.position.asc()).all()


@router.post("/")
def create_experience(img: str, db: Session = Depends(get_db)):
    exp = Experience(img=img)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


# -----------------------
# Reorder API (แก้ 422)
# -----------------------
@router.put("/reorder")
def reorder_experience(payload: ReorderPayload, db: Session = Depends(get_db)):

    # payload.order เป็น List[int] ที่ validate แล้ว
    order_list = payload.order

    for index, exp_id in enumerate(order_list):
        exp = db.query(Experience).filter(Experience.id == exp_id).first()
        if not exp:
            raise HTTPException(404, f"Experience ID {exp_id} not found")

        exp.position = index

    db.commit()
    return {"detail": "ok"}


@router.get("/{experience_id}")
def get_experience(experience_id: int, db: Session = Depends(get_db)):
    exp = db.query(Experience).filter(Experience.id == experience_id).first()
    if not exp:
        raise HTTPException(404, "Experience not found")
    return exp


@router.put("/{experience_id}")
def update_experience(experience_id: int, img: str = None, db: Session = Depends(get_db)):
    exp = db.query(Experience).filter(Experience.id == experience_id).first()
    if not exp:
        raise HTTPException(404, "Experience not found")

    if img:
        exp.img = img

    db.commit()
    db.refresh(exp)
    return exp


@router.delete("/{experience_id}")
def delete_experience(experience_id: int, db: Session = Depends(get_db)):
    exp = db.query(Experience).filter(Experience.id == experience_id).first()
    if not exp:
        raise HTTPException(404, "Experience not found")

    db.delete(exp)
    db.commit()
    return {"detail": "Experience deleted successfully"}


# -----------------------
# File Upload
# -----------------------
@router.post("/upload-image/")
def upload_experience_image(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    upload_dir = os.path.join(os.getcwd(), "app", "static", "experience")
    os.makedirs(upload_dir, exist_ok=True)

    file_location = os.path.join(upload_dir, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"/static/experience/{file.filename}"
    max_position = db.query(func.max(Experience.position)).scalar() or 0
    exp = Experience(img=image_url, position=max_position + 1)
    db.add(exp)
    db.commit()
    db.refresh(exp)

    return exp
