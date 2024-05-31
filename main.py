import os
from dotenv import load_dotenv
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

load_dotenv()

API_KEY: str = os.getenv("API_KEY")
API_KEY_NAME: str = os.getenv("API_KEY_NAME")
COOKIE_DOMAIN: str = os.getenv("COOKIE_DOMAIN")

if not API_KEY or not API_KEY_NAME or not COOKIE_DOMAIN:
    raise ValueError("API_KEY and API_KEY_NAME must be set in the environment variables")

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


# app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app = FastAPI()


@app.get("/")
async def homepage():
    return "Welcome to the security test!"

@app.get("/secure_endpoint", tags=["test"])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = "How cool is this?"
    return response