from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.standardSetDetail import StandardSetDetail
from datetime import datetime
from fastapi import UploadFile, File, Form
import os
import shutil
from pydantic import BaseModel

router = APIRouter(
    prefix="/standard_set_detail",
    tags=["standard_set_detail"]
)

@router.get("/")
def get_standard_set_details(db: Session = Depends(get_db)):
    standard_set_details = db.query(StandardSetDetail).all()
    return standard_set_details

@router.post("/")
def create_standard_set_detail(
        file: UploadFile = File(...), 
        s_id: int = Form(...),
        s_set_id: str = Form(""), 
        s_set_title: str = Form(""), 
        s_set_desc: str = Form(""),
        s_set_chk_main: int = None,
        db: Session = Depends(get_db)
    ):
    upload_dir = os.path.join(os.getcwd(), "app", "static", "productdetailImg")
    os.makedirs(upload_dir, exist_ok=True)
    max_position = db.query(func.max(StandardSetDetail.position)).scalar() or 0

    # create a unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    filename = f"{timestamp}_{os.path.basename(file.filename)}"
    dest_path = os.path.join(upload_dir, filename)

    # save file to disk
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    img = f"/static/productdetailImg/{filename}"
    standard_set_detail = StandardSetDetail(
        s_id=s_id,
        s_set_img=img,
        s_set_id=s_set_id,
        s_set_title=s_set_title,
        s_set_desc=s_set_desc,
        s_set_chk_main=s_set_chk_main,
        position=max_position + 1
    )
    db.add(standard_set_detail)
    db.commit()
    db.refresh(standard_set_detail)
    return standard_set_detail


@router.get("/standard_set")
def get_standard_set_details_by_s_set_id(s_id: int, s_set_id: int, db: Session = Depends(get_db)):
    standard_set_details = db.query(StandardSetDetail).filter(StandardSetDetail.s_set_id == s_set_id, StandardSetDetail.s_id == s_id).all()
    if not standard_set_details:
        raise HTTPException(status_code=404, detail="No Standard Set Details found for the given Standard Set ID")
    return standard_set_details

@router.get("/{standard_set_detail_id}")
def get_standard_set_detail(standard_set_detail_id: int, db: Session = Depends(get_db)):
    standard_set_detail = db.query(StandardSetDetail).filter(StandardSetDetail.id == standard_set_detail_id).first()
    if not standard_set_detail:
        raise HTTPException(status_code=404, detail="Standard Set Detail not found")
    return standard_set_detail

@router.put("/{standard_set_detail_id}")
def update_standard_set_detail(
        standard_set_detail_id: int, 
        s_set_title: str = None,
        s_set_desc: str = None,
        s_set_img: UploadFile = File(...) , 
        s_set_chk_main: int = None,
        db: Session = Depends(get_db)
    ):
    print(f"qqqqqq: {s_set_chk_main}")
    standard_set_detail = db.query(StandardSetDetail).filter(
        StandardSetDetail.id == standard_set_detail_id
    ).first()

    if not standard_set_detail:
        raise HTTPException(status_code=404, detail="Standard Set Detail not found")

    # ถ้าเลือก main ต้อง reset ตัวอื่นเป็น 0
    if s_set_chk_main == 1:
        db.query(StandardSetDetail).filter(
            StandardSetDetail.s_set_id == standard_set_detail.s_set_id
        ).update({ StandardSetDetail.s_set_chk_main: 0 })

    # อัปเดตตัวที่เลือก
    if s_set_chk_main is not None:
        standard_set_detail.s_set_chk_main = s_set_chk_main
    if s_set_title is not None:
        standard_set_detail.s_set_title = s_set_title
    if s_set_desc is not None:
        standard_set_detail.s_set_desc = s_set_desc
    if s_set_img is not None:
        standard_set_detail.s_set_img = s_set_img

    db.commit()
    db.refresh(standard_set_detail)
    return standard_set_detail


@router.delete("/{standard_set_detail_id}")
def delete_standard_set_detail(standard_set_detail_id: int, db: Session = Depends(get_db)):
    standard_set_detail = db.query(StandardSetDetail).filter(StandardSetDetail.id == standard_set_detail_id).first()
    if not standard_set_detail:
        raise HTTPException(status_code=404, detail="Standard Set Detail not found")
    
    db.delete(standard_set_detail)
    db.commit()
    return {"detail": "Standard Set Detail deleted successfully"}