from pydantic import BaseModel, Field
from typing import Optional

class ItemBase(BaseModel):
    name: str = Field(..., example="Mi producto")
    description: Optional[str] = Field(None, example="Descripción del producto")
    price: float = Field(..., example=9.99)
    available: bool = Field(True, example=True)

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int