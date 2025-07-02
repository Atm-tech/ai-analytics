from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DefinitionBase(BaseModel):
    key: str
    expression: str

class DefinitionCreate(DefinitionBase):
    pass

class Definition(DefinitionBase):
    id: int

    class Config:
        orm_mode = True

class DefinitionSetBase(BaseModel):
    name: str

class DefinitionSetCreate(DefinitionSetBase):
    definitions: List[DefinitionCreate]

class DefinitionSet(DefinitionSetBase):
    id: int
    created_at: datetime
    definitions: List[Definition]

    class Config:
        orm_mode = True
