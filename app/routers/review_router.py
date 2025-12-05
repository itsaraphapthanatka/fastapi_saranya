from fastapi import APIRouter
from app.models.review import Review
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import os, time, shutil
from fastapi import UploadFile, File, Form

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

# Pydantic model สำหรับรับข้อมูลสร้าง review
class ReviewCreate(BaseModel):
    title: str
    title_th: str
    desc: str
    desc_th: str
    src: UploadFile = File(...)
    reviewstatus: int
    position: int
    createBy: str
    createAt: datetime

class ReviewUpdate(BaseModel):
    title: Optional[str] 
    title_th: Optional[str]
    desc: Optional[str]
    desc_th: Optional[str]
    src: Optional[str] = File(...)
    reviewstatus: Optional[str]
    position: Optional[int]
    editBy: Optional[str]
    editAt: Optional[datetime]

@router.get("/")
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).order_by(Review.position.asc()).all()

@router.get("/{review_id}")
def get_review(review_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.id == review_id).first()

@router.post("/")
def create_review(
    title: str = Form(...),
    title_th: str = Form(...),
    desc: str = Form(...),
    desc_th: str = Form(...),
    file: UploadFile = File(...),
    createBy: str = Form(...),
    db: Session = Depends(get_db)
):
    max_position = db.query(func.max(Review.position)).scalar() or 0
    upload_dir = os.path.join(os.getcwd(), "app", "static", "review")
    os.makedirs(upload_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    filename = f"{timestamp}_{os.path.basename(file.filename)}"
    dest_path = os.path.join(upload_dir, filename)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img_url = f"/static/review/{filename}"

    db_review = Review(
        title=title,
        title_th=title_th,
        desc=desc,
        desc_th=desc_th,
        src=img_url,
        reviewstatus='active',
        position=max_position + 1,
        createBy=createBy,
        createAt=datetime.now(),
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review    

@router.put("/{review_id}")
async def update_review(
    review_id: int,
    title: str = Form(...),
    title_th: str = Form(...),
    desc: str = Form(...),
    desc_th: str = Form(...),
    src: UploadFile = File(None),   # ← optional file
    reviewstatus: str = Form(...),
    editBy: str = Form(...),
    db: Session = Depends(get_db)
):

    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    # อัปเดตข้อมูลทั่วไป
    db_review.title = title
    db_review.title_th = title_th
    db_review.desc = desc
    db_review.desc_th = desc_th
    db_review.reviewstatus = reviewstatus
    db_review.editBy = editBy
    db_review.editAt = datetime.now()

    # อัปโหลดไฟล์เฉพาะกรณีมีไฟล์ใหม่
    if src is not None:
        upload_dir = os.path.join(os.getcwd(), "app", "static", "review")
        os.makedirs(upload_dir, exist_ok=True)

        timestamp = int(time.time())
        filename = f"{timestamp}_{os.path.basename(src.filename)}"
        dest_path = os.path.join(upload_dir, filename)

        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(src.file, buffer)

        img_url = f"/static/review/{filename}"
        db_review.src = img_url  # บันทึกเฉพาะกรณีมีไฟล์ใหม่

    db.commit()
    db.refresh(db_review)

    return db_review

@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(db_review)
    db.commit()
    return {"detail": "Review deleted successfully"}

