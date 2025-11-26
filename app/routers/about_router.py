from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.about import About
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile, File, Form
import os
import shutil

router = APIRouter(
    prefix="/about",
    tags=["about"]
)

class AboutUpdate(BaseModel):
    desc: Optional[str] = None
    founderName: Optional[str] = None
    founderDesc: Optional[str] = None
    founderImg: Optional[str] = None
    sec2Desc: Optional[str] = None
    sec2Img: Optional[str] = None
    sec3Desc: Optional[str] = None
    sec3img: Optional[str] = None
    sec3Experience: Optional[str] = None
    sec4Desc: Optional[str] = None
    sec4img: Optional[str] = None

@router.post("/")
def create_about(
        desc: str, 
        founderName: str = None,
        founderDesc: str = None,
        founderImg: str = None,
        sec2Desc: str = None,
        sec2Img: str = None,
        sec3Desc: str = None,
        sec3img: str = None,
        sec3Experience: str = None,
        sec4Desc: str = None,
        sec4img: str = None,
        db: Session = Depends(get_db)
    ):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    about = About(
        Desc=desc,
        founderName=founderName,
        founderDesc=founderDesc,
        founderImg=founderImg,
        sec2Desc=sec2Desc,
        sec2Img=sec2Img,
        sec3Desc=sec3Desc,
        sec3img=sec3img,
        sec3Experience=sec3Experience,
        sec4Desc=sec4Desc,
        sec4img=sec4img
        )
    db.add(about)
    db.commit()
    db.refresh(about)
    return about

@router.get("/")
def get_about(db: Session = Depends(get_db)):
    about = db.query(About).all()
    return about

@router.get("/{about_id}")
def get_about_section(about_id: int, db: Session = Depends(get_db)):
    about = db.query(About).filter(About.id == about_id).first()
    if not about:
        raise HTTPException(status_code=404, detail="About section not found")
    return about

@router.put("/{about_id}")
def update_about(
        about_id: int, 
        about_update: AboutUpdate,
        db: Session = Depends(get_db)
    ):
    existing_about = db.query(About).filter(About.id == about_id).first()
    if not existing_about:
        raise HTTPException(status_code=404, detail="About section not found")
    
    existing_about.desc = about_update.desc or existing_about.Desc
    existing_about.founderName = about_update.founderName or existing_about.founderName
    existing_about.founderDesc = about_update.founderDesc or existing_about.founderDesc
    existing_about.founderImg = about_update.founderImg or existing_about.founderImg
    existing_about.sec2Desc = about_update.sec2Desc or existing_about.sec2Desc
    existing_about.sec2Img = about_update.sec2Img or existing_about.sec2Img
    existing_about.sec3Desc = about_update.sec3Desc or existing_about.sec3Desc
    existing_about.sec3img = about_update.sec3img or existing_about.sec3img
    existing_about.sec3Experience = about_update.sec3Experience or existing_about.sec3Experience
    existing_about.sec4Desc = about_update.sec4Desc or existing_about.sec4Desc
    existing_about.sec4img = about_update.sec4img or existing_about.sec4img

    db.commit()
    db.refresh(existing_about)
    return existing_about

@router.delete("/{about_id}")
def delete_about(about_id: int, db: Session = Depends(get_db)):
    about = db.query(About).filter(About.id == about_id).first()
    if not about:
        raise HTTPException(status_code=404, detail="About section not found")
    
    db.delete(about)
    db.commit()
    return {"detail": "About section deleted successfully"}

@router.put("/update-founder-image/{about_id}")
def update_founder_image(
    about_id: int,
    founderImg: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    existing_about = db.query(About).filter(About.id == about_id).first()
    if not existing_about:
        raise HTTPException(status_code=404, detail="About not found")

    # directory
    upload_dir = os.path.join(os.getcwd(), "app", "static", "about")
    os.makedirs(upload_dir, exist_ok=True)

    # filename
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{time_stamp}_{founderImg.filename}"
    dest_path = os.path.join(upload_dir, filename)

    # save file
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(founderImg.file, buffer)

    # set URL
    founderImg_url = f"/static/about/{filename}"

    # update existing record
    existing_about.founderImg = founderImg_url

    db.commit()
    db.refresh(existing_about)

    return existing_about

@router.put("/update-sec2-image/{about_id}")
def update_sec2_image(
    about_id: int,
    sec2Img: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    existing_about = db.query(About).filter(About.id == about_id).first()
    if not existing_about:
        raise HTTPException(status_code=404, detail="About not found")

    # directory
    upload_dir = os.path.join(os.getcwd(), "app", "static", "about")
    os.makedirs(upload_dir, exist_ok=True)

    # filename
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{time_stamp}_{sec2Img.filename}"
    dest_path = os.path.join(upload_dir, filename)

    # save file
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(sec2Img.file, buffer)

    # set URL
    sec2Img_url = f"/static/about/{filename}"

    # update existing record
    existing_about.sec2Img = sec2Img_url

    db.commit()
    db.refresh(existing_about)

    return existing_about

@router.put("/update-sec3-image/{about_id}")
def update_sec3_image(
    about_id: int,
    sec3img: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    existing_about = db.query(About).filter(About.id == about_id).first()
    if not existing_about:
        raise HTTPException(status_code=404, detail="About not found")

    # directory
    upload_dir = os.path.join(os.getcwd(), "app", "static", "about")
    os.makedirs(upload_dir, exist_ok=True)

    # filename
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{time_stamp}_{sec3img.filename}"
    dest_path = os.path.join(upload_dir, filename)

    # save file
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(sec3img.file, buffer)

    # set URL
    sec3img_url = f"/static/about/{filename}"

    # update existing record
    existing_about.sec3img = sec3img_url

    db.commit()
    db.refresh(existing_about)

    return existing_about

@router.put("/update-sec4-image/{about_id}")
def update_sec4_image(
    about_id: int,
    sec4img: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    existing_about = db.query(About).filter(About.id == about_id).first()
    if not existing_about:
        raise HTTPException(status_code=404, detail="About not found")

    # directory
    upload_dir = os.path.join(os.getcwd(), "app", "static", "about")
    os.makedirs(upload_dir, exist_ok=True)

    # filename
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{time_stamp}_{sec4img.filename}"
    dest_path = os.path.join(upload_dir, filename)

    # save file
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(sec4img.file, buffer)

    # set URL
    sec4img_url = f"/static/about/{filename}"

    # update existing record
    existing_about.sec4img = sec4img_url

    db.commit()
    db.refresh(existing_about)

    return existing_about

