# app/custom_request.py
from starlette.requests import Request
from starlette.formparsers import MultiPartParser


class CustomMultipartParser(MultiPartParser):
    # จำกัดขนาดไฟล์ต่อไฟล์ (200MB)
    max_file_size = 1024 * 1024 * 200
    max_part_size = 1024 * 1024 * 200


class CustomRequest(Request):
    async def form(self):
        # ใช้ parser ใหม่แทนของเดิม
        parser = CustomMultipartParser(self)
        return await parser.parse()
