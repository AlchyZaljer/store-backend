from fastapi import HTTPException
import httpx


GLOSSARY_SERVICE_URL = "http://localhost:8000"


def is_product_exist(product_id: int) -> bool:
    url = f"{GLOSSARY_SERVICE_URL}/products/{product_id}"
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(url)
            if response.status_code != 200:
                return False

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error connecting to Glossary service: {str(e)}"
        )

    return True
