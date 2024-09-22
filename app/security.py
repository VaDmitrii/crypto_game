from fastapi import HTTPException, Security
from fastapi.security import APIKeyQuery

from config import settings

api_key_query = APIKeyQuery(name="api-key", auto_error=False)


async def check_token(api_key: str = Security(api_key_query)):
    if api_key != f"{settings.API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return api_key_query
