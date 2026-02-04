from pydantic import BaseModel
from typing import Optional

class AddItemRequest(BaseModel):
    order_id: int
    nomenclature_id: int
    quantity: int

class AddItemResponse(BaseModel):
    success: bool
    message: str
    order_item_id: Optional[int] = None
