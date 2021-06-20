from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List

from models.internal import Apiclient
from services.internal import postApiclient, deleteApiclient, getApiclients


router = APIRouter()

@router.get("/apiclients", response_description="Get all API Clients")
def get_apiclients():

    clients = getApiclients()

    if clients is not None:
        return clients
    else:
        return {}


@router.post("/apiclient", response_description="Add new API client", response_model=Apiclient)
def create_apiclient(client: Apiclient):
    client = jsonable_encoder(client)
    clients = postApiclient(client)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=clients)


@router.delete("/apiclient/{id}", response_description="Delete API Client")
def delete_apiclient(id: str):

    client = deleteApiclient(id)

    if client is not None:
        return client

    raise HTTPException(status_code=404, detail=f"API Client {id} not found")
