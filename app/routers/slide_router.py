from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.slide import Slide
from datetime import datetime
from fastapi import UploadFile, File, Form
import os
import shutil
from pydantic import BaseModel

router = APIRouter(
    prefix="/slides",
    tags=["slides"]
)

# Pydantic model สำหรับรับข้อมูลสร้าง slide
class SlideCreate(BaseModel):
    slide_image: str
    slide_desc: str

# Pydantic model สำหรับ response
class SlideResponse(BaseModel):
    id: int
    slide_image: str
    slide_desc: str
    position: int

    class Config:
        orm_mode = True

@router.get("/")
def get_slides(db: Session = Depends(get_db)):
    return db.query(Slide).order_by(Slide.position.asc()).all()


@router.post("/", response_model=SlideResponse)
def create_slide(slide: SlideCreate, db: Session = Depends(get_db)):
    max_position = db.query(func.max(Slide.position)).scalar() or 0
    db_slide = Slide(
        slide_image=slide.slide_image,
        slide_desc=slide.slide_desc,
        position=max_position + 1
    )
    db.add(db_slide)
    db.commit()
    db.refresh(db_slide)
    return db_slide


@router.post("/upload")
def upload_slide(file: UploadFile = File(...), slide_desc: str = Form(""), db: Session = Depends(get_db)):
    # ensure upload directory exists
    upload_dir = os.path.join(os.getcwd(), "app", "static", "slides")
    os.makedirs(upload_dir, exist_ok=True)

    # create a unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    filename = f"{timestamp}_{os.path.basename(file.filename)}"
    dest_path = os.path.join(upload_dir, filename)

    # save file to disk
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # store a web-friendly path in the DB (serve /static/ with your web server)
    slide_image_url = f"/static/slides/{filename}"
    max_position = db.query(func.max(Slide.position)).scalar() or 0
    slide = Slide(slide_image=slide_image_url, slide_desc=slide_desc, position=max_position + 1)
    db.add(slide)
    db.commit()
    db.refresh(slide)
    return slide

@router.put("/reorder")
def reorder_slides(payload: dict, db: Session = Depends(get_db)):
    order = payload.get("order", [])

    for index, slide_id in enumerate(order):
        slide = db.query(Slide).filter(Slide.id == slide_id).first()
        if slide:
            slide.position = index

    db.commit()
    return {"detail": "ok"}

@router.get("/{slide_id}")
def get_slide(slide_id: int, db: Session = Depends(get_db)):
    slide = db.query(Slide).filter(Slide.id == slide_id).first()
    if not slide:
        raise HTTPException(status_code=404, detail="Slide not found")
    return slide

@router.put("/{slide_id}")
def update_slide(slide_id: int, slide_image: str = None, slide_desc: str = None, position: int = None,   db: Session = Depends(get_db)):
    slide = db.query(Slide).filter(Slide.id == slide_id).first()
    if not slide:
        raise HTTPException(status_code=404, detail="Slide not found")
    
    if slide_image:
        slide.slide_image = slide_image
    if slide_desc:
        slide.slide_desc = slide_desc
    if position:
        slide.position = position
    
    db.commit()
    db.refresh(slide)
    return slide

@router.delete("/{slide_id}")
def delete_slide(slide_id: int, db: Session = Depends(get_db)):
    slide = db.query(Slide).filter(Slide.id == slide_id).first()
    if not slide:
        raise HTTPException(status_code=404, detail="Slide not found")
    
    db.delete(slide)
    db.commit()
    return {"detail": "Slide deleted successfully"}