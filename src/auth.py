from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")


def check_api_key(value_from_header: str = Security(api_key_header)):
    # In production code, we would check the API key passed in the header against a value stored somewhere, typically a
    # database. I've done it in a simple way here just to save time and to structure the project to make productionising
    # it a little bit easier.
    if value_from_header != "abc123":
        raise HTTPException(status_code=401, detail="Invalid API key")
