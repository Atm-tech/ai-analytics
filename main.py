from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.database import SessionLocal
from app.routers import (
    upload_product,
    upload_purchase,
    upload_closing_stock,
    upload_sales,
    upload_router,
    query_router,
    definition_seed,
    speed_tier_router,
    analytics_router
)
from sqlalchemy.orm import Session
import os

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# App instance
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(upload_product.router, prefix="/api", tags=["Upload - Product Base"])
app.include_router(upload_purchase.router, prefix="/api", tags=["Upload - Purchase File"])
app.include_router(upload_closing_stock.router, prefix="/api", tags=["Upload - Closing Stock"])
app.include_router(upload_sales.router, prefix="/api", tags=["Upload - Sales File"])
app.include_router(upload_router.router)
app.include_router(query_router.router)
app.include_router(definition_seed.router)
app.include_router(speed_tier_router.router)
app.include_router(analytics_router.router)

# Serve React frontend from frontend/dist
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend", "dist")

if os.path.exists(FRONTEND_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        index_path = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"detail": "index.html not found"}
