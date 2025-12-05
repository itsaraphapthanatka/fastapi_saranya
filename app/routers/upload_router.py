from fastapi import APIRouter, UploadFile, File
from fastapi.staticfiles import StaticFiles
import os
import shutil
from datetime import datetime
router = APIRouter(
     prefix="/upload",
    tags=["upload"]
)

# สร้างโฟลเดอร์เก็บรูป

@router.post("/upload-image")
async  def upload_file(file: UploadFile = File(...)):
    print(file)
    upload_dir = os.path.join(os.getcwd(), "app", "static", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    # Mount static files
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    filename = f"{timestamp}_{os.path.basename(file.filename)}"
    dest_path = os.path.join(upload_dir, filename)

    file_path = os.path.join(dest_path, file.filename)
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    slide_image_url = f"/static/uploads/{filename}"
    return {"url": slide_image_url}
