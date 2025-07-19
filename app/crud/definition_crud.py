# crud/definition_crud.py

from sqlalchemy.orm import Session
from app.models.definition import Definition
from app.models.definition_set import DefinitionSet

def create_global_definitions(db: Session):
    # Check if already seeded
    existing_set = db.query(DefinitionSet).filter_by(is_global=True).first()
    if existing_set:
        return {"message": "Global definitions already exist."}

    # Create the DefinitionSet
    def_set = DefinitionSet(
        name="Predefined Definitions",
        session_id=None,
        is_global=True
    )
    db.add(def_set)
    db.commit()
    db.refresh(def_set)

    # Create definitions
    default_defs = [
        {"name": "superfast", "logic": "80% sold in 30 days"},
        {"name": "slow", "logic": "<30% sold in 30 days"},
        {"name": "good_margin", "logic": "margin > 30%"},
        {"name": "abc_class", "logic": "A = top 20%, B = next 30%, C = rest"}
    ]

    for d in default_defs:
        db.add(Definition(name=d["name"], logic=d["logic"], set_id=def_set.id))

    db.commit()
    return {"message": "Global definitions seeded."}
