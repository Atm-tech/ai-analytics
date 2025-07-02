from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.definition import DefinitionSet, Definition
from app.schemas.definition import DefinitionSetCreate, DefinitionSet as DefinitionSetSchema

router = APIRouter(prefix="/definitions", tags=["Definitions"])

@router.post("/", response_model=DefinitionSetSchema)
def create_definition_set(payload: DefinitionSetCreate, db: Session = Depends(get_db)):
    definition_set = DefinitionSet(name=payload.name)
    db.add(definition_set)
    db.flush()

    for d in payload.definitions:
        definition = Definition(
            key=d.key,
            expression=d.expression,
            definition_set_id=definition_set.id
        )
        db.add(definition)

    db.commit()
    db.refresh(definition_set)
    return definition_set

@router.get("/", response_model=list[DefinitionSetSchema])
def list_definition_sets(db: Session = Depends(get_db)):
    return db.query(DefinitionSet).all()
