from fastapi import APIRouter, Depends
from app.dependancies.deps import validate_shopify_webhook
from app.models import  SheetUpdate
from app.utils import get_inventory_data
from app.celery_app import process_webhook

router = APIRouter(prefix='', tags=['items'])
@router.post("/")
async def inventory_update(payload: dict = Depends(validate_shopify_webhook)):
    print(payload)
    

    product_data = await get_inventory_data("gid://shopify/InventoryItem/" + str(payload.get('inventory_item_id')))
    updates = SheetUpdate(**payload, **product_data)
    
    process_webhook.delay(updates.model_dump())  # Pass the payload to the Celery task queue

    return {"status": "queued", "message": "Webhook queued for processing"}   


#uvicorn main:app --workers 4
