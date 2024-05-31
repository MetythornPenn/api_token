from fastapi import FastAPI, Depends, HTTPException, Security, Request
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_KEY: str = os.getenv("API_KEY")
API_KEY_NAME: str = os.getenv("API_KEY_NAME")

# If either of the variables is None, raise an error
if not API_KEY or not API_KEY_NAME:
    raise ValueError("API_KEY and API_KEY_NAME must be set in the environment variables")

app = FastAPI()

class SecureDataRequest(BaseModel):
    data: str

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header), request: Request = None):
    print(f"Request headers: {request.headers}")
    print(f"api key header: {api_key_header}")
    print(f"api key .env: {API_KEY}")
    print(f"api key name .env: {API_KEY_NAME}")
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}

@app.get("/secure-data/")
async def read_secure_data(api_key: str = Depends(get_api_key), query_param: str = None):
    return {"message": "This is secured data", "query_param": query_param}

@app.post("/secure-data/")
async def create_secure_data(request: SecureDataRequest, api_key: str = Depends(get_api_key)):
    return {"message": "You have created secured data", "data": request.data}
