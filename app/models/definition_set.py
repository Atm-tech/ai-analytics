# models/definition_set.py
from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class DefinitionSet(Base):
    __tablename__ = "definition_sets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    session_id = Column(String, nullable=True)  # null for global
    is_global = Column(Boolean, default=False)
