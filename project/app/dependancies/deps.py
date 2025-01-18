from datetime import datetime
from typing import Annotated, Dict, Any
from pydantic import BeforeValidator
import json
import base64
import hashlib
import hmac
from fastapi import Request, HTTPException
from app.core.config import settings
def format_updated_at(value: datetime) -> str:
    """Format the updatedAt field during validation."""
    # Parse the ISO 8601 datetime string into a datetime object
    dt = datetime.fromisoformat(value)
    # Format it into the desired string format
    return dt.strftime("%Y-%m-%d, %H:%M:%S")

DateFormatter = Annotated[str, BeforeValidator(format_updated_at)]


async def validate_shopify_webhook(request: Request) -> Dict[str, Any]:
    """
    Validates the HMAC of an incoming Shopify webhook request.

    Args:
        request (Request): The incoming FastAPI request.

    Raises:
        HTTPException: If the HMAC validation fails.

    Returns:
        bytes: The body of the request, if validation succeeds.
    """
    # Get the raw body of the request
    body = await request.body()

    # Extract the Shopify HMAC from headers
    shopify_hmac = request.headers.get("X-Shopify-Hmac-Sha256")
    
    triggered_time = request.headers.get("X-Shopify-Triggered-At")

    if not shopify_hmac:
        raise HTTPException(status_code=400, detail="Missing HMAC header")

    # Calculate the expected HMAC
    calculated_hmac = base64.b64encode(
        hmac.new(
            settings.SHOPIFY_WEBHOOK_SECRET.encode("utf-8"),
            body,
            hashlib.sha256
        ).digest()
    ).decode("utf-8")

    # Compare the HMACs securely
    if not hmac.compare_digest(shopify_hmac, calculated_hmac):
        raise HTTPException(status_code=401, detail="Unauthorized")

        # Parse the JSON payload
    try:
        payload = json.loads(body)
        payload['triggeredAt'] = triggered_time
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    return payload
