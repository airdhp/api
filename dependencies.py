import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException, status
from services.internal import verifyApiCredentials

load_dotenv()

def verify_api_token(api_key: str = Header(...), api_secret: str = Header(...)):

    auth = verifyApiCredentials(api_key, api_secret)
    if auth is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed.")

def verify_admin_token(api_key: str = Header(...), api_secret: str = Header(...)):

    api_admin = os.environ['API_ADMIN_KEY']
    api_secret = os.environ['API_ADMIN_SECRET']
    if api_key != api_admin or api_secret != api_secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed.")
