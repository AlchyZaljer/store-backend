import os

from ariadne import QueryType, ObjectType
import httpx

from utils import load_schema


SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.graphql")
type_defs = load_schema(SCHEMA_PATH)

ORDER_SERVICE_URL = "http://localhost:8002"
GLOSSARY_SERVICE_URL = "http://localhost:8000"

query = QueryType()
order_item = ObjectType("OrderItem")


@query.field("products")
async def resolve_products(_, __):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GLOSSARY_SERVICE_URL}/products/")
        response.raise_for_status()
        return response.json()


@query.field("product")
async def resolve_product(*_, product_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GLOSSARY_SERVICE_URL}/products/{product_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


@query.field("orders")
async def resolve_orders(*_):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORDER_SERVICE_URL}/orders/")
        response.raise_for_status()
        return response.json()


@query.field("order")
async def resolve_order(*_, order_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORDER_SERVICE_URL}/orders/{order_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


@order_item.field("name")
@order_item.field("price")
@order_item.field("description")
async def resolve_order_item_field(item, info):
    product_id = item["product_id"]
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GLOSSARY_SERVICE_URL}/products/{product_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        product_data = response.json()
    return product_data[info.field_name]
