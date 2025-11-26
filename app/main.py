from fastapi import FastAPI
from app.routers import about_router
from app.routers import experience_router
from app.routers import professionalteam_router
from app.routers import naturalfibers_router
from app.routers import international_router
from app.routers import odm_router
from app.routers import oem_router
from app.routers import odmDetail_router
from app.routers import oemDetail_router
from app.routers import collection_router
from app.routers import collectionImage_router
from app.routers import standardProduct_router
from app.routers import standardset_router
from app.routers import standardSetDetail_router
from app.routers import blogs_router
from app.routers import contact_router
from app.routers import customerRequest_router
from app.routers import users_router
from app.routers import slide_router
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # หรือ ระบุ origin ก็ได้
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

app.include_router(about_router.router)
app.include_router(experience_router.router)
app.include_router(professionalteam_router.router)
app.include_router(naturalfibers_router.router)
app.include_router(international_router.router)
app.include_router(odm_router.router)
app.include_router(oem_router.router)
app.include_router(odmDetail_router.router)
app.include_router(oemDetail_router.router)
app.include_router(collection_router.router)
app.include_router(collectionImage_router.router)
app.include_router(standardProduct_router.router)
app.include_router(standardset_router.router)
app.include_router(standardSetDetail_router.router)
app.include_router(blogs_router.router)
app.include_router(contact_router.router)
app.include_router(customerRequest_router.router)
app.include_router(users_router.router)
app.include_router(slide_router.router)
