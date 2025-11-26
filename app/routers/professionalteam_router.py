from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.professionalteam import ProfessionalTeam
from pydantic import BaseModel
from typing import List
import os
import shutil

router = APIRouter(
    prefix="/professionalteam",
    tags=["professionalteam"]
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
def get_professtionalTeam(db: Session = Depends(get_db)):    
    return db.query(ProfessionalTeam).order_by(ProfessionalTeam.position.asc()).all()


@router.post("/")
def create_ProfessionalTeam(img: str, db: Session = Depends(get_db)):
    exp = ProfessionalTeam(img=img)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


# -----------------------
# Reorder API (แก้ 422)
# -----------------------
@router.put("/reorder")
def reorder_ProfessionalTeam(payload: ReorderPayload, db: Session = Depends(get_db)):

    # payload.order เป็น List[int] ที่ validate แล้ว
    order_list = payload.order

    for index, exp_id in enumerate(order_list):
        exp = db.query(ProfessionalTeam).filter(ProfessionalTeam.id == exp_id).first()
        if not exp:
            raise HTTPException(404, f"ProfessionalTeam ID {exp_id} not found")

        exp.position = index

    db.commit()
    return {"detail": "ok"}


@router.get("/{ProfessionalTeam_id}")
def get_ProfessionalTeam(ProfessionalTeam_id: int, db: Session = Depends(get_db)):
    exp = db.query(ProfessionalTeam).filter(ProfessionalTeam.id == ProfessionalTeam_id).first()
    if not exp:
        raise HTTPException(404, "ProfessionalTeam not found")
    return exp


@router.put("/{ProfessionalTeam_id}")
def update_ProfessionalTeam(ProfessionalTeam_id: int, img: str = None, db: Session = Depends(get_db)):
    exp = db.query(ProfessionalTeam).filter(ProfessionalTeam.id == ProfessionalTeam_id).first()
    if not exp:
        raise HTTPException(404, "ProfessionalTeam not found")

    if img:
        exp.img = img

    db.commit()
    db.refresh(exp)
    return exp


@router.delete("/{ProfessionalTeam_id}")
def delete_ProfessionalTeam(ProfessionalTeam_id: int, db: Session = Depends(get_db)):
    exp = db.query(ProfessionalTeam).filter(ProfessionalTeam.id == ProfessionalTeam_id).first()
    if not exp:
        raise HTTPException(404, "ProfessionalTeam not found")

    db.delete(exp)
    db.commit()
    return {"detail": "ProfessionalTeam deleted successfully"}


# -----------------------
# File Upload
# -----------------------
@router.post("/upload-image/")
def upload_ProfessionalTeam_image(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    upload_dir = os.path.join(os.getcwd(), "app", "static", "ProfessionalTeam")
    os.makedirs(upload_dir, exist_ok=True)

    file_location = os.path.join(upload_dir, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"/static/ProfessionalTeam/{file.filename}"
    max_position = db.query(func.max(ProfessionalTeam.position)).scalar() or 0
    exp = ProfessionalTeam(img=image_url, position=max_position + 1)
    db.add(exp)
    db.commit()
    db.refresh(exp)

    return exp
