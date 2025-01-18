import httpx
from app.core.config import settings

    # query($first: Int!, $after: String) {
    #   products(first: $first, after: $after) {

async def get_inventory_data(inventory_id: str):
    query = """
    query inventoryItem($id: ID!) {
    inventoryItem(id : $id) {
        id
        tracked
        updatedAt
        sku
        variant{
            product{
                id
                title
                totalInventory
                createdAt
            }
        }
    }
    }
    """
    
    variables = {
        "id": inventory_id
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=settings.GRAPHQL_URL,
            headers=settings.SHOPIFY_HEADERS,
            json={"query": query, "variables": variables},
        )
        #print(response.text)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        items = data.get("data").get("inventoryItem")
        
        sku = items.get("sku", None)
        
        updated_at = items.get("updatedAt")
        
        title = items.get('variant').get('product').get("title")
        
        totalInventory = items.get('variant').get('product').get("totalInventory")
        
        return {
            "sku": sku,
            "updatedAt": updated_at,
            "title": title,
            "totalInventory": totalInventory
        }
