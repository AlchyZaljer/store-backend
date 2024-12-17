from fastapi import HTTPException
import httpx


STORAGE_SERVICE_URL = "http://localhost:8001"


async def reserve_products(items: list[dict]):
    url = f"{STORAGE_SERVICE_URL}/reserve/"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=items)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Error reserving products in StorageService")
            )
    return response.json()


async def return_products(items: list[dict]):
    url = f"{STORAGE_SERVICE_URL}/items/add/"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=items)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Error returning products to StorageService")
            )
    return response.json()
