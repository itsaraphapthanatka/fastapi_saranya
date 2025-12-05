from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import UploadFile
import tempfile

MAX_UPLOAD_SIZE = 1024 * 1024 * 100   # 100MB

class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if "multipart/form-data" in request.headers.get("Content-Type", ""):

            # อ่านข้อมูลทั้งหมด (stream)
            body = await request.body()

            if len(body) > MAX_UPLOAD_SIZE:
                return Response(
                    content=f"File too large. Max size is {MAX_UPLOAD_SIZE / (1024*1024)} MB",
                    status_code=413,
                )

        return await call_next(request)
