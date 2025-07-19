# routers/definition_seed.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.definition_crud import create_global_definitions

router = APIRouter(prefix="/admin/definitions", tags=["Definition Admin"])

@router.post("/seed-global")
def seed_global_definitions(db: Session = Depends(get_db)):
    return create_global_definitions(db)
