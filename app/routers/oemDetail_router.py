from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.oemDetail import OEMDtail
from datetime import datetime
from fastapi import UploadFile, File, Form
import os
import shutil
from pydantic import BaseModel
from typing import List 

router = APIRouter(
    prefix="/oem_detail",
    tags=["oem_detail"]
)

class ReorderPayload(BaseModel):
    orderIds: List[int]

@router.get("/{oem_id}")
def get_oem_details(oem_id: int, db: Session = Depends(get_db)):
    oem_details = db.query(OEMDtail).filter(OEMDtail.oem_id == oem_id).all()
    if not oem_details:
        raise HTTPException(status_code=404, detail="oem Details not found")
    return oem_details


@router.post("/")
def create_oem_detail(oem_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    upload_dir = os.path.join(os.getcwd(), "app", "static", "oemImg")
    os.makedirs(upload_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    filename = f"{timestamp}_{os.path.basename(file.filename)}"
    dest_path = os.path.join(upload_dir, filename)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = f"/static/oemImg/{filename}"
    max_position = db.query(func.max(OEMDtail.id)).scalar() or 0

    oem_detail = OEMDtail(oem_id=oem_id, img=img, position=max_position + 1)
    db.add(oem_detail)
    db.commit()
    db.refresh(oem_detail)
    return oem_detail

@router.get("/{oem_detail_id}")
def get_oem_detail(oem_detail_id: int, oem_detail_oem_id: int, db: Session = Depends(get_db)):
    oem_detail = db.query(OEMDtail).filter(OEMDtail.id == oem_detail_id, OEMDtail.oem_id == oem_detail_oem_id).first()
    if not oem_detail:
        raise HTTPException(status_code=404, detail="oem Detail not found")
    return oem_detail

@router.put("/{oem_detail_id}")
def update_oem_detail(oem_detail_id: int, img: str = None, db: Session = Depends(get_db)):
    oem_detail = db.query(OEMDtail).filter(OEMDtail.id == oem_detail_id).first()
    if not oem_detail:
        raise HTTPException(status_code=404, detail="oem Detail not found")
    
    if img:
        oem_detail.img = img
    
    db.commit()
    db.refresh(oem_detail)
    return oem_detail

@router.delete("/oem_detail/{oem_detail_id}")
def delete_oem_detail(oem_detail_id: int, db: Session = Depends(get_db)):
    oem_detail = db.query(OEMDtail).filter(OEMDtail.id == oem_detail_id).first()
    if not oem_detail:
        raise HTTPException(status_code=404, detail="oem Detail not found")
    
    # ลบไฟล์รูปภาพจากโฟลเดอร์ด้วย
    file_path = oem_detail.img.replace("/static", os.path.join(os.getcwd(), "app", "static"))
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(oem_detail)
    db.commit()
    return {"detail": "oem Detail deleted successfully"}

@router.put("/reorder/")
def reorder_oem_details(payload: ReorderPayload, oem_id: int, db: Session = Depends(get_db)):
    for position, detail_id in enumerate(payload.orderIds):
        oem_detail = db.query(OEMDtail).filter(
            OEMDtail.id == detail_id,
            OEMDtail.oem_id == oem_id
        ).first()
        if oem_detail:
            oem_detail.position = position

    db.commit()
    return {"detail": "ok"}

@router.post("/upload-image/")
def upload_oem_detail_image(
    oem_id: int,
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    upload_dir = os.path.join(os.getcwd(), "app", "static", "oemImg")
    os.makedirs(upload_dir, exist_ok=True)

    file_location = os.path.join(upload_dir, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"/static/oemImg/{file.filename}"
    max_position = db.query(func.max(OEMDtail.position)).filter(OEMDtail.oem_id == oem_id).scalar() or 0
    oem_detail = OEMDtail(oem_id=oem_id,img=image_url, position=max_position + 1)
    db.add(oem_detail)
    db.commit()
    db.refresh(oem_detail)
    return oem_detail