# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dbb.database import engine, Base
from routers import user_routes, admin_routes

app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

# Rotaları ekle
app.include_router(user_routes.router)
app.include_router(admin_routes.router)
