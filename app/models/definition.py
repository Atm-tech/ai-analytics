from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class DefinitionSet(Base):
    __tablename__ = "definition_sets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    definitions = relationship("Definition", back_populates="definition_set", cascade="all, delete")

class Definition(Base):
    __tablename__ = "definitions"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, nullable=False)         # e.g. 'superfast'
    expression = Column(Text, nullable=False)    # e.g. '80% sold in 30 days'
    definition_set_id = Column(Integer, ForeignKey("definition_sets.id"))

    definition_set = relationship("DefinitionSet", back_populates="definitions")
