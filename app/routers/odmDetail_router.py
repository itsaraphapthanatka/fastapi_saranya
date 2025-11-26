from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.odmDetail import OdmDetail
from datetime import datetime
from fastapi import UploadFile, File, Form
import os
import shutil
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/odm_detail",
    tags=["odm_detail"]
)

class ReorderPayload(BaseModel):
    orderIds: List[int]

@router.get("/{odm_id}")
def get_odm_details(odm_id: int, db: Session = Depends(get_db)):
    odm_details = db.query(OdmDetail).filter(OdmDetail.odm_id == odm_id).all()
    if not odm_details:
        raise HTTPException(status_code=404, detail="ODM Details not found")
    return odm_details


@router.post("/")
def create_odm_detail(odm_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    upload_dir = os.path.join(os.getcwd(), "app", "static", "odmImg")
    os.makedirs(upload_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    filename = f"{timestamp}_{os.path.basename(file.filename)}"
    dest_path = os.path.join(upload_dir, filename)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = f"/static/odmImg/{filename}"
    max_position = db.query(func.max(OdmDetail.id)).scalar() or 0

    odm_detail = OdmDetail(odm_id=odm_id, img=img, position=max_position + 1)
    db.add(odm_detail)
    db.commit()
    db.refresh(odm_detail)
    return odm_detail

@router.get("/{odm_detail_id}")
def get_odm_detail(odm_detail_id: int, odm_detail_odm_id: int, db: Session = Depends(get_db)):
    odm_detail = db.query(OdmDetail).filter(OdmDetail.id == odm_detail_id, OdmDetail.odm_id == odm_detail_odm_id).first()
    if not odm_detail:
        raise HTTPException(status_code=404, detail="ODM Detail not found")
    return odm_detail

@router.put("/{odm_detail_id}")
def update_odm_detail(odm_detail_id: int, img: str = None, db: Session = Depends(get_db)):
    odm_detail = db.query(OdmDetail).filter(OdmDetail.id == odm_detail_id).first()
    if not odm_detail:
        raise HTTPException(status_code=404, detail="ODM Detail not found")
    
    if img:
        odm_detail.img = img
    
    db.commit()
    db.refresh(odm_detail)
    return odm_detail

@router.delete("/odm_detail/{odm_detail_id}")
def delete_odm_detail(odm_detail_id: int, db: Session = Depends(get_db)):
    odm_detail = db.query(OdmDetail).filter(OdmDetail.id == odm_detail_id).first()
    if not odm_detail:
        raise HTTPException(status_code=404, detail="ODM Detail not found")
    
    # ลบไฟล์รูปภาพจากโฟลเดอร์ด้วย
    file_path = odm_detail.img.replace("/static", os.path.join(os.getcwd(), "app", "static"))
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(odm_detail)
    db.commit()
    return {"detail": "ODM Detail deleted successfully"}

@router.put("/reorder/")
def reorder_odm_details(payload: ReorderPayload, odm_id: int, db: Session = Depends(get_db)):
    for position, detail_id in enumerate(payload.orderIds):
        odm_detail = db.query(OdmDetail).filter(
            OdmDetail.id == detail_id,
            OdmDetail.odm_id == odm_id
        ).first()
        if odm_detail:
            odm_detail.position = position

    db.commit()
    return {"detail": "ok"}

@router.post("/upload-image/")
def upload_odm_detail_image(
    odm_id: int,
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    upload_dir = os.path.join(os.getcwd(), "app", "static", "odmImg")
    os.makedirs(upload_dir, exist_ok=True)

    file_location = os.path.join(upload_dir, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"/static/odmImg/{file.filename}"
    max_position = db.query(func.max(OdmDetail.position)).filter(OdmDetail.odm_id == odm_id).scalar() or 0
    odm_detail = OdmDetail(odm_id=odm_id,img=image_url, position=max_position + 1)
    db.add(odm_detail)
    db.commit()
    db.refresh(odm_detail)
    return odm_detail