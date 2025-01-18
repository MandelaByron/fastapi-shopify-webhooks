from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



class Settings:
    SHOPIFY_WEBHOOK_SECRET: str = config("SHOPIFY_WEBHOOK_SECRET")
    GOOGLE_CREDENTIALS_FILE: str = os.path.join(BASE_DIR, "creds.json")
    SHOP_URL: str = config("SHOP_URL")
    API_VERSION: str = config("API_VERSION")
    TOKEN: str = config("TOKEN")
    GRAPHQL_URL: str = f"https://{SHOP_URL}/admin/api/{API_VERSION}/graphql.json"
    SHOPIFY_HEADERS: dict = {
    "X-Shopify-Access-Token": TOKEN,
    "Content-Type": "application/json"
}

print(BASE_DIR)
settings = Settings()  # type: ignore
