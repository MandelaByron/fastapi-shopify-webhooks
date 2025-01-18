from celery import Celery
from decouple import config
import time
from datetime import datetime
from app.core.googlesheets import work_sheet

celery = Celery(__name__)
celery.conf.broker_url = config("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = config("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

@celery.task(name="process_webhook")

def process_webhook(payload):
    # Process the inventory update and update the Google Sheet
    inventory_item_id = payload["inventory_item_id"]
    available = payload["available"]
    location_id = payload["location_id"]
    sku = payload['sku']
    title = payload['title']
    updatedAt = payload['updatedAt']
    triggeredAt = payload['triggeredAt']
    try:
        cell = work_sheet.find(sku)
        row_number = cell.row

        work_sheet.update(f"A{row_number}:G{row_number}", [[sku,title, inventory_item_id, available, location_id, updatedAt, triggeredAt]])
        return "Updated Work Sheet"
    except Exception as e:
        work_sheet.append_row([sku, title, inventory_item_id, available, location_id, updatedAt, triggeredAt])
        return f"SKU not found in the sheet.{e}"

    
{'inventory_item_id': 45254738804781, 'available': 43, 'location_id': 73823617069, 'sku': "SKU-1234", 'title': 'The Compare at Price Snowboard', 'updatedAt': '2025-01-12, 10:05:43'}