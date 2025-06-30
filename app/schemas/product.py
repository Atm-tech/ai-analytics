from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    barcode: str
    article_name: Optional[str]
    category1: Optional[str]
    category2: Optional[str]
    category3: Optional[str]
    category4: Optional[str]
    category5: Optional[str]
    category6: Optional[str]
    division: Optional[str]
    department: Optional[str]
    section: Optional[str]
    rsp: Optional[float]
    wsp: Optional[float]
    mrp: Optional[float]
    hsn_sac_code: Optional[str]
    tax_name: Optional[str]

    class Config:
        orm_mode = True

# For create (future use if needed)
class ProductCreate(ProductBase):
    pass

# For read (API response)
class ProductResponse(ProductBase):
    pass
