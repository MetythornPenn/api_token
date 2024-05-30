from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN
from dotenv import load_dotenv
import os



load_dotenv()  # Load environment variables from .env file

app = FastAPI()

class SecureDataRequest(BaseModel):
    data: str


API_KEY = "apikey"
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
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
