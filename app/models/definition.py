# models/definition.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Definition(Base):
    __tablename__ = "definitions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    logic = Column(String, nullable=False)

    set_id = Column(Integer, ForeignKey("definition_sets.id"), nullable=False)
    definition_set = relationship("DefinitionSet", backref="definitions")
