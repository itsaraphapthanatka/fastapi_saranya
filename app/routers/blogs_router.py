from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import UploadFile, File
from app.database import get_db
from app.models.blogs import Blogs
from datetime import datetime
import os
import shutil
from pydantic import BaseModel
from typing import List




router = APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)

class BlogCreate(BaseModel):
    title: str
    title_th: str = None
    content: str
    content_th: str = None
    blogsType: str = None
    createBy: str = None
    blogsStatus: str = None
    img: str  # URL หรือ path ของรูปที่ส่งมาใน JSON

@router.get("/")
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blogs).all()
    return blogs

@router.post("/")
def create_blog(
    title: str = Form(...),
    title_th: str = Form(None),
    content: str = Form(...),
    content_th: str = Form(None),
    blogsType: str = Form(None),
    createBy: str = Form(None),
    blogsStatus: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    upload_dir = os.path.join(os.getcwd(), "app", "static", "blogImg")
    os.makedirs(upload_dir, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    filename = f"{timestamp}_{os.path.basename(file.filename)}"
    dest_path = os.path.join(upload_dir, filename)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img_url = f"/static/blogImg/{filename}"
    blog = Blogs(
        title=title,
        title_th=title_th,
        content=content,
        content_th=content_th,
        img=img_url,
        blogsType=blogsType,
        createBy=createBy,
        blogsStatus='active' if blogsStatus is None else blogsStatus
    )

    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@router.get("/{blog_id}")
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blogs).filter(Blogs.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.put("/{blog_id}")
def update_blog(
    blog_id: int,
    title: str = Form(None),
    title_th: str = Form(None),
    content: str = Form(None),
    content_th: str = Form(None),
    blogsType: str = Form(None),
    blogsStatus: str = Form(None),
    file: UploadFile = File(None),  # <-- optional
    db: Session = Depends(get_db)
):
    blog = db.query(Blogs).filter(Blogs.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # อัปเดตข้อมูลที่มี aaaaaa
    if title:
        blog.title = title
    if title_th:
            blog.title_th = title_th
    if content:
        blog.content = content
    if content_th:
        blog.content_th = content_th
    if blogsType:
        blog.blogsType = blogsType
    if blogsStatus:
        blog.blogsStatus = blogsStatus

    # อัปโหลดไฟล์ถ้ามี
    if file:
        upload_dir = os.path.join(os.getcwd(), "app", "static", "blogImg")
        os.makedirs(upload_dir, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        blog.img = f"/static/blogImg/{filename}"

    db.commit()
    db.refresh(blog)
    return blog



@router.delete("/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blogs).filter(Blogs.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    db.delete(blog)
    db.commit()
    return {"detail": "Blog deleted successfully"}