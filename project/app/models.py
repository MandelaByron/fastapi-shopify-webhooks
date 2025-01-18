

from pydantic import BaseModel
from app.dependancies.deps import DateFormatter
class InventoryUpdate(BaseModel):
    inventory_item_id: int
    available: int | None
    location_id: int
    
class SheetUpdate(InventoryUpdate):
    sku: str | None
    title: str
    updatedAt: DateFormatter
    triggeredAt: DateFormatter